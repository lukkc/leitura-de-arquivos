import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { NgModule, LOCALE_ID } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { NgxSpinnerModule } from 'ngx-spinner';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { EnvioArquivosComponent } from './screens/envio-arquivos/envio-arquivos.component';
import { ListaArquivosComponent } from './screens/lista-arquivos/lista-arquivos.component';

import { registerLocaleData } from '@angular/common';
import localeDeAt from '@angular/common/locales/pt';
import { FiltroArquivosPipe } from './pipes/filtro-tipo-arquivo.pipe';

import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatMomentDateModule} from '@angular/material-moment-adapter';

registerLocaleData(localeDeAt);

@NgModule({
  declarations: [
    AppComponent,
    EnvioArquivosComponent,
    ListaArquivosComponent,
    FiltroArquivosPipe
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule,
    MatDatepickerModule,
    MatMomentDateModule,
    NgxSpinnerModule,
  ],
  providers: [
    { provide: LOCALE_ID, useValue: 'pt' }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
