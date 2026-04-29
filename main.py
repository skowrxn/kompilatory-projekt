from scanner import scan_expression
from color_syntax import generate_html

PREDEFINIOWANE = [
    "TEMPO 120 | C4 E4 G4 | C+4",
    "LOOP 4 [ A-8 C8 E8 P4 ]",
    "C4 D4 E4 | F4 @ G4",
    "  [ C 4 + E 4 ] | P 2  ",
    "TEMPO 90 invalid_note",
]

if __name__ == "__main__":
    for expr in PREDEFINIOWANE:
        scan_expression(expr)
        print("-" * 30)

    extra: list[str] = []
    while True:
        expr = input("Wyrażenie muzyczne (lub koniec): ")
        if expr.strip().lower() == "koniec":
            break
        scan_expression(expr)
        print()
        extra.append(expr)

    output_path = "output.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(generate_html(PREDEFINIOWANE + extra))
    print(f"\nZapisano kolorowy HTML: {output_path}")