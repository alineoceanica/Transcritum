\# Transcritum — Verum Scientia



Transcritum é uma ferramenta de transcrição de áudio desenvolvida para Windows, com suporte a português, espanhol e inglês.



O programa utiliza o faster-whisper para realizar transcrições localmente no computador do usuário.



\## Recursos



\- Transcrição em português

\- Transcrição em espanhol

\- Transcrição em inglês

\- Detecção automática de idioma

\- Processamento local dos arquivos

\- Organização por projetos

\- Processamento de um ou vários áudios

\- Geração de arquivos TXT, SRT, VTT, TSV e JSON

\- Registro detalhado da transcrição em arquivo de log



\## Formatos de áudio aceitos



\- M4A

\- MP3

\- WAV

\- M4B



\## Estrutura dos projetos



O Transcritum cria automaticamente uma pasta de trabalho no diretório do usuário:



```text

Transcritum

└── Projetos

&#x20;   └── Nome do Projeto

&#x20;       ├── Audios

&#x20;       ├── Transcricoes

&#x20;       └── Traduções

Os arquivos de áudio devem ser colocados na pasta Audios.



As transcrições são armazenadas automaticamente na pasta Transcricoes.



\# Requisitos para execução pelo código-fonte

Windows

Python 3.12

faster-whisper 1.2.1



Instale as dependências com:



python -m pip install -r requirements.txt



Depois execute:



python transcritum.py

Privacidade



A transcrição é realizada localmente no computador.



Os arquivos de áudio não precisam ser enviados a serviços externos para serem transcritos.



Na primeira utilização de determinado modelo, poderá ser necessário realizar o download dos arquivos correspondentes.



Projeto open source



Transcritum — Verum Scientia é um projeto de código aberto.



Licença prevista: GNU General Public License v3.0 (GPLv3).



Autoria



Transcritum — Verum Scientia



Projeto criado por Aline Cardinale.



Versão



Versão 1.0 — em desenvolvimento

