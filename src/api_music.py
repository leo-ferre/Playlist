"""
Módulo para buscar informações de músicas e capas de álbuns via APIs
Suporta: iTunes API (sem necessidade de chave de autenticação)
"""

import requests
from io import BytesIO
from PIL import Image
import os
from pathlib import Path


class MusicAPI:
    """Classe para buscar informações de músicas via APIs"""

    def __init__(self):
        # iTunes API (não requer autenticação)
        self.itunes_base_url = "https://itunes.apple.com/search"

    def buscar_capa_album(self, titulo, artista):
        """
        Busca a capa do álbum usando a iTunes API.
        Retorna o caminho da imagem salva ou None se não encontrar.

        Args:
            titulo (str): Título da música
            artista (str): Nome do artista

        Returns:
            str: Caminho da imagem salva ou None
        """
        try:
            # Monta a query de busca
            query = f"{artista} {titulo}"
            params = {
                'term': query,
                'media': 'music',
                'entity': 'song',
                'limit': 1
            }

            print(f"🔍 Buscando: {query}")

            # Faz requisição para a iTunes API
            response = requests.get(self.itunes_base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Verifica se encontrou resultados
            if data['resultCount'] > 0:
                resultado = data['results'][0]

                # Obtém a URL da imagem em alta resolução
                imagem_url = resultado.get('artworkUrl100', '')

                # Troca para resolução maior (600x600)
                imagem_url = imagem_url.replace('100x100', '600x600')

                if imagem_url:
                    album_nome = resultado.get('collectionName', 'unknown')
                    return self.baixar_imagem(imagem_url, album_nome)

            print("❌ Nenhum resultado encontrado na API")
            return None

        except Exception as e:
            print(f"❌ Erro ao buscar capa do álbum: {e}")
            return None

    def baixar_imagem(self, url, album_nome):
        """
        Baixa a imagem da URL e salva localmente.

        Args:
            url (str): URL da imagem
            album_nome (str): Nome do álbum (usado para nomear o arquivo)

        Returns:
            str: Caminho da imagem salva
        """
        try:
            print(f"📥 Baixando imagem do álbum...")

            # Faz download da imagem
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Abre a imagem com PIL
            img = Image.open(BytesIO(response.content))

            # Define pasta de destino dentro de data/album_covers
            project_root = Path(__file__).resolve().parent.parent
            pasta_destino = project_root / 'data' / 'album_covers'
            pasta_destino.mkdir(parents=True, exist_ok=True)

            # Nome do arquivo (limpa caracteres especiais)
            nome_arquivo = "".join(c for c in album_nome if c.isalnum() or c in (' ', '-', '_')).strip()
            nome_arquivo = nome_arquivo.replace(' ', '_').lower()
            caminho_destino = pasta_destino / f"{nome_arquivo}.png"

            # Salva a imagem
            img.save(str(caminho_destino), 'PNG')
            print(f"✅ Capa do álbum salva: {caminho_destino}")

            return str(caminho_destino)

        except Exception as e:
            print(f"❌ Erro ao baixar imagem: {e}")
            return None

    def buscar_informacoes_completas(self, titulo, artista):
        """
        Busca informações completas da música (álbum, gênero, ano, capa).

        Args:
            titulo (str): Título da música
            artista (str): Nome do artista

        Returns:
            dict: Dicionário com informações da música ou None
        """
        try:
            query = f"{artista} {titulo}"
            params = {
                'term': query,
                'media': 'music',
                'entity': 'song',
                'limit': 1
            }

            print(f"🔍 Buscando informações completas: {query}")

            response = requests.get(self.itunes_base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data['resultCount'] > 0:
                resultado = data['results'][0]

                # Extrai informações
                info = {
                    'titulo': resultado.get('trackName', titulo),
                    'artista': resultado.get('artistName', artista),
                    'album': resultado.get('collectionName', 'Desconhecido'),
                    'genero': resultado.get('primaryGenreName', 'Desconhecido'),
                    'ano': resultado.get('releaseDate', '').split('-')[0] if resultado.get('releaseDate') else '----',
                    'capa_url': resultado.get('artworkUrl100', '').replace('100x100', '600x600'),
                    'preview_url': resultado.get('previewUrl', '')
                }

                print(f"✅ Informações encontradas:")
                print(f"   📀 Álbum: {info['album']}")
                print(f"   🎸 Gênero: {info['genero']}")
                print(f"   📅 Ano: {info['ano']}")

                # Baixa a capa
                if info['capa_url']:
                    info['capa_path'] = self.baixar_imagem(info['capa_url'], info['album'])
                else:
                    info['capa_path'] = None

                return info

            print("❌ Nenhum resultado encontrado")
            return None

        except Exception as e:
            print(f"❌ Erro ao buscar informações: {e}")
            return None


# Funções auxiliares para usar diretamente
def buscar_e_salvar_capa(titulo, artista):
    """
    Função simplificada para buscar e salvar capa do álbum.

    Args:
        titulo (str): Título da música
        artista (str): Nome do artista

    Returns:
        str: Caminho da imagem ou None
    """
    api = MusicAPI()
    return api.buscar_capa_album(titulo, artista)


def buscar_informacoes_musica(titulo, artista):
    """
    Função simplificada para buscar informações completas.

    Args:
        titulo (str): Título da música
        artista (str): Nome do artista

    Returns:
        dict: Informações da música ou None
    """
    api = MusicAPI()
    return api.buscar_informacoes_completas(titulo, artista)
