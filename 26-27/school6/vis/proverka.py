#!/usr/bin/env python3
"""Проверка HTML-учебника 6 класса перед сдачей.

1. Собирает учебник с его .vis.json и прогоняет сверку текста (md2html --check: потеряно / дописано = 0).
2. Ловит рисунки без якоря, рисунки, не вставшие на страницу, повторы id маркеров, ASCII-блоки без замены.
3. На узкой ширине (400 px) ищет вылезание: страница шире экрана, рисунок/формула/карточка шире колонки
   (таблица в обёртке .tw прокручивается вбок сама — это не ошибка).
4. С --kadry снимает headless Chrome:
   стр/<глава>_d<k>.png  — страница целиком на десктопе 1440 px, срезами по 1500 px, анимации доиграны;
   фиг/<глава>_<n>_400.png — каждый рисунок главы на ширине телефона, доигранный;
   анм/<глава>_<n>_start.png / _end.png — анимированный рисунок в начале и в конце.
   Всё это смотреть глазами (Read по картинке).

Запуск: python3 26-27/school6/vis/proverka.py <учебник.md> [--str NN] [--kadry]
--str NN — только страница NN-…html (номер страницы, не главы: страница 01 — ритуалы).
Кадры: 26-27/school6/vis/kadry/<учебник>/{стр,фиг,анм}/
"""
import glob, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CONV = os.path.join(ROOT, 'tools', 'md2html.py')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
# временные страницы и профиль Chrome — вне папки сборки (она в git) и свои у каждого запуска:
# семь пар проверяются параллельно, общие имена перепутали бы кадры
TMP = os.path.join(HERE, 'kadry', '.tmp', str(os.getpid()))
os.makedirs(TMP, exist_ok=True)

# доиграть всё: проявление текста, анимации рисунков; потом прокрутить к Y
FINISH = ("<script>(function(){var r=document.documentElement;r.classList.add('anim');"
          "var m=document.querySelector('main');if(m)m.style.paddingBottom='40px';"
          "document.querySelectorAll('.st,figure.fx').forEach(function(e){e.classList.add('seen');});"
          "setTimeout(function(){document.getAnimations().forEach(function(a){try{a.finish();}catch(e){}});"
          "%s},200);})();</script>")

OVERFLOW = ("var W=document.documentElement.clientWidth,bad=[];"
            "if(document.documentElement.scrollWidth>W+1)bad.push('страница шире экрана: '+document.documentElement.scrollWidth+' > '+W);"
            "document.querySelectorAll('main figure, main svg, main table, main .frm, main pre:not([hidden]), main .card, main img')"
            ".forEach(function(e){if(e.closest('.tw'))return;var b=e.getBoundingClientRect();if(b.width&&(b.right>W+1||b.left<-1))"
            "bad.push(e.tagName.toLowerCase()+(e.className&&e.className.baseVal===undefined?'.'+e.className:'')+"
            "' вылезает: '+Math.round(b.left)+'…'+Math.round(b.right)+' при ширине '+W+' — '+"
            "(e.textContent||'').trim().slice(0,60));});"
            "var o=document.createElement('pre');o.id='__ovf';o.textContent=JSON.stringify({h:document.documentElement.scrollHeight,bad:bad});"
            "document.body.appendChild(o);")


def chrome(url, w, h, png=None, dump=False, scale=1):
    args = [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
            f'--window-size={w},{h}', f'--force-device-scale-factor={scale}',
            f'--user-data-dir={os.path.join(TMP, "chrome")}', '--virtual-time-budget=5000']
    args += ['--dump-dom'] if dump else [f'--screenshot={png}']
    r = subprocess.run(args + [url], capture_output=True, text=True)
    return r.stdout


def phone(inner, w=400, h=900):
    """Окно Chrome уже ~500 px не бывает — телефон изображает iframe шириной w (его медиазапросы видят w)."""
    return ('<!doctype html><html><body style="margin:0;background:#000">'
            f'<iframe id="__f" src="file://{inner}" scrolling="no" style="width:{w}px;height:{h}px;border:0;display:block"></iframe>'
            '<script>document.getElementById("__f").onload=function(){var fr=this;setTimeout(function(){'
            'try{var o=fr.contentDocument.getElementById("__ovf");if(o){var c=document.createElement("pre");'
            'c.id="__ovf";c.textContent=o.textContent;document.body.appendChild(c);}}catch(e){}},1500);};</script>'
            '</body></html>')


def probe(page, w):
    """Высота страницы и список вылезаний при ширине w (узкая ширина — через iframe)."""
    tmp = os.path.join(TMP, f'__probe{w}.html')
    h = open(page).read().replace('</body>', FINISH % OVERFLOW + '</body>')
    open(tmp, 'w').write(h)
    if w < 600:
        wrap = os.path.join(TMP, '__phone.html')
        open(wrap, 'w').write(phone(tmp, w))
        out = chrome('file://' + wrap, 700, 900, dump=True)
        os.remove(wrap)
    else:
        out = chrome('file://' + tmp, w, 900, dump=True)
    os.remove(tmp)
    m = re.search(r'<pre id="__ovf">(.*?)</pre>', out, re.S)
    if not m:
        return 0, ['не удалось измерить страницу']
    import html as H
    d = json.loads(H.unescape(m.group(1)))
    return d['h'], d['bad']


def iso_page(style, figs, w):
    return ('<!doctype html><html class="anim"><head><meta charset="utf-8">' + style
            + '</head><body style="background:#0d1117"><div class="wrap single"><main style="max-width:%dpx;padding:16px">'
            % w + ''.join(figs) + '</main></div>')


def main():
    md = os.path.abspath(sys.argv[1])
    name = os.path.basename(md)[:-3]
    out = os.path.join(os.path.dirname(md), name)
    vis = md[:-3] + '.vis.json'
    glava = int(sys.argv[sys.argv.index('--str') + 1]) if '--str' in sys.argv else None   # номер страницы NN-…html
    kadry = '--kadry' in sys.argv
    bad = 0

    args = [sys.executable, CONV, md, out] + ([vis] if os.path.exists(vis) else [])
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stdout + r.stderr)
    if 'без якоря' in r.stderr:
        bad += 1
        print('✗', r.stderr.strip())
    r = subprocess.run([sys.executable, CONV, '--check', md, out], capture_output=True, text=True)
    print(r.stdout.strip())
    if '✗ заголовок' in r.stdout:
        bad += 1
    if r.returncode:
        bad += 1
        print('✗ сверка текста:', r.stderr.strip())

    pages = sorted(p for p in glob.glob(os.path.join(out, '*.html')) if not p.endswith('index.html'))
    allpages = ''.join(open(p).read() for p in pages)
    if os.path.exists(vis):
        for anchor, f in json.load(open(vis)).items():
            if f[:80] not in allpages:
                bad += 1
                print(f'✗ рисунок не встал: якорь «{anchor}»')

    kd = os.path.join(HERE, 'kadry', name)
    if kadry:
        for sub in ('стр', 'фиг', 'анм'):
            d = os.path.join(kd, sub)
            if glava is None and os.path.isdir(d):
                shutil.rmtree(d)
            os.makedirs(d, exist_ok=True)

    tot_f = tot_a = 0
    for p in pages:
        base = os.path.basename(p)
        h = open(p).read()
        m = re.match(r'(\d+)-', base)
        n = int(m.group(1)) if m else None
        figs = re.findall(r'<figure[ >].*?</figure>', h, re.S)
        nfx = sum(1 for f in figs if re.match(r'<figure class="[^"]*\bfx\b', f))
        tot_f += len(figs)
        tot_a += nfx
        nasc = len(re.findall(r'<pre class="ascii st">', h))
        print(f'{base}: рисунков {len(figs)}, анимаций {nfx}' + (f', ASCII-блоков без замены {nasc}' if nasc else ''))
        ids = re.findall(r"<marker id='([^']+)'", h) + re.findall(r'<marker id="([^"]+)"', h)
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            bad += 1
            print(f'  ✗ id маркеров повторяются на странице: {sorted(dup)}')
        if glava is not None and n != glava:
            continue
        height, ovf = probe(p, 400)
        for o in ovf:
            bad += 1
            print('  ✗ 400 px:', o)
        if not kadry:
            continue
        tag = base[:-5][:40]
        # 1) страница целиком на десктопе, срезами
        hd, _ = probe(p, 1440)
        step = 1500
        for k, y in enumerate(range(0, max(hd - 60, 1), step)):
            tmp = os.path.join(TMP, '__shot.html')
            open(tmp, 'w').write(h.replace('</body>', FINISH % f"document.querySelector('.wrap').style.marginTop='-{y}px';" + '</body>'))
            chrome('file://' + tmp, 1440, step, os.path.join(kd, 'стр', f'{tag}_d{k + 1}.png'))
            os.remove(tmp)
        style = re.search(r'<style>.*?</style>', h, re.S).group(0)
        # 2) каждый рисунок на ширине телефона, доигранный: страница-рисунок внутри iframe 400 px
        for i, f in enumerate(figs, 1):
            tmp = os.path.join(TMP, '__f.html')
            wrap = os.path.join(TMP, '__w.html')
            open(tmp, 'w').write(iso_page(style, [f], 400).replace('max-width:400px;padding:16px', 'padding:16px')
                                 + FINISH % '' + '</body></html>')
            open(wrap, 'w').write(phone(tmp))
            chrome('file://' + wrap, 600, 900, os.path.join(kd, 'фиг', f'{tag}_{i}_400.png'))
            os.remove(tmp)
            os.remove(wrap)
        # 3) анимации: начало и конец
        for i, f in enumerate(figs, 1):
            if not re.match(r'<figure class="[^"]*\bfx\b', f):
                continue
            for when, js in (('start', ''), ('end', FINISH % '')):
                tmp = os.path.join(TMP, '__a.html')
                open(tmp, 'w').write(iso_page(style, [f], 760) + js + '</body></html>')
                chrome('file://' + tmp, 800, 900, os.path.join(kd, 'анм', f'{tag}_{i}_{when}.png'))
                os.remove(tmp)
    print(f'итого: рисунков {tot_f}, анимаций {tot_a}')
    if kadry:
        print('кадры:', os.path.relpath(kd, ROOT))
    shutil.rmtree(TMP, ignore_errors=True)
    print('ошибок нет' if not bad else f'ошибок: {bad}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
