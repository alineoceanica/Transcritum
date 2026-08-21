# Transcritum — Verum Scientia


Transcritum é uma ferramenta open source de transcrição local de áudio para Windows, desenvolvida com `faster-whisper`.


O programa foi criado para facilitar a transcrição de arquivos em português, espanhol e inglês, organizando automaticamente os resultados por projetos.


## Recursos


- Transcrição em português
- Transcrição em espanhol
- Transcrição em inglês
- Detecção automática de idioma
- Processamento local dos arquivos de áudio
- Organização por projetos
- Processamento individual ou em lote
- Geração de arquivos TXT, SRT, VTT, TSV e JSON
- Registro segmentado da transcrição em arquivo de log
- Processamento otimizado para CPU com `faster-whisper`


## Formatos de áudio aceitos


- M4A
- MP3
- WAV
- M4B


## Estrutura dos projetos


O Transcritum cria automaticamente uma área de trabalho dentro da pasta do usuário:


```text
Transcritum
└── Projetos
    └── Nome do Projeto
        ├── Audios
        ├── Transcricoes
        └── Traducoes

Os arquivos de áudio devem ser colocados na pasta Audios.

Os arquivos gerados pelo Transcritum são armazenados automaticamente na pasta Transcricoes.

A pasta Traducoes está reservada para uma funcionalidade futura.

Arquivos gerados

Para cada áudio transcrito, o Transcritum pode gerar:

.txt — texto simples
.srt — legendas no formato SubRip
.vtt — legendas WebVTT
.tsv — dados tabulados com marcações de tempo
.json — dados estruturados da transcrição
_whisper.log — registro segmentado da transcrição
Requisitos

A versão atual foi desenvolvida e testada em:

Windows
Python 3.12
faster-whisper 1.2.1
Instalação pelo código-fonte

Clone o repositório:

git clone https://github.com/alineoceanica/Transcritum.git

Entre na pasta do projeto:

cd Transcritum

Crie um ambiente virtual:

python -m venv venv

No Windows, ative o ambiente:

venv\Scripts\activate

Instale as dependências:

python -m pip install -r requirements.txt

Execute o programa:

python transcritum.py
Primeira utilização

Na primeira utilização de determinado modelo de transcrição, os arquivos necessários são baixados automaticamente.

Esse download pode levar alguns instantes, dependendo da velocidade da conexão.

Depois de armazenado localmente, o modelo pode ser reutilizado nas próximas transcrições sem precisar ser baixado novamente.

Privacidade

A transcrição dos arquivos de áudio é realizada localmente no computador do usuário.

Os arquivos de áudio não precisam ser enviados a um serviço externo para serem transcritos.

Uma conexão com a internet pode ser necessária na primeira utilização para baixar o modelo de transcrição.

Desempenho

O tempo necessário para transcrever um arquivo depende de fatores como:

duração do áudio;
capacidade do processador;
modelo utilizado;
qualidade e características do áudio.

O Transcritum utiliza faster-whisper com processamento otimizado para CPU.

Idiomas

Atualmente, o programa oferece quatro opções:

Português
Español
English
Detecção automática de idioma

Para inglês, o Transcritum utiliza o modelo small.en.

Para português, espanhol e detecção automática, utiliza o modelo multilíngue small.

Projeto open source

Transcritum — Verum Scientia é um projeto de código aberto.

Contribuições, correções e melhorias são bem-vindas.

Licença

Este projeto é distribuído sob a GNU General Public License v3.0 (GPLv3).

Consulte o arquivo LICENSE para o texto completo da licença.

Autoria

Transcritum — Verum Scientia

Criado por Aline Cardinale.

GitHub: alineoceanica

Versão

v1.0.0

