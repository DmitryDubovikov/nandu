#!/usr/bin/env python3
"""MD-учебник курса → HTML-учебник (сплошной скролл, ¼ сухой остаток | ¾ изложение).

Перенос текста дословный: конвертер не сочиняет и не сокращает.
Визуальный слой навешивается отдельно — словарём VISUALS в файле-надстройке.
Проверка переноса: python3 tools/md2html.py --check src.md out.html
"""
import re, sys, html, json, unicodedata

# ——————————————————————————— разбор markdown ———————————————————————————

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', s)
    return s

FORMULA = re.compile(r'^[0-9A-Za-zА-Яа-яЁё\s()+\-−·×÷:=,.…\'’≠≤≥/]*[=][0-9A-Za-zА-Яа-яЁё\s()+\-−·×÷:=,.…\'’≠≤≥/]*$')

def is_formula(line):
    """Строка-формула (правило 10: формула стоит на своей строке).

    Допускается короткая оговорка в скобках после формулы: **10a + b** (a ≠ 0).
    """
    t = line.strip()
    tail = ''
    m = re.fullmatch(r'(\*\*[^*]+\*\*)\s*(\([^()]{,60}\))', t)
    if m:
        t, tail = m.group(1), ' ' + m.group(2)
    m = re.fullmatch(r'\*\*([^*]+)\*\*', t)
    if m:
        t = m.group(1)
        if '=' in t or '·' in t or '→' in t:
            return t + tail
        # выражение без знака равенства: «100a + 10b + c»
        if ('—' not in t and len(t) <= 60 and len(t.split()) <= 10
                and re.search(r'[+\-−:]', t) and not t.rstrip().endswith(('.', ':', '!', '?'))
                and re.search(r'\d', t)):
            return t + tail
        return None
    if len(t) > 70 or '=' not in t or '. ' in t or '—' in t:
        return None
    if t.endswith(':') or re.search(r',\s+(и|а|но|значит|поэтому)\s', t.lower()):
        return None   # это фраза, вводящая формулу, а не сама формула
    if FORMULA.match(t) and len(t.split()) <= 14:
        return t
    return None

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


def artifact(k, v, in_example=False):
    """Что из блока попадает в сухой остаток. Только дословный текст MD.

    Из разобранных примеров в остаток идут план и наблюдение, но не промежуточная
    арифметика: формулы берём лишь из теоретической части главы.
    """
    if k == 'quote' and '✅' in v:
        m = re.search(r'Ответ\s*=\s*[^\n]+', v.replace('*', ''))
        return ('План', m.group(0).strip()) if m else ('План', first_sentence(v.replace('>', '')))
    if k != 'p':
        return None
    f = is_formula(v)
    if f:
        return None if in_example else ('Формула', f)
    if v.startswith('**Идея.**'):
        return ('Идея', first_sentence(v))
    if v.startswith('**Заметь главное'):
        return ('Заметь главное', first_sentence(v))
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
        if k == 'h1':
            part = v
            continue
        if k == 'h2':
            cur = {'title': v, 'part': part, 'blocks': []}
            chapters.append(cur)
            continue
        if cur is None:
            pre.append((k, v))
            continue
        cur['blocks'].append((k, v))
    return title, sub, chapters, pre


def val_html(lbl, val):
    """Формулы в сухом остатке переносятся по знаку равенства."""
    h = inline(val)
    if lbl == 'Формула':
        h = re.sub(r'\s+=\s+', '<br>= ', h)
    return h


def build_pages(md, visuals=None):
    visuals = visuals or {}
    title, sub, chapters, pre = split_chapters(md)
    files, used = {}, set()
    names = ['%02d-%s.html' % (n + 1, slug(c['title'])) for n, c in enumerate(chapters)]

    for n, c in enumerate(chapters):
        arts, body, in_ex, seen = [], [], False, set()
        for k, v in c['blocks']:
            if k == 'p' and re.match(r'^\*\*Пример ', v):
                in_ex = True
            a = artifact(k, v, in_ex)
            if a and a[1] in seen:
                a = None
            if a:
                seen.add(a[1])
            h = render_block((k, v))
            if a:
                i = len(arts)
                arts.append(a)
                h = f'<div id="a{i}" data-art="{i}">{h}</div>'
            body.append(h)
            key = re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', v))[:60].strip()
            for anchor, figure in visuals.items():
                if anchor in key and anchor not in used:
                    used.add(anchor)
                    body.append(figure)

        nav = '\n'.join(
            f'<button class="art" data-art="{i}"><span class="lbl">{html.escape(lbl)}</span>'
            f'<span class="val{" f" if lbl == "Формула" else ""}">{val_html(lbl, val)}</span>'
            f'</button>'
            for i, (lbl, val) in enumerate(arts)) or \
            '<p class="flab">В этой главе выносить в остаток нечего — она вводная.</p>'

        prev = f'<a href="{names[n-1]}">← {html.escape(chapters[n-1]["title"])}</a>' if n else ''
        nxt = f'<a href="{names[n+1]}">{html.escape(chapters[n+1]["title"])} →</a>' if n < len(chapters) - 1 else ''
        chapnav = (f'<a href="index.html">все главы</a> · {n+1} из {len(chapters)}')

        files[names[n]] = (TEMPLATE
            .replace('{{TITLE}}', html.escape(c['title']))
            .replace('{{DOC}}', html.escape(title))
            .replace('{{SUB}}', html.escape(c['part'] or sub))
            .replace('{{CHAPNAV}}', chapnav)
            .replace('{{NAV}}', nav)
            .replace('{{BODY}}', '\n'.join(body))
            .replace('{{FOOT}}', f'<div class="pager">{prev}{nxt}</div>'))

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
    raw = re.sub(r'<main>\s*<h1>.*?</p>', '<main>', raw, flags=re.S)
    raw = re.sub(r'<div class="pager">.*?</div>', ' ', raw, flags=re.S)
    a = words(md_text(open(md_path).read(), drop_head=True, drop_h2=os.path.isdir(html_path)))
    b = words(visible_text(raw))
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    lost, added = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ('delete', 'replace') and i2 - i1 >= minrun:
            lost.append(' '.join(a[i1:i2]))
        if tag in ('insert', 'replace') and j2 - j1 >= minrun:
            added.append(' '.join(b[j1:j2]))
    print(f'слов в MD: {len(a)} · слов в HTML: {len(b)} · иллюстраций: {nfig}')
    print('скрипт страницы:', js_ok(parts[0]))
    print('страниц:', len(parts))
    if len(parts) > 1:
        heads = [v for k, v in parse(open(md_path).read()) if k == 'h2']
        pages = '\n'.join(open(f).read() for f in parts)
        lost_t = [h for h in heads if norm(h) not in norm(visible_text(pages))]
        print('заголовки глав на страницах: %d из %d' % (len(heads) - len(lost_t), len(heads)))
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
    os.makedirs(dst, exist_ok=True)
    pages = build_pages(open(src).read(), vis)
    for name, content in pages.items():
        open(os.path.join(dst, name), 'w').write(content)
    print('→ %s: %d страниц' % (dst, len(pages) - 1))
