import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'filtroArquivos'
})
export class FiltroArquivosPipe implements PipeTransform {

  transform(arquivos: any[], tipoArquivo: string): any[] {
    return arquivos;
  }

  filtroDataEnvio(arquivos: any[], dataEnvio: string) {
    let arquivosFiltrados = arquivos;
    
    // if (!arquivos) {
    //   return arquivos;
    // }
    
    // if (!arquivos.length) {
    //   return arquivos;
    // }

    // if (!tipoArquivo) {
    //   return arquivos;
    // }

    // if (typeof tipoArquivo !== 'string') {
    //   return arquivos;
    // }

    // if (tipoArquivo === 'todos') {
    //   return arquivos;
    // }

    // arquivosFiltrados = arquivosFiltrados.filter(arquivo => {
    //   const regexTipoArquivo = RegExp(`^${tipoArquivo}$`, 'ig');
    //   console.log(regexTipoArquivo)
    //   return !!arquivo["tipo_arquivo"].match(regexTipoArquivo);
    // });

    return arquivosFiltrados;
  }

  filtroTipoArquivo(arquivos: any[], tipoArquivo: string) {
    let arquivosFiltrados = arquivos;
    
    if (!arquivos) {
      return arquivos;
    }
    
    if (!arquivos.length) {
      return arquivos;
    }

    if (!tipoArquivo) {
      return arquivos;
    }

    if (typeof tipoArquivo !== 'string') {
      return arquivos;
    }

    if (tipoArquivo === 'todos') {
      return arquivos;
    }

    arquivosFiltrados = arquivosFiltrados.filter(arquivo => {
      const regexTipoArquivo = RegExp(`^${tipoArquivo}$`, 'ig');
      console.log(regexTipoArquivo)
      return !!arquivo["tipo_arquivo"].match(regexTipoArquivo);
    });

    return arquivosFiltrados;
  }
}
