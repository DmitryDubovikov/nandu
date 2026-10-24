#!/usr/bin/env python3
"""Проверка главы учебника комбинаторики перед показом родителю (роадмап §4, п. 5).

Ловит дефекты, найденные родителем в главах 1–2:
  - отсылки и мета-комментарии, персонажи образца (Беня);
  - абзац из нескольких мыслей (одна мысль — один абзац);
  - рамка «Задача.», которая кончается не вопросом;
  - нумерованный список, где номера не идут 1, 2, 3, …;
  - рисунок из .vis.json, не нашедший свой абзац.
С --kadry снимает headless Chrome кадры анимаций (1.5, 3.5, 5.5 с и конец) — их смотреть глазами.

Запуск: python3 26-27/nandu_level2/kombinatorika/vis/proverka.py <N> <папка для HTML> [--kadry]
"""
import glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
MD = os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.md')
VIS = os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.vis.json')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

ZAPRET = (r'как в примере|в примере [0-9]|примера [0-9]|пока нечего|не помещается|Идея главы|'
          r'что здесь произошло|\(Р[1-4]\)|Бен[яиюе]\b')


def chapter(md, n):
    m = re.search(rf'^## Глава {n}\..*?(?=^## Глава |\Z)', md, re.S | re.M)
    if not m:
        sys.exit(f'нет главы {n}')
    start = md[:m.start()].count('\n') + 1
    return m.group(0), start


def main():
    n, out = int(sys.argv[1]), sys.argv[2]
    md = open(MD).read()
    text, start = chapter(md, n)
    lines = text.split('\n')
    bad = 0

    def err(msg):
        nonlocal bad
        bad += 1
        print('✗', msg)

    for i, ln in enumerate(lines):
        if re.search(ZAPRET, ln):
            err(f'стр. {start+i}: отсылка / персонаж образца: {ln.strip()[:90]}')

    # абзац из нескольких мыслей: обычный абзац, где после точки начинается новое предложение
    para, p0 = [], 0
    for i, ln in enumerate(lines + ['']):
        if ln.strip():
            if not para:
                p0 = i
            para.append(ln.strip())
            continue
        if para and not re.match(r'^(#|\||- |\d+\. |>|:::|<|```)', para[0]):
            s = ' '.join(para)
            s = re.sub(r'\*\*[^*]+\*\*', '', s)          # жирный ярлык «**Почему …**» — не предложение
            if re.search(r'[.!?] [А-ЯЁA-Z«]', s):
                err(f'стр. {start+p0}: в абзаце больше одной мысли: {s[:90]}…')
        para = []

    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'md2html.py'), MD, out, VIS],
                   check=True, stdout=subprocess.DEVNULL)
    pages = glob.glob(os.path.join(out, f'*-glava-{n}-*.html'))
    if not pages:
        sys.exit(f'нет страницы главы {n} в {out}')
    page = pages[0]
    h = open(page).read()

    for m in re.finditer(r'<div class="card task st">(.*?)</div>\s*(?=<)', h, re.S):
        tail = re.sub(r'<[^>]+>', ' ', m.group(1)).strip()
        if not tail.endswith('?'):
            err(f'рамка «Задача.» кончается не вопросом: …{" ".join(tail.split())[-80:]}')

    for m in re.finditer(r'<ol class="st num">(.*?)</ol>', h, re.S):
        nums = re.findall(r'class="lin">(\d+)\.<', m.group(1))
        if nums != [str(k) for k in range(1, len(nums) + 1)]:
            err(f'нумерованный список: номера {nums}')

    vis = json.load(open(VIS))
    allpages = ''.join(open(p).read() for p in glob.glob(os.path.join(out, '*.html')))
    for anchor, fig in vis.items():
        if fig[:80] not in allpages:
            err(f'рисунок не встал: якорь «{anchor}» не найден ни в одном абзаце')

    figs, anim = h.count('<figure'), h.count('<figure class="fx"')
    print(f'глава {n}: рисунков {figs}, из них анимаций {anim} · {os.path.relpath(page)}')

    if '--kadry' in sys.argv:
        style = re.search(r'<style>.*?</style>', h, re.S).group(0)
        fx = re.findall(r'<figure class="fx">.*?</figure>', h, re.S)
        for t in (1.5, 3.5, 5.5, 30):
            js = ("<script>document.querySelectorAll('figure.fx').forEach(f=>f.classList.add('seen'));"
                  "requestAnimationFrame(()=>requestAnimationFrame(()=>{document.getAnimations()"
                  f".forEach(a=>{{a.pause();a.currentTime={int(t*1000)};}});}}));</script>")
            f = os.path.join(out, f'kadr_{t}.html')
            open(f, 'w').write('<!doctype html><html class="anim"><head><meta charset="utf-8">' + style
                               + '</head><body style="background:#0d1117"><main style="max-width:720px;padding:20px">'
                               + ''.join(fx) + '</main>' + js + '</body></html>')
            png = f[:-5] + '.png'
            subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                            f'--user-data-dir={os.path.join(out, ".chrome")}', '--window-size=760,2400',
                            '--virtual-time-budget=3000', f'--screenshot={png}', 'file://' + f],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('кадр:', png)

    print('ошибок нет' if not bad else f'ошибок: {bad}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
