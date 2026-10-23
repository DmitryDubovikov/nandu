# CLAUDE.md

## What this repository is

Not a software project. It is a set of **Russian-language study materials** preparing a child
for the Argentine math olympiad **Olimpíada Matemática Ñandú** — Primer Nivel in season 25-26 (finished),
**Segundo Nivel in season 26-27 (the current target)**. The "source code" is markdown
documents; the "data" is the corpus of original problem statements in `korpus/`.

**Layout.** Top level is the season (`25-26/`, `26-27/`, `27-28/`) — a season runs **late October to late
October**, by the Ñandú calendar: the national tour closes one and opens the next. Inside a season the unit is
the **whole course**, not the stage: `<season>/<course>/<stage>/files`. Outside the seasons: `korpus/` (raw
statements), `arhiv/` (superseded material), `tools/` (corpus download/extraction scripts, venv).
The repo map is `README.md`.

**Every path written in a document is relative to the repo root**, never to the containing file.

## Current focus — Segundo Nivel, season 26-27

**Primer Nivel is over**: the national tour 20–23 Oct 2026 finished with its second day on 23 Oct 2026, and with
it season 25-26. **From now on the target is Ñandú Segundo Nivel** — the course `26-27/nandu_level2/`, aimed at the
2027 tours: Interescolar 7 May, Zonal 25 Jun, Provincial 19–21 Aug, Regional 27 Aug, **Nacional 20–23 Oct 2027**
(the 2026 calendar carried over — a user assumption, no official 2027 calendar yet).

The 2026 result was weak (about 1.5 problems a day), and the way the course is built changed with it
(23 Oct 2026). **Solutions come first, textbooks are derived from them** — this is hard rule 7, the only course-building
method in the repo:

1. **Model problems** — one real corpus problem per typology subtype, 17 in all: `26-27/nandu_level2/nandu_n2_obraztsy.md`
   (entry point: the models, their backups, solution status, corpus moves the models miss, the moves registry).
2. **Ideal solutions** — the parent and Claude solve each model and polish it until the parent accepts it as
   optimal; sources in `26-27/nandu_level2/idealnye_resheniya/`.
3. **Moves** — every move, notion and technique of an accepted solution goes into the registry (`nandu_n2_obraztsy.md`
   §3) under the name and notation it has in the solution.
4. **Textbooks** — written for exactly those moves, introduced and written the way the ideal solutions use them.
5. **Whole-corpus solutions** — last.

The model solutions are the parent's working material for writing textbooks — not the child's practice. Solving a
model does not take it out of the corpus.

**Before writing anything in `26-27/nandu_level2/`, read its `README.md`** (method, 2027 tours, what counts as learned
at level 1, the level-1 audit gaps) and `nandu_n2_obraztsy.md`. Inputs: per-stage typologies and corpora
`26-27/nandu_level2/{zonal,provincial,regional,national}/nandu_n2_*_{tipologia,korpus}.md`, summary
`nandu_n2_tipologia_svodnaya.md`. Segundo Nivel 2026 statements are not in the corpus yet — the user adds them when
the organisers publish them.

`arhiv/n2_v1/` holds the abandoned first level-2 approach (chapter ladders planned from the typology, textbooks
written before solutions, session prompts, pairs 1–3). **It is not an instruction**; its live parts were moved out.

## Primer Nivel, season 25-26 — finished

`25-26/nandu_level1/` is the whole Primer Nivel course: `regional/` and `provincial/` (linsys, perevod, figury,
the счёт suite 1–5, the doski pair, типологии, тренировка, per-year keys, памятка, `!!!_*.md` cheat sheets),
`national/` (pairs cifry, figury2, doski2, arifmetika2, tipologia, praktika trio, per-year battle keys; its own
`README.md` is the branch registry), `zonal/`, `obshchee/`, `animacii/`. Detailed map:
**`25-26/nandu_level1/README.md`**. It is now **reference and foundation** for level 2 — no new level-1 work unasked;
the national branch's open debts (keys 2017/2024, national памятка) are not pursued unless the user asks.

⚠ **Corpus key `korpus/historico/Nacionales_N1.md` has three confirmed errors** — 2020 №5, 2021 №6
(that row also drops №3) and 2025 №6. Never quote the key without checking these: the corrected values, their
verification and the PDF figure corrections are in `25-26/nandu_level1/national/README.md`.

## Where everything else lives

- `korpus/` — original statements. ⚠ Two different olympiads live here: **Ñandú = `omn_*`** (this course)
  and **OMA = `oma/`** (a separate, harder secundaria olympiad, no course material targets it).
  `korpus/2025/` is OMA, not Ñandú. Details in `README.md`.
- `26-27/{school5,school6,nandu_level2,tinkov}` — the current season (school tracks run alongside level 2 —
  `26-27/nandu_level2/rezhim_sezona.md`); `27-28/{tinkov,school7,nandu_level3}` — the next one. A season's work never
  requires hopping between directories.
  Each has its own `README.md` — read it before writing there. Two standing prohibitions:
  the `tinkov/` folders are a **карман, not a schedule** (no dates, no ☐-days in any tracker), and
  **no briefs or roadmaps in `27-28/`** — either write the concrete pair or drop the idea.
- `arhiv/` — superseded material, never an instruction: `schet_v1/` (first level-1 счёт version, incl. the old
  staged-workflow `session_prompt`), `n2_v1/` (first level-2 approach).

**No PDF builds, and nothing is printed at all.** `build_pdf.py` and the `/pdf` slash command were removed
(Aug 2026); since 29 Aug 2026 **all material is read from the screen** — paper is out of the workflow entirely.
Do not re-create the builds unasked, do not add print-build instructions to documents, and never argue against
a solution on print grounds (animation, colour, interactivity, GIF, page width are all fair game). The
printed-page-width wording in rule 10 stands only as a proxy for a narrow reading column.

## How to answer the user

**Кратко и структурированно.** Short answers, structure over prose: заголовки, списки, таблицы; вывод и
рекомендация впереди, обоснование одной строкой. Не разворачивать аргумент в абзацы, если хватает пункта.

## Domain model

Problem types are stable across stages and largely fixed by position:
**Т1** — arithmetic / linear systems, **Т2** — perimeter geometry from a lettered figure,
**Т3** — systematic counting, **Т4** — the national branch's own harder mixed genre.
At the regional stage each paper is exactly 3 problems with the type fixed by position (№1 = Т1, №2 = Т2, №3 = Т3);
the national paper has 6 over two days. Per-stage типологии hold the full breakdown:
`25-26/nandu_level1/national/nandu_n1_nacional_tipologia.md` and
`25-26/nandu_level1/provincial/nandu_n1_provincial_tipologia.md`.

**Segundo Nivel** keeps the positions on all four stages (№1 numbers, №2 lettered figure, №3 counting; national
№4–№6 repeat them) and adds **Т4** доски-головоломки (⚠ sits in slot №1/№4, where a text problem is expected),
**Т5** числа как предмет (делимость, остатки, инвариант), **Т6** графы — these live at the provincial and national
stages (zonal and regional see Т5 only as a tool). Geometry is **areas**, not perimeters. Stages are not ordered by
difficulty: the provincial needs Т4–Т6, the regional hardly any. Glossary and counts:
`26-27/nandu_level2/nandu_n2_tipologia_svodnaya.md`.

## Hard rules when authoring or editing materials

These conventions are load-bearing across all materials — keep them.

1. **Corpus problems are never copied into child material.** Real problems (numbers or plots) do not go into
   textbook examples or reshebnik problems — they stay unseen for the child's battle practice. The parent's ideal
   solutions of corpus problems (rule 7) are not child material and do not use them up.
2. Textbook examples must not duplicate reshebnik problems, and vice versa — neither in numbers nor in plot.
   **A reshebnik block is 3 problems** with distinct roles: the move in pure form · the move with a trap or in
   unfamiliar dress · the move in the corpus's battle format (2–3 questions, «explica», real difficulty). A fourth only
   when the move has a third genuinely different face. Tests: **дубль** — two problems solved by the same sequence of
   moves → drop the second, don't re-number it; **выпуклость** — solvable without the chapter's move → unfit.
   (User decision, July 2026.)
3. One chapter = one new move — a move taken from the ideal solutions' registry (rule 7); a problem block's difficulty
   comes only from that chapter's titular move; tools only from already-covered chapters. No «см. главу 5» in child
   text: every «делай так» is justified on the spot, on the numbers of the example.
4. Every answer must be computed and **independently re-verified**: a separate agent sees only the statement (no
   answer, no technique), solves it and, where possible, runs a brute-force program; a mismatch or an ambiguity
   complaint means the problem is rewritten, not patched in brackets. No unchecked answers. The user does not
   proofread — quality rests on verification done inside the work.
5. Language is Russian. **Real mathematical terminology is allowed and expected** (July 2026 decision, reversing the
   earlier ban): «сочетания», «размещения», «перестановки», «факториал», «остаток по модулю», «делимость», «инвариант»
   and the like are working vocabulary, not just 🔎 footnotes. The requirement is pedagogical, not lexical:
   introduce a term the first time it appears — name it, show it on the numbers of a concrete example, then use it freely.
   Do not retro-translate existing materials wholesale. **Systems of linear equations are named by their standard methods**
   (метод подстановки, метод сложения/вычитания = исключение неизвестной, приведение к треугольному виду);
   the nickname «вычти сценарий» was retired (Aug 2026) and purged. «Сценарий» stays legitimate only where it names a
   *situation in the statement* («если бы…»), i.e. at the translation stage, never as the name of a solving move.
6. Each textbook opens with «ритуалы» (standing habits) and each chapter includes typical mistakes; worked examples
   follow the step format of rule 8. A move is named and written exactly as in the ideal solution it came from.
7. **Solutions first, textbooks from them** (Oct 2026 — replaces the old «corpus → chapter ladder → textbook» workflow,
   now in `arhiv/`). A course is built in this order: (а) one model corpus problem per typology subtype;
   (б) an ideal solution of each, polished with the parent until accepted; (в) the registry of moves those solutions
   use; (г) textbooks covering exactly those moves, in the solutions' form and notation; (д) solutions of the whole
   corpus. No chapter is planned from the typology alone, and no textbook is written before its moves exist in
   accepted solutions. Level 2 runs it in `26-27/nandu_level2/nandu_n2_obraztsy.md`.
8. **Разборы and composite worked examples are iterative steps with несгораемые артефакты** (июль–авг 2026 decision).
   Structure: **шаг 1 — план**, ending with a `> ✅ **План готов:** Ответ = …` block — the answer expressed through
   subtasks. That artifact may be an algebraic combination of blocks («Ответ = Д × М»), a reduction
   («Ответ = все a, при которых …»), or, for the «какие значения возможны?» genre, **«оценка плюс пример»**.
   Then each subtask is its own bold «Шаг N — …» ending with its result (`→ **Д = 10**`); the last step is сборка —
   plugging the numbers into the plan's formula. **Every step opens with the goal, not the action**: not
   «делаю А, потому что Б» but «нужно Б — для этого делаю А» — the red thread must read from the goals alone.
   A «что делаем | что получается» table as the *skeleton* of a разбор is forbidden (wastes horizontal space,
   caps cell text, hides the thread); a mini-table or bullet list of «И»-factors is allowed only *inside* a step for
   ≥2 short uniform moves, preceded by a goal phrase. Deliberate wrong-way demos («как хочется сделать») may keep the
   old table look to stay visually distinct. Applies to new and edited разборы; don't retro-rewrite untouched documents unasked.
   **After the plan, steps are the plan's parts** (сент 2026): each step is named after a term of the artifact
   («Шаг 2 — все пары для короткого столбца»), an auxiliary fact is computed inside the step that needs it, the plan
   uses only what is already known (no numbers or objects from later steps, no «это проверит шаг 4»), and a plan with
   «+ …» is rewritten concretely once the cases are listed (`> ✅ **План уточнён:** …`). A world in `N(…)` carries its
   defining condition: `N(короткий = {6, 9})`. Model: `25-26/nandu_level1/national/boevye_resheniya/_md/parts/2025_3.md`.
   **Составной операнд получает свой план** (окт 2026). The point of the whole format: a hard problem = a formula
   over simple ones, and every step computes one operand of a formula *already on screen*. This must hold at every
   level, not only the top. When an operand is itself composite (a world with its own перебор and расстановка),
   the step computing it opens with its own artifact — `> ✅ **План мира:** N(a₄ = 1) = цена первого набора + …` —
   inside that step, not in шаг 1 (the plan still sees only the first развилка). The first such operand builds the
   sub-plan on its own numbers; sibling operands reuse it. Defects: (а) a step that computes no operand of a visible
   formula — «подготовка для всех миров сразу», a general formula with a new letter («цена = k · 2 · (4 − k)») before
   the first world: the fact moves into the first operand that needs it; (б) an invented object that never stands in
   a formula — drop it (5–7 names per problem is already too many); (в) an observation that cuts the problem
   («центр ловит все крупные окна») surfacing mid-solution — put it before шаг 1 and let it shape the plan.
   Evidence: 2021 №6, 2023 №3, 2024 №1 were too heavy for the child even to read, while 2022 №1/№3 of the same length
   (flat plans) went fine. Models: those three `parts/` files after the Oct 2026 rewrite.
9. **Наблюдение, на котором держится приём, называется отдельно** (авг 2026). If a разбор works because of a specific
   property of the problem (в таблице 2×2 любые две клетки лежат в общей строке или столбце; расстановка одинаковых
   фишек = выбор дырок; островок одноцветный; условие связывает только соседние строки; одиночка тянет за собой
   неразличимую пару), that property gets its own **«Заметь главное»** paragraph — before шаг 1, or before the step
   where it first does its work — and is not dissolved into the mechanics of a step. The paragraph answers
   «почему так вообще можно», the steps answer «как считать».
10. **Формулы не стоят внутри абзаца** (авг 2026). A formula inside a text line wraps across the line break and has to
    be read in pieces from two rows — unreadable in print. Put on **its own paragraph**: any expression containing letters,
    and any chain longer than a single operation. Only a one-operation numeric fact (`3 + 5 = 8`) and a value assignment
    (`О = 9`) may stay inline. One formula per line. Applies to all text; a formula that only looks fine because
    the screen is wide is still a defect — check it at printed-page width.
11. **У боевой записи есть фраза-объяснение** (авг 2026). The child solves fast enough to write the maths but not prose,
    and a bare calculation loses the explanation point — Ñandú pays for «Explica cómo las contaste».
    So **every non-trivial problem whose material carries a «что пишешь / что достаточно написать на туре»-style record
    gets a `#### 💬 Фраза-объяснение (в начале)`**: one or two sentences written *before* the calculations —
    Spanish in bold, Russian translation in italics below. Counting and enumeration problems get a second
    `#### 💬 Фраза в конце — полнота` after the answer. The rest of the record goes under `#### Запись`, and the
    paragraph in the разбор the phrase is drawn from is tagged with an italic `💬` line.
    - **Content:** the phrase carries **«почему так вообще можно считать»** — the load-bearing observation of rule 9
      («случаи не пересекаются», «общая сторона ушла внутрь», «конец известен точно»). A phrase that retells the
      arithmetic already visible in the record is a defect.
    - **Perimeters (Т2) get none — deliberate user decision.** There the record speaks for itself.
    - **The phrases are instances of one closed phrase-book, not per-problem texts.** Thirty separate texts are thirty
      memorised strings; a dozen constructions transfer to an unseen problem. The provincial book lives in
      `25-26/nandu_level1/provincial/nandu_n1_provincial_pamyatka.md`, section «💬 Что писать словами». New material reuses those wordings verbatim
      where the приём matches, and only extends the book when the приём is genuinely new — extending it is a book edit,
      not a local one. **The national branch has no phrases yet**: it gets its own phrase-book section in the national
      памятка, seeded from the provincial one, before phrases are added to national material.
    - **Budget ≈180 Spanish characters** (two handwritten lines), simple rioplatense at 10–11-year-old level.
    - **Verification by rule 4's standard**, plus: the claim is *true*, it carries justification rather than arithmetic,
      the Spanish is natural, it fits the budget. The first pass caught three false phrases — not a formality.
    - `grep -rn 💬` lists the whole layer.
12. **Every tour gets a wide corpus sweep** (Aug 2026). Deep preparation stays on the target stage and the recent
    years — that is where ~99% of the effort belongs. On top of it, before each tour, write
    `<stage>/nandu_n<N>_<stage>_chego_ne_bylo.md`: the types that occur in the corpus **at or below the target stage,
    over all years** and that the preparation does not cover — each as a name, one real example, and the single move
    it turns on. The goal is recognition, not skill; the length is what the child will read in one sitting.

13. **У разобранного примера постановка — отдельный ограниченный блок** (сент 2026). Пример открывается блоком
    `**Задача.**` (в документах с решениями — `**Условие.**`), и внутри него стоит только «что дано» и «на какой
    вопрос отвечаем»; кончается блок этим вопросом. Прикидки, мотивирующие вычисления и гипотезы идут **после**
    блока: пока вопрос не назван, ребёнок читает арифметику, не понимая, ради чего она (замечание пользователя по
    главе 6 пары `cifry`: «просто случайным образом пошли какие-то вычисления, а ради чего вообще непонятно»).
    Условие не разрывается картинкой или столбиком — иллюстрация встаёт **под** блоком, а не между условием и
    вопросом. Разбор отвечает ровно на поставленный вопрос: если в постановке две половины («на что делится **и**
    от каких цифр зависит»), обе стоят и в цели шага 1, и в конце. Последняя строка примера — **«Ответ на задачу»**,
    отвечающая именно на вопрос постановки, а не просто последняя формула разбора. В HTML блок рисуется рамкой
    (класс `.task`; конвертер ловит абзацы `**Задача.**` и `**Условие.**`).

14. **Цель шага берётся из плана или из структуры записи, а не выдумывается задним числом** (сент 2026).
    Правило 8 требует, чтобы шаг открывался целью. Но цель законна только если она **уже названа**: стоит в блоке
    `> ✅ **План готов:** Ответ = …` шага 1, спрошена в самом условии или поставлена в предыдущем шаге. Заголовок
    вида «Шаг 2 — нужны w, g и косая d», когда план требовал все буквы разом, — телега впереди лошади: порядок на
    деле диктует **структура уравнений** («в (5) и (6) стоит один и тот же хвост g + d»), а не потребность, видная
    лишь тому, кто уже знает ответ. Так же дефектно «нужно» вокруг средства: «нужно второе уравнение», «нужно
    укоротить перебор», «нужна карта позиций». Замечание пользователя: «Ты всегда заглядываешь в будущее и потом
    приписываешь нам потребность в X. С какой стати он нам нужен? Мы замечаем вещи внутри уравнений и потом из них
    выводим x и v — сама структура уравнений подсказывает, что искать».
    - **Чинится так:** заголовок = наблюдение, которое делает шаг возможным; тело шага = что из наблюдения вышло.
      «Шаг 5 — нужны a и c по отдельности» → «Шаг 5 — в третьем данном контуре стоит a, но не стоит c».
    - **Законно и трогать не надо**, когда величина названа в плане («Ответ = Д × М» → «Шаг 2 — нужно М»), спрошена
      в условии или когда план сам задал порядок («c, v, s, а затем стороны треугольника»).
    - Весь слой виден по `grep -rn "Шаг [0-9] — нуж"` (форма «нужен» прежним шаблоном не ловилась). Сплошная чистка
      прошла в сент. 2026; хук `tools/pre-commit.sh` тормозит новые такие заголовки.

15. **Анимация — только там, где показывает ход** (сент 2026). Материал читается с экрана (см. выше), движение
    доступно всегда — и именно поэтому его надо держать в узде. Анимируется **переход**: как отрезок переезжает на
    другое место, как змейка обходит контур, как случай ветвится. **Рисунок условия рисуется сразу и статично**: на
    туре ребёнок видит готовый чертёж, и прорисовка «по разрезам» только заставляет ждать. Замечание пользователя:
    «Это только заставляет ждать и смотреть на картинку, пока картинка прорисуется. Добавляй анимацию только там,
    где она хоть что-то поясняет, а не везде, куда только можно». Перед тем как анимировать элемент — назвать
    вслух, какую мысль показывает именно движение; не назвал — статика. В сборке за это отвечает класс `fx` на
    `<figure>` (без него иллюстрация статична) и классы `dr` / `fi` / `sl` внутри SVG; у анимированной фигуры
    появляется кнопка «↻ ещё раз».
