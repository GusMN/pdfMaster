import pypandoc
import os
import tempfile
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings


def home(request):
    return render(request, 'pdfSite/home.html')


def converter(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        txt_file = request.FILES['arquivo']

        # Criando arquivo temporário seguro
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', dir=settings.MEDIA_ROOT) as tmp:
            for chunk in txt_file.chunks():
                tmp.write(chunk)
            txt_path = tmp.name

        # Nome do PDF de saída
        pdf_path = os.path.splitext(txt_path)[0] + '.pdf'

        try:
            # Conversão com Pandoc
            pypandoc.convert_file(
                txt_path, 'pdf', format='markdown', outputfile=pdf_path, extra_args=['--standalone'])

            # Lê e retorna o PDF como download
            with open(pdf_path, 'rb') as pdf:
                response = HttpResponse(
                    pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="resultado.pdf"'
                return response

        except Exception as e:
            return HttpResponse(f"Erro ao converter o arquivo: {e}", status=500)

        finally:
            # Limpa os arquivos temporários
            if os.path.exists(txt_path):
                os.remove(txt_path)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

    return HttpResponse("Erro: Nenhum arquivo enviado.", status=400)
