REQUISITOS DE USO DO SITE

1. Linguagem
- Python 3.8 ou superior

2. Gerenciador de Pacotes
- pip (já vem com o Python, mas atualize se necessário)

3. Dependências Python
Instale com:
    pip install django pypandoc pillow

Ou use o requirements.txt:
    pip install -r requirements.txt

4. Conversor de Arquivos
- Pandoc → https://pandoc.org/installing.html

5. Renderizador LaTeX (necessário para gerar PDFs via Pandoc)
- MikTeX (Windows) → https://miktex.org/download
- TeX Live (Linux/macOS) → https://tug.org/texlive/

⚠️ Durante a instalação do MikTeX, habilite a opção de baixar pacotes automaticamente.

6. Outras Bibliotecas do Sistema
- Ghostscript (opcional, mas recomendado para melhor compatibilidade com PDFs de imagens):
  - Windows: https://ghostscript.com/releases/gsdnld.html
  - Linux/macOS: instale via gerenciador de pacotes (apt, brew, etc.)


Funcionalidades

- Conversão de arquivos `.txt`, `.md`, `.docx`, `.odt`, `.html` em PDF via **Pandoc**
- Conversão de imagens (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.webp`) em PDF com **Pillow**
- Download automático do PDF com o mesmo nome do arquivo enviado