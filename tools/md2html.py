#!/usr/bin/env python3
"""MD-учебник курса → HTML-учебник (сплошной скролл, ¼ сухой остаток | ¾ изложение).

Перенос текста дословный: конвертер не сочиняет и не сокращает.
Визуальный слой навешивается отдельно — словарём VISUALS в файле-надстройке.
Проверка переноса: python3 tools/md2html.py --check src.md out.html
"""
import re, sys, os, html, json, unicodedata

# ——————————————————————————— разбор markdown ———————————————————————————

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', s)
    return s

FORMULA = re.compile(r'^[0-9A-Za-zА-Яа-яЁё\s()+\-−·×÷:=,.…\'’≠≤≥<>/√²³|]+$')

def is_formula(line):
    """Строка-формула (правило 10: формула стоит на своей строке).

    Признаются: **жирная** строка, `строка в бэктиках`, голая строка-выражение.
    Допускается короткая оговорка в скобках: **10a + b** (a ≠ 0).
    """
    t = line.strip()
    tail = ''
    m = re.fullmatch(r'((?:\*\*[^*]+\*\*)|(?:`[^`]+`))\s*(\([^()]{,60}\))', t)
    if m:
        t, tail = m.group(1), ' ' + m.group(2)
    marked = False
    m = re.fullmatch(r'\*\*([^*]+)\*\*', t) or re.fullmatch(r'`([^`]+)`', t)
    if m:
        t, marked = m.group(1).strip(), True

    if is_prose(t):
        return None
    if len(t) > 90 or len(t.split()) > 30:
        return None
    if marked:
        if re.search(r'[=≤≥<>·→]', t):
            return t + tail
        # выражение без знака отношения: «100a + 10b + c»
        if re.search(r'[+−:]', t) and re.search(r'\d', t) and len(t.split()) <= 10:
            return t + tail
        return None
    # голая строка без разметки — требования строже
    if not re.search(r'[=≤≥]', t) or '. ' in t or '—' in t:
        return None
    return t + tail if FORMULA.match(t) else None


def is_prose(t):
    """Фраза, а не формула: точка в конце, кавычки, двоеточие, союз-хвост."""
    if t.endswith(('.', '!', '?', ':', ';', ',')):
        return True
    if re.search(r'[«»„“”]', t):
        return True
    if ',' in t and re.search(r'[а-яё]{4,}$', t.lower()):
        return True
    if re.search(r',\s+(и|а|но|значит|поэтому|тогда)\s', t.lower()):
        return True
    return False


def parse(md):
    lines = md.split('\n')
    blocks, i = [], 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            i += 1; continue
        if s == '---':
            blocks.append(('hr', '')); i += 1; continue
        if s.startswith('```'):
            j = i + 1; buf = []
            while j < len(lines) and not lines[j].strip().startswith('```'):
                buf.append(lines[j]); j += 1
            blocks.append(('code', '\n'.join(buf))); i = j + 1; continue
        m = re.match(r'^(#{1,4}) (.+)$', s)
        if m:
            blocks.append(('h%d' % len(m.group(1)), m.group(2))); i += 1; continue
        if s.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(re.sub(r'^>\s?', '', lines[i].strip())); i += 1
            blocks.append(('quote', '\n'.join(buf))); continue
        if s.startswith('|'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                buf.append(lines[i].strip()); i += 1
            blocks.append(('table', '\n'.join(buf))); continue
        if re.match(r'^([-*]|\d+\.) ', s):
            buf = []
            while i < len(lines) and (re.match(r'^\s*([-*]|\d+\.) ', lines[i]) or
                                      (lines[i].startswith('  ') and lines[i].strip())):
                buf.append(lines[i].rstrip()); i += 1
            blocks.append(('list', '\n'.join(buf))); continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r'^\s*(#|>|\||```|---|[-*] |\d+\. )', lines[i].strip()):
            buf.append(lines[i].strip()); i += 1
        blocks.append(('p', ' '.join(buf)))
    return blocks

# ——————————————————————————— рендер ———————————————————————————

CARDS = [
    (r'^\*\*Типичная ошибка',            'wrong',  'Типичная ошибка'),
    (r'^\*\*Заметь главное',             'key',    'Заметь главное'),
    (r'^\*\*🎯 ?Боевой арсенал',         'arsenal','🎯 Боевой арсенал'),
    (r'^\*\*Идея\.',                     'idea',   'Идея'),
    (r'^\*\*Ритуал ',                    'ritual', None),
    (r'^\*\*Пример ',                    'exam',   None),
    (r'^\*\*Шаг \d',                     'step',   None),
]

def render_table(src):
    rows = [r for r in src.split('\n') if not re.match(r'^\|[\s:|-]+\|$', r)]
    out = ['<div class="tw"><table>']
    for n, r in enumerate(rows):
        cells = [c.strip() for c in r.strip('|').split('|')]
        tag = 'th' if n == 0 else 'td'
        out.append('<tr>' + ''.join(f'<{tag}>{inline(c)}</{tag}>' for c in cells) + '</tr>')
    out.append('</table></div>')
    return '\n'.join(out)

def render_quote(src):
    cls = 'plan' if '✅' in src else 'note'
    inner = []
    for blk in parse(src):
        inner.append(render_block(blk))
    return f'<div class="{cls} st">' + '\n'.join(inner) + '</div>'

def render_list(src):
    items, cur = [], None
    for ln in src.split('\n'):
        m = re.match(r'^\s*([-*]|\d+\.) (.*)$', ln)
        if m:
            if cur is not None: items.append(cur)
            cur = m.group(2)
        elif cur is not None:
            cur += ' ' + ln.strip()
    if cur is not None: items.append(cur)
    if re.match(r'^\s*\d+\.', src):
        li = ''.join(f'<li><span class="lin">{n+1}.</span> {inline(x)}</li>'
                     for n, x in enumerate(items))
        return f'<ol class="st num">{li}</ol>'
    return '<ul class="st">' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>'

def render_block(b):
    k, v = b
    if k == 'hr':   return '<hr>'
    if k == 'code': return f'<pre class="ascii st">{html.escape(v)}</pre>'
    if k == 'table':return f'<div class="st">{render_table(v)}</div>'
    if k == 'quote':return render_quote(v)
    if k == 'list': return render_list(v)
    if k.startswith('h'):
        n = int(k[1])
        return f'<h{n} class="st">{inline(v)}</h{n}>'
    f = is_formula(v)
    if f:
        return f'<div class="frm st">{inline(f)}</div>'
    for pat, cls, tag in CARDS:
        if re.match(pat, v):
            body = inline(v)
            if tag:
                m = re.match(r'^<b>(.+?)</b>\s*', body)
                if m:
                    tag, body = m.group(1).rstrip(':.'), body[m.end():]
                return (f'<div class="card {cls} st"><span class="tag">{tag}</span>'
                        f'<p>{body}</p></div>')
            return f'<p class="{cls} st">{body}</p>'
    return f'<p class="st">{inline(v)}</p>'

def first_sentence(t, limit=150):
    t = re.sub(r'^\*\*[^*]+\*\*[:\s]*', '', t)
    t = re.sub(r'\*\*|\*|`', '', t)
    m = re.search(r'^(.+?[.!?])(\s|$)', t)
    r = m.group(1) if m else t
    return r if len(r) <= limit else r[:limit].rsplit(' ', 1)[0] + '…'


TRANS = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z','и':'i',
         'й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t',
         'у':'u','ф':'f','х':'h','ц':'c','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'',
         'э':'e','ю':'yu','я':'ya'}

def slug(t):
    t = t.lower().replace('ё', 'е')
    out = ''.join(TRANS.get(c, c if c.isalnum() else '-') for c in t)
    return re.sub(r'-+', '-', out).strip('-')[:48]


BATTLE_H = re.compile(r'^\s*✍')
# Чем ✍-блок кончается. Заголовка у следующего разбора нет — он набран жирными
# абзацами, и без этого списка «боевой записью» становился весь разбор следующей
# задачи: 88 из 300 пунктов колонки решебника, включая её ответ.
BATTLE_END = re.compile(r'^\*\*(Шаг |Разобранный пример|Пример |Разбор|Ход |\d+\.\d+ — )')
BATTLE_H4 = re.compile(r'^\s*(Запись|💬)')


def doc_kind(src_path):
    """Учебник или документ с решениями. От вида зависит вся левая колонка.

    У учебника в колонке сухой остаток главы — то, что из неё уносят: идея,
    формула, ритуал, наблюдение. У документа с решениями уносить нечего:
    там нет ни идей, ни ритуалов, есть разборы, и остаток вырождается.
    Полезна там боевая запись — план и то, что ребёнок пишет на туре.
    """
    name = os.path.basename(src_path or '')
    if '_uchebnik' in name:
        return 'uchebnik'
    if re.search(r'_(resheniya|reshebnik|klyuch|podskazki)', name):
        return 'resheniya'
    return 'uchebnik'   # родительские документы идут учебниковой веткой: у неё свой фолбэк


def battle_artifact(k, v, want_phrase):
    """Что из ✍-блока попадает в колонку: план, фраза, строки записи.

    Дословно и в порядке появления. Проза ✍-блока (курсивная шапка, легенда,
    словесная проверка) не идёт — в колонке нужна запись, а не текст о ней.
    Точка в конце строки здесь формуле не мешает: боевая запись кончается
    предложением-итогом («Ответ = 13 + 21 + 21 + 13 = 68.»), и терять его нельзя.
    """
    if k == 'quote' and '✅' in v:
        clean = re.sub(r'[*`>#]', '', v)
        m = re.search(r'Ответ[^=\n]{0,24}=\s*[^\n]+', clean)
        if m:
            return ('План', m.group(0).strip())
        # план без строки «Ответ = …»: у периметров он и есть набор формул
        out = [('План', f) for f in
               (is_formula(ln.strip()) for ln in clean.split('\n')) if f]
        return out or None
    if k == 'list':
        out = []
        for ln in v.split('\n'):
            ln = re.sub(r'^\s*(?:[-*]|\d+\.)\s+', '', ln).strip()
            if ln:
                out.append(('На туре', ln))
        return out
    if k != 'p':
        return None
    if want_phrase:
        m = re.fullmatch(r'\*\*(.+)\*\*', v.strip())
        if m:
            return (want_phrase, m.group(1).strip())
    f = is_formula(v) or is_formula(re.sub(r'\.(\*{0,2})$', r'\1', v.strip()))
    if f:
        return ('На туре', f)
    # Итог записи бывает без знака отношения: «а) 97 цифр», «Нельзя.»,
    # «{1, 2, 7, 8} и {3, 4, 5, 6}». Внутри ✍-блока жирная строка — это запись
    # по определению, и терять из-за is_formula именно ответ нельзя.
    m = re.fullmatch(r'\*\*(.+?)\*\*\.?', v.strip())
    if m and len(m.group(1)) <= 90:
        return ('На туре', m.group(1).strip())
    # легенда обозначений открывает запись, но записью не является
    if re.match(r'^(Кирпичики|Обозначения)\s*:', v.strip()):
        return ('Кирпичики', first_sentence(v))
    return None


def battle_spec(blocks):
    """Боевая запись главы: содержимое её ✍-блоков, в порядке появления.

    Фраза-объяснение идёт в колонку **обеими строками** — испанской и русским
    переводом под ней: на бумагу выносится испанская, но читать колонку ребёнок
    должен без перевода в уме. Пара склеивается в один пункт, а не в два.
    """
    spec, seen = [], set()
    in_battle, want_phrase, pending = False, '', None

    def add(idx, art):
        # дедуп только против соседа: одна и та же фраза законно стоит
        # у двух задач одного блока, и выбрасывать второй показ нельзя
        if art and (not spec or spec[-1][1][1] != art[1]):
            spec.append((idx, art))

    def flush():
        nonlocal pending
        if pending:
            add(pending[0], (pending[1], pending[2]))
            pending = None

    for idx, (k, v) in enumerate(blocks):
        if k in ('h1', 'h2', 'h3'):
            flush()
            in_battle, want_phrase = bool(BATTLE_H.match(v)), ''
            continue
        if k == 'h4':
            flush()
            want_phrase = ''
            if in_battle and not BATTLE_H4.match(v):
                in_battle = False      # чужой подзаголовок — ✍-блок кончился
            elif in_battle and '💬' in v:
                want_phrase = '💬 Полнота' if 'конц' in v.lower() else '💬 Фраза'
            continue
        if in_battle and k == 'p' and BATTLE_END.match(v.strip()):
            flush()
            in_battle, want_phrase = False, ''
            continue
        if not in_battle:
            continue
        if want_phrase and k == 'p':
            s = v.strip()
            m = re.fullmatch(r'\*\*(.+)\*\*', s)
            if m and pending is None:
                pending = (idx, want_phrase, m.group(1).strip())
                continue
            m = re.fullmatch(r'\*(.+)\*', s)
            if pending and m:
                add(pending[0], (pending[1], pending[2] + '\n*' + m.group(1).strip() + '*'))
                pending, want_phrase = None, ''
                continue
            flush()
            want_phrase = ''
        got = battle_artifact(k, v, '')
        for a in (got if isinstance(got, list) else [got]):
            add(idx, a)
    flush()
    return spec


def dry_spec(blocks):
    """Сухой остаток главы — то, что из неё уносят. Ветка учебника."""
    spec, seen, in_ex, in_battle = [], set(), False, False
    for idx, (k, v) in enumerate(blocks):
        if k in ('h1', 'h2', 'h3'):
            in_battle = bool(BATTLE_H.match(v))
            continue
        if in_battle:
            continue          # ✍-блок разобранного примера в сухой остаток не идёт
        if k == 'p' and re.match(r'^\*\*(Разобранный пример|Пример|Разбор|Шаг \d)', v):
            in_ex = True
        a = artifact(k, v, in_ex)
        if a and a[1] not in seen:
            seen.add(a[1])
            spec.append((idx, a))
    return spec


def chapter_artifacts(blocks, kind):
    """Левая колонка главы — список (индекс блока, (ярлык, текст)).

    У учебника это всегда сухой остаток: ✍-блоки разобранных примеров в него
    не попадают, колонка остаётся ровно той же, что была до их появления.
    У документа с решениями колонка — боевая запись; если в главе ✍-блоков нет
    (вводные разделы «Условия — коротко», «Порядок решения на туре»),
    работает тот же сухой остаток.

    Второй элемент — сработала ли боевая ветка. От него зависит шапка колонки:
    обещать «Что пишешь на туре» над списком разделов нельзя.
    """
    if kind == 'uchebnik':
        return dry_spec(blocks), False
    b = battle_spec(blocks)
    return (b, True) if b else (dry_spec(blocks), False)


def artifact(k, v, in_example=False):
    """Что из блока попадает в сухой остаток. Только дословный текст MD.

    Из разобранных примеров в остаток идут план и наблюдение, но не промежуточная
    арифметика: формулы берём лишь из теоретической части главы.
    """
    if k == 'quote' and '✅' in v:
        clean = re.sub(r'[*`>#]', '', v)
        m = re.search(r'Ответ[^=\n]{0,24}=\s*[^\n]+', clean)
        if m:
            return ('План', m.group(0).strip())
        clean = re.sub(r'✅|План готов[.:]?', '', clean)
        return ('План', first_sentence(clean.strip()))
    if k != 'p':
        return None
    f = is_formula(v)
    if f:
        return None if in_example else ('Формула', f)
    if v.startswith('**Идея.**'):
        return ('Идея', first_sentence(v))
    if v.startswith('**Заметь главное'):
        return ('Заметь главное', first_sentence(v))
    m = re.match(r'^\*\*(Подсказка \d+)', v)
    if m:
        return (m.group(1), first_sentence(v))
    m = re.match(r'^\*\*(Ритуал [^*—-]+)', v)
    if m:
        return (m.group(1).strip(' .—-'), first_sentence(v))
    m = re.match(r'^\*\*(Типичная ошибка №\d+)', v)
    if m:
        return (m.group(1), first_sentence(v))
    return None


def split_chapters(md):
    """[(титул документа, подзаголовок), [(часть, заголовок главы, блоки)]]"""
    blocks = parse(md)
    head = []
    while blocks and blocks[0][0] in ('h1', 'h2', 'h3'):
        head.append(blocks.pop(0)[1])
    title = head[0] if head else 'Учебник'
    sub = ' · '.join(head[1:])
    chapters, part, cur, pre = [], '', None, []
    for k, v in blocks:
        if k in ('h1', 'h2'):
            part = v if k == 'h1' else part
            cur = {'title': v, 'part': part if k == 'h2' else '',
                   'ispart': k == 'h1', 'blocks': []}
            chapters.append(cur)
            continue
        if cur is None:
            pre.append((k, v))
            continue
        cur['blocks'].append((k, v))
    return title, sub, [c for c in chapters if c['blocks']], pre


def xlink_html(x):
    if not x:
        return ''
    lbl, href, title = x
    arrow = '←' if lbl.startswith('Теория') else '→'
    return (f'<p class="xlink"><a href="{href}">{arrow} {html.escape(lbl)}: '
            f'<b>{html.escape(title)}</b></a></p>')


def val_html(lbl, val):
    """Формулы в сухом остатке переносятся по знаку равенства."""
    h = inline(val).replace('\n', '<br>')
    # перенос по «=» — только когда строка длиннее строки колонки, и один раз:
    # иначе «KL = 27» занимало две строки и колонка выглядела столбиком сирот
    if lbl == 'Формула' and ',' not in val and len(val) > 46:
        h = re.sub(r'\s+=\s+', '<br>= ', h, count=1)
    return h


def page_names(chapters):
    return ['%02d-%s.html' % (n + 1, slug(c['title'])) for n, c in enumerate(chapters)]


def counterpart(src_path):
    """Учебник ↔ решебник: файл-напарник рядом, если он есть."""
    if not src_path:
        return None
    for a, b in (('_uchebnik.md', '_reshebnik.md'), ('_reshebnik.md', '_uchebnik.md')):
        if src_path.endswith(a):
            cand = src_path[:-len(a)] + b
            if os.path.exists(cand):
                return cand
    return None


def crosslinks(src_path, chapters, names):
    """Связка «глава ↔ её блок задач» по явной пометке «(глава N)» в решебнике.

    Номер берётся из самого заголовка, а не из порядка глав: переставят главы —
    ссылка либо останется верной, либо не построится, но не соврёт.
    """
    other = counterpart(src_path)
    if not other:
        return {}
    _, _, ochaps, _ = split_chapters(open(other).read())
    onames = page_names(ochaps)
    odir = os.path.basename(other)[:-3]
    by_chapter, by_block = {}, {}
    for oc, on in zip(ochaps, onames):
        m = re.match(r'^Глава (\d+)', oc['title'])
        if m:
            by_chapter[m.group(1)] = (on, oc['title'])
        m = re.search(r'\(глава (\d+)\)', oc['title'])
        if m:
            by_block[m.group(1)] = (on, oc['title'])
    out = {}
    for n, c in enumerate(chapters):
        m = re.match(r'^Глава (\d+)', c['title'])
        if m and m.group(1) in by_block:
            f, t = by_block[m.group(1)]
            out.setdefault(n, []).append(
                ('Задачи к этой главе', f'../{odir}/{f}', re.sub(r'\s*\(глава \d+\)', '', t)))
            continue
        m = re.search(r'\(глава (\d+)\)', c['title'])
        if m and m.group(1) in by_chapter:
            f, t = by_chapter[m.group(1)]
            out.setdefault(n, []).append(('Теория к этому блоку', f'../{odir}/{f}', t))
    return out


def razbor_links(src_path, chapters):
    """Решебник → отдельный файл разборов: блок N ведёт к первому разбору N.x."""
    if not src_path or not src_path.endswith('_reshebnik.md'):
        return {}
    other = src_path[:-len('_reshebnik.md')] + '_resheniya.md'
    if not os.path.exists(other):
        return {}
    _, _, ochaps, _ = split_chapters(open(other).read())
    onames = page_names(ochaps)
    odir = os.path.basename(other)[:-3]
    first = {}
    for oc, on in zip(ochaps, onames):
        m = re.match(r'^(\d+)\.\d+', oc['title'])
        if m:
            first.setdefault(m.group(1), (on, oc['title']))
    out = {}
    for n, c in enumerate(chapters):
        m = re.match(r'^Блок (\d+)', c['title'])
        if m and m.group(1) in first:
            f, t = first[m.group(1)]
            out[n] = ('Разборы по шагам', f'../{odir}/{f}', t)
    return out


def build_pages(md, visuals=None, src_path=None):
    visuals = visuals or {}
    kind = doc_kind(src_path)
    title, sub, chapters, pre = split_chapters(md)
    files, used, shown_part = {}, set(), None
    names = page_names(chapters)
    xmap = crosslinks(src_path, chapters, names)
    for n, lk in razbor_links(src_path, chapters).items():
        xmap.setdefault(n, []).append(lk)

    for n, c in enumerate(chapters):
        # 1) какие блоки главы дают левую колонку
        spec, is_battle = chapter_artifacts(c['blocks'], kind)
        if not spec:      # родительские документы: остаток из подзаголовков
            # ✍-блок и его подзаголовки сюда не попадают: в учебниковой колонке
            # боевой записи не место, а глава без остатка иначе показывала бы
            # ярлык «Раздел ✍ Что достаточно написать на туре»
            spec = [(idx, ('Раздел', re.sub(r'\*\*|\*|`', '', v)))
                    for idx, (k, v) in enumerate(c['blocks'])
                    if k in ('h3', 'h4') and not BATTLE_H.match(v)
                    and '💬' not in v and 'Запись' != v.strip()]
        at = {idx: n for n, (idx, _) in enumerate(spec)}
        arts = [a for _, a in spec]

        # 2) одна сборка тела: разметка + якоря артефактов + иллюстрации
        body = []
        for idx, (k, v) in enumerate(c['blocks']):
            h = render_block((k, v))
            if idx in at:
                h = f'<div id="a{at[idx]}" data-art="{at[idx]}">{h}</div>'
            body.append(h)
            key = re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', v)).strip()
            for anchor, figure in visuals.items():
                if anchor in key and anchor not in used:
                    used.add(anchor)
                    body.append(figure)

        # ярлык печатается только когда он сменился: подряд идущие строки боевой
        # записи — одна группа, и семь раз «На туре» ничего не сообщают
        btns, prev = [], None
        for i, (lbl, val) in enumerate(arts):
            # схлопывание ярлыка — только в боевой колонке; учебниковый
            # сухой остаток остаётся ровно таким, каким был
            cont = (is_battle and lbl == prev
                    and (lbl == 'На туре' or lbl.startswith('💬')))
            head = '' if cont else f'<span class="lbl">{html.escape(lbl)}</span>'
            mono = ' f' if (lbl in ('Формула', 'На туре')
                            or (is_battle and lbl == 'План')) else ''
            if lbl.startswith('💬'):
                mono = ' ph'          # испанская фраза с переводом — свой кегль
            btns.append(f'<button class="art{" cont" if cont else ""}" data-art="{i}">'
                        f'{head}<span class="val{mono}">{val_html(lbl, val)}</span></button>')
            prev = lbl
        nav = '\n'.join(btns) or \
            '<p class="flab">В этом разделе выносить в остаток нечего.</p>'

        prev = f'<a href="{names[n-1]}">← {html.escape(chapters[n-1]["title"])}</a>' if n else ''
        nxt = f'<a href="{names[n+1]}">{html.escape(chapters[n+1]["title"])} →</a>' if n < len(chapters) - 1 else ''
        chapnav = (f'<a href="index.html">все главы</a> · {n+1} из {len(chapters)}')
        partlab = ''
        if c.get('ispart'):
            shown_part = c['title']   # заголовок части уже стоит титулом страницы
        if c['part'] and c['part'] != shown_part:
            partlab = f'<p class="partlab">{inline(c["part"])}</p>'
            shown_part = c['part']

        files[names[n]] = (TEMPLATE
            .replace('{{TITLE}}', html.escape(c['title']))
            .replace('{{DOC}}', html.escape(title))
            .replace('{{PARTLAB}}', partlab)
            .replace('{{SUB}}', '')
            .replace('{{CHAPNAV}}', chapnav)
            .replace('{{RTITLE_TAG}}', '' if not spec else
                     '<p class="rtitle">%s</p>' %
                     ('Что пишешь на туре' if is_battle else 'Сухой остаток главы'))
            # ширину задаёт факт боевой записи, а не имя файла: у вводных
            # разделов документа-решения колонка обычная, и растягивать её незачем
            .replace('{{WRAPCLASS}}', ' battle' if is_battle else '')
            .replace('{{NAV}}', nav)
            .replace('{{BODY}}', '\n'.join(body))
            .replace('{{FOOT}}', ''.join(xlink_html(x) for x in xmap.get(n, [])) +
                     f'<div class="pager">{prev}{nxt}</div>'))

    rows = []
    lastpart = None
    for n, c in enumerate(chapters):
        if c['part'] != lastpart and c['part']:
            rows.append(f'<div class="navpart">{html.escape(c["part"])}</div>')
            lastpart = c['part']
        idea = next((artifact(k, v)[1] for k, v in c['blocks']
                     if artifact(k, v) and artifact(k, v)[0] == 'Идея'), '')
        rows.append(f'<a class="ix" href="{names[n]}"><b>{html.escape(c["title"])}</b>'
                    f'<span>{html.escape(idea)}</span></a>')
    files['index.html'] = (INDEX
        .replace('{{TITLE}}', html.escape(title))
        .replace('{{RTITLE_TAG}}', '').replace('{{WRAPCLASS}}', '')
        .replace('{{SUB}}', html.escape(sub))
        .replace('{{PRE}}', '\n'.join(render_block(b) for b in pre))
        .replace('{{ROWS}}', '\n'.join(rows)))

    missed = [a for a in visuals if a not in used]
    if missed:
        print('⚠ иллюстрации без якоря в тексте:', missed, file=sys.stderr)
    return files


# ——————————————————————————— сверка переноса ———————————————————————————

def visible_text(h):
    h = re.sub(r'<style.*?</style>|<script.*?</script>|<aside.*?</aside>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return html.unescape(h)

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'[*`_>#|\[\]]', '', s)
    s = s.replace('—', '-').replace('–', '-').replace('−', '-')
    s = re.sub(r'[«»"“”]', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()

def sentences(t):
    t = re.sub(r'\s+', ' ', t)
    return [x.strip() for x in re.split(r'(?<=[.!?:;])\s+', t) if len(x.strip()) > 25]

def md_text(md, drop_head=False, drop_h2=False):
    """Плоский текст MD — ровно те слова, которые обязаны доехать до HTML."""
    out = []
    blocks = parse(md)
    if drop_head:
        while blocks and blocks[0][0] in ('h1', 'h2', 'h3'):
            blocks.pop(0)
    for k, v in blocks:
        if k == 'hr' or (drop_h2 and k in ('h1', 'h2')):
            continue
        if k == 'table':
            for r in v.split('\n'):
                if re.match(r'^\|[\s:|-]+\|$', r):
                    continue
                out.append(' '.join(c.strip() for c in r.strip('|').split('|')))
        elif k == 'quote':
            out.append(md_text(v))
        else:
            out.append(v)
    return ' '.join(out)

WORD = re.compile(r"[0-9a-zA-Zа-яёА-ЯЁ]+", re.U)

def words(t):
    t = unicodedata.normalize('NFKC', t)
    return WORD.findall(t.lower())

def js_ok(html_path):
    """Синтаксис скрипта страницы: сломанный JS гасит всё проявление."""
    import subprocess, tempfile, shutil
    src = open(html_path).read()
    m = re.search(r'<script>(.*?)</script>', src, re.S)
    if not m:
        return 'скрипта нет'
    if not shutil.which('node'):
        return 'node недоступен — не проверен'
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as f:
        f.write(m.group(1)); tmp = f.name
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
    return 'ок' if r.returncode == 0 else 'СЛОМАН: ' + r.stderr.strip().split(chr(10))[0]


def check(md_path, html_path, minrun=3):
    import difflib
    import glob, os
    if os.path.isdir(html_path):
        parts = sorted(f for f in glob.glob(os.path.join(html_path, '*.html'))
                       if not f.endswith('index.html'))
        idx = open(os.path.join(html_path, 'index.html')).read()
        m = re.search(r'<div class="pre">(.*?)</div>\s*<div class="navpart"|'
                      r'<div class="pre">(.*?)</div>\s*<a class="ix"', idx, re.S)
        pre = (m.group(1) or m.group(2)) if m else ''
        raw = pre + '\n' + '\n'.join(open(f).read() for f in parts)
    else:
        parts = [html_path]
        raw = open(html_path).read()
    nfig = len(re.findall(r'<figure', raw))
    raw = re.sub(r'<figure.*?</figure>|<title>.*?</title>', ' ', raw, flags=re.S)
    raw = re.sub(r'<p class="sub">.*?</p>', ' ', raw, flags=re.S)
    raw = re.sub(r'<div class="pager">.*?</div>', ' ', raw, flags=re.S)
    nx = len(re.findall(r'<p class="xlink">', raw))
    raw = re.sub(r'<p class="xlink">.*?</p>', ' ', raw, flags=re.S)
    a = words(md_text(open(md_path).read(), drop_head=True))
    b = words(visible_text(raw))
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    lost, added = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ('delete', 'replace') and i2 - i1 >= minrun:
            lost.append(' '.join(a[i1:i2]))
        if tag in ('insert', 'replace') and j2 - j1 >= minrun:
            added.append(' '.join(b[j1:j2]))
    print(f'слов в MD: {len(a)} · слов в HTML: {len(b)} · иллюстраций: {nfig}'
          f' · перекрёстных ссылок: {nx}')
    print('скрипт страницы:', js_ok(parts[0]))
    print('страниц:', len(parts))
    if len(parts) > 1:
        blocks = parse(open(md_path).read())
        while blocks and blocks[0][0] in ('h1', 'h2', 'h3'):
            blocks.pop(0)
        heads = [v for k, v in blocks if k in ('h1', 'h2', 'h3', 'h4')]
        pages = norm(visible_text('\n'.join(open(f).read() for f in parts)))
        lost_t = [h for h in heads if norm(h) not in pages]
        print('заголовки в тексте страниц: %d из %d' % (len(heads) - len(lost_t), len(heads)))
        for h in lost_t:
            print('  ✗ заголовок', h)
    print(f'потеряно фрагментов (≥{minrun} слов): {len(lost)}')
    for x in lost:
        print('  ✗', x[:120])
    print(f'дописано фрагментов (≥{minrun} слов): {len(added)}')
    for x in added:
        print('  +', x[:120])
    return len(lost) + len(added)

TEMPLATE = open(__file__.replace('md2html.py', 'md2html_template.html')).read()
INDEX = open(__file__.replace('md2html.py', 'md2html_index.html')).read()

if __name__ == '__main__':
    if sys.argv[1] == '--check':
        sys.exit(1 if check(sys.argv[2], sys.argv[3]) else 0)
    import os
    src, dst = sys.argv[1], sys.argv[2]
    vis = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {}
    import glob as _glob
    os.makedirs(dst, exist_ok=True)
    for stale in _glob.glob(os.path.join(dst, '*.html')):
        os.remove(stale)          # имена страниц зависят от нумерации глав
    pages = build_pages(open(src).read(), vis, src_path=src)
    for name, content in pages.items():
        open(os.path.join(dst, name), 'w').write(content)
    print('→ %s: %d страниц' % (dst, len(pages) - 1))
