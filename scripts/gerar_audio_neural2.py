#!/usr/bin/env python3
"""
Gerador de áudios MP3 para o app "Sofi learns English" v2.0
Usa Google Cloud Text-to-Speech com voz Neural2 (en-US-Neural2-H)

SETUP (fazer uma vez):
  1. Instale a biblioteca:
       pip install google-cloud-texttospeech
  2. Configure a autenticação (escolha uma das opções):
     - Opção A (mais simples): Crie uma API key no Google Cloud Console
       e defina: GOOGLE_API_KEY = "SUA_CHAVE_AQUI" (linha 30)
     - Opção B (service account): Baixe o JSON e defina a variável de ambiente:
       set GOOGLE_APPLICATION_CREDENTIALS=caminho\para\chave.json
  3. Execute:
       python gerar_audio_neural2.py

OUTPUT:
  Gera arquivos MP3 em ./audio/{unit}/ relativo ao diretório onde o script é executado.
  Execute da raiz do projeto (onde está o index.html).
"""

import os
import re
import time
from pathlib import Path

# ─── CONFIGURAÇÃO ─────────────────────────────────────────────────────────────

# Coloque sua API key aqui se não usar service account
GOOGLE_API_KEY = ""  # ex: "AIzaSyXXXXXXXX"

# Voz escolhida: Chirp3-HD-Zephyr (testada e aprovada em 28/06/2026)
# Modelo mais recente do Google — qualidade superior ao Neural2
VOICE_NAME = "en-US-Chirp3-HD-Zephyr"
LANGUAGE_CODE = "en-US"

# Velocidade de fala (0.75 = devagar, bom para crianças)
WORD_SPEED  = 0.80   # para palavras isoladas
PHRASE_SPEED = 0.85  # para frases

# Pausa entre tentativas se der erro de rate limit (segundos)
RETRY_WAIT = 2

# ─── CONTEÚDO DO APP ──────────────────────────────────────────────────────────

UNITS = {
    "hello": {
        "words": [
            ("Red",        "red.png",        "Red!"),
            ("Blue",       "blue.png",       "Blue!"),
            ("Green",      "green.png",      "Green!"),
            ("Orange",     "orange.png",     "Orange!"),
            ("Purple",     "purple.png",     "Purple!"),
            ("Yellow",     "yellow.png",     "Yellow!"),
        ],
        "expressions": [
            "Hello!",
            "What's your name?",
            "I'm Sofia.",
        ],
    },
    "unit1": {
        "words": [
            ("Pencil",  "pencil.png",  "This is a pencil."),
            ("Chair",   "chair.png",   "This is a chair."),
            ("Bag",     "bag.png",     "This is a bag."),
            ("Rubber",  "rubber.png",  "This is a rubber."),
            ("Book",    "book.png",    "This is a book."),
            ("Desk",    "desk.png",    "This is a desk."),
            ("Seven",   "seven.png",   "Seven."),
            ("Eight",   "eight.png",   "Eight."),
            ("Nine",    "nine.png",    "Nine."),
            ("Ten",     "ten.png",     "Ten."),
        ],
        "expressions": [
            "Stand up.",
            "Sit down.",
            "Open your book.",
            "Close your book.",
            "Pick up your pencil.",
            "Put your bag on your desk.",
        ],
    },
    "unit2": {
        "words": [
            ("Grandpa", "grandpa.png", "This is grandpa."),
            ("Grandma", "grandma.png", "This is grandma."),
            ("Mum",     "mum.png",     "This is mum."),
            ("Dad",     "dad.png",     "This is dad."),
            ("Sister",  "sister.png",  "This is my sister."),
            ("Brother", "brother.png", "This is my brother."),
        ],
        "expressions": [
            "This is my brother.",
            "Open the door.",
            "Say hello to your mum.",
            "What's that?",
            "It's a sandwich.",
        ],
    },
    "unit3": {
        "words": [
            ("Eyes",   "eyes.png",  "These are eyes."),
            ("Ears",   "ears.png",  "These are ears."),
            ("Nose",   "nose.png",  "This is a nose."),
            ("Face",   "face.png",  "This is a face."),
            ("Teeth",  "teeth.png", "These are teeth."),
            ("Mouth",  "mouth.png", "This is a mouth."),
        ],
        "expressions": [
            "I'm happy.",
            "You're happy.",
            "I'm angry.",
            "I'm sad.",
            "I'm scared.",
            "Close your eyes.",
            "Open your eyes.",
            "Give your friend a hug.",
        ],
    },
    "unit4": {
        "words": [
            ("Ball",       "ball.png",       "I've got a ball."),
            ("Kite",       "kite.png",       "I've got a kite."),
            ("Rope",       "rope.png",       "This is a rope."),
            ("Teddy bear", "teddy-bear.png", "This is a teddy bear."),
            ("Doll",       "doll.png",       "This is a doll."),
            ("Plane",      "plane.png",      "This is a plane."),
        ],
        "expressions": [
            "I've got a ball.",
            "Throw the ball.",
            "Catch the ball.",
            "Bounce the ball.",
            "Put the ball in your bag.",
            "I haven't got a kite.",
        ],
    },
    "unit5": {
        "words": [
            ("Bathtub",    "bathtub.png",    "This is a bathtub. I love bubbles in the bathtub."),
            ("Cabinet",    "cabinet.png",    "This is a cabinet. My cookies are in the cabinet."),
            ("Bed",        "bed.png",        "This is a bed. My teddy bear is on the bed."),
            ("Couch",      "couch.png",      "This is a couch. My cat is under the couch."),
            ("Table",      "table.png",      "This is a table. The cups are on the table."),
            ("Armchair",   "armchair.png",   "This is an armchair. Grandpa sits on the armchair."),
            ("Caravan",    "caravan.png",    "This is a caravan. It has a bed and a table inside."),
            ("Houseboat",  "houseboat.png",  "This is a houseboat. It is on the water."),
            ("Palace",     "palace.png",     "This is a palace. It is big and beautiful."),
            ("Tree house", "treehouse.png",  "This is a tree house. It is up in the tree."),
            ("Tent",       "tent.png",       "This is a tent. I sleep in the tent."),
        ],
        "expressions": [
            "The doll is in the cabinet.",
            "The doll is on the cabinet.",
            "The doll is under the cabinet.",
            "Where's the cat?",
            "Look on the couch.",
            "Look under the table.",
            "It's in the cabinet.",
            "Tidy up!",
            "Put the kite in the cabinet.",
        ],
    },
    "unit6": {
        "words": [
            ("Cat",    "cat.png",    "This is a cat."),
            ("Horse",  "horse.png",  "This is a horse."),
            ("Cow",    "cow.png",    "This is a cow."),
            ("Dog",    "dog.png",    "This is a dog."),
            ("Rabbit", "rabbit.png", "This is a rabbit."),
            ("Sheep",  "sheep.png",  "This is a sheep."),
        ],
        "expressions": [
            "My favorite color is orange.",
            "I like your colors.",
            "Sniff like a rabbit.",
            "Eat like a rabbit.",
            "Hop, rabbit, hop!",
            "Run, dog, run!",
        ],
    },
    "unit7": {
        "words": [
            ("Carrots",    "carrots.png",    "I like carrots."),
            ("Sausages",   "sausages.png",   "I like sausages."),
            ("Apples",     "apples.png",     "I like apples."),
            ("Cakes",      "cakes.png",      "I like cakes."),
            ("Ice cream",  "ice-cream.png",  "I like ice cream."),
            ("Chips",      "chips.png",      "I like chips."),
        ],
        "expressions": [
            "I like carrots.",
            "I don't like carrots.",
            "What's that smell?",
            "You're hungry.",
            "Go into the kitchen.",
            "Take one.",
            "Eat the chip.",
            "Yummy!",
        ],
    },
    "unit8": {
        "words": [
            ("Boat",    "boat.png",    "This is a boat."),
            ("Train",   "train.png",   "This is a train."),
            ("Car",     "car.png",     "This is a car."),
            ("Scooter", "scooter.png", "This is a scooter."),
            ("Bus",     "bus.png",     "This is a bus."),
            ("Bike",    "bike.png",    "This is a bike."),
        ],
        "expressions": [
            "I'm riding a bike.",
            "You're riding a bike.",
            "Oh what fun!",
            "Thank you.",
            "We're having fun!",
        ],
    },
    "unit9": {
        "words": [
            ("Hat",   "hat.png",   "This is a hat."),
            ("Belt",  "belt.png",  "This is a belt."),
            ("Boots", "boots.png", "These are boots."),
            ("Shirt", "shirt.png", "This is a shirt."),
            ("Badge", "badge.png", "This is a badge."),
            ("Shoes", "shoes.png", "These are shoes."),
        ],
        "expressions": [
            "Let's have biscuits.",
            "Let's have crisps.",
            "Let's have salad.",
            "Let's have sweets.",
            "Nice work!",
            "Walk home.",
            "Open the door.",
            "Surprise!",
            "Put on your party hat.",
            "Dance with your friends.",
        ],
    },
}

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def expression_slug(text: str) -> str:
    """Mesmo algoritmo do JS: lowercase, remove apóstrofos, troca não-alfanuméricos por hífen."""
    s = text.lower()
    s = s.replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "expression"

def img_slug(img_filename: str) -> str:
    """Remove extensão da imagem para usar como slug do MP3."""
    return Path(img_filename).stem

def synthesize(client, text: str, speed: float) -> bytes:
    """Chama a API e retorna bytes do MP3."""
    from google.cloud import texttospeech

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=LANGUAGE_CODE,
        name=VOICE_NAME,
    )
    # Chirp3-HD NÃO suporta pitch nem effects_profile_id
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    return response.audio_content

def save_mp3(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    kb = len(data) / 1024
    print(f"  ✓  {path}  ({kb:.0f} KB)")

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    try:
        from google.cloud import texttospeech
    except ImportError:
        print("❌  Biblioteca não encontrada. Execute:")
        print("    pip install google-cloud-texttospeech")
        return

    # Inicializa cliente
    if GOOGLE_API_KEY:
        client = texttospeech.TextToSpeechClient(
            client_options={"api_key": GOOGLE_API_KEY}
        )
    else:
        # Usa GOOGLE_APPLICATION_CREDENTIALS automaticamente
        client = texttospeech.TextToSpeechClient()

    total = sum(
        len(u["words"]) * 2 + len(u["expressions"])
        for u in UNITS.values()
    )
    print(f"\n🎙  Gerando {total} arquivos de áudio com {VOICE_NAME}...\n")

    gerados = 0
    erros   = 0

    for unit_key, unit_data in UNITS.items():
        print(f"\n{'─'*50}")
        print(f"📂  {unit_key.upper()}")
        print(f"{'─'*50}")
        base = Path("audio") / unit_key

        # ── Palavras ──────────────────────────────────────
        for (word, img, phrase) in unit_data["words"]:
            slug = img_slug(img)

            # 1. Palavra isolada
            word_path = base / f"{slug}.mp3"
            if word_path.exists():
                print(f"  ⏭  {word_path}  (já existe, pulando)")
            else:
                try:
                    data = synthesize(client, word, WORD_SPEED)
                    save_mp3(word_path, data)
                    gerados += 1
                    time.sleep(0.15)  # evita rate limit
                except Exception as e:
                    print(f"  ✗  {word_path}  ERRO: {e}")
                    erros += 1
                    time.sleep(RETRY_WAIT)

            # 2. Frase
            phrase_path = base / f"{slug}_phrase.mp3"
            if phrase_path.exists():
                print(f"  ⏭  {phrase_path}  (já existe, pulando)")
            else:
                try:
                    data = synthesize(client, phrase, PHRASE_SPEED)
                    save_mp3(phrase_path, data)
                    gerados += 1
                    time.sleep(0.15)
                except Exception as e:
                    print(f"  ✗  {phrase_path}  ERRO: {e}")
                    erros += 1
                    time.sleep(RETRY_WAIT)

        # ── Expressões ────────────────────────────────────
        for expr in unit_data["expressions"]:
            slug = expression_slug(expr)
            expr_path = base / f"expr_{slug}.mp3"
            if expr_path.exists():
                print(f"  ⏭  {expr_path}  (já existe, pulando)")
            else:
                try:
                    data = synthesize(client, expr, PHRASE_SPEED)
                    save_mp3(expr_path, data)
                    gerados += 1
                    time.sleep(0.15)
                except Exception as e:
                    print(f"  ✗  {expr_path}  ERRO: {e}")
                    erros += 1
                    time.sleep(RETRY_WAIT)

    print(f"\n{'═'*50}")
    print(f"✅  Concluído! {gerados} gerados, {erros} erros.")
    print(f"{'═'*50}\n")
    if erros:
        print("💡  Dica: Execute novamente — arquivos existentes são pulados automaticamente.")

if __name__ == "__main__":
    main()
