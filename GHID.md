# Agentul zice că e gata. Cum verifici că chiar e?

*Construiești primul tău verificator: un mic program care prinde o greșeală a agentului înainte să plece mai departe.*

Nu scrii cod. Îi spui lui Claude, în cuvinte obișnuite, ce să verifice, iar el construiește programul. Tu îl testezi și îl legi de agent.

Forma avansată, cu orchestratorul și chitanța, e în `GHID-AVANSAT.md`.

---

## Ce ai nevoie

Claude Code, deschis în VS Code. Atât.

## Cu ce pleci

- cele două liste: ce lași judecății agentului și ce scrii ca program;
- harta celor opt mecanisme care țin munca agentului departe de interpretare;
- un verificator construit de tine, pe care l-ai văzut prinzând o greșeală;
- un agent care își rulează singur verificatorul înainte să predea;
- un al doilea verificator, făcut fără ajutor, după același tipar.

---

## Ideea, pe scurt

Un agent primește reguli scrise în instrucțiunile lui: „linkul trebuie să fie cel din brief”, „fără emoji”, „maxim 1.300 de caractere”. De cele mai multe ori le respectă. Uneori nu, și raportează totuși „gata”.

Exemplu real: în flota de producție a lui Dănuț, Copywriterul a predat de patru ori la rând o pagină fără linkul de înscriere. Regula era scrisă clar în instrucțiunile lui. Nimic nu verifica.

**O regulă scrisă în instrucțiuni e o rugăminte. O regulă verificată de un program e o garanție.** Programul nu obosește și nu interpretează: citește fișierul și spune „trece” sau „pică”.

---

## Ce lași agentului și ce scrii ca program

Un agent e cel mai bun când instrucțiunile lui conțin doar meseria: ce cere judecată. Tot ce se poate număra, căuta sau compara iese din instrucțiuni și trece într-un program. Așa agentul nu-și mai împarte atenția între treizeci de reguli de formă și lucrul pentru care l-ai construit.

**Testul rapid:** dă sarcina la doi oameni atenți. Dacă ar ajunge la același răspuns fără să discute, e de program. Dacă ar avea de discutat, e de agent.

### Lași judecății agentului

- dacă textul e convingător, cald, clar, dacă sună a tine;
- alegerea cuvintelor, a ideilor, a exemplelor și a ordinii lor;
- titlurile, deschiderile, primul rând care oprește scroll-ul;
- rezumatul, sinteza, interpretarea unui document sau a unei discuții;
- adaptarea la cine citește: client, începător, specialist;
- situațiile noi, pe care nicio regulă nu le-a prevăzut;
- alegerea între variante bune, când criteriile trag în direcții diferite (cu aprobarea ta, când miza e mare).

### Scrii ca program

- **numere și limite:** caractere, cuvinte, slide-uri, dimensiuni de imagine;
- **date care vin de la tine și se copiază exact:** linkuri, prețuri, date, ore, adrese, nume;
- **ce e interzis și se poate căuta:** emoji, em dash, cuvinte pe care nu le folosești;
- **fișierele:** dacă livrabilul există, are numele corect și stă unde trebuie;
- **potrivirea între fișiere:** același link și același preț în postare și în carusel;
- **calcule:** totaluri, procente, conversii, zile din calendar;
- **forma:** câmpurile obligatorii sunt completate, structura șablonului e respectată;
- **ordinea:** ce pas urmează și cine are voie să treacă mai departe;
- **ce se face identic de fiecare dată:** redenumiri, mutări, așezarea în pagină.

Ce e în a doua listă se poate verifica sau face de un program. Mai jos vezi cele opt feluri în care o faci.

---

## Ce poți construi ca munca agentului să nu depindă de interpretare

Verificatorul e un singur mecanism dintre mai multe. Toate pornesc de la aceeași întrebare: **ce trebuie să se întâmple la fel, de fiecare dată?** Ce răspunde la întrebarea asta nu se lasă în instrucțiuni. Îl face un program sau îl impune un program.

Mai jos sunt opt mecanisme, de la cel mai simplu la cel mai complex. Fiecare are problema pe care o rezolvă, ce face și un exemplu pe flota din folder. În folder există deja verificatorul (îl construiești azi) și memoria cu corecturi. Celelalte exemple arată cum ar arăta mecanismul pe aceeași flotă.

### 1. Verificatorul

**Problema:** agentul spune „gata”, dar livrabilul încalcă o regulă.
**Ce face:** un mic program citește livrabilul și spune „trece” sau „pică”, cu locul greșelii.
**Exemplu:** programul compară linkul din postare cu linkul din brief.

Pe acesta îl construiești azi.

### 2. Poarta de la început

**Problema:** agentul inventează sau lasă gol ce trebuia să vină de la tine (un link, un preț, o adresă).
**Ce face:** înainte să pornească lucrarea, un program verifică dacă toate datele de la om sunt completate. Dacă lipsește una, lucrarea nu pornește și îți spune ce lipsește.
**Exemplu:** fără linkul de înscriere completat în brief, Copywriterul nu primește sarcina.

Verificatorul prinde greșeala după ce s-a produs. Poarta o face imposibilă.

### 3. Pasul făcut de program în locul agentului

**Problema:** agentul face aproximativ ce se poate calcula exact (numără greșit, așază greșit, denumește greșit fișierele).
**Ce face:** împarți lucrarea: agentul face doar ce cere judecată (textul), programul face restul.
**Exemplu:** agentul scrie textul slide-urilor, iar un program îl pune în pagină, la dimensiunile corecte.

### 4. Forma fixă

**Problema:** fiecare predare arată altfel, așa că nimeni (om sau program) nu știe unde să caute.
**Ce face:** agentul completează un șablon cu câmpuri obligatorii, în loc să scrie liber.
**Exemplu:** caruselul are mereu titlurile „Slide 1”, „Slide 2” și așa mai departe, ca un program să poată număra slide-urile.

### 5. Paznicul automat

**Problema:** agentul poate uita să ruleze verificatorul sau poate face ceva ce nu are voie.
**Ce face:** Claude Code poate rula automat un program înainte sau după o acțiune a agentului (de exemplu, de fiecare dată când scrie un fișier). Programul poate opri acțiunea. Se numește *hook*.
**Exemplu:** de fiecare dată când Copywriterul salvează postarea, verificatorul rulează singur, fără să depindă de agent.

### 6. Limitele

**Problema:** agentul atinge ce nu trebuie: scrie în alt folder, folosește internetul când n-are nevoie, citește fișiere care nu-l privesc.
**Ce face:** din setări, îi spui ce poate citi, ce poate scrie și ce unelte poate folosi. Ce nu e permis nu se poate face.
**Exemplu:** Copywriterul poate scrie doar în `livrabile/`, nu și în brief.

### 7. Ordinea stabilită de program

**Problema:** coordonatorul sare un pas sau pornește pasul următor înainte ca primul să fie bun.
**Ce face:** un program decide ce pas urmează, pornește agentul și trece mai departe doar după ce verificatorul spune „trece”.
**Exemplu:** Designerul primește postarea doar după ce verificatorul Copywriterului a spus „trece”.

### 8. Memoria pe care agentul nu și-o scrie singur

**Problema:** agentul își notează reguli pe care nu i le-a dat nimeni sau uită corecturile tale.
**Ce face:** corecturile tale se notează exact cum le-ai spus, iar agentul le citește la fiecare pornire. O corectură devine regulă permanentă doar cu aprobarea ta.
**Exemplu:** fișierul `copywriter/memorie/corecturi.md` din folder.

---

## Primul mecanism: verificatorul

### Ce reguli merită un verificator

Te întrebi un singur lucru: **pot verifica regula fără să judec textul?**

| Regula | Se poate verifica fără judecată? |
|---|---|
| linkul e cel din brief | da: compari două linkuri |
| fără emoji | da: cauți emoji |
| maxim 1.300 de caractere | da: numeri |
| exact 5 slide-uri | da: numeri |
| primul rând oprește scroll-ul | nu: e judecată |
| tonul e cald | nu: e judecată |

Ce are „da” poate deveni verificator. Ce are „nu” rămâne la agent și la ochiul tău.

---

## Pasul 0. Descarci materialul

Deschizi VS Code într-un folder oarecare (de exemplu `Documente`), pornești Claude Code și scrii:

```
Clonează https://github.com/danutmitrut/atelier-regula-in-cod.git aici.
Apoi verifică dacă am Python 3 instalat. Nu instala nimic fără să mă întrebi.
```

Dacă lipsește ceva:
- **git** lipsește: deschizi pagina repo-ului în browser, apeși **Code**, apoi **Download ZIP**, și dezarhivezi folderul.
- **Python** lipsește pe Mac: îi ceri lui Claude „Rulează `xcode-select --install`” și urmezi fereastra care se deschide.
- **Python** lipsește pe Windows: îl instalezi de pe python.org și bifezi **Add python.exe to PATH**.

Apoi deschizi folderul `atelier-regula-in-cod` în VS Code (**File**, apoi **Open Folder**) și pornești o sesiune nouă de Claude Code. În fereastra asta lucrezi tot timpul.

**Ce e în folder:** un brief (`brief/brief.md`), un agent Copywriter (`copywriter/`) cu instrucțiunile lui și două postări de probă: una bună (`exemple/bune/postare.md`) și una cu greșeli (`exemple/rele/postare.md`).

---

## Pasul 1. Vezi greșeala cu ochii tăi

```
Compară exemple/bune/postare.md cu exemple/rele/postare.md și cu linkul de
înscriere din brief/brief.md. Spune-mi ce e greșit în postarea rea.
Nu modifica nimic.
```

**Ce vezi:** postarea rea are alt link decât cel din brief, plus un emoji și o linie lungă (em dash). Linkul greșit e cea mai gravă: cititorul ajunge pe o pagină care nu există.

Alegem regula linkului pentru primul verificator.

---

## Pasul 2. Îi ceri lui Claude verificatorul

```
Fă-mi un verificator pentru Copywriter: un mic program care ia linkul de
înscriere din brief/brief.md și verifică dacă o postare are exact același link.
Salvează-l în copywriter/scripts/verifica_link.py. Programul primește două
fișiere, în ordinea asta: întâi brieful, apoi postarea. Folosește doar Python
standard, fără nimic de instalat. Dacă linkul e greșit sau lipsește, programul
scrie PICĂ și pe ce rând e problema. Dacă e bun, scrie TRECE.
Nu-l rula încă.
```

Nu trebuie să înțelegi codul. Trebuie doar să știi ce verifică (dacă linkul din postare e cel din brief) și ce primește (brieful și postarea, în ordinea asta). Ordinea contează la pasul 4, când agentul îl va porni singur.

---

## Pasul 3. Îl testezi: întâi pe greșeală

```
Rulează verificatorul întâi pe exemple/rele/postare.md, apoi pe
exemple/bune/postare.md. Arată-mi exact ce scrie la fiecare.
```

**Trebuie să vezi:**
- la postarea rea: **PICĂ**, cu rândul pe care e linkul greșit;
- la postarea bună: **TRECE**.

**De ce întâi pe greșeală:** un verificator care spune mereu „trece” arată exact ca unul bun. Afli că funcționează doar când îl vezi prinzând greșeala.

**Dacă amândouă spun TRECE**, verificatorul e greșit. Îi scrii lui Claude: „Postarea rea trebuie să pice. Repară verificatorul și testează din nou.”

---

## Pasul 4. Îl legi de agent

Acum regula iese din instrucțiunile Copywriterului și în locul ei intră verificatorul.

```
În copywriter/CLAUDE.md, înlocuiește regula despre linkul de înscriere cu:
„Înainte să predai postarea, rulezi python3 scripts/verifica_link.py
../brief/brief.md ../livrabile/postare.md. Dacă scrie PICĂ, repari și rulezi
din nou. Predai doar când scrie TRECE.”
Arată-mi schimbarea înainte să salvezi.
```

**De ce scoatem regula veche:** dacă rămâne și regula, și verificatorul, ai două locuri care spun același lucru. Când schimbi unul și îl uiți pe celălalt, agentul primește instrucțiuni care se bat cap în cap. Regula stă într-un singur loc: în verificator.

---

## Pasul 5. Îl vezi lucrând

```
Lucrează ca Copywriterul: urmează întocmai copywriter/CLAUDE.md și scrie
postarea după brief. Arată-mi ce a scris verificatorul înainte de predare.
```

**Trebuie să vezi:** agentul scrie postarea în `livrabile/postare.md`, rulează verificatorul și predă doar după ce acesta scrie **TRECE**.

**Proba cu greșeală:**

```
Copiază exemple/rele/postare.md peste livrabile/postare.md și rulează
verificatorul Copywriterului pe ea.
```

Verificatorul scrie **PICĂ**. Aceasta e greșeala care ar fi plecat mai departe dacă regula ar fi rămas doar o rugăminte în instrucțiuni.

---

## Pasul 6. Al doilea verificator, singur

Alegi o regulă din tabelul de la început care are „da”: fără emoji, maxim 1.300 de caractere sau exact 5 slide-uri (cea din urmă e pentru `designer/`, pe carusel). Repeți pașii 2-4 cu propriile cuvinte. Tiparul e mereu același:

1. **Ceri** verificatorul în cuvinte obișnuite: ce verifică, unde îl salvezi, ce scrie la PICĂ și la TRECE.
2. **Îl testezi** întâi pe exemplul rău (`exemple/rele/`), apoi pe cel bun (`exemple/bune/`).
3. **Îl legi** de agent și scoți regula veche din `CLAUDE.md`.

---

## Tema, până pe 24 noiembrie

Un verificator pentru unul din agenții tăi. Alegi o regulă pe care agentul a încălcat-o cel puțin o dată și care trece testul „se poate verifica fără judecată”. Aduci ce a scris verificatorul pe exemplul rău și pe cel bun.

---

## Ce să nu faci

- **Un verificator pentru mai multe reguli odată.** Când pică, nu știi ce a picat. Una câte una.
- **Verificator netestat pe greșeală.** Dacă nu l-ai văzut scriind PICĂ, nu știi dacă prinde ceva.
- **Verificator pentru ton sau stil.** Ce cere judecată rămâne la agent și la tine.
- **Regula lăsată și în instrucțiuni.** O ții într-un singur loc.
