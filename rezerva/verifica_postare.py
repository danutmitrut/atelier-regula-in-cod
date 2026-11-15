#!/usr/bin/env python3
"""Verifică forma postării (o rulează Copywriterul înainte să predea).

    python3 verifica_postare.py livrabile/postare.md

Ieșire: 0 = regulile de formă sunt respectate, 1 = cel puțin o abatere, 2 = eroare de chemare.
Nu judecă tonul sau calitatea. Doar fapte care se pot număra.
"""
import re
import sys
from pathlib import Path

MAX_CARACTERE = 1300
LINIUTE = re.compile("[—–]")  # em dash și en dash
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⬀-⯿️]")


def verifica(cale):
    text = Path(cale).read_text(encoding="utf-8")
    abateri = []
    if len(text.strip()) > MAX_CARACTERE:
        abateri.append(f"are {len(text.strip())} de caractere, maximul e {MAX_CARACTERE}")
    for nr, rand in enumerate(text.splitlines(), 1):
        if LINIUTE.search(rand):
            abateri.append(f"rândul {nr}: are em dash sau en dash")
        if EMOJI.search(rand):
            abateri.append(f"rândul {nr}: are emoji")
    return abateri


if __name__ == "__main__":
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_file():
        print("Folosire: python3 verifica_postare.py <postare.md>")
        sys.exit(2)
    abateri = verifica(sys.argv[1])
    for a in abateri:
        print("ABATERE:", a)
    print("REZULTAT:", "trece" if not abateri else f"pică (abateri: {len(abateri)})")
    sys.exit(1 if abateri else 0)
