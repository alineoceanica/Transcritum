import sys
import os
import json
import traceback
from pathlib import Path

from faster_whisper import WhisperModel


APP_NAME = "Transcritum"
APP_BRAND = "Verum Scientia"
APP_VERSION = "1.0"

EXTENSOES_AUDIO = {".m4a", ".mp3", ".wav", ".m4b"}


# ===============================================================
# CABEÇALHO
# ===============================================================

def cabecalho():
    print()
    print("=" * 59)
    print("                    T R A N S C R I T U M")
    print("                       VERUM SCIENTIA")
    print("=" * 59)
    print(f"Versão {APP_VERSION}")
    print()


# ===============================================================
# ÁREA DO TRANSCRITUM
# ===============================================================

def preparar_area():
    base = Path.home() / "Transcritum"
    projetos = base / "Projetos"

    projetos.mkdir(parents=True, exist_ok=True)

    return base, projetos

# ===============================================================
# NOMES DE PROJETOS
# ===============================================================

def limpar_nome(nome):
    caracteres_invalidos = '<>:"/\\|?*'

    for caractere in caracteres_invalidos:
        nome = nome.replace(caractere, "_")

    return nome.strip()


# ===============================================================
# CRIAR PROJETO
# ===============================================================

def criar_projeto(pasta_projetos):
    print()
    nome = input("Digite o nome do novo projeto: ").strip()

    if not nome:
        print()
        print("[ERRO] O projeto precisa ter um nome.")
        return None

    nome = limpar_nome(nome)

    projeto = pasta_projetos / nome

    (projeto / "Audios").mkdir(parents=True, exist_ok=True)
    (projeto / "Transcricoes").mkdir(parents=True, exist_ok=True)
    (projeto / "Traducoes").mkdir(parents=True, exist_ok=True)

    print()
    print("Projeto preparado com sucesso:")
    print(projeto)

    return projeto


# ===============================================================
# ESCOLHER PROJETO
# ===============================================================

def escolher_projeto(pasta_projetos):
    projetos = sorted(
        [p for p in pasta_projetos.iterdir() if p.is_dir()],
        key=lambda p: p.name.lower()
    )

    if not projetos:
        print()
        print("Ainda não existem projetos.")
        return criar_projeto(pasta_projetos)

    print()
    print("=" * 59)
    print("PROJETOS")
    print("=" * 59)
    print()

    for numero, projeto in enumerate(projetos, start=1):
        print(f"{numero}) {projeto.name}")

    print()
    escolha = input("Digite o número do projeto: ").strip()

    if not escolha.isdigit():
        print()
        print("[ERRO] Escolha inválida.")
        return None

    numero = int(escolha)

    if numero < 1 or numero > len(projetos):
        print()
        print("[ERRO] Escolha inválida.")
        return None

    projeto = projetos[numero - 1]

    (projeto / "Audios").mkdir(exist_ok=True)
    (projeto / "Transcricoes").mkdir(exist_ok=True)
    (projeto / "Traducoes").mkdir(exist_ok=True)

    return projeto


# ===============================================================
# MENU DE PROJETOS
# ===============================================================

def menu_projetos(pasta_projetos):
    print("O que deseja fazer?")
    print()
    print("1) Criar novo projeto")
    print("2) Abrir projeto existente")
    print()

    escolha = input("Escolha (1 ou 2): ").strip()

    if escolha == "1":
        return criar_projeto(pasta_projetos)

    if escolha == "2":
        return escolher_projeto(pasta_projetos)

    print()
    print("[ERRO] Opção inválida.")
    return None


# ===============================================================
# IDIOMA
# ===============================================================

def escolher_idioma():
    print()
    print("=" * 59)
    print("IDIOMA DO ÁUDIO")
    print("=" * 59)
    print()
    print("1) Português")
    print("2) Español")
    print("3) English")
    print("4) Detectar automaticamente")
    print()

    escolha = input("Escolha o idioma do áudio (1 a 4): ").strip()

    idiomas = {
        "1": ("Português", "pt", "small"),
        "2": ("Español", "es", "small"),
        "3": ("English", "en", "small.en"),
        "4": ("Detecção automática", None, "small"),
    }

    return idiomas.get(escolha)


# ===============================================================
# LOCALIZAR ÁUDIOS
# ===============================================================

def localizar_audios(projeto):
    pasta_audios = projeto / "Audios"

    audios = sorted(
        [
            arquivo
            for arquivo in pasta_audios.iterdir()
            if arquivo.is_file()
            and arquivo.suffix.lower() in EXTENSOES_AUDIO
        ],
        key=lambda p: p.name.lower()
    )

    return audios


# ===============================================================
# ESCOLHER ÁUDIOS
# ===============================================================

def escolher_audios(projeto):
    audios = localizar_audios(projeto)

    if not audios:
        print()
        print("[ERRO] Nenhum áudio encontrado.")
        print()
        print("Coloque o arquivo de áudio nesta pasta:")
        print(projeto / "Audios")
        return None

    print()
    print("=" * 59)
    print("ÁUDIOS")
    print("=" * 59)
    print()

    for numero, audio in enumerate(audios, start=1):
        print(f"{numero}) {audio.name}")

    print()
    print("A) Transcrever TODOS")
    print()

    escolha = input("Escolha: ").strip()

    if escolha.upper() == "A":
        return audios

    if not escolha.isdigit():
        print()
        print("[ERRO] Escolha inválida.")
        return None

    numero = int(escolha)

    if numero < 1 or numero > len(audios):
        print()
        print("[ERRO] Escolha inválida.")
        return None

    return [audios[numero - 1]]


# ===============================================================
# FORMATAÇÃO DE TEMPO
# ===============================================================

def timestamp_log(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos_restantes = segundos % 60

    return (
        f"{horas:02d}:"
        f"{minutos:02d}:"
        f"{segundos_restantes:06.3f}"
    )


def timestamp_srt(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos_inteiros = int(segundos % 60)
    milissegundos = int(round((segundos - int(segundos)) * 1000))

    if milissegundos == 1000:
        milissegundos = 0
        segundos_inteiros += 1

    return (
        f"{horas:02d}:"
        f"{minutos:02d}:"
        f"{segundos_inteiros:02d},"
        f"{milissegundos:03d}"
    )


def timestamp_vtt(segundos):
    return timestamp_srt(segundos).replace(",", ".")


# ===============================================================
# GRAVAR ARQUIVOS
# ===============================================================

def gravar_saidas(audio, segmentos, idioma, duracao, pasta_saida):
    stem = audio.stem

    caminho_txt = pasta_saida / f"{stem}.txt"
    caminho_srt = pasta_saida / f"{stem}.srt"
    caminho_vtt = pasta_saida / f"{stem}.vtt"
    caminho_tsv = pasta_saida / f"{stem}.tsv"
    caminho_json = pasta_saida / f"{stem}.json"

    # TXT
    with open(caminho_txt, "w", encoding="utf-8") as arquivo:
        for segmento in segmentos:
            texto = segmento["text"].strip()

            if texto:
                arquivo.write(texto + "\n")

    # SRT
    with open(caminho_srt, "w", encoding="utf-8") as arquivo:
        for numero, segmento in enumerate(segmentos, start=1):
            arquivo.write(f"{numero}\n")
            arquivo.write(
                f"{timestamp_srt(segmento['start'])} --> "
                f"{timestamp_srt(segmento['end'])}\n"
            )
            arquivo.write(segmento["text"].strip() + "\n\n")

    # VTT
    with open(caminho_vtt, "w", encoding="utf-8") as arquivo:
        arquivo.write("WEBVTT\n\n")

        for segmento in segmentos:
            arquivo.write(
                f"{timestamp_vtt(segmento['start'])} --> "
                f"{timestamp_vtt(segmento['end'])}\n"
            )
            arquivo.write(segmento["text"].strip() + "\n\n")

    # TSV
    with open(caminho_tsv, "w", encoding="utf-8") as arquivo:
        arquivo.write("start\tend\ttext\n")

        for segmento in segmentos:
            inicio_ms = int(round(segmento["start"] * 1000))
            fim_ms = int(round(segmento["end"] * 1000))
            texto = segmento["text"].strip().replace("\t", " ")

            arquivo.write(
                f"{inicio_ms}\t{fim_ms}\t{texto}\n"
            )

    # JSON
    dados_json = {
        "language": idioma,
        "duration": duracao,
        "text": " ".join(
            segmento["text"].strip()
            for segmento in segmentos
            if segmento["text"].strip()
        ),
        "segments": segmentos,
    }

    with open(caminho_json, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados_json,
            arquivo,
            ensure_ascii=False,
            indent=2
        )


# ===============================================================
# TRANSCRIÇÃO
# ===============================================================

def transcrever_audio(
    modelo,
    audio,
    idioma_codigo,
    idioma_nome,
    pasta_saida
):
    stem = audio.stem
    log = pasta_saida / f"{stem}_whisper.log"

    print()
    print("-" * 59)
    print(f"Transcrevendo: {audio.name}")
    print(f"Idioma:        {idioma_nome}")
    print(f"Saída:         {pasta_saida}")
    print(f"Log:           {log}")
    print("-" * 59)
    print()

    try:
        segmentos_gerador, info = modelo.transcribe(
            str(audio),
            language=idioma_codigo,
            task="transcribe",
            beam_size=1,
            temperature=0.0,
            vad_filter=False
        )

        segmentos = []

        duracao = float(info.duration) if info.duration else 0.0

        with open(log, "w", encoding="utf-8") as arquivo_log:

            if idioma_codigo is None:
                arquivo_log.write(
                    f"Idioma detectado: {info.language}\n"
                )
                arquivo_log.write(
                    f"Probabilidade: {info.language_probability:.4f}\n\n"
                )

            for segmento in segmentos_gerador:
                texto = segmento.text.strip()

                dados_segmento = {
                    "id": segmento.id,
                    "start": float(segmento.start),
                    "end": float(segmento.end),
                    "text": texto,
                }

                segmentos.append(dados_segmento)

                linha_log = (
                    f"[{timestamp_log(segmento.start)} --> "
                    f"{timestamp_log(segmento.end)}]  "
                    f"{texto}"
                )

                arquivo_log.write(linha_log + "\n")
                arquivo_log.flush()

                if duracao > 0:
                    progresso = min(
                        100.0,
                        (segmento.end / duracao) * 100
                    )

                    print(
                        f"\rProgresso: {progresso:5.1f}%",
                        end="",
                        flush=True
                    )

        print("\rProgresso: 100.0%")

        gravar_saidas(
            audio=audio,
            segmentos=segmentos,
            idioma=info.language,
            duracao=duracao,
            pasta_saida=pasta_saida
        )

        print()
        print(f"OK: {audio.name}")

        return True

    except Exception:
        with open(log, "a", encoding="utf-8") as arquivo_log:
            arquivo_log.write("\n\n")
            arquivo_log.write("=" * 59)
            arquivo_log.write("\nERRO DURANTE A TRANSCRIÇÃO\n")
            arquivo_log.write("=" * 59)
            arquivo_log.write("\n\n")
            traceback.print_exc(file=arquivo_log)

        print()
        print()
        print(f"[ERRO] Não foi possível transcrever: {audio.name}")
        print(f"Consulte o log: {log}")

        return False


# ===============================================================
# PROGRAMA PRINCIPAL
# ===============================================================

def main():
    cabecalho()

    base, pasta_projetos = preparar_area()

    print("Área de trabalho:")
    print(base)
    print()

    projeto = menu_projetos(pasta_projetos)

    if projeto is None:
        input("\nPressione Enter para sair...")
        sys.exit(1)

    print()
    print("=" * 59)
    print(f"PROJETO: {projeto.name}")
    print("=" * 59)

    idioma = escolher_idioma()

    if idioma is None:
        print()
        print("[ERRO] Opção de idioma inválida.")
        input("\nPressione Enter para sair...")
        sys.exit(1)

    idioma_nome, idioma_codigo, nome_modelo = idioma

    audios = escolher_audios(projeto)

    if not audios:
        input("\nPressione Enter para sair...")
        sys.exit(1)

    pasta_saida = projeto / "Transcricoes"

    print()
    print("=" * 59)
    print("PREPARANDO A TRANSCRIÇÃO")
    print("=" * 59)
    print()
    print(f"Idioma: {idioma_nome}")
    print(f"Modelo: {nome_modelo}")
    print()
    print("Preparando o modelo de transcrição...")
    print("Isso pode levar alguns instantes na primeira utilização.")
    print()

    try:
        numero_processadores = os.cpu_count() or 1

        modelo = WhisperModel(
            nome_modelo,
            device="cpu",
            compute_type="int8",
            cpu_threads=numero_processadores,
            num_workers=1
        )

    except Exception:
        print()
        print("[ERRO] Não foi possível preparar o modelo de transcrição.")
        print()
        traceback.print_exc()
        input("\nPressione Enter para sair...")
        sys.exit(1)

    print("Modelo preparado com sucesso.")
    print()

    falhas = 0

    for audio in audios:
        sucesso = transcrever_audio(
            modelo=modelo,
            audio=audio,
            idioma_codigo=idioma_codigo,
            idioma_nome=idioma_nome,
            pasta_saida=pasta_saida
        )

        if not sucesso:
            falhas += 1

    print()
    print("=" * 59)

    if falhas == 0:
        print("                 TRANSCRIÇÃO CONCLUÍDA")
        print("=" * 59)
        print()
        print("Todos os arquivos foram processados com sucesso.")

    else:
        print("              CONCLUÍDO COM ERROS")
        print("=" * 59)
        print()
        print(f"Arquivos com erro: {falhas}")
        print("Consulte os respectivos arquivos _whisper.log.")

    print()
    print("Resultados em:")
    print(pasta_saida)
    print()

    input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()