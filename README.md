# MelodyLang - Kompilator Języka Muzycznego (Transpiler źródło-MIDI)

**Przedmiot:** Techniki Kompilacji i Konfiguracji (TKiK)
**ZESPÓŁ:**

- Bartłomiej Skowron (bskowron@student.agh.edu.pl)
- Kajetan Skitał (kskital@student.agh.edu.pl)
- Jan Ster (sterjan@student.agh.edu.pl)

## Opis projektu

Projekt **MelodyLang** to kompleksowy kompilator zbudowany w oparciu o specyfikację DSL (Domain Specific Language) dedykowanego do zapisu i sekwencjonowania utworów muzycznych. Kompilator przetwarza pliki z rozszerzeniem `.music`, przeprowadzając analizę leksykalną i syntaktyczną (z wykorzystaniem biblioteki **Lark**), w celu wygenerowania w pełni funkcjonalnego pliku binarnego MIDI (`.mid`).

Kompilator wspiera:

- Definiowanie struktur blokowych utworów
- Zmienne i operacje podstawiania
- Metaprogramowanie sekwencji muzycznych (pętle, rozwijanie pętli w locie)
- Polimorficzne typy danych takie jak nuty obok całych akordów

## Spis Tokenów

W procesie skanowania tekst wejściowy rozbijany jest na tokeny zaprezentowane w poniższej tabeli:

| Token         | Wzorzec (Regex / String)             | Opis                                                                  |
| ------------- | ------------------------------------ | --------------------------------------------------------------------- |
| `TRACK`       | `"TRACK"`                            | Rozpoczęcie definicji domyślnej ścieżki w utworze.                    |
| `SET`         | `"SET"`                              | Słowo kluczowe służące do ustalenia parametrów globalnych utworu.     |
| `LOOP`        | `"LOOP"`                             | Definicja pętli sekwencyjnej (unrolling).                             |
| `PLAY`        | `"PLAY"`                             | Wywołanie zdefiniowanej zmiennej.                                     |
| `NOTE_PITCH`  | `/[A-G][b#]?[0-9]?(?![a-zA-Z0-9_])/` | Wzorzec definiujący literę nutową (np. C4, Db3, F#).                  |
| `REST_CHAR`   | `/P(?![a-zA-Z0-9_])/`                | Pauza (przerwa) w sekwencji MIDI.                                     |
| `CNAME`       | `/[a-zA-Z_]\w*/`                     | Standardowy identyfikator nazwy zmiennej bazujący na bibliotece lark. |
| `INT`         | `/[0-9]+/`                           | Wartości całkowite.                                                   |
| `EQUAL`       | `"="`                                | Operator przypisania wartości do zmiennej.                            |
| `LBRACE`      | `"{"`                                | Otwarcie bloku instrukcji.                                            |
| `RBRACE`      | `"}"`                                | Zamknięcie bloku instrukcji.                                          |
| `LSQB`        | `"["`                                | Otwarcie sekwencji zmiennej (listy).                                  |
| `RSQB`        | `"]"`                                | Zamknięcie sekwencji zmiennej.                                        |
| `LESSTHAN`    | `"<"`                                | Otwarcie akordu muzycznego.                                           |
| `GREATERTHAN` | `">"`                                | Zamknięcie akordu muzycznego.                                         |
| `COLON`       | `":"`                                | Przedrostek definiujący czas trwania nuty.                            |

## Gramatyka EBNF

```ebnf
start: program

program: statement*

?statement: track_def
          | assignment
          | set_param
          | loop_block
          | play_func
          | sequence

track_def: "TRACK" CNAME "{" statement* "}"

assignment: CNAME "=" sequence

set_param: "SET" CNAME "=" INT

loop_block: "LOOP" INT "{" statement* "}"

play_func: "PLAY" "(" CNAME ("," "times=" INT)? ")"

sequence: "[" (note_item ("," note_item)*)? "]"
        | note_item

?note_item: note
          | chord
          | rest
          | CNAME -> var_reference

note: NOTE_PITCH duration?
chord: "<" NOTE_PITCH ("," NOTE_PITCH)* ">" duration?
rest: REST_CHAR duration?

duration: ":" INT

NOTE_PITCH.2: /[A-G][b#]?[0-9]?(?![a-zA-Z0-9_])/
REST_CHAR.2: /P(?![a-zA-Z0-9_])/

%import common.CNAME
%import common.INT
%import common.WS
%import common.SH_COMMENT -> COMMENT

%ignore WS
%ignore COMMENT
```

## Architektura Translatora

Rozwinięty potok kompilacji dzieli się na trzy fazy:

1. **Skaner i Parser (LARK)** - `grammar.lark` stanowi rdzeń definiujący parsowanie kodu wejściowego do formy bezkontekstowego drzewa (Parse Tree).
2. **AST Transformer** - `compiler.py` nadpisuje wygenerowane węzły drzewa ujednolicając wszystko do potężnej listy (spłaszczanie / "Loop unrolling") gotowej dla Backend'u. Logika ta również waliduje występowanie symboli (weryfikacja semantyczna w trakcie przypisywań i wywołań używając tzw. Tablicy Symboli).
3. **Generator MIDI** - Klasa zawarta w module `midi_gen.py` iteruje po gotowych instrukcjach i śledząc absolutny upływ czasu konwertuje struktury notacyjne i uderzenia na finalny schemat i uderzenia `midiutil.MIDIFile`, tworząc ostateczny, binarny i bezbłędnie renderowany plik muzyczny.

## Instrukcja uruchomienia

Upewnij się, że wirtualne środowisko Python posiada zainstalowane zewnętrzne moduły: `lark`, dla procesowania teorii języka, oraz `midiutil`, by nadpisywać standardowy ciąg bitów dla wirtualnych instrumentów.

Aby zainstalować wszystkie wymagane moduły, użyj komendy:

```bash
pip install lark midiutil
```

Aby skompilować plik z własnym kodem (domyślnie użyje `example.music` i wyrzuci `output.mid`):

```bash
python main.py --input example.music --output output.mid
```

Następnie bez problemu otwórz gotowy plik `.mid` przy pomocy narzędzi DAW (np. FL Studio/Ableton), odtwarzaczy systemowych bądź internetowych odtwarzaczy MIDI!
