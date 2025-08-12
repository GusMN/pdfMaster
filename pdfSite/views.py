import pypandoc
import os
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

def home(request):
    return render(request, 'pdfSite/home.html')

def converter(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        txt_file = request.FILES['arquivo']

        # Salvando temporariamente o arquivo .txt
        txt_path = os.path.join(settings.MEDIA_ROOT, txt_file.name)
        with open(txt_path, 'wb+') as destino:
            for chunk in txt_file.chunks():
                destino.write(chunk)

        # Nome do PDF de saída
        pdf_path = os.path.splitext(txt_path)[0] + '.pdf'

        # Conversão usando pypandoc
        output = pypandoc.convert_file(txt_path, 'pdf', outputfile=pdf_path)

        # Lendo o PDF e enviando como resposta
        with open(pdf_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'

        # Limpando arquivos temporários
        os.remove(txt_path)
        os.remove(pdf_path)

        return response

    return HttpResponse("Erro: Nenhum arquivo enviado.", status=400)
