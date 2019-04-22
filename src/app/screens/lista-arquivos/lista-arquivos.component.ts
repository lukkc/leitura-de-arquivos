import { Component, OnInit } from '@angular/core';
import { ArquivoService } from 'src/app/services/arquivo.service';

@Component({
  selector: 'app-lista-arquivos',
  templateUrl: './lista-arquivos.component.html',
  styleUrls: ['./lista-arquivos.component.scss']
})
export class ListaArquivosComponent implements OnInit {

  public arquivos = [];
  public arquivoVisualizar = {};
  public modal = false;
  public tipoArquivo = "todos";
  public dataEnvio = "";

  constructor(private _arquivoService: ArquivoService) { 
    this.obterArquivos();
  }

  ngOnInit() {
    
  }

  obterArquivos = async () => {
     this.arquivos = await this._arquivoService.obterArquivos();
     this.arquivoVisualizar = this.arquivos[0];
  }

  visualizar = (arquivo) => {
    this.arquivoVisualizar = arquivo;
    this.modal = true;
    const html = window.document.querySelector('html');
    html.style.overflow = 'hidden';
  }

  fecharModal = () => {
    this.modal = false;
    const html = window.document.querySelector('html');
    html.style.overflow = 'scroll';
  }

}
