import os
import requests
from zipfile import ZipFile

base_dir = "webScraping"
download_dir = os.path.join(base_dir, "downloads")

os.makedirs(download_dir, exist_ok=True)

urls = {
    "Anexo_I.pdf": "https://www.gov.br/ans/pt-br/arquivos/assuntos/consumidor/o-que-seu-plano-deve-cobrir/Anexo_I_Rol_2021RN_465.2021_RN473.pdf",
    "Anexo_II.pdf": "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN624_RN625.2024.pdf"
}

def download_file(url, filename):
    filepath = os.path.join(download_dir, filename)
    
    if os.path.exists(filepath):
        print(f"Arquivo já existe: {filename}")
        return filepath

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(filepath, 'wb') as file:
            file.write(response.content)

        print(f"Download concluído: {filename}")
        return filepath
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar {filename}: {e}")
        return None

downloaded_files = []
for filename, url in urls.items():
    filepath = download_file(url, filename)
    if filepath:
        downloaded_files.append(filepath)

zip_filename = os.path.join(base_dir, "Anexos.zip")

try:
    with ZipFile(zip_filename, 'w') as zipf:
        for file in downloaded_files:
            zipf.write(file, os.path.basename(file))
            print(f"Arquivo adicionado ao ZIP: {file}")
    print(f"Arquivo ZIP criado em: {zip_filename}")
except Exception as e:
    print(f"Erro ao criar o ZIP: {e}")
