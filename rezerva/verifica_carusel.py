#!/usr/bin/env python3
"""Verifică forma caruselului (o rulează Designerul înainte să predea).

    python3 verifica_carusel.py livrabile/carusel.md

Caruselul are slide-urile ca titluri „## Slide N”.
Ieșire: 0 = trece, 1 = cel puțin o abatere, 2 = eroare de chemare.
"""
import re
import sys
from pathlib import Path

NR_SLIDEURI = 5
MAX_CUVINTE = 30


def verifica(cale):
    text = Path(cale).read_text(encoding="utf-8")
    bucati = re.split(r"^## Slide \d+\s*$", text, flags=re.M)[1:]
    abateri = []
    if len(bucati) != NR_SLIDEURI:
        abateri.append(f"are {len(bucati)} slide-uri, trebuie exact {NR_SLIDEURI}")
    for nr, bucata in enumerate(bucati, 1):
        cuvinte = len(bucata.split())
        if cuvinte > MAX_CUVINTE:
            abateri.append(f"slide-ul {nr} are {cuvinte} de cuvinte, maximul e {MAX_CUVINTE}")
    return abateri


if __name__ == "__main__":
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_file():
        print("Folosire: python3 verifica_carusel.py <carusel.md>")
        sys.exit(2)
    abateri = verifica(sys.argv[1])
    for a in abateri:
        print("ABATERE:", a)
    print("REZULTAT:", "trece" if not abateri else f"pică (abateri: {len(abateri)})")
    sys.exit(1 if abateri else 0)
