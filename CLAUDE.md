# CLAUDE.md

## What this repository is

Not a software project. It is a set of **Russian-language study materials** preparing a child (10–11 y.o.)
for the Argentine math olympiad **Olimpíada Matemática Ñandú, Primer Nivel**. The "source code" is markdown
documents; the "data" is the corpus of original problem statements in `korpus/`.

**Layout.** Top level is the season (`25-26/`, `26-27/`, `27-28/`) — a season runs **late October to late
October**, by the Ñandú calendar: the national tour closes one and opens the next. Inside a season the unit is
the **whole course**, not the stage: `<season>/<course>/<stage>/files`. Outside the seasons: `korpus/` (raw
statements), `arhiv/` (superseded material), `tools/` (corpus download/extraction scripts, venv).
The repo map is `README.md`.

**Every path written in a document is relative to the repo root**, never to the containing file.

## Current focus — the national stage (Nacional, Primer Nivel)

Regional and provincial tours are **behind us** (20 and 27 Aug 2026). The live work is the **national branch**
in `25-26/nandu_level1/national/`, aimed at the **national tour, 20–23 Oct 2026** (a two-day tour inside that window;
holiday 26 Sep – 3 Oct, no sessions).

**Before writing or editing anything in `25-26/nandu_level1/national/`, read that folder's `README.md`** — it is the
branch registry: what exists, the cross-branch rituals Ч1–Ч5, terms already introduced (later pairs use them
without re-introducing), each pair's debts, the corpus-key errors and the pace decisions. Start any new
national topic from `nandu_n1_nacional_brief.md` (the reconnaissance brief: corpus classification 2013–2025,
regional→national delta, block plan).

What the branch holds today, in study order:

1. `nandu_n1_nacional_1_cifry_*` — остатки/делимость → числа/цифры. Introduces rituals **Ч1–Ч5**
   (Ч5 «полнота письменно» answers the national «Explica cómo las contaste» and is reused by every later pair).
   Pairs 3 and 4 stand on its remainders.
2. `nandu_n1_nacional_2_figury2_*` — сетка равных деталей; textbook + parent's key, no reshebnik.
3. `nandu_n1_nacional_3_doski2_*` — delta over the provincial `doski` pair; adds ritual **Д6 «сначала жанр ответа»**.
4. `nandu_n1_nacional_4_arifmetika2_*` — доли от неизвестных, процессы/циклы, целые решения и оптимизация.

Plus `nandu_n1_nacional_tipologia.md` (parent-facing determiner for the whole branch, incl. the two-day tour
order derived from the window data), the practice trio `nandu_n1_nacional_praktika{,_podskazki,_resheniya}.md`
(21 generated problems over 12 types, rebalanced by real frequency), and `resheniya/` — per-year battle keys
(2025 written).

⚠ **Corpus key `korpus/historico/Nacionales_N1.md` has three confirmed errors** — 2020 №5, 2021 №6
(that row also drops №3) and 2025 №6. Never quote the key without checking these: the corrected values, their
verification and the PDF figure corrections are in `25-26/nandu_level1/national/README.md`.

⚠ **There is no day-by-day plan for the national branch.** `nandu_n1_nacional_plan{,_short,_szhatyy}.md` were
written and then **deleted by the user (28 July 2026)** — dating the branch was judged premature. Do not
re-create them unasked. Branch debts: `resheniya/nandu_n1_nacional_resheniya_{2017,2024}.md` and a national
памятка (analogue of `25-26/nandu_level1/provincial/nandu_n1_provincial_pamyatka.md`, which must carry the branch's own phrase-book — see rule 11).

## Where everything else lives

- `25-26/nandu_level1/` — the whole Primer Nivel course of this season. `regional/` and `provincial/` hold the
  finished materials (linsys, perevod, figury, the счёт suite 1–5, the provincial doski pair, типологии,
  тренировка, per-year keys, памятка, `!!!_*.md` cheat sheets); `national/` is the branch above;
  `zonal/`, `obshchee/` (plans, observation sheet), `animacii/` (html visualisations).
  Detailed map: **`25-26/nandu_level1/README.md`**. The regional and provincial materials are the foundation
  the national pairs build on and reference — read there before touching them.
- `korpus/` — original statements. ⚠ Two different olympiads live here: **Ñandú = `omn_*`** (this course)
  and **OMA = `oma/`** (a separate, harder secundaria olympiad, no course material targets it).
  `korpus/2025/` is OMA, not Ñandú. Details in `README.md`.
- `26-27/{school5,school6,nandu_level2,tinkov}`, `27-28/{tinkov,school7,nandu_level3}` — later seasons, so a
  season's work never requires hopping between directories.
  Each has its own `README.md` — read it before writing there. Two standing prohibitions:
  the `tinkov/` folders are a **карман, not a schedule** (no dates, no ☐-days in any tracker), and
  **no briefs or roadmaps in `27-28/`** — either write the concrete pair or drop the idea.
- `arhiv/schet_v1/` — the superseded first счёт version; only its `session_prompt` is still live (hard rule 7).

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

## Hard rules when authoring or editing materials

These conventions are load-bearing across all existing pairs — keep them.

1. **The roadmap's problem bank is untouchable.** Real problems from the bank are reserved for the боевая фаза;
   never copy them (numbers or plots) into textbook examples or reshebnik problems.
2. Textbook examples must not duplicate reshebnik problems, and vice versa — neither in numbers nor in plot.
3. One chapter = one new technique; a problem block's difficulty comes only from that chapter's titular skill;
   tools only from already-covered chapters.
4. Every reshebnik answer must be computed and **independently re-verified** (e.g. brute-force enumeration vs.
   the technique). No unchecked answers. The user does not proofread — quality rests on verification done inside the work.
5. Language is Russian. **Real mathematical terminology is allowed and expected** (July 2026 decision, reversing the
   earlier ban): «сочетания», «размещения», «перестановки», «факториал», «остаток по модулю», «делимость», «инвариант»
   and the like are working vocabulary, not just 🔎 footnotes. The requirement is pedagogical, not lexical:
   introduce a term the first time it appears — name it, show it on the numbers of a concrete example, then use it freely.
   Do not retro-translate existing materials wholesale. **Systems of linear equations are named by their standard methods**
   (метод подстановки, метод сложения/вычитания = исключение неизвестной, приведение к треугольному виду);
   the nickname «вычти сценарий» was retired (Aug 2026) and purged. «Сценарий» stays legitimate only where it names a
   *situation in the statement* («если бы…»), i.e. at the translation stage, never as the name of a solving move.
6. Each textbook opens with «ритуалы» (standing habits) and each chapter includes typical mistakes; worked examples
   follow the step format of rule 8. Match the tone and structure of the existing pairs.
7. When adding a new topic pair, follow the staged workflow from
   `arhiv/schet_v1/nandu_n1_regional_schet_session_prompt.md`: research corpus → derive techniques from the corpus
   (not from textbooks) → propose chapter ladder + coverage map → **stop for approval** → write the pair;
   then update the plan/tracker files.
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
