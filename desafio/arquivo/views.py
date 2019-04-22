import re
import datetime
from django.http import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView
)

from arquivo.serializers import (
    ArquivoChecagemSerializer,
    ArquivoHistoricoSerializer
)
from arquivo.models import (
    ArquivoChecagem,
    ArquivoHistorico,
    DadosArquivoChecagem,
    DadosArquivoHistorico
)
from arquivo.validators import (
    ValidadorArquivoChecagem,
    ValidadorArquivoHistorico,
    validar_campos_arquivo
)


class ListarOuCriarArquivos(ListCreateAPIView):
    serializer_class = ArquivoChecagemSerializer
    queryset = ArquivoChecagem.objects.all()

    def list(self, request):
        arquivos_serializados = []
        arquivos_checagem = ArquivoChecagem.objects.all()
        arquivos_historico = ArquivoHistorico.objects.all()
        arquivos_checagem_serializados = self._obter_arquivos_serializados(
            arquivos_checagem,
            'checagem'
        )
        arquivos_historico_serializados = self._obter_arquivos_serializados(
            arquivos_historico,
            'historico'
        )
        arquivos_serializados.extend(arquivos_checagem_serializados)
        arquivos_serializados.extend(arquivos_historico_serializados)

        return Response(arquivos_serializados, status=200)

    def create(self, request):
        try:
            arquivos = request.data.get("arquivos", [])
            quantidade_de_arquivos = len(arquivos)

            if quantidade_de_arquivos < 2 or type(arquivos) != list:
                return Response(
                    {
                        "erro": "Está faltando arquivos",
                    },
                    status=400
                )

            for dado_request in arquivos:
                if dado_request is not None and type(dado_request) == dict:
                    model_arquivo = ArquivoChecagem
                    validador_arquivo = ValidadorArquivoChecagem
                    arquivo = dado_request.get("arquivo", None)
                    tipo_arquivo = dado_request.get("tipo_arquivo", None)

                    if tipo_arquivo == 'historico':
                        model_arquivo = ArquivoHistorico
                        validador_arquivo = ValidadorArquivoHistorico

                    if validar_campos_arquivo(dado_request) is False:
                        return Response(
                            {
                                "erro": "Os campos estão incorretos",
                            },
                            status=400
                        )

                    validacao_arquivo = validador_arquivo(
                        arquivo
                    )

                    if validacao_arquivo.valido() is False:
                        return Response(
                            {
                                "erro": "Arquivo de checagem formato invalido",
                                "detalhes": validacao_arquivo.detalhes_validacao()
                            },
                            status=415
                        )

                    obj_arquivo = model_arquivo.objects.create(
                        agencia=dado_request["agencia"],
                        competencia=dado_request["competencia"],
                        observacao=dado_request["observacao"]
                    )

                    for dado in validacao_arquivo.dados:
                        if tipo_arquivo == 'checagem':
                            DadosArquivoChecagem.objects.create(
                                num_linha=int(dado["num_linha"]),
                                num_registro=int(dado["num_registro"]),
                                cnpj=int(dado["cnpj"]),
                                indicador=dado["indicador"],
                                data_inicio=dado["data_inicio"],
                                data_fim=dado["data_fim"],
                                arquivo=obj_arquivo
                            )
                        elif tipo_arquivo == 'historico':
                            DadosArquivoHistorico.objects.create(
                                num_linha=int(dado["num_linha"]),
                                num_registro=int(dado["num_registro"]),
                                cod_conta=dado["cod_conta"],
                                data_inicio=dado["data_inicio"],
                                data_fim=dado["data_fim"],
                                arquivo=obj_arquivo
                            )

                else:
                    return Response(
                        {
                            "erro": "Está faltando arquivos",
                        },
                        status=400
                    )

            return Response(
                {"mensagem": "Arquivos criados com sucesso"},
                status=201
            )
        except:
            return Response(
                {
                    "erro": "Algo inesperado aconteceu. Tente novamente mais tarde",
                },
                status=500
            )

    def _obter_arquivos_serializados(self, lista_arquivos, tipo_arquivo):
        serializer = ArquivoChecagemSerializer
        arquivos_serializados = []

        if tipo_arquivo == 'historico':
            serializer = ArquivoHistoricoSerializer
        
        for arquivo in lista_arquivos:
            arquivo_serializado = serializer(arquivo).data
            arquivos_serializados.append(arquivo_serializado)
        
        return arquivos_serializados


class ValidarArquivo(APIView):
    validador = ValidadorArquivoChecagem

    def post(self, request, format=None):
        try:
            arquivo = request.data.get("arquivo", None)
            
            if arquivo is None or type(arquivo) != InMemoryUploadedFile:
                return Response({"erro": "Arquivo incorreto"}, status=400)
            
            arquivo = arquivo.read().decode('utf-8')
            validacao = self.validador(arquivo)

            if validacao.valido() is False:
                return Response(
                    {
                        "valido": False,
                        "detalhes": validacao.detalhes_validacao()
                    },
                    status=200
                )
            
            return Response({"valido": True}, status=200)
        except:
            return Response(
                {
                    "erro": "Algo inesperado aconteceu. Tente novamente mais tarde",
                },
                status=500
            )


class ValidarArquivoChecagem(ValidarArquivo):
    pass


class ValidarArquivoHistorico(ValidarArquivo):
    validador = ValidadorArquivoHistorico