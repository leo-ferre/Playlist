# Guia Completo - Sistema de Gerenciamento de Playlist

**Versão:** 1.0  
**Data:** Outubro 2025  
**Plataformas:** Windows, macOS, Linux

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Como Usar](#como-usar)
4. [Funcionalidades Detalhadas](#funcionalidades-detalhadas)
5. [Interface Gráfica (GUI)](#interface-gráfica-gui)
6. [Interface de Linha de Comando (CLI)](#interface-de-linha-de-comando-cli)
7. [Busca Automática de Músicas](#busca-automática-de-músicas)
8. [Solução de Problemas](#solução-de-problemas)
9. [Perguntas Frequentes](#perguntas-frequentes)

---

## Visão Geral

O **Sistema de Gerenciamento de Playlist** é uma aplicação completa para organizar suas músicas favoritas. Desenvolvido em Python, oferece duas interfaces:

- **Interface Gráfica (GUI)** - Visual, moderna e intuitiva
- **Interface de Linha de Comando (CLI)** - Rápida e direta

### Principais Recursos:

✅ Adicionar músicas manualmente ou com busca automática via API  
✅ Listar todas as músicas com informações completas  
✅ Buscar músicas por qualquer campo (título, artista, álbum, etc.)  
✅ Editar informações de músicas existentes  
✅ Remover músicas com confirmação  
✅ Gerar relatórios filtrados por critérios  
✅ Download automático de capas de álbuns  
✅ Persistência automática dos dados  

---

## Instalação

### Requisitos Mínimos:

- **Python 3.8+** (Python 3.9 ou superior recomendado)
- **Conexão com internet** (apenas para busca automática)
- **150 MB de espaço em disco**

### Instalação Simplificada:

#### Windows

1. **Execute o launcher:**
   - Duplo-clique em `executar_windows.bat`
   
2. **O que acontece automaticamente:**
   - ✅ Verifica se Python está instalado
   - ✅ Verifica se tkinter está disponível (para GUI)
   - ✅ Instala dependências necessárias (Pillow, requests)
   - ✅ Cria estrutura de pastas
   - ✅ Inicia o programa

3. **Se Python não estiver instalado:**
   - Baixe em: https://www.python.org/downloads/
   - **IMPORTANTE:** Durante a instalação, marque:
     - ☑️ Add Python to PATH
     - ☑️ Install tcl/tk and IDLE

#### macOS / Linux

1. **Execute o launcher:**
   ```bash
   ./executar_macos_linux.sh
   ```

2. **O script faz tudo automaticamente:**
   - ✅ Verifica Python3
   - ✅ Verifica tkinter
   - ✅ Instala dependências
   - ✅ Cria estrutura de pastas
   - ✅ Inicia o programa

3. **Se tkinter não estiver instalado:**
   ```bash
   # macOS (Homebrew)
   brew install python-tk
   
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # Fedora/RHEL
   sudo dnf install python3-tkinter
   ```

#### Instalação Manual (Alternativa)

```bash
# Clone ou baixe o projeto
cd PythonProject

# Instale as dependências
pip install Pillow requests

# Execute o programa
python playlist.py        # Windows
python3 playlist.py       # macOS/Linux
```

---

## Como Usar

### Primeira Execução

Ao executar pela primeira vez, você verá o menu principal:

```
============================================================
     SISTEMA DE GERENCIAMENTO DE PLAYLIST
============================================================

------------------------------------------------------------
                  OPÇÕES DISPONÍVEIS
------------------------------------------------------------

  1. Interface Gráfica
  2. Linha de Comando (CLI)
  3. Ver Documentação
  4. Sair

------------------------------------------------------------

Escolha uma opção (1-4):
```

### Opção 1: Interface Gráfica (GUI)

A interface gráfica oferece a melhor experiência visual:

- **Visualização de capas** de álbuns
- **Design moderno** e intuitivo
- **Busca em tempo real** enquanto você digita
- **Operações com cliques** simples
- **Estatísticas visuais** da playlist

**Requisito:** tkinter instalado (verificado automaticamente)

### Opção 2: Linha de Comando (CLI)

Interface rápida e eficiente via terminal:

- **Rápida e leve**
- **Funciona em qualquer terminal**
- **Ideal para servidores sem GUI**
- **Navegação por teclado**

**Requisito:** Apenas Python (sempre disponível)

### Opção 3: Ver Documentação

Abre este guia no seu navegador ou editor padrão.

### Opção 4: Sair

Encerra o programa de forma segura.

---

## Funcionalidades Detalhadas

### Adicionar Música

#### Modo Manual:
1. Digite o título da música
2. Digite o nome do artista
3. (Opcional) Digite álbum, gênero e ano

#### Modo Automático (Recomendado):
1. Digite o título da música
2. Digite o nome do artista
3. Clique em "🔍 Buscar Informações Automáticas"
4. O sistema busca automaticamente:
   - Nome do álbum
   - Gênero musical
   - Ano de lançamento
   - Capa do álbum (600x600px)

**Exemplo:**
```
Título: Thriller
Artista: Michael Jackson
[Buscar Automático]

Resultado:
✅ Álbum: Thriller
✅ Gênero: Pop
✅ Ano: 1982
✅ Capa: Baixada
```

### Listar Músicas

**Na GUI:**
- Visualização em cards com capas
- Informações completas de cada música
- Rolagem suave
- Cores por gênero

**Na CLI:**
```
--- Lista de Músicas ---
1. Título: Thriller | Artista: Michael Jackson | Álbum: Thriller | Gênero: Pop | Ano: 1982
2. Título: Imagine | Artista: John Lennon | Álbum: Imagine | Gênero: Rock | Ano: 1971
```

### Buscar Música

**Busca Inteligente:**
- ✅ Busca em **todos os campos** (título, artista, álbum, gênero)
- ✅ **Ignora acentos** (busque "beyonce" e encontre "Beyoncé")
- ✅ **Ignora maiúsculas/minúsculas**
- ✅ **Correspondência parcial** (busque "thrill" e encontre "Thriller")
- ✅ **Busca em tempo real** na GUI

**Exemplos de busca:**
- "rock" → Encontra todas as músicas do gênero Rock
- "beatles" → Encontra todas as músicas dos Beatles
- "198" → Encontra todas as músicas dos anos 1980-1989
- "love" → Encontra títulos como "Love Me Do", "Lovely Day", etc.

### Editar Música

1. Selecione a música a editar
2. Modifique os campos desejados
3. Salve as alterações

**Campos editáveis:**
- Título
- Artista
- Álbum
- Gênero
- Ano

### Remover Música

1. Selecione a música a remover
2. Confirme a remoção
3. A música é excluída permanentemente

**Aviso:** Esta ação não pode ser desfeita!

### Gerar Relatório

Crie relatórios personalizados filtrando por:

- **Título** - Músicas com título específico
- **Artista** - Todas as músicas de um artista
- **Álbum** - Todas as músicas de um álbum
- **Gênero** - Todas as músicas de um gênero
- **Ano** - Músicas de um ano específico

**Exemplo de relatório:**
```
=== Relatório: GÊNERO = Pop ===

Total: 5 música(s)

1. Thriller
   Artista: Michael Jackson
   Álbum: Thriller (1982)
   Gênero: Pop

2. Billie Jean
   Artista: Michael Jackson
   Álbum: Thriller (1982)
   Gênero: Pop
```

### Recursos da GUI:

#### Barra de Busca
- Digite para filtrar em tempo real
- Busca em todos os campos
- Ignora acentos e maiúsculas

#### Cards de Música
- **Capa do álbum** (se disponível)
- **Título em destaque**
- Artista, álbum e ano
- Gênero
- Botões de ação:
  -  Editar
  -  Remover
  -  Trocar Imagem

#### Painel de Ações
- Adicionar Música
- Gerar Relatório
- Salvar Playlist
- Recarregar Dados

#### Painel de Estatísticas
- Total de músicas
- Artistas únicos
- Gêneros únicos

### Atalhos de Teclado (GUI):

- `Ctrl + F` - Focar na busca
- `Ctrl + N` - Nova música
- `Ctrl + S` - Salvar playlist
- `Ctrl + R` - Recarregar dados
- `Escape` - Cancelar janela modal

---

## 💻 Interface de Linha de Comando (CLI)

### Menu Principal (CLI)

```
--- MENU PLAYLIST ---
1. Adicionar Música
2. Listar Músicas
3. Buscar Música (por Título)
4. Editar Música
5. Remover Música
6. Gerar Relatório (Filtrar por Campo)
7. Sair

Escolha uma opção:
```

### Fluxo de Uso (CLI)

#### Adicionar Música:
```
--- Adicionar Nova Música ---
Título: Bohemian Rhapsody
Artista: Queen
Álbum: A Night at the Opera
Gênero: Rock
Ano: 1975

Música adicionada com sucesso!
```

#### Buscar Música:
```
--- Buscar Música ---
Digite o título da música: rock

2 música(s) encontrada(s):
Título: Bohemian Rhapsody | Artista: Queen | Álbum: A Night at the Opera | Gênero: Rock | Ano: 1975
Título: Stairway to Heaven | Artista: Led Zeppelin | Álbum: Led Zeppelin IV | Gênero: Rock | Ano: 1971
```

#### Gerar Relatório:
```
--- Gerar Relatório ---
Escolha o campo para filtrar:
1. Título
2. Artista
3. Álbum
4. Gênero
5. Ano

Escolha uma opção (1-5): 4
Digite o Gênero para filtrar: Rock

--- Relatório: Gênero = Rock ---
Total de 2 música(s) encontrada(s):

1. Título: Bohemian Rhapsody | Artista: Queen | Álbum: A Night at the Opera | Gênero: Rock | Ano: 1975
2. Título: Stairway to Heaven | Artista: Led Zeppelin | Álbum: Led Zeppelin IV | Gênero: Rock | Ano: 1971
```

---

## Busca Automática de Músicas

### Como Funciona:

O sistema utiliza a **iTunes Search API** para buscar informações:

1. Você fornece título e artista
2. O sistema consulta a API da Apple
3. Recebe informações oficiais:
   - Nome correto do álbum
   - Gênero musical
   - Ano de lançamento
   - URL da capa (600x600px)
4. Baixa a capa automaticamente
5. Salva em `data/album_covers/`

---

## Solução de Problemas

### Problema: "Python não encontrado"

**Windows:**
1. Baixe Python em: https://www.python.org/downloads/
2. Execute o instalador
3. **MARQUE:** ☑️ Add Python to PATH
4. **MARQUE:** ☑️ Install tcl/tk and IDLE
5. Reinicie o computador
6. Execute o launcher novamente

**macOS:**
```bash
brew install python3
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip
```

### Problema: "tkinter não encontrado"

**Sintoma:** Interface gráfica não abre

**Windows:**
- Reinstale o Python marcando: ☑️ Install tcl/tk and IDLE

**macOS:**
```bash
brew install python-tk
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### Problema: "TERM environment variable not set"

**Solução:** Este problema foi corrigido na versão atual. Atualize o arquivo `playlist.py`.

### Problema: Dependências não instalam

**Solução manual:**
```bash
# Windows
python -m pip install --upgrade pip
python -m pip install Pillow requests

# macOS/Linux
python3 -m pip install --upgrade pip
python3 -m pip install Pillow requests
```

### Problema: Busca automática não funciona

**Causas possíveis:**
1. Sem conexão com internet
2. Nome da música/artista incorreto
3. Música muito obscura

**Solução:**
- Verifique sua conexão
- Use nomes oficiais
- Adicione manualmente se necessário

### Problema: Capas não aparecem

**Causas possíveis:**
1. Capa não foi baixada
2. Arquivo corrompido
3. Pasta album_covers com permissões incorretas

**Solução:**
```bash
# Verifique a pasta
ls -la data/album_covers/

# Dê permissões corretas (Unix)
chmod 755 data/album_covers/

# Tente baixar novamente
# Opção: Clique em "Imagem" no card da música
```

### Problema: Playlist não salva

**Causas possíveis:**
1. Sem permissão de escrita
2. Pasta data/ não existe

**Solução:**
```bash
# Crie a pasta manualmente
mkdir -p data

# Dê permissões corretas (Unix)
chmod 755 data/
```

---

## Perguntas Frequentes

### 1. Preciso estar online para usar?

**Não!** O programa funciona 100% offline, exceto:
- Busca automática de músicas (requer internet)
- Download de capas de álbuns (requer internet)

Você pode adicionar músicas manualmente sem internet.

### 2. Onde ficam salvos meus dados?

Seus dados ficam em:
- **Playlist:** `data/playlist.txt`
- **Capas:** `data/album_covers/`

### 3. Posso fazer backup da minha playlist?

**Sim!** Basta copiar a pasta `data/`:
```bash
# Backup
cp -r data/ backup_playlist/

# Restaurar
cp -r backup_playlist/ data/
```

### 4. Como importar músicas de outro arquivo?

Edite manualmente o arquivo `data/playlist.txt`:

Formato: `Título;Artista;Álbum;Gênero;Ano`

Exemplo:
```
Bohemian Rhapsody;Queen;A Night at the Opera;Rock;1975
Imagine;John Lennon;Imagine;Rock;1971
```

### 5. Quantas músicas posso adicionar?

**Ilimitadas!** O programa não tem limite de músicas.

### 6. Posso usar em um servidor sem GUI?

**Sim!** Use a opção 2 (CLI) que funciona via terminal.

### 7. Como contribuir com o projeto?

O projeto é open source. Entre em contato com os desenvolvedores.

### 8. Há versão mobile?

Não no momento. Apenas desktop (Windows, macOS, Linux).

### 9. Posso tocar as músicas pelo programa?

Não. O programa apenas **gerencia informações** sobre as músicas, não toca áudio.

### 10. Como atualizar o programa?

Baixe a versão mais recente e substitua os arquivos, mantendo a pasta `data/` para preservar suas músicas.

---

### API Utilizada:

**iTunes Search API**
- URL: https://itunes.apple.com/search
- Documentação: https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/
- Licença: Gratuita, sem necessidade de cadastro

---

*Última atualização: Novembro 2025*

