from rest_framework import serializers

from arquivo.models import (
    ArquivoChecagem,
    ArquivoHistorico,
    DadosArquivoChecagem,
    DadosArquivoHistorico
) 


class DadosArquivoChecagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosArquivoChecagem
        # fields = '__all__'
        exclude = ('arquivo',)


class DadosArquivoHistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosArquivoHistorico
        # fields = '__all__'
        exclude = ('arquivo',)


class ArquivoChecagemSerializer(serializers.ModelSerializer):
    dados_arquivo = DadosArquivoChecagemSerializer(many=True)

    class Meta:
        model = ArquivoChecagem
        fields = '__all__'
        depth = 2


class ArquivoHistoricoSerializer(serializers.ModelSerializer):
    dados_arquivo = DadosArquivoHistoricoSerializer(many=True)

    class Meta:
        model = ArquivoHistorico
        fields = '__all__'
        depth = 2
