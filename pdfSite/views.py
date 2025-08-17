import os
import tempfile
import pypandoc
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings


def home(request):
    return render(request, 'pdfSite/home.html')


def converter(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        uploaded_file = request.FILES['arquivo']
        original_name, original_ext = os.path.splitext(uploaded_file.name)
        original_ext = original_ext.lower()

        # Arquivo temporário com a extensão correta
        with tempfile.NamedTemporaryFile(delete=False, suffix=original_ext, dir=settings.MEDIA_ROOT) as tmp:
            for chunk in uploaded_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        output_pdf_name = original_name + ".pdf"
        output_pdf_path = os.path.join(settings.MEDIA_ROOT, output_pdf_name)

        try:
            # Verifica se é uma imagem
            if original_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']:
                image = Image.open(tmp_path).convert("RGB")
                image.save(output_pdf_path, "PDF")

            # Se for documento de texto ou Word
            elif original_ext in ['.txt', '.md', '.docx', '.odt', '.html', '.rst']:
                pypandoc.convert_file(
                    tmp_path,
                    'pdf',
                    outputfile=output_pdf_path,
                    extra_args=['--standalone']
                )
            else:
                return HttpResponse("Tipo de arquivo não suportado.", status=400)

            with open(output_pdf_path, 'rb') as pdf_file:
                response = HttpResponse(
                    pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{output_pdf_name}"'
                return response

        except Exception as e:
            return HttpResponse(f"Erro ao converter o arquivo: {e}", status=500)

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            if os.path.exists(output_pdf_path):
                os.remove(output_pdf_path)

    return HttpResponse("Erro: Nenhum arquivo enviado.", status=400)
