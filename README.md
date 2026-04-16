# MusicDSL - Interpreter Języka Muzycznego

Projekt realizowany w ramach przedmiotu **Teoria Kompilatorów**. Skupia się na budowie interpretera języka dziedzinowego (DSL) do algorytmicznej kompozycji muzyki, ze szczególnym uwzględnieniem analizy leksykalnej i wizualizacji kodu.

## Zakres Projektu

1. **Specyfikacja leksykalna:** Opracowanie zbioru tokenów definiujących nuty, parametry i struktury sterujące.
2. **Modelowanie automatu:** Przygotowanie diagramu przejść (DFA) dla skanera.
3. **Implementacja skanera:** Program analizujący kod źródłowy i rozpoznający tokeny.
4. **Syntax Highlighting:** Generator plików HTML kolorujący składnię wejściową z zachowaniem formatowania tekstu.

## Zadania

- [x] Przygotowanie tabeli tokenów własnego formatu.
- [x] Opracowanie diagramu przejść dla lekseru.
- [x] Implementacja skanera w języku Python.
- [x] Automatyczne generowanie pliku HTML z pokolorowanym kodem.

## Tabela Tokenów

| Token | Nazwa | Wzorzec (Regex) | Kolor (CSS) |
| :--- | :--- | :--- | :--- |
| **T_NOTE** | Nuta | `[A-G][#b]?[0-8]` | `#D2691E` |
| **T_KEYWORD** | Słowo kluczowe | `tempo\|play\|repeat\|instr` | `#0000FF` |
| **T_DUR** | Czas trwania | `\[(1\|2\|4\|8\|16)\]` | `#008000` |
| **T_NUM** | Liczba | `[0-9]+` | `#FF4500` |
| **T_COMMENT** | Komentarz | `//.*` | `#808080` |
| **T_OP** | Operator/Symbol | `\{ \| \} \| = \| ,` | `#555555` |

## Diagram Przejść (DFA)

Poniższy diagram przedstawia logikę rozpoznawania kluczowych tokenów przez skaner:

```mermaid
stateDiagram-v2
    [*] --> START
    START --> T_COMMENT: "/"
    START --> T_NOTE: "[A-G]"
    START --> T_KEYWORD: "[a-z]"
    START --> T_NUM: "[0-9]"
    START --> T_DUR: "["
    START --> T_OP: "{ } = ,"
    
    T_COMMENT --> [*]: Koniec linii
    T_NOTE --> [*]: Cyfra/Znak
    T_NUM --> T_NUM: Cyfra
    T_NUM --> [*]: Inny
    T_KEYWORD --> T_KEYWORD: Litera
    T_KEYWORD --> [*]: Inny
    T_DUR --> [*]: "]"
