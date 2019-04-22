from django.db import models


class Arquivo(models.Model):
    agencia = models.IntegerField(blank=False, null=False)
    competencia = models.DateField(auto_now=False, blank=False, null=False)
    observacao = models.TextField(blank=False, null=False)
    data_envio = models.DateField(auto_now=False, auto_now_add=True)

    def get_data_envio(self):
        return self.data_envio;


class ArquivoChecagem(Arquivo):
    tipo_arquivo = models.CharField(default='checagem', max_length=150)


class ArquivoHistorico(Arquivo):
    tipo_arquivo = models.CharField(default='historico', max_length=150)


class DadosArquivo(models.Model):
    num_linha = models.IntegerField(blank=False, null=False)
    num_registro = models.IntegerField(blank=False, null=False)
    data_inicio = models.DateField(auto_now=False, blank=False, null=False)
    data_fim = models.DateField(auto_now=False, blank=False, null=False)


class DadosArquivoChecagem(DadosArquivo):
    cnpj = models.IntegerField(blank=False, null=False)
    indicador = models.CharField(max_length=250, blank=False, null=False)
    arquivo = models.ForeignKey(
        ArquivoChecagem,
        related_name='dados_arquivo',
        on_delete=models.CASCADE
    )


class DadosArquivoHistorico(DadosArquivo):
    cod_conta = models.CharField(max_length=250, blank=False, null=False)
    arquivo = models.ForeignKey(
        ArquivoHistorico,
        related_name='dados_arquivo',
        on_delete=models.CASCADE
    )
