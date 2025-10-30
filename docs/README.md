# 📚 Documentação - Sistema de Gerenciamento de Playlist

---

## 📖 Documentos Disponíveis

### 🎯 [GUIA_COMPLETO.md](GUIA_COMPLETO.md)
**Guia detalhado com tudo que você precisa saber:**
- ✅ Instalação passo a passo
- ✅ Como usar cada funcionalidade
- ✅ Interface Gráfica e CLI detalhadas
- ✅ Busca automática de músicas
- ✅ Solução de problemas
- ✅ Perguntas frequentes
- ✅ Exemplos práticos

👉 **Recomendado para iniciantes e para consulta completa!**

---

## 🚀 Início Rápido

### Windows
```cmd
executar_windows.bat
```
(Duplo-clique no arquivo)

### macOS / Linux
```bash
./executar_macos_linux.sh
```

### Alternativa Universal
```bash
python playlist.py        # Windows
python3 playlist.py       # macOS/Linux
```

---

## ✨ Principais Funcionalidades

### 🎵 Gerenciamento de Músicas
- ➕ Adicionar músicas (manual ou automático)
- 📚 Listar com visualização de capas
- 🔍 Buscar de forma inteligente
- ✏️ Editar informações
- 🗑️ Remover com confirmação

### 🌐 Busca Automática (iTunes API)
- 📀 Nome do álbum
- 🎸 Gênero musical
- 📅 Ano de lançamento
- 🖼️ Capa do álbum (600x600px)

### 📊 Relatórios e Estatísticas
- Filtros por título, artista, álbum, gênero, ano
- Estatísticas da playlist
- Exportação de dados

---

## 🛠️ Requisitos

- **Python 3.8+**
- **Pillow** - Processamento de imagens
- **requests** - Chamadas à API
- **tkinter** - Interface gráfica (opcional)

> ✅ Os launchers instalam tudo automaticamente!

---

## 📁 Estrutura de Dados

### Arquivo da Playlist
**Localização:** `data/playlist.txt`  
**Formato:** `Título;Artista;Álbum;Gênero;Ano`

**Exemplo:**
```
Thriller;Michael Jackson;Thriller;Pop;1982
Imagine;John Lennon;Imagine;Rock;1971
Bohemian Rhapsody;Queen;A Night at the Opera;Rock;1975
```

### Capas de Álbuns
**Localização:** `data/album_covers/`  
**Formato:** PNG (600x600px)

---

## ❓ Problemas Comuns

### Python não encontrado?
👉 [Guia Completo - Instalação](GUIA_COMPLETO.md#instalação)

### tkinter não funciona?
👉 [Guia Completo - Solução: tkinter](GUIA_COMPLETO.md#problema-tkinter-não-encontrado)

### Busca automática não funciona?
👉 [Guia Completo - Busca Automática](GUIA_COMPLETO.md#busca-automática-de-músicas)

### Dependências não instalam?
👉 [Guia Completo - Solução: Dependências](GUIA_COMPLETO.md#problema-dependências-não-instalam)

---

## 🎨 Interfaces

### Interface Gráfica (GUI)
- 🖼️ Cards visuais com capas
- 🔍 Busca em tempo real
- 🎨 Design moderno
- 📊 Estatísticas visuais

### Linha de Comando (CLI)
- ⚡ Rápida e leve
- 💻 Funciona em qualquer terminal
- ⌨️ Navegação por teclado
- 🔧 Ideal para servidores

---

## 📞 Suporte

**Para informações detalhadas, consulte:**
📖 [GUIA_COMPLETO.md](GUIA_COMPLETO.md)

**Seções principais do guia:**
1. Visão Geral
2. Instalação Detalhada
3. Como Usar
4. Interface Gráfica
5. Interface CLI
6. Busca Automática
7. Solução de Problemas (15+ problemas cobertos)
8. Perguntas Frequentes (10+ perguntas)

---

## 🎓 Tecnologias

- **Python 3.8+**
- **Tkinter** - GUI multiplataforma
- **Pillow** - Processamento de imagens
- **requests** - HTTP
- **iTunes Search API** - Dados musicais

---

## 📄 Licença

Este projeto é de código aberto para fins educacionais.

---

**🎵 Boa música! 🎶**

*Para o guia completo e detalhado, veja [GUIA_COMPLETO.md](GUIA_COMPLETO.md)*

