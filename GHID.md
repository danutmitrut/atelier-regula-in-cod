# Agentul zice că e gata. Cum verifici că chiar e?

*Construiești pas cu pas verificarea care prinde linkul greșit, textul prea lung sau fișierul lipsă, și o legi de flotă, ca nicio greșeală de felul ăsta să nu mai treacă mai departe.*

**Data:** luni, 16 noiembrie 2026, 18:30-21:30
**Acces:** T2, T3
**Cum folosești ghidul:** îl ții deschis tot atelierul. Explicațiile stau lângă pașii la care se aplică. Prompturile din casete se copiază întocmai.

---

## Ce ai nevoie

Doar Claude Code, deschis în VS Code. Restul îl instalăm împreună în primele minute.

## Ce iei cu tine la final

1. Un verificator scris de tine, pe care l-ai văzut picând pe exemplul rău și trecând pe exemplul bun.
2. O regulă scoasă din promptul unui agent și înlocuită cu trimiterea la verificator.
3. Un orchestrator care citește chitanța scrisă de verificator, nu raportul agentului. L-ai văzut oprind o postare greșită pe care înainte o lăsa să treacă.

---

## Partea 0. Pregătirea (aproximativ 10 minute)

Deschizi VS Code într-un folder oarecare (de exemplu `Documente`), pornești Claude Code și dai promptul:

```
Clonează https://github.com/danutmitrut/atelier-regula-in-cod.git aici.
Apoi rulează git --version și python3 --version și spune-mi ce lipsește.
Nu instala nimic fără să mă întrebi.
```

Dacă lipsește ceva:
- **git** lipsește: deschizi pagina repo-ului în browser, apeși **Code**, apoi **Download ZIP**, și dezarhivezi folderul.
- **Python** lipsește pe Mac: îi ceri lui Claude „Rulează `xcode-select --install`”. Se deschide o fereastră de instalare, iar Python 3 vine odată cu ea.
- **Python** lipsește pe Windows: instalezi Python 3 de pe python.org și bifezi **Add python.exe to PATH** la instalare. Pe Windows, comanda poate fi `python` în loc de `python3`. Claude se descurcă cu oricare.

La final deschizi folderul `atelier-regula-in-cod` în VS Code (**File**, apoi **Open Folder**) și pornești o sesiune Claude Code nouă. Asta e **fereastra principală**. Aici lucrezi tot atelierul, în afară de momentele în care ghidul îți cere altă fereastră.

### Ce e în folder

```
atelier-regula-in-cod/
├── brief/brief.md         brieful omului: atelier online, data, prețul, linkul de înscriere
├── copywriter/            agentul care scrie postarea de LinkedIn
│   ├── CLAUDE.md          instrucțiunile lui, cu regulile scrise în prompt
│   └── memorie/           corecturile primite de la om
├── designer/              agentul care face caruselul de 5 slide-uri
├── orchestrator/          cel care dă sarcinile și primește rapoartele
├── livrabile/             aici predau agenții
├── exemple/bune, rele/    o postare și un carusel care respectă regulile, și aceleași cu greșeli
└── rezerva/               verificatoarele gata făcute, dacă te blochezi
```

E o flotă mică, construită la fel ca șablonul de pe 2 noiembrie: fiecare agent are folderul lui și vede doar fișierele lui, iar orchestratorul ține legătura dintre ei.

---

## Partea 1. De ce (aproximativ 20 de minute)

### Ce s-a întâmplat în flota de producție

Flota de producție a lui Dănuț a rulat aceeași campanie de test de mai multe ori, între 4 și 9 noiembrie 2026. În patru rulări la rând, Copywriterul a predat pagina fără linkul de înscriere: în locul linkului rămânea un marcaj de completat. Promptul cerea text gata de publicat. Nimic nu verifica.

Greșeala a fost prinsă abia la verificarea contractului, după ce trecuse de Copywriter. Repararea a cerut o rulare de corectură: circa 15 minute și peste 1 $ consum, pentru un rând de text.

Concluzia scrisă atunci în analiza flotei: ce nu poate inventa niciun agent (linkuri, adrese, texte legale, reguli comerciale) se declară la început și se verifică cu un script, nu se lasă în seama promptului.

### Trei idei pe care se sprijină tot atelierul

**1. O regulă scrisă în prompt e o rugăminte. O regulă verificată în cod e o garanție.**
Modelul citește promptul și, de cele mai multe ori, îl respectă. „De cele mai multe ori” e problema: când are mult context, multe reguli sau o sarcină lungă, unele reguli se pierd. Un script nu obosește și nu interpretează. Primește un fișier și spune da sau nu. (Fraza vine din skill-ul `deterministic-vs-llm`, pasul 5.)

**2. Raportul agentului nu e un fapt. Faptul e chitanța scrisă de script.**
Când agentul scrie „am verificat, totul e în regulă”, descrie ce crede că a făcut. Poate fi adevărat, poate fi înmuiat, poate fi greșit fără rea intenție: agentul nu vede ce s-a schimbat în afara turei lui. Un fișier scris de script, cu data și rezultatul, e o dovadă pe care o poate citi oricine. (Din `docs/PRINCIPII.md`, în șablonul de flotă de pe 2 noiembrie.)

**3. Un verificator pe care nu l-ai văzut picând nu e verificat.**
Un script care spune mereu „trece” arată exact ca un script bun. Singurul fel în care afli că prinde greșeala e să i-o dai intenționat și să-l vezi oprind-o. De aceea, în atelier, exemplul rău se scrie înaintea scriptului.

### Cele trei trepte ale garanției

Același script poate fi rulat de trei „persoane” diferite, iar asta schimbă cât de mult te poți baza pe el.

| Treapta | Cine rulează scriptul | Ce obții |
|---|---|---|
| 1 | agentul, înainte să predea | o rugăminte cu unealtă: agentul poate uita să-l ruleze |
| 2 | orchestratorul, la predare, citind chitanța | un fapt: predarea nu trece fără chitanță bună |
| 3 | un hook, automat | o barieră: nimeni nu poate ocoli scriptul |

Azi construiești treptele 1 și 2. Treapta 3 o arată Dănuț, demonstrativ, pentru T3.

---

## Partea 2. Când merită un script (aproximativ 15 minute)

Nu orice regulă devine cod. Cele cinci semnale de mai jos spun când merită.

1. **Aceeași corectură apare de două ori în memoria unui agent.** Prima oară e o scăpare. A doua oară e un tipar, iar promptul n-a fost de ajuns.
2. **Agentul raportează „gata”, dar fișierul lipsește**, e în alt loc sau are alt format.
3. **Regula se verifică fără să judeci textul.** Număr de caractere, de slide-uri sau de cuvinte, caractere interzise, nume de fișier, dată, link.
4. **Informația trece de la un agent la altul.** Fiecare agent vede doar fișierul lui. Potrivirea dintre fișiere o vede doar orchestratorul.
5. **Rezultatul pleacă în public** sau nu se mai poate retrage.

**Contra-semnalul.** Tonul, „e convingător?”, „sună a mine?” rămân la model, adică la evaluatorul cu criterii. Un script nu poate judeca limbajul. Cine încearcă să scrie reguli fixe pentru ton ajunge la scripturi care resping texte bune și lasă să treacă texte proaste.

Deschide `brief/brief.md`. Brieful împarte deja regulile în două: **reguli de formă (verificabile)** și **reguli de judecată (rămân la evaluator)**. Împărțirea asta e, pe scurt, tot atelierul.

Cifrele din brief (1.300 de caractere, 30 de cuvinte pe slide) sunt alese pentru exemplu. Nu vin dintr-o sursă despre LinkedIn.

---

## Partea 3. Demonstrația (Dănuț, aproximativ 10 minute)

Dănuț rulează verificatoarele gata făcute din `rezerva/` pe exemplele cu greșeli și pe cele bune. Poți rula și tu, în fereastra principală:

```
Rulează, pe rând, și arată-mi ieșirea fiecăruia și codul de ieșire:
python3 rezerva/verifica_postare.py exemple/rele/postare.md
python3 rezerva/verifica_carusel.py exemple/rele/carusel.md
python3 rezerva/verifica_predare.py brief/brief.md exemple/rele
python3 rezerva/verifica_predare.py brief/brief.md exemple/bune
```

Ce vezi:
- postarea rea pică pe două abateri: emoji pe rândul 1, em dash pe rândul 3;
- caruselul rău pică pe două abateri: 6 slide-uri în loc de 5, slide-ul 2 cu 34 de cuvinte;
- predarea rea pică pe 6 abateri, printre ele linkul `exemplu.ro/inscriere`, care nu e cel din brief;
- predarea bună trece și scrie chitanța `exemple/bune/verificare.json`. Deschide-o și vezi ce conține o chitanță.

Uită-te la al treilea rezultat. Linkul greșit nu l-ar fi prins nici verificatorul postării, nici al caruselului. Fiecare se uită la un singur fișier. Doar verificatorul predării pune brieful lângă livrabile. Acesta e semnalul 4 în practică.

**Ce înseamnă codul de ieșire.** Orice program lasă la final un număr pe care îl pot citi alte programe. Convenția e 0 pentru „totul e bine” și altceva pentru „ceva nu e bine”. Orchestratorul și hook-urile citesc numărul ăsta, nu textul afișat. De aceea un verificator trebuie să iasă cu 1 la greșeală, nu doar să scrie „atenție”.

---

## Partea 4. Cei cinci pași, pe Copywriter (aproximativ 60 de minute)

Lucrezi în fereastra principală.

### Pasul 1. Inventarul regulilor

```
Citește copywriter/CLAUDE.md și copywriter/memorie/corecturi.md.
Scoate într-un tabel fiecare regulă formulată cu „trebuie”, „mereu”, „niciodată”,
„maxim”, „obligatoriu”. Pentru fiecare regulă scrie: unde apare, dacă se poate
verifica printr-o regulă fixă fără să judeci textul (da / nu / parțial) și de câte
ori apare ca o corectură în memorie. Nu modifica nimic.
```

**Criteriu de succes:** tabelul are regulile din `CLAUDE.md`. Regula linkului are „da” și două corecturi (20 octombrie și 3 noiembrie). Regulile despre primul rând și ton au „nu” sau „parțial”. În fișiere nu s-a schimbat nimic.

### Pasul 2. Alegi o singură regulă

Criteriile, în ordine:
1. are „da” la verificare;
2. a fost corectată cel mai des;
3. la egalitate, câștigă regula care pleacă în public.

Pe tabelul tău câștigă regula linkului: „linkul de înscriere trebuie să fie mereu exact linkul din brief”. E corectată de două ori (semnalul 1), se verifică fără judecată (semnalul 3), leagă două fișiere (semnalul 4) și pleacă în public (semnalul 5).

Una singură. Cine alege trei reguli odată nu le vede pe niciuna picând cum trebuie.

### Pasul 3. Exemplele înaintea scriptului

```
Pentru regula „linkul de înscriere trebuie să fie mereu exact linkul din brief”,
creează folderul copywriter/teste/ cu două fișiere: bun.md, o postare care
folosește exact linkul din brief/brief.md, și rau.md, aceeași postare cu linkul
greșit din corectura din 3 noiembrie. Nu scrie încă niciun script.
```

**De ce întâi exemplele:** exemplul rău e definiția greșelii. Dacă scrii întâi scriptul, îl scrii după ce crezi tu că e greșeala, iar exemplul îl potrivești apoi pe script. Invers, scriptul trebuie să se potrivească pe greșeala reală, cea din memorie.

**Criteriu de succes:** `rau.md` diferă de `bun.md` doar prin link.

### Pasul 4. Scriptul, văzut întâi picând

```
Scrie copywriter/scripts/verifica_link.py. Primește calea briefului și calea
postării. Iese cu 0 dacă linkul din postare e exact linkul de înscriere din
brief, cu 1 dacă nu. La 1 spune pe ce rând e problema și de ce. Doar Python
standard, fără biblioteci instalate. Rulează-l întâi pe copywriter/teste/rau.md
și arată-mi că pică, apoi pe copywriter/teste/bun.md și arată-mi că trece.
Dacă rau.md trece, scriptul e greșit, nu exemplul.
```

**Criteriu de succes:** ai văzut două rulări: `rau.md` iese cu 1 și spune rândul, `bun.md` iese cu 0.

**Dacă te blochezi:** îi ceri lui Claude „Copiază rezerva/verifica_predare.py, verifica_postare.py și verifica_carusel.py în copywriter/scripts/ și folosește verifica_predare.py ca verificator de link.” Apoi treci la pasul 5.

### Pasul 5. Regula iese din prompt (treapta 1)

```
În copywriter/CLAUDE.md, înlocuiește regula despre linkul de înscriere cu:
„Înainte să predai, rulezi python3 scripts/verifica_link.py ../brief/brief.md
../livrabile/postare.md. Dacă iese cu 1, repari și rulezi din nou. Predai doar
cu 0 și pui în raport ieșirea scriptului copiată, nu povestită.”
Arată-mi diferența înainte să salvezi.
```

**De ce se scoate regula din prompt.** Dacă regula rămâne și în prompt, și în script, ai două surse pentru același lucru. Când schimbi una, cealaltă rămâne pe varianta veche și agentul primește instrucțiuni contradictorii. Promptul păstrează doar trimiterea la script. Așa promptul rămâne cu meseria, iar regula stă într-un singur loc.

**De ce „copiată, nu povestită”.** Ieșirea copiată poate fi comparată cu ce dă scriptul la o nouă rulare. O frază ca „am verificat, trece” nu poate fi comparată cu nimic.

**Criteriu de succes:** ai văzut diferența înainte de salvare. Regula veche despre link nu mai apare în `copywriter/CLAUDE.md`.

---

## Partea 5. Sabotajul controlat și treapta 2 (aproximativ 35 de minute)

Acum verifici dacă flota oprește o greșeală care a ajuns totuși la predare.

**De ce nu îi cerem Copywriterului să greșească.** La testul din 15 noiembrie, Copywriterul căruia i s-a cerut „pune alt link decât cel din brief” a refuzat. A citit corecturile din memorie și verificatorul și a cerut confirmare. Bine pentru el, dar greșelile reale nu sunt cerute: în flota de producție, marcajul de completat a apărut patru rulări la rând fără ca cineva să-l ceară. De aceea simulăm greșeala direct: punem în `livrabile/` o postare greșită, ca și cum agentul ar fi scris-o, și vedem ce face orchestratorul.

### Sabotajul 1: orchestratorul fără chitanță

1. În fereastra principală:

```
Copiază exemple/rele/postare.md în livrabile/postare.md.
```

2. Deschizi o fereastră nouă de VS Code (**File**, apoi **New Window**), deschizi în ea folderul `orchestrator` și pornești Claude Code. Asta e **fereastra orchestratorului**. Când Claude cere voie să citească fișiere din folderul de deasupra, aprobi.

3. În fereastra orchestratorului:

```
Copywriterul a raportat: „Postarea e gata, în livrabile/postare.md.” Continuă lucrarea.
```

**Ce vezi:** orchestratorul îi dă Designerului sarcina, cu postarea greșită: link inventat, emoji, em dash. Raportul a spus „gata”, iar orchestratorul a crezut raportul.

### Pasul 5b. Chitanța (treapta 2)

În fereastra principală:

```
Modifică copywriter/scripts/verifica_link.py să scrie, lângă postare, un fișier
verificare.json cu data, fișierul, regula, rezultatul (0 sau 1) și abaterile.
Apoi adaugă în orchestrator/CLAUDE.md, la reguli: „La predarea postării rulezi
python3 ../copywriter/scripts/verifica_link.py ../brief/brief.md
../livrabile/postare.md, apoi citești ../livrabile/verificare.json, nu raportul
agentului. Fără verificare.json cu rezultat 0, pasul nu e predat: îi trimiți
Copywriterului abaterile și nu dai sarcina Designerului.”
Arată-mi diferența înainte să salvezi.
```

### Sabotajul 2: orchestratorul cu chitanță

În fereastra orchestratorului pornești o sesiune nouă (ca să citească noul `CLAUDE.md`) și dai același prompt:

```
Copywriterul a raportat: „Postarea e gata, în livrabile/postare.md.” Continuă lucrarea.
```

**Ce vezi:** orchestratorul rulează verificatorul, citește `verificare.json` cu `"rezultat": 1` și linkul greșit pe rândul lui, și nu dă sarcina Designerului. Îi trimite Copywriterului abaterea. Raportul spunea „gata”, chitanța spunea altceva, iar orchestratorul a mers pe chitanță.

**Criteriu de succes:** ai văzut aceeași postare greșită trecând la sabotajul 1 și oprită la sabotajul 2. Singura diferență dintre cele două e pasul 5b.

### Treapta 3 (demonstrație Dănuț, pentru T3)

Același verificator, legat de un hook: scriptul rulează automat la fiecare scriere în `livrabile/`, fără să depindă de cineva care să-și amintească să-l ruleze.

---

## Închiderea (aproximativ 10 minute)

### Tema, până pe 24 noiembrie

Încă o regulă mutată în cod, cu aceiași cinci pași. Două variante:
- pe mini-flotă: o regulă a Designerului (exact 5 slide-uri, maxim 30 de cuvinte pe slide), cu corectura din `designer/memorie/corecturi.md` ca exemplu rău;
- pe flota ta de pe 2 noiembrie, dacă o ai: o regulă aleasă cu pasul 2, din `CLAUDE.md`-ul unui rol.

Obligatoriu: exemplul rău văzut picând. Aduci la atelierul următor ieșirea celor două rulări (rău și bun), copiată.

---

## Ce să nu faci

- **Mai multe reguli într-un singur script, de la început.** Când pică, nu știi care regulă a picat. Una pe script, până ai văzut-o mergând.
- **Script fără exemplu rău.** Un script care trece mereu arată exact ca unul bun.
- **Regula lăsată și în prompt, și în script.** Două surse ajung, la prima schimbare, să spună lucruri diferite.
- **Script pentru ton sau stil.** Ce cere judecată rămâne la evaluatorul cu criterii.
- **Agentul își scrie singur chitanța.** Chitanța o scrie scriptul. Altfel ai tot un raport, doar cu alt nume.
- **Biblioteci instalate pentru un verificator simplu.** Python standard ajunge pentru numărat, căutat și comparat. Fiecare bibliotecă în plus e încă o piesă care se poate strica pe alt calculator.

---

## Surse

- Povestea de deschidere: analiza rulărilor flotei de producție a lui Dănuț, 4-9 noiembrie 2026.
- „O regulă scrisă în prompt e o rugăminte...”: skill-ul `deterministic-vs-llm`, pasul 5 (atelierul din 27 octombrie).
- Raport și chitanță, verificarea după cine vede: `sablon-flota-agenti/docs/PRINCIPII.md` (atelierul din 2 noiembrie).
- Mini-flota și sabotajul: testate cap-coadă pe 15 noiembrie 2026 (verificatoarele, pașii 3-5, orchestratorul înainte și după pasul 5b, cu Claude Sonnet).
