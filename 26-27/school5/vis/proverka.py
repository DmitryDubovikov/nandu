#!/usr/bin/env python3
"""Проверка HTML-учебника 5 класса перед показом родителю.

Собирает учебник с его .vis.json, прогоняет сверку текста (md2html --check: потеряно / дописано = 0)
и ловит рисунки, не нашедшие свой абзац. С --kadry снимает headless Chrome кадры анимаций
(1.5, 3.5, 5.5 с и конец) каждой главы или одной главы (--glava N) — их смотреть глазами.

Запуск: python3 26-27/school5/vis/proverka.py <учебник.md> [--glava N] [--kadry]
Кадры: 26-27/school5/vis/kadry/<учебник>/glava_N_<t>.png
"""
import glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CONV = os.path.join(ROOT, 'tools', 'md2html.py')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


def main():
    md = os.path.abspath(sys.argv[1])
    name = os.path.basename(md)[:-3]
    out = os.path.join(os.path.dirname(md), name)
    vis = md[:-3] + '.vis.json'
    glava = int(sys.argv[sys.argv.index('--glava') + 1]) if '--glava' in sys.argv else None
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
    if r.returncode:
        bad += 1
        print('✗ сверка текста:', r.stderr.strip())

    pages = sorted(glob.glob(os.path.join(out, '*.html')))
    pages = [p for p in pages if not p.endswith('index.html')]
    if os.path.exists(vis):
        allpages = ''.join(open(p).read() for p in pages)
        for anchor, f in json.load(open(vis)).items():
            if f[:80] not in allpages:
                bad += 1
                print(f'✗ рисунок не встал: якорь «{anchor}»')

    for p in pages:
        h = open(p).read()
        m = re.search(r'-glava-(\d+)-', os.path.basename(p))
        n = int(m.group(1)) if m else None
        nfig, nfx = h.count('<figure'), h.count('<figure class="fx"')
        print(f'{os.path.basename(p)}: рисунков {nfig}, анимаций {nfx}')
        ids = re.findall(r"<marker id='([^']+)'", h)
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            bad += 1
            print(f'✗ {os.path.basename(p)}: id маркеров повторяются на странице: {sorted(dup)}')
        if '--kadry' not in sys.argv or (glava is not None and n != glava):
            continue
        fx = re.findall(r'<figure class="fx">.*?</figure>', h, re.S)
        if not fx:
            continue
        style = re.search(r'<style>.*?</style>', h, re.S).group(0)
        kd = os.path.join(HERE, 'kadry', name)
        os.makedirs(kd, exist_ok=True)
        tag = f'glava_{n}' if n is not None else os.path.basename(p)[:-5]
        for tt in (1.5, 3.5, 5.5, 30):
            js = ("<script>document.querySelectorAll('figure.fx').forEach(f=>f.classList.add('seen'));"
                  "requestAnimationFrame(()=>requestAnimationFrame(()=>{document.getAnimations()"
                  f".forEach(a=>{{a.pause();a.currentTime={int(tt*1000)};}});}}));</script>")
            f = os.path.join(kd, f'{tag}_{tt}.html')
            open(f, 'w').write('<!doctype html><html class="anim"><head><meta charset="utf-8">' + style
                               + '</head><body style="background:#0d1117"><main style="max-width:720px;padding:20px">'
                               + ''.join(fx) + '</main>' + js + '</body></html>')
            png = f[:-5] + '.png'
            subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                            f'--user-data-dir={os.path.join(kd, ".chrome")}', '--window-size=760,3000',
                            '--virtual-time-budget=3000', f'--screenshot={png}', 'file://' + f],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.remove(f)
            print('кадр:', os.path.relpath(png, ROOT))

    print('ошибок нет' if not bad else f'ошибок: {bad}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
