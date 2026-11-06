import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('lab_in_out.tex', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

print("=== ДЕТАЛЬНИЙ ПОШУК ПРОБЛЕМ У lab_in_out.tex ===")

for i, line in enumerate(lines, 1):
    s = line.strip()
    if s.startswith('%'): continue
    
    # 1. Справжнє злипання $ з попереднім словом (буква перед $)
    m = re.findall(r'[а-яА-ЯіїєґІЇЄҐa-zA-Z0-9]\$', line)
    if m:
        # filter out math delimiters like $$
        m_filtered = [x for x in m if not x.endswith('$$')]
        if m_filtered:
            print(f"L{i} Буква перед $: {line.strip()}")
            
    # 2. Справжнє злипання $ з наступним словом ($ потім буква без пробілу чи розділового знаку)
    m2 = re.findall(r'\$[а-яА-ЯіїєґІЇЄҐa-zA-Z]', line)
    if m2:
        print(f"L{i} Буква після $: {line.strip()}")
        
    # 3. Злипання зі словом після розділового знаку (кома/крапка/двокрапка з наступною літерою без пробілу)
    m3 = re.findall(r'[а-яА-ЯіїєґІЇЄҐa-zA-Z][,:;][а-яА-ЯіїєґІЇЄҐa-zA-Z]', line)
    if m3:
        print(f"L{i} Немає пробілу після розділового знаку: {m3} -> {line.strip()}")
        
    # 4. Пробіл перед розділовим знаком у тексті: "слово ," чи "$x$ ,"
    m4 = re.findall(r'(?:\w|\$)\s+[,.:;](?!\s*\.\.)', line)
    if m4:
        # avoid false positives
        print(f"L{i} Пробіл перед розділовим знаком: {m4} -> {line.strip()}")
        
    # 5. \itshape без пробілу
    if r'\itshape' in line and re.search(r'\\itshape[А-Яа-яA-Za-z]', line):
        print(f"L{i} \\itshape злипся з текстом: {line.strip()}")
        
    # 6. Тире без пробілів
    if re.search(r'\S"---', line) or re.search(r'"---\S', line):
        print(f"L{i} Тире \"--- злиплося: {line.strip()}")
        
    # 7. Злипання формули $$ з текстом
    if re.search(r'\w\$\$', line):
        print(f"L{i} Текст злипся з $$: {line.strip()}")
        
    # 8. Дві крапки або зайві крапки: "..) або ".)" або " . "
    if '..) ' in line or ' .) ' in line:
        print(f"L{i} Зайва крапка: {line.strip()}")

