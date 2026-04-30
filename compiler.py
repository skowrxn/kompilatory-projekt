import re
import logging
from lark import Transformer, v_args

logger = logging.getLogger(__name__)

class MelodyTransformer(Transformer):
    """
    Transformuje Drzewo Składniowe (AST) wygenerowane przez LARK
    do wewnętrznej reprezentacji zdarzeń muzycznych.
    """
    def __init__(self):
        super().__init__()
        self.symbol_table = {}
        self.global_params = {
            "TEMPO": 120,
            "INSTRUMENT": 1
        }
        self.current_time = 0.0

    def program(self, items):
        # Spłaszcz główną strukturę
        flat_events = []
        for item in items:
            if isinstance(item, list):
                flat_events.extend(item)
            elif isinstance(item, dict) and item.get("type") != "assignment":
                flat_events.append(item)
        return flat_events

    def set_param(self, items):
        param_name = str(items[0])
        param_value = int(items[1])
        self.global_params[param_name] = param_value
        return {"type": "set_param", "name": param_name, "value": param_value}

    def assignment(self, items):
        var_name = str(items[0])
        sequence_data = items[1]
        self.symbol_table[var_name] = sequence_data
        return {"type": "assignment", "name": var_name, "value": sequence_data}

    def sequence(self, items):
        # Flatten the sequence containing notes, chords, or rests
        flattened = []
        for item in items:
            if isinstance(item, list):
                flattened.extend(item)
            else:
                flattened.append(item)
        return {"type": "sequence", "elements": flattened}

    def loop_block(self, items):
        iterations = int(items[0])
        body = items[1:]
        
        flat_body = []
        for b in body:
            if isinstance(b, list):
                flat_body.extend(b)
            elif isinstance(b, dict) and b.get("type") != "assignment":
                flat_body.append(b)
                
        unrolled = []
        for _ in range(iterations):
            unrolled.extend(flat_body)
            
        return unrolled

    def track_def(self, items):
        body = items[1:]
        flat = []
        for b in body:
            if isinstance(b, list):
                flat.extend(b)
            elif isinstance(b, dict) and b.get("type") != "assignment":
                flat.append(b)
        return flat

    def play_func(self, items):
        var_name = str(items[0])
        times = int(items[1]) if len(items) > 1 else 1
        
        if var_name not in self.symbol_table:
            raise ValueError(f"Semantic Error: Zmienna motywu '{var_name}' nie została zdefiniowana!")
            
        seq = self.symbol_table[var_name].get("elements", [])
        expanded = []
        for _ in range(times):
            expanded.extend(seq)
        return expanded

    def var_reference(self, items):
        var_name = str(items[0])
        if var_name not in self.symbol_table:
            raise ValueError(f"Semantic Error: Użycie niezdefiniowanej zmiennej '{var_name}'")
        return self.symbol_table[var_name]

    # Szablony do rozwinięcia dla poszczególnych nut
    def note(self, items):
        raw_pitch = str(items[0])
        match = re.match(r"([A-G][b#]?)([0-9]?)", raw_pitch)
        pitch = match.group(1)
        octave = int(match.group(2)) if match.group(2) else 4
        
        duration = 4
        if len(items) > 1 and items[1] is not None:
            duration = items[1]
            
        return {"type": "note", "pitch": pitch, "octave": octave, "duration": duration}

    def chord(self, items):
        duration = 4
        pitches = []
        
        for item in items:
            if isinstance(item, int):
                duration = item
            elif item is not None:
                match = re.match(r"([A-G][b#]?)([0-9]?)", str(item))
                p = match.group(1)
                o = int(match.group(2)) if match.group(2) else 4
                pitches.append({"pitch": p, "octave": o})
                
        return {"type": "chord", "pitches": pitches, "duration": duration}

    def rest(self, items):
        duration = 4
        for item in items:
            if isinstance(item, int):
                duration = item
                break
        return {"type": "rest", "duration": duration}
        
    def duration(self, items):
        return int(items[0])

# Przykład użycia / testowania
if __name__ == '__main__':
    from lark import Lark
    with open('grammar.lark', 'r', encoding='utf-8') as f:
        grammar = f.read()
        
    parser = Lark(grammar, parser='lalr', start='program')
    
    with open('example.music', 'r', encoding='utf-8') as f:
        src = f.read()
        
    tree = parser.parse(src)
    print("Drzewo AST:")
    print(tree.pretty())
    
    transformer = MelodyTransformer()
    ast_processed = transformer.transform(tree)
    print("Przetworzone zdarzenia:")
    import json
    # Obiekty posiadają customowe klasy, więc print będzie uproszczony
    print(ast_processed)
