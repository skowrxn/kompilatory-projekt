# Ściągawka z Projektu: Kompilator MelodyLang

Ten plik to Twoje koło ratunkowe. Wyjaśnia prostymi słowami (na tak zwany "chłopski rozum"), co dokładnie zbudowaliśmy i jak to działa, abyś mógł zabłysnąć przed prowadzącym.

---

## 1. O czym w ogóle jest ten projekt?

Zbudowaliśmy **własny język programowania** (nazwaliśmy go MelodyLang), który służy wyłącznie do tworzenia muzyki. Użytkownik pisze zwykły tekst (kod w pliku `.music`), a nasz program (tzw. **Kompilator**) tłumaczy to na plik dźwiękowy MIDI (`.mid`), którego można od razu posłuchać.

Nasz język to **DSL (Domain Specific Language)** – to mądre pojęcie, które oznacza język "dziedzinowy". Python to język ogólnego przeznaczenia (napiszesz w nim stronę, grę i AI), a MelodyLang to język DSL, bo służy do **tylko jednej konkretnej dziedziny** – notacji muzycznej.

---

## 2. Jak to działa krok po kroku? (Potok Kompilacji)

Kompilatory nigdy nie czytają kodu na raz. Dzielą pracę na kilka faz:

### Faza 1: Skaner (Lekser) i Tokeny

Prowadzący zapyta: _"Jak dzielicie tekst na mniejsze fragmenty?"_

- Skaner to taki "czytacz". Bierze ciąg znaków (literki z pliku) i grupuje je w sensowne słowa, czyli **Tokeny**.
- Zamiast widzieć tekst `TRACK main {`, skaner widzi to jako listę tokenów: `[TOKEN_TRACK, TOKEN_SPACJA, TOKEN_NAZWA("main"), TOKEN_LEWY_NAWIAS]`. Skaner pozbywa się też śmieci (np. odrzuca w ogóle białe znaki i komentarze, bo są niepotrzebne programowi).

### Faza 2: Parser (Gramatyka i Lark)

Prowadzący zapyta: _"Skąd kompilator wie, czy użytkownik nie napisał bzdur?"_

- Parser bierze Tokeny i sprawdza, czy układają się w poprawne zdania. Używamy do tego biblioteki **Lark**.
- Narzuciliśmy konkretne reguły języka. Zapisaliśmy je za pomocą **EBNF** (to taki uniwersalny format zapisywania reguł gramatyki, widoczny w pliku `grammar.lark`).
- Jeśli reguły są spełnione, Parser buduje z nich **Drzewo Parsowania** (strukturę zależności, co jest wewnątrz czego).

### Faza 3: Analiza Semantyczna i AST (Abstract Syntax Tree)

Prowadzący zapyta: _"Co to jest AST i po co wam Tablica Symboli?"_

- Drzewo parsowania ma dużo zbędnych rzeczy (np. klamerki, przecinki). My zamieniamy je na **AST (Drzewo Składni Abstracyjnej)** – zostaje w nim sam gęsty sens, np. "Ustaw tempo na 120", "Zagraj nutę C4". Dzieje się to w klasie `MelodyTransformer`.
- **Tablica Symboli (Symbol Table)** to po prostu słownik w kodzie kompilatora. To tu zapamiętujemy zmienne. Jeśli użytkownik wpisze `bassline = [C2, D2]`, wrzucamy to do słownika pod klucz "bassline". Kiedy potem wywoła `PLAY(bassline)`, zaglądamy do tego słownika (Tablicy Symboli) i wiemy, co ma zagrać. Jak zawoła zmienną, której nie było – rzucamy błąd semantyczny.

### Faza 4: Generator Kodu (Backend)

Prowadzący zapyta: _"Jak ostatecznie powstaje z tego plik MIDI?"_

- Kiedy już mamy spłaszczone, proste AST ułożone w listę komend krok po kroku (np. Zagraj, Pauza, Zagraj), rusza nasz plik `midi_gen.py`.
- Używa on zewnętrznej biblioteki `midiutil`. Śledzi "absolutny czas trwania". Z każdą nutą dokłada odpowiedni dźwięk w czasie i przesuwa swój 'licznik czasu' o czas trwania tej nuty lub wrzuca kilka dźwięków naraz w tym samym momencie (dla akordów). Na końcu wypluwa gotowy plik `.mid`.

---

## 3. Trudne pytania i proste odpowiedzi

**Q: Jak obsługujecie pętle (LOOP)?**
A: Stosujemy tzw. "Loop unrolling" (Rozwijanie pętli) na etapie budowania AST (w _Transformerze_). Zamiast jakoś skomplikowanie zapętlać maszynę grającą, kompilator po prostu np. widząc pętlę `LOOP 4 { zagraj A ; zagraj B}`, kopiuje tę instrukcję w pamięci wewnętrznej 4 razy (`zagraj A, zagraj B, zagraj A, zagraj B, ...`). Generator muzyki widzi potem długą, gotową linię prostą, bez żadnych pętli.

**Q: Czym różni się Skaner od Parsera?**
A: Skaner (Lekser) rozpoznaje "_Słowa_" (daje nam listę Tokenów np. "Nuta", "Znak równości"). Parser sprawdza czy z tych ułożone są sensowne "_Zdania_" bazując na gramatyce EBNF (np. wie, że po znaku równości musi być jakaś wartość, inna kolejność rzuci tzw. błąd składni).

**Q: Co dokładnie robi biblioteka Lark?**
A: Lark to gotowy parser napisany w Pythonie – generuje za nas Skaner i Parser na bazie naszego pliku tekstowego `grammar.lark`. Dzięki temu nie musieliśmy ręcznie pisać setek instrukcji "IF", sprawdzających literka po literce całej logiki wyrażeń. Wystarczyło zadeklarować mu tylko wzorce ułożenia "zdań".

**Q: Gdzie następuje sprawdzenie błędów?**
A: Błędy "literówek" i "złej kolejności" (błędy składniowe - tzw. Syntax Error) wypadają podczas Parserowania w Larku. Natomiast Błędy Logiczne (np. użycie usuniętej zmiennej w poleceniu PLAY) łapiemy później w kodzie Pythonowym (tzw. błędy Semantyczne - Semantic Error) sprawdzając naszą Tablicę Symboli.
