import re
import sys

TOKENS = [
    ('T_COMMENT', r'//.*'),
    ('T_NOTE',    r'[A-G][#b]?[0-8]'),
    ('T_KEYWORD', r'\b(tempo|play|repeat|instr)\b'),
    ('T_DUR',     r'\[(1|2|4|8|16)\]'),
    ('T_NUM',     r'\d+'),
    ('T_OP',      r'[\{\}\=\,]'),
    ('T_WHITESPACE', r'\s+'),
    ('T_UNKNOWN', r'.'),
]

CSS = """
body { background: #1e1e1e; color: #d4d4d4; font-family: monospace; white-space: pre; padding: 20px; }
.T_COMMENT { color: #6a9955; }
.T_NOTE { color: #d2691e; font-weight: bold; }
.T_KEYWORD { color: #569cd6; }
.T_DUR { color: #b5cea8; }
.T_NUM { color: #ce9178; }
.T_OP { color: #808080; }
.T_UNKNOWN { color: #f44336; text-decoration: underline; }
"""

def highlight(source_code):
    html = ["<html><head><style>", CSS, "</style></head><body>"]
    pos = 0
    while pos < len(source_code):
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(source_code, pos)
            if match:
                text = match.group(0)
                if token_type == 'T_WHITESPACE':
                    html.append(text.replace(' ', '&nbsp;').replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;'))
                else:
                    html.append(f'<span class="{token_type}">{text}</span>')
                pos = match.end()
                break
    html.append("</body></html>")
    return "".join(html)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scanner.py input.music output.html")
    else:
        with open(sys.argv[1], 'r') as f:
            code = f.read()
        with open(sys.argv[2], 'w') as f:
            f.write(highlight(code))
