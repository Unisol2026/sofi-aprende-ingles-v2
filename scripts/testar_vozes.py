#!/usr/bin/env python3
"""
Script de comparação de vozes para o app "Sofi learns English"
Gera amostras de áudio para você ouvir e escolher a melhor voz.

COMO USAR:
  1. Cole sua API key abaixo (linha 20)
  2. Execute:  python scripts/testar_vozes.py
  3. Ouça os arquivos gerados em: teste_vozes/
  4. Escolha sua favorita e informe para atualizar o script principal

Não precisa ter o projeto configurado — este script roda sozinho.
"""

# ─── SUA CHAVE AQUI ───────────────────────────────────────────────────────────
GOOGLE_API_KEY = ""   # ex: "AIzaSyXXXXXXXXXXXXXXX"
# ──────────────────────────────────────────────────────────────────────────────

from pathlib import Path
import time

# Frases de teste — típicas do app da Sofia
FRASES_TESTE = [
    ("red",         "Red!",                             "word"),
    ("sit_down",    "Sit down.",                        "expression"),
    ("teddy_bear",  "This is a teddy bear.",            "phrase"),
    ("im_happy",    "I'm happy.",                       "expression"),
    ("i_like",      "I like ice cream.",                "phrase"),
]

# Vozes para testar
# Formato: (nome_arquivo, modelo, nome_da_voz, descrição)
VOZES = [
    # ── Chirp 3 HD (mais recente, mais natural) ────────────────────────
    ("chirp3_kore",       "Chirp3-HD", "en-US-Chirp3-HD-Kore",       "Chirp3 HD · Kore (feminina, suave)"),
    ("chirp3_aoede",      "Chirp3-HD", "en-US-Chirp3-HD-Aoede",      "Chirp3 HD · Aoede (feminina, calorosa)"),
    ("chirp3_leda",       "Chirp3-HD", "en-US-Chirp3-HD-Leda",       "Chirp3 HD · Leda (feminina, clara)"),
    ("chirp3_zephyr",     "Chirp3-HD", "en-US-Chirp3-HD-Zephyr",     "Chirp3 HD · Zephyr (feminina, leve)"),
    ("chirp3_callirrhoe", "Chirp3-HD", "en-US-Chirp3-HD-Callirrhoe", "Chirp3 HD · Callirrhoe (feminina)"),
    # ── Neural2 (plano original — referência de comparação) ────────────
    ("neural2_h",         "Neural2",   "en-US-Neural2-H",             "Neural2 · H (feminina) ← referência"),
    ("neural2_f",         "Neural2",   "en-US-Neural2-F",             "Neural2 · F (feminina, mais jovem)"),
]

FRASE_DEMO = "Red! This is a teddy bear. Sit down. I'm happy. I like ice cream."


def sintetizar_chirp3(client, texto: str, voz: str, speed: float) -> bytes:
    """Chirp 3 HD: suporta speaking_rate, MAS não suporta pitch nem effects_profile_id."""
    from google.cloud import texttospeech
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=texto),
        voice=texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voz,
        ),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed,
            # ⚠️  Chirp3-HD NÃO suporta pitch nem effects_profile_id
        ),
    )
    return response.audio_content


def sintetizar_neural2(client, texto: str, voz: str, speed: float) -> bytes:
    """Neural2: suporta speaking_rate, pitch e effects_profile_id."""
    from google.cloud import texttospeech
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=texto),
        voice=texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voz,
        ),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed,
            pitch=0.0,
            effects_profile_id=["headphone-class-device"],
        ),
    )
    return response.audio_content


def main():
    try:
        from google.cloud import texttospeech
    except ImportError:
        print("❌  Instale a biblioteca primeiro:")
        print("    pip install google-cloud-texttospeech")
        return

    if not GOOGLE_API_KEY:
        print("❌  Cole sua API key na linha 20 do script.")
        return

    client = texttospeech.TextToSpeechClient(
        client_options={"api_key": GOOGLE_API_KEY}
    )

    out_dir = Path("teste_vozes")
    out_dir.mkdir(exist_ok=True)

    print(f"\n🎙  Gerando amostras de {len(VOZES)} vozes × {len(FRASES_TESTE)} frases...\n")
    print("📂  Arquivos serão salvos em: ./teste_vozes/\n")
    print("─" * 60)

    erros = 0
    gerados = 0

    for voz_slug, modelo, voz_nome, descricao in VOZES:
        voz_dir = out_dir / voz_slug
        voz_dir.mkdir(exist_ok=True)

        print(f"\n🎤  {descricao}")

        # Gera um arquivo combinado com todas as frases (mais fácil de comparar)
        demo_path = voz_dir / "00_DEMO_TODAS_AS_FRASES.mp3"
        if not demo_path.exists():
            try:
                if modelo == "Chirp3-HD":
                    data = sintetizar_chirp3(client, FRASE_DEMO, voz_nome, speed=0.85)
                else:
                    data = sintetizar_neural2(client, FRASE_DEMO, voz_nome, speed=0.85)
                demo_path.write_bytes(data)
                kb = len(data) / 1024
                print(f"  ✓  {demo_path.name}  ({kb:.0f} KB)  ← OUÇA ESTE PRIMEIRO")
                gerados += 1
                time.sleep(0.2)
            except Exception as e:
                print(f"  ✗  ERRO no demo: {e}")
                erros += 1
                time.sleep(1)
                continue

        # Gera cada frase individualmente
        for slug, texto, tipo in FRASES_TESTE:
            path = voz_dir / f"{slug}.mp3"
            if path.exists():
                print(f"  ⏭  {path.name}  (já existe)")
                continue
            try:
                speed = 0.80 if tipo == "word" else 0.85
                if modelo == "Chirp3-HD":
                    data = sintetizar_chirp3(client, texto, voz_nome, speed)
                else:
                    data = sintetizar_neural2(client, texto, voz_nome, speed)
                path.write_bytes(data)
                kb = len(data) / 1024
                print(f"  ✓  {path.name}  ({kb:.0f} KB)")
                gerados += 1
                time.sleep(0.15)
            except Exception as e:
                print(f"  ✗  {path.name}  ERRO: {e}")
                erros += 1
                time.sleep(1)

    print(f"\n{'═' * 60}")
    print(f"✅  {gerados} arquivos gerados, {erros} erros.")
    print(f"\n📂  Abra a pasta:  teste_vozes\\")
    print(f"🎧  Ouça o arquivo '00_DEMO_TODAS_AS_FRASES.mp3' de cada voz.")
    print(f"\n📋  Vozes disponíveis:")
    for slug, modelo, nome, desc in VOZES:
        print(f"     {slug:25s}  →  {desc}")
    print(f"\n💬  Me diga qual preferiu e atualizo o script principal!")
    print(f"{'═' * 60}\n")


if __name__ == "__main__":
    main()
