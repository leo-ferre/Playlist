"""
NOMES
Leonardo Ferreira
Heloi Vecchi Sgarbi
Kaua Schiavolin Monteiro

Módulo para buscar informações de músicas e capas de álbuns via APIs
Suporta: iTunes API (sem necessidade de chave de autenticação)
"""

import requests
from io import BytesIO
from PIL import Image
from pathlib import Path
import unicodedata
import re


def normalizar_texto(texto):
    """
    Normaliza texto removendo acentos e caracteres especiais para melhorar busca.

    Args:
        texto (str): Texto a ser normalizado

    Returns:
        str: Texto normalizado
    """
    if not texto:
        return ""

    # Remove acentos
    texto_nfd = unicodedata.normalize('NFD', texto)
    texto_sem_acento = ''.join(char for char in texto_nfd if unicodedata.category(char) != 'Mn')

    # Remove caracteres especiais exceto espaços e hífens
    texto_limpo = re.sub(r'[^\w\s-]', '', texto_sem_acento)

    # Remove espaços extras
    texto_limpo = ' '.join(texto_limpo.split())

    return texto_limpo


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

            print(f"Buscando: {query}")

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

            print("Nenhum resultado encontrado na API")
            return None

        except Exception as e:
            print(f"Erro ao buscar capa do álbum: {e}")
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
            print(f"Capa do álbum salva: {caminho_destino}")

            return str(caminho_destino)

        except Exception as e:
            print(f"Erro ao baixar imagem: {e}")
            return None

    def buscar_informacoes_completas(self, titulo, artista):
        """
        Busca informações completas da música (álbum, gênero, ano, capa).
        Tenta múltiplas estratégias de busca para aumentar chances de sucesso.

        Args:
            titulo (str): Título da música
            artista (str): Nome do artista

        Returns:
            dict: Dicionário com informações da música ou None
        """
        # Normaliza os textos de entrada
        titulo_norm = normalizar_texto(titulo)
        artista_norm = normalizar_texto(artista)

        # Tenta diferentes estratégias de busca
        estrategias = [
            # 1. Artista + Título (normalizado)
            f"{artista_norm} {titulo_norm}",
            # 2. Título + Artista (normalizado)
            f"{titulo_norm} {artista_norm}",
            # 3. Artista + Título (original)
            f"{artista} {titulo}",
            # 4. Título + Artista (original)
            f"{titulo} {artista}",
            # 5. Apenas título (normalizado)
            titulo_norm,
            # 6. Apenas título (original)
            titulo,
        ]

        print(f"🔍 Buscando: '{titulo}' por '{artista}'")

        melhor_resultado = None
        melhor_score = 0

        for i, query in enumerate(estrategias):
            if not query.strip():
                continue

            try:
                params = {
                    'term': query,
                    'media': 'music',
                    'entity': 'song',
                    'limit': 10  # Aumenta limite para ter mais opções
                }

                if i == 0:  # Só mostra a primeira tentativa
                    print(f"   Tentando: {query}")

                response = requests.get(self.itunes_base_url, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()

                if data['resultCount'] > 0:
                    # Procura o melhor match entre os resultados
                    for resultado in data['results']:
                        track_name = resultado.get('trackName', '').lower()
                        artist_name = resultado.get('artistName', '').lower()

                        # Calcula score de similaridade
                        score = 0

                        # Verifica se o título está presente
                        if titulo.lower() in track_name or track_name in titulo.lower():
                            score += 50
                        if normalizar_texto(titulo).lower() in normalizar_texto(track_name).lower():
                            score += 30

                        # Verifica se o artista está presente
                        if artista.lower() in artist_name or artist_name in artista.lower():
                            score += 50
                        if normalizar_texto(artista).lower() in normalizar_texto(artist_name).lower():
                            score += 30

                        # Atualiza melhor resultado se score for maior
                        if score > melhor_score:
                            melhor_score = score
                            melhor_resultado = resultado

                            # Se encontrou um match muito bom (score >= 80), para de buscar
                            if score >= 80:
                                break

                    # Se encontrou um match razoável, para de tentar outras estratégias
                    if melhor_score >= 80:
                        break

            except Exception as e:
                if i == 0:  # Só mostra erro na primeira tentativa
                    print(f"Erro na busca: {e}")
                continue

        # Se encontrou algum resultado
        if melhor_resultado and melhor_score >= 30:  # Score mínimo aceitável
            # Extrai informações
            info = {
                'titulo': melhor_resultado.get('trackName', titulo),
                'artista': melhor_resultado.get('artistName', artista),
                'album': melhor_resultado.get('collectionName', 'Desconhecido'),
                'genero': melhor_resultado.get('primaryGenreName', 'Desconhecido'),
                'ano': melhor_resultado.get('releaseDate', '').split('-')[0] if melhor_resultado.get('releaseDate') else '----',
                'capa_url': melhor_resultado.get('artworkUrl100', '').replace('100x100', '600x600'),
                'preview_url': melhor_resultado.get('previewUrl', '')
            }

            print(f"Informações encontradas (score: {melhor_score}):")
            print(f"Música: {info['titulo']}")
            print(f"Artista: {info['artista']}")
            print(f"Álbum: {info['album']}")
            print(f"Gênero: {info['genero']}")
            print(f"Ano: {info['ano']}")

            # Baixa a capa
            if info['capa_url']:
                info['capa_path'] = self.baixar_imagem(info['capa_url'], info['album'])
            else:
                info['capa_path'] = None

            return info

        print(f"Nenhum resultado encontrado para '{titulo}' - '{artista}'")
        print(f"   Melhor score alcançado: {melhor_score}")
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
