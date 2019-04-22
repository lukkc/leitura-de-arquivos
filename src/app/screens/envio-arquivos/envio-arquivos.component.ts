import { Component, OnInit } from '@angular/core';
import { ArquivoService } from 'src/app/services/arquivo.service';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-envio-arquivos',
  templateUrl: './envio-arquivos.component.html',
  styleUrls: ['./envio-arquivos.component.scss']
})
export class EnvioArquivosComponent {

  public mensagensErroArquivos = [];
  public validandoChecagem = false;
  public nomeArquivoChecagem = "";
  public checagemValido = false;
  public mensagensErroChecagem = []
  public mensagensValidoChecagem = []
  private checagemArquivoVerificado = null;
  public checagem = {
    agencia: null,
    competencia: null,
    observacao: null,
    arquivo: null,
    tipo_arquivo: "checagem"
  }
  public validandoHistorico = false;
  public nomeArquivoHistorico = "";
  public historicoValido = false;
  public mensagensErroHistorico = []
  public mensagensValidoHistorico = []
  private historicoArquivoVerificado = null;
  public historico = {
    agencia: null,
    competencia: null,
    observacao: null,
    arquivo: null,
    tipo_arquivo: "historico"
  }
  public formValido = false;
  public formSubmitted = false;
  public formSubmitting = false;
  public formEnviado = false;

  constructor(
    private _arquivoService: ArquivoService,
    private _spinnerService: NgxSpinnerService
  ) { }

  validarArquivoChecagem = (file) => {
    const arquivo = file.files.item(0);
    const nomeArquivo = arquivo.name;
    const tipoArquivo = arquivo.type;
    const formData = new FormData();
    const regexFormato = /\.txt$/ig;
    this.mensagensValidoChecagem = [];
    this.mensagensErroChecagem = [];
    this.checagemArquivoVerificado = null;

    this._spinnerService.show('arquivo-checagem');
    this.validandoChecagem = true;
    this.nomeArquivoChecagem = nomeArquivo;

    formData.append('arquivo', arquivo, nomeArquivo)

    if (!regexFormato.test(nomeArquivo) && tipoArquivo != 'text/plain') {
      setTimeout(() => {
        this._spinnerService.hide('arquivo-checagem');
        this.validandoChecagem = false;
        this.checagemValido = false;
        this.mensagensValidoChecagem = [];
        this.mensagensErroChecagem = [
          'O formato do arquivo escolhido está errado.',
          'Você precisa escolher um arquivo no formato .txt'
        ]
      }, 2000);
      return null;
    }
  
    this._arquivoService.validarArquivoChecagem(formData)
      .then(response => {
        
        const arquivoValido = response['valido'];

        if (arquivoValido) {
          this.checagemArquivoVerificado = arquivo;
          setTimeout(() => {
            this._spinnerService.hide('arquivo-checagem');
            this.validandoChecagem = false;
            this.checagemValido = true;
            this.mensagensValidoChecagem = [
              'Arquivo Aprovado!'
            ]
            this.mensagensErroChecagem = []
          }, 2000);
        } else {
          setTimeout(() => {
            this._spinnerService.hide('arquivo-checagem');
            this.validandoChecagem = false;
            this.checagemValido = false;
            this.mensagensValidoChecagem = []
            this.mensagensErroChecagem = [
              'O arquivo escolhido tem erro de formatação.'
            ]
          }, 2000);
        }
      }).catch(error => {
        setTimeout(() => {
          this._spinnerService.hide('arquivo-checagem');
          this.validandoChecagem = false;
          this.checagemValido = false;
          this.mensagensValidoChecagem = []
          this.mensagensErroChecagem = [
            'Ocorreu um problema inesperado ao tentar verificar seu arquivo.',
            'Tente novamente mais tarde.'
          ]
        }, 2000);
      });
  }

  validarArquivoHistorico = (file) => {
    const arquivo = file.files.item(0);
    const nomeArquivo = arquivo.name;
    const tipoArquivo = arquivo.type;
    const formData = new FormData();
    const regexFormato = /\.txt$/ig;
    this.mensagensValidoHistorico = [];
    this.mensagensErroHistorico = [];
    this.historicoArquivoVerificado = null;

    this._spinnerService.show('arquivo-historico');
    this.validandoHistorico = true;
    this.nomeArquivoHistorico = nomeArquivo;

    formData.append('arquivo', arquivo, nomeArquivo)

    if (!regexFormato.test(nomeArquivo) && tipoArquivo != 'text/plain') {
      setTimeout(() => {
        this._spinnerService.hide('arquivo-historico');
        this.validandoHistorico= false;
        this.historicoValido = false;
        this.mensagensValidoHistorico = [];
        this.mensagensErroHistorico = [
          'O formato do arquivo escolhido está errado.',
          'Você precisa escolher um arquivo no formato .txt'
        ]
      }, 2000);
      return null;
    }
  
    this._arquivoService.validarArquivoHistorico(formData)
      .then(response => {
        
        const arquivoValido = response['valido'];

        if (arquivoValido) {
          this.historicoArquivoVerificado = arquivo;
          setTimeout(() => {
            this._spinnerService.hide('arquivo-historico');
            this.validandoHistorico = false;
            this.historicoValido = true;
            this.mensagensValidoHistorico = [
              'Arquivo Aprovado!'
            ]
            this.mensagensErroHistorico = []
          }, 2000);
        } else {
          setTimeout(() => {
            this._spinnerService.hide('arquivo-historico');
            this.validandoHistorico = false;
            this.historicoValido = false;
            this.mensagensValidoHistorico = []
            this.mensagensErroHistorico = [
              'O arquivo escolhido tem erro de formatação.'
            ]
          }, 2000);
        }
      }).catch(erro => {
        setTimeout(() => {
          this._spinnerService.hide('arquivo-historico');
          this.validandoHistorico = false;
          this.historicoValido = false;
          this.mensagensValidoHistorico = []
          this.mensagensErroChecagem = [
            'Ocorreu um problema inesperado ao tentar verificar seu arquivo.',
            'Tente novamente mais tarde.'
          ]
        }, 2000);
      });
  }

  onSubmit = (form) => {
    
    const checagem = {
      ...this.checagem
    }
    const historico= {
      ...this.historico
    }
    const dados = {"arquivos": []};
    const readerChecagem = new FileReader();
    const readerHistorico = new FileReader();

    this.mensagensErroArquivos = [];
    this._spinnerService.show('form-submit');
    this.formSubmitting = true;
    this.formValido = form.valid;
    this.formSubmitted = form.submitted;

    if (!form.valid || !this.checagemValido || !this.historicoValido) {
      setTimeout(() => {
        this._spinnerService.hide('form-submit');
        this.formSubmitting = false;
      }, 2000);
      return;
    }
   
    readerChecagem.onload = (event) => {
      checagem.arquivo = readerChecagem.result;
      readerHistorico.readAsText(this.historicoArquivoVerificado);
    };

    readerHistorico.onload = (event) => {
      historico.arquivo = readerHistorico.result;

      dados.arquivos.push(checagem, historico);

      this._arquivoService.enviarArquivos(dados)
        .then(response => {
          setTimeout(() => {
            this._spinnerService.hide('form-submit');
            this.formSubmitting = false;
            this.formEnviado = true;

            setTimeout(() => {
              this.formEnviado = false;
            }, 5000);
            form.reset();
          }, 2000);
        }).catch(erro => {
          setTimeout(() => {
            this.mensagensErroArquivos = [
              'Ocorreu um problema inesperado ao tentar enviar seus arquivos.',
              'Tente novamente mais tarde.'
            ]
            this._spinnerService.hide('form-submit');
            this.formSubmitting = false;
          }, 2000);
        });    
    };
    
    readerChecagem.readAsText(this.checagemArquivoVerificado);
  }
}
