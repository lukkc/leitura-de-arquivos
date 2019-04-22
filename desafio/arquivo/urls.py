from django.urls import path

from arquivo.views import (
    ListarOuCriarArquivos,
    ValidarArquivoChecagem,
    ValidarArquivoHistorico
)

urlpatterns = [
    path('arquivos', ListarOuCriarArquivos.as_view(), name='listar-ou-criar-arquivos'),
    path('arquivos/checagem/validar', ValidarArquivoChecagem.as_view(), name='validar-arquivo-checagem'),
    path('arquivos/historico/validar', ValidarArquivoHistorico.as_view(), name='validar-arquivo-historico'),
]
