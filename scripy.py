import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

##CÓDIGO VERSÃO 1.0 - Desenvolvido por Emanuel Gomes Soares - Engenheiro Ambiental


BASE_URL = "https://geo.fbds.org.br/PB/"
DOWNLOAD_DIR = "PB_download"

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

def download_file(url, folder):
    """Baixa um arquivo e salva na pasta especificada."""
    try:
        os.makedirs(folder, exist_ok=True)
        filename = os.path.basename(urlparse(url).path)
        local_path = os.path.join(folder, filename)

        if os.path.exists(local_path):
            print(f"[SKIP] Já existe: {local_path}")
            return

        print(f"[DOWN] {url}")
        resp = session.get(url, timeout=20, stream=True)
        resp.raise_for_status()

        with open(local_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"[OK] Salvo: {local_path}")

    except Exception as e:
        print(f"[ERRO] Falha ao baixar {url}: {e}")

def is_valid_relative_link(href):
    """Verifica se o href é um link relativo válido."""
    if not href or href.startswith(("http://", "https://", "//", "?")):
        return False
    if ":" in href.split("/")[0]:
        return False
    return True

def scrape_directory_parallel(start_url, base_folder):
    """Varre diretórios e baixa arquivos usando processamento paralelo."""
    queue = [(start_url, base_folder)]
    download_tasks = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        while queue:
            url, folder = queue.pop(0)
            print(f"[DIR] Acessando: {url}")

            try:
                resp = session.get(url, timeout=20)
                resp.raise_for_status()
            except Exception as e:
                print(f"[ERRO] Não acessou {url}: {e}")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            links = soup.find_all("a", href=True)

            for link in links:
                href = link["href"]

                if not is_valid_relative_link(href):
                    continue

                full_url = urljoin(url, href)

                if href.endswith("/"):
                    new_folder = os.path.join(folder, href.rstrip("/"))
                    queue.append((full_url, new_folder))
                else:
                    download_tasks.append(
                        executor.submit(download_file, full_url, folder)
                    )

        for task in as_completed(download_tasks):
            pass

if __name__ == "__main__":
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    scrape_directory_parallel(BASE_URL, DOWNLOAD_DIR)
    print("✔ Download concluído!")
