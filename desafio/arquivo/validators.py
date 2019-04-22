import re

'''
    class ValidadorArquivo
    param arquivo IOstreamText
    param quantidade_colunas int
    param tipo_dado_por_coluna dict
        exemplo arquivo historico
            {
                "num_linha": "int",
                "num_registro": "int",
                "cod_conta": "str",
                "data_inicio": "date",
                "data_fim": "date",
            }
        exemplo arquivo checagem
            {
                "num_linha": "int",
                "num_registro": "int",
                "cnpj": "int",
                "indicador": "str",
                "data_inicio": "date",
                "data_fim": "date",
            }
'''


class ValidadorArquivo:
    def __init__(self, arquivo, quantidade_colunas, tipo_dado_por_coluna):
        self._definir_linhas_arquivo(arquivo)
        self._definir_quantidade_colunas(quantidade_colunas)
        self._definir_tipo_dado_por_coluna(tipo_dado_por_coluna)
        self._validar_em_ordem()
        self._definir_dados() # obrigatorio ser após as validações

    def _definir_linhas_arquivo(self, arquivo):
        self.linhas_arquivo = arquivo.split("\n")

    def _definir_quantidade_colunas(self, quantidade):
        self.quantidade_colunas = quantidade

    def _definir_tipo_dado_por_coluna(self, tipo_dado_por_coluna):
        self.tipo_dado_por_coluna = tipo_dado_por_coluna

    def _definir_dados(self):
        arquivo_estruturado = self._estruturar_aquivo()
        self.dados = arquivo_estruturado["dados"]

    def _validar_em_ordem(self):
        # existe dependencia entre as validações, é necessario executar na ordem abaixo
        self.validacao_quantidade_minima_linha = self._validar_quantidade_minima_linha()  # primeiro
        self.validacao_linha_por_dados = self._validar_linha_por_dados()  # segundo
        self.validacao_dados = self._validar_dados()  # terceiro

    def _validar_quantidade_minima_linha(self):
        linhas_arquivo = self.linhas_arquivo
        quantidade_linhas = len(linhas_arquivo)
        return {"status": quantidade_linhas >= 2}

    def _validar_linha_por_dados(self):
        linhas_arquivo = self.linhas_arquivo
        quantidade_linhas = len(linhas_arquivo)
        validacao = {
            "linhas": [],
            "status": True
        }

        for indice in range(quantidade_linhas):
            linha = linhas_arquivo[indice]
            dados = linha.split("|")
            quantidade_dados = len(dados)

            if quantidade_dados != self.quantidade_colunas:
                validacao["linhas"].append(indice + 1)
                validacao["status"] = False
        return validacao

    def _validar_dados(self):
        arquivo_estruturado = self._estruturar_aquivo()
        cabecalhos_arquivo = arquivo_estruturado["cabecalhos"]
        quantidade_cabecalhos = len(cabecalhos_arquivo)
        cabecalhos_esperado = self.tipo_dado_por_coluna
        dados = arquivo_estruturado["dados"]
        quantidade_dados = len(dados)
        validacao = {
            "dados": [],
            "status": True
        }

        for indice_cabecalho in range(quantidade_cabecalhos):
            cabecalho = cabecalhos_arquivo[indice_cabecalho]
            temCabecalho = cabecalhos_esperado.get(cabecalho)
            if temCabecalho is None:
                validacao["status"] = False
                validacao["dados"].append({
                    "linha": 1,
                    "coluna": indice_cabecalho + 1,
                    "dado": cabecalho,
                    "erro": "O dado '" + cabecalho + "' não corresponde ao formato do arquivo"
                })

        for indice_dado in range(quantidade_dados):
            coluna = 1
            linha = indice_dado + 1
            if linha == 1:
                linha += 1
            for cabecalho in cabecalhos_esperado:
                dado = dados[indice_dado][cabecalho]
                dado_valido = validar_tipo_de_dado(
                    dado,
                    cabecalhos_esperado[cabecalho]
                )
                if dado_valido is False:
                    validacao["status"] = False
                    validacao["dados"].append({
                        "linha": linha,
                        "coluna": coluna,
                        "dado": dado,
                        "erro": "O tipo do dado '" + dado + "' está errado"
                    })
                coluna += 1

        return validacao

    def _estruturar_dados(self, dados):
        dados_estruturados = {}
        indice = 0
        cabecalhos = self.tipo_dado_por_coluna
        for cabecalho in cabecalhos:
            dados_estruturados[cabecalho] = dados[indice]
            indice += 1
        return dados_estruturados

    def _estruturar_aquivo(self):
        validacao_quantidade_minima_linha = self.validacao_quantidade_minima_linha["status"]
        validacao_linha_por_dados = self.validacao_linha_por_dados["status"]
        arquivo_estruturado = {
            "cabecalhos": [],
            "dados": []
        }

        if validacao_quantidade_minima_linha and validacao_linha_por_dados:
            linhas_arquivo = self.linhas_arquivo
            quantidade_linhas = len(linhas_arquivo)

            for indice in range(quantidade_linhas):
                linha = linhas_arquivo[indice]
                dados = linha.split("|")

                if indice == 0:
                    arquivo_estruturado["cabecalhos"].extend(dados)
                else:
                    arquivo_estruturado["dados"].append(
                        self._estruturar_dados(dados))
        return arquivo_estruturado

    def detalhes_validacao(self):
        return {
            "validacao_quantidade_minima_linha": self.validacao_quantidade_minima_linha,
            "validacao_por_linha": self.validacao_linha_por_dados,
            "validacao_por_dado": self.validacao_dados
        }

    def valido(self):
        if self.validacao_quantidade_minima_linha["status"] is False:
            return False
        elif self.validacao_linha_por_dados["status"] is False:
            return False
        elif self.validacao_dados["status"] is False:
            return False
        return True


class ValidadorArquivoChecagem(ValidadorArquivo):
    def __init__(self, arquivo):
        super().__init__(
            arquivo,
            6, 
            {
                "num_linha": "int",
                "num_registro": "int",
                "cnpj": "int",
                "indicador": "str",
                "data_inicio": "date",
                "data_fim": "date",
            }
        )


class ValidadorArquivoHistorico(ValidadorArquivo):
    def __init__(self, arquivo):
        super().__init__(
            arquivo,
            5, 
            {
                "num_linha": "int",
                "num_registro": "int",
                "cod_conta": "str",
                "data_inicio": "date",
                "data_fim": "date",
            }
        )


def validar_campos_arquivo(arquivo):
    if arquivo is None or type(arquivo) != dict:
        return False
    
    agencia = arquivo.get("agencia", None)
    competencia = arquivo.get("competencia", None)
    observacao = arquivo.get("observacao", None)
    tipo_arquivo = arquivo.get("tipo_arquivo", None)
    arquivo_check = arquivo.get("arquivo", None)

    if agencia is None or validar_tipo_de_dado(agencia, 'int') is False:
        return False
    elif competencia is None or validar_tipo_de_dado(competencia, 'date') is False:
        return False
    elif observacao is None or validar_tipo_de_dado(observacao, 'str') is False:
        return False
    elif tipo_arquivo is None or validar_tipo_de_dado(tipo_arquivo, 'str') is False:
        return False
    elif tipo_arquivo != 'checagem' and tipo_arquivo != 'historico':
        return False
    elif arquivo_check is None:
        return False

    return True


def validar_tipo_de_dado(dado, tipo_dado):
    if tipo_dado == 'int':
        test = re.match(r'^\d+$', str(dado))
        return re.match(r'^\d+$', str(dado)) is not None
    elif tipo_dado == 'str':
        return re.match(r'^\w[\w\s]*$', str(dado)) is not None
    elif tipo_dado == 'date':
        return re.match(r'^\d{4}-\d{2}-\d{2}$', str(dado)) is not None
