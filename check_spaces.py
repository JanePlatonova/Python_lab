import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('lab_in_out.tex', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')

patterns = [
    # 1. Missing space before math: word$math$
    (r'([а-яА-ЯіїєґІЇЄҐa-zA-Z0-9])(\$[^$]+\$)', 'Злипання слова перед формулою'),
    # 2. Missing space after math: $math$word
    (r'(\$[^$]+\$)([а-яА-ЯіїєґІЇЄҐa-zA-Z])', 'Злипання формули зі словом після неї'),
    # 3. Missing space after punctuation (excluding numbers like 3.14 or 1,2 or special LaTeX tags)
    (r'([а-яА-ЯіїєґІЇЄҐa-zA-Z])([,;:])([а-яА-ЯіїєґІЇЄҐa-zA-Z])', 'Відсутній пробіл після розділового знака'),
    # 4. Space before punctuation like $x$ , or word ,
    (r'(\S)\s+([,.:;!?])(?!\w)', 'Зайвий пробіл перед знаком пунктуації'),
    # 5. Missing space around em-dash: word"---word or similar
    (r'([а-яА-ЯіїєґІЇЄҐa-zA-Z0-9])"---', 'Відсутній пробіл перед тире "---'),
    (r'"---([а-яА-ЯіїєґІЇЄҐa-zA-Z0-9])', 'Відсутній пробіл після тире "---'),
    # 6. Specific TeX anomalies: $$ formula $$ attached to text
    (r'(\S)\$\$', 'Текст злипся з виключною формулою $$'),
    # 7. \itshape directly touching words: {\itshapeТекст...}
    (r'\\itshape([а-яА-ЯіїєґІЇЄҐa-zA-Z])', 'Відсутній пробіл після \\itshape')
]

for idx, line in enumerate(lines, 1):
    s = line.strip()
    if s.startswith('%'):
        continue
    # remove inline comments
    clean_line = re.sub(r'(?<!\\)%.*$', '', line).rstrip('\r\n')
    for pat, desc in patterns:
        for m in re.finditer(pat, clean_line):
            matched = m.group(0)
            start_pos = max(0, m.start() - 20)
            end_pos = min(len(clean_line), m.end() + 20)
            snippet = clean_line[start_pos:end_pos]
            print(f'Рядок {idx:3d} [{desc}]:  "{matched}"\n    Контекст: ...{snippet}...\n')

