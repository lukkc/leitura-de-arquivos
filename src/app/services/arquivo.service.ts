import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ArquivoService {

  constructor(private _http: HttpClient) { }

  obterArquivos = () => {
    return this._http.get<[]>('http://127.0.0.1:8000/api/arquivos').toPromise();
  }

  enviarArquivos = (arquivos) => {

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      })
    };

    return this._http.post(
      'http://127.0.0.1:8000/api/arquivos',
      arquivos,
      httpOptions
    ).toPromise();
  }

  validarArquivoChecagem = (arquivo) => {
    return this._http.post(
      'http://127.0.0.1:8000/api/arquivos/checagem/validar',
      arquivo
    ).toPromise();
  }

  validarArquivoHistorico = (arquivo) => {
    return this._http.post(
      'http://127.0.0.1:8000/api/arquivos/historico/validar',
      arquivo
    ).toPromise();
  }
}
