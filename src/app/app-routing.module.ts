import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { EnvioArquivosComponent } from './screens/envio-arquivos/envio-arquivos.component';
import { ListaArquivosComponent } from './screens/lista-arquivos/lista-arquivos.component';

const routes: Routes = [
  { path: 'arquivos/enviar', component: EnvioArquivosComponent },
  { path: 'arquivos/listar', component: ListaArquivosComponent },
  { path: '',
    redirectTo: '/arquivos/enviar',
    pathMatch: 'full'
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
