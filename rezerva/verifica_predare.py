#!/usr/bin/env python3
"""Verifică predarea (o rulează orchestratorul) și scrie chitanța.

    python3 verifica_predare.py brief/brief.md livrabile/

Ce verifică, și ce niciun agent nu poate vedea singur:
  1. fișierele cerute în brief există în folderul de livrabile;
  2. linkul din postare și din carusel e exact linkul din brief (nu unul inventat);
  3. reia verificările de formă ale fiecărui rol, ca să nu se bazeze pe raportul lor.

Scrie lângă livrabile fișierul verificare.json (chitanța). Orchestratorul citește
chitanța, nu raportul agentului.
Ieșire: 0 = predarea e bună, 1 = abateri, 2 = eroare de chemare.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import verifica_carusel
import verifica_postare

FISIERE = ["postare.md", "carusel.md"]
LINK_BRIEF = re.compile(r"\*\*Link de înscriere:\*\*\s*(\S+)")
LINK = re.compile(r"(?:https?://)?[\w.-]+\.[a-z]{2,}/[\w./-]*", re.I)


def normal(link):
    """Compară linkuri fără schemă și fără punctuația de la final."""
    return re.sub(r"^https?://", "", link).rstrip("/.,;:)")


def verifica(brief, folder):
    m = LINK_BRIEF.search(Path(brief).read_text(encoding="utf-8"))
    if not m:
        return ["brieful nu are rândul „**Link de înscriere:** …”"]
    link_corect = normal(m.group(1))
    abateri = []
    for nume in FISIERE:
        cale = Path(folder) / nume
        if not cale.is_file():
            abateri.append(f"{nume}: lipsește din {folder}")
            continue
        linkuri = [normal(l) for l in LINK.findall(cale.read_text(encoding="utf-8"))]
        if not linkuri:
            abateri.append(f"{nume}: nu are linkul de înscriere")
        for l in linkuri:
            if l != link_corect:
                abateri.append(f"{nume}: linkul „{l}” nu e cel din brief („{link_corect}”)")
        rol = verifica_postare if nume == "postare.md" else verifica_carusel
        abateri += [f"{nume}: {a}" for a in rol.verifica(cale)]
    return abateri


if __name__ == "__main__":
    if len(sys.argv) != 3 or not Path(sys.argv[1]).is_file() or not Path(sys.argv[2]).is_dir():
        print("Folosire: python3 verifica_predare.py <brief.md> <folder livrabile>")
        sys.exit(2)
    brief, folder = sys.argv[1], sys.argv[2]
    abateri = verifica(brief, folder)
    chitanta = {
        "data": datetime.now().isoformat(timespec="seconds"),
        "brief": brief,
        "livrabile": folder,
        "rezultat": 0 if not abateri else 1,
        "abateri": abateri,
    }
    Path(folder, "verificare.json").write_text(
        json.dumps(chitanta, ensure_ascii=False, indent=2), encoding="utf-8")
    for a in abateri:
        print("ABATERE:", a)
    print("REZULTAT:", "predarea e bună" if not abateri else f"pică (abateri: {len(abateri)})")
    print("Chitanța:", Path(folder, "verificare.json"))
    sys.exit(1 if abateri else 0)
