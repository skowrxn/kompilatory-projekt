# Skaner Języka Generującego Muzykę

## O projekcie
Projekt implementuje analizator leksykalny (skaner) dla prostego języka opisu muzyki. Język ten pozwala na definiowanie tempa, wprowadzanie nut, pauz, określanie oktaw oraz grupowanie sekwencji w takty i powtórzenia. Głównym celem programu jest podział wejściowego ciągu znaków (kodu źródłowego) na logiczne jednostki zwane tokenami oraz wygenerowanie pliku HTML z pokolorowaną składnią i zaznaczonymi błędami leksykalnymi.

## Struktura projektu

* **`scanner.py`** – Rdzeń skanera. Zawiera definicje tokenów (`TokenType`, `Token`), klasę obsługującą błędy (`ScannerError`) oraz główną logikę analizatora leksykalnego (`Scanner`), która czyta tekst znak po znaku.
* **`color_syntax.py`** – Moduł odpowiedzialny za generowanie wizualizacji. Tłumaczy rozpoznane tokeny na kod HTML, przypisując im odpowiednie kolory i formatowanie (np. pogrubienie dla słów kluczowych).
* **`main.py`** – Skrypt uruchomieniowy. Testuje skaner na predefiniowanych przykładach, pozwala użytkownikowi na wprowadzanie własnych wyrażeń z poziomu konsoli i ostatecznie zapisuje wynik do pliku `output.html`.

## Zbiór tokenów

| Kod | Opis |
| :--- | :--- |
| `SŁOWO_KLUCZOWE` | Słowo kluczowe sterujące (np. `TEMPO`, `LOOP`) |
| `NUTA` | Pojedyncza litera oznaczająca dźwięk (A, B, C, D, E, F, G) |
| `PAUZA` | Litera oznaczająca pauzę (P) |
| `LICZBA` | Ciąg cyfr (używany do określania czasu trwania nuty, tempa lub powtórzeń) |
| `MODYFIKATOR_GORA` | Znak `+` (np. podwyższenie oktawy lub krzyżyk) |
| `MODYFIKATOR_DOL` | Znak `-` (np. obniżenie oktawy lub bemol) |
| `ZNAK_TAKTOWY` | Kreska pionowa `|` oddzielająca takty |
| `NAWIAS_L` | Nawias kwadratowy otwierający `[` (do grupowania akordów/sekwencji) |
| `NAWIAS_P` | Nawias kwadratowy zamykający `]` |
| `KONIEC` | Koniec strumienia znaków |

## Diagram przejść (Logika rozpoznawania)

1. **Stan początkowy (START)**:
   * Pomijaj białe znaki (spacje, tabulatory).
   * Jeśli znak to litera `A-Z, a-z` -> przejdź do stanu **IDENTYFIKATOR**.
   * Jeśli znak to cyfra `0-9` -> przejdź do stanu **LICZBA**.
   * Jeśli znak to `+`, `-`, `|`, `[`, `]` -> rozpoznaj pojedynczy znak, zwróć odpowiedni token i wróć do START.
   * Jeśli brak znaków (EOF) -> zwróć **KONIEC**.
   * W przeciwnym razie -> rzuć **Błąd (Nierozpoznany znak)**.

2. **Stan LICZBA**:
   * Czytaj kolejne znaki. Dopóki są cyframi, dodawaj do bufora. Po zakończeniu zwróć token `LICZBA`.

3. **Stan IDENTYFIKATOR**:
   * Czytaj kolejne litery i cyfry do bufora.
   * Jeśli wartość to "TEMPO" lub "LOOP" -> zwróć `SŁOWO_KLUCZOWE`.
   * Jeśli długość to 1 i znak jest z zakresu A-G -> zwróć `NUTA`.
   * Jeśli długość to 1 i znak to P -> zwróć `PAUZA`.
   * W przeciwnym razie -> rzuć **Błąd (Nieznany identyfikator)**.

## Jak uruchomić

1. Upewnij się, że masz zainstalowanego Pythona w wersji 3.10 lub nowszej.
2. Pobierz pliki projektu do jednego folderu.
3. Otwórz terminal w folderze z projektem i uruchom skrypt poleceniem:
   ```bash
   python main.py
