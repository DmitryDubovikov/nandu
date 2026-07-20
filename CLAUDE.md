# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Not a software project. It is a set of **Russian-language study materials** for preparing a child (10–11 y.o.) for the Argentine math olympiad **Olimpíada Matemática Ñandú, Nivel 1** (regional stage, previously zonal). The "source code" is markdown documents; the "data" is the corpus of original problem statements in `nandu_problemas/`.

## Layout and naming

Course files follow `nandu_n1_<stage>_<topic>_<kind>.md`, where stage is `regional`/`zonal`/`provincial` and kind is:

- `uchebnik` — textbook: theory, "rituals", chapters with worked examples in «что делаем | что получается» tables.
- `reshebnik` — problem book: one block of 6–8 problems per textbook chapter, answers in a separate section at the end.
- `roadmap` — ⚠ **deleted by the user (July 2026).** `nandu_n1_regional_roadmap.md` held the corpus map and the problem bank; it no longer exists. Real problems now come straight from `nandu_problemas/oma_regional/regional_<year>.md` (answers: `historico/Regionales_N1.md`; worked №3 by year: `nandu_n1_regional_schet_korpus_resheniya.md`). ⚠ The regional textbooks still contain dangling references to it — they are frozen and must not be edited. `nandu_n1_zonal_roadmap.md` survives and is unrelated.
- `plan` — day-by-day course tracker (checkbox per day); `plan_short` is its compact version. ⚠ **Both are superseded for scheduling by `nandu_n1_plan_2026.md`** — the dated schedule up to the 20 Aug 2026 provincial tour (and on to the 27 Aug regional). It carries a per-day file list and a «Пров.» flag marking material that prepares for provincial-only problems. The old `plan`/`plan_short` remain only as a reference for course composition.
- The **"счёт" (Type-3) suite is numbered 1–5 in first-use order**: `schet_1_atomy_uchebnik` (atoms textbook, ch. 1–4: list/tree, chain+row, group, distribution + the 2×2 matrix), `schet_2_reshebnik` (55 problems in 8 blocks + a 15-item diagnosis dictation), `schet_3_tablitsa` (fact tables «знать в лицо» + 5-minute daily warm-ups), `schet_4_sborka_uchebnik` (assembly textbook, ch. 5–8: stages/worlds, modifiers, bounded distributions, tiles/colorings + battle route), `schet_5_opredelitel` (4-step protocol + 9 worked walkthroughs; on day 33 the child hand-copies them, and the document goes to the exam).
- `schet_korpus_resheniya` — parent's answer key to the roadmap's Type-3 bank; outside the 1–5 numbering.
- The **provincial pair** `nandu_n1_provincial_doski_{uchebnik,reshebnik}` (days 37–44 of the plan) covers the provincial-stage gap: boards with sums, adjacency bans, row-by-row chains, holes-instead-of-pieces, worlds-of-bad when subtraction double-counts (ch. 5), islands on a strip (ch. 6) + three appendices (parity gatekeeper, growing patterns, working backwards — the last one is about problem №1, not boards). Builds on the счёт suite (rituals, «И/ИЛИ», лесенка, «минус»); its battle problems come from `nandu_problemas/oma_provincial/` (answer key: `historico/Provinciales_N1.md`; worked solutions for the 2022–2025 tours: `nandu_n1_provincial_korpus_resheniya.md`, a parent file like `schet_korpus_resheniya`).
- `combinatorics_v1/` — archived first version of the счёт materials (uchebnik, reshebnik, spravochnik, opredelitel, session_prompt); not used by the course.
- `nandu_n1_nacional_brief.md` — reconnaissance brief for the **national** stage: full classification of the 2013–2025 Primer Nivel corpus, regional→national delta, proposed new blocks (1d/1e, 2c, 3d/3e/3f) and the document plan. **Start here for any national-stage work.**

`nandu_problemas/` holds original statements per year as `<stage>_<year>.pdf` + extracted `.md` (subdirs: `oma_regional`, `oma_zonal`, `oma_nacional`, `oma_provincial`, `historico`, `2025`). The **provincial** stage sits between zonal and regional (in CABA it is called Metropolitano); `oma_provincial/README.md` documents variants, missing years, and where its answer key lives. ⚠ **`2025/` is NOT Ñandú**: all six `2025_*_N1.*` files are the senior **OMA** olympiad, downloaded by mistake; the real Ñandú 2025 statements for every stage live in the `historico/*_N1.md` compilations (section «Año 2025»).

Scraping/download artifacts: `download.sh` (gdown fetch of PDFs; needs `source venv/bin/activate` first), `oma_index.json`, `oma_page.html`, `enunciados.js`, `zonal_list.txt` — all derived from www.oma.org.ar. The `venv/` has PDF-extraction tooling (pypdf, pymupdf, pdfplumber) used via `python3` one-liners/scripts to turn PDFs into `.md`.

## Domain model

Every regional-stage paper has exactly 3 problems with the type fixed by position: №1 = Т1 (arithmetic/linear systems), №2 = Т2 (perimeter geometry from a lettered figure), №3 = Т3 (systematic counting). Types split into 8 blocks (1a–1c, 2a–2b, 3a–3c); their definitions lived in the now-deleted regional roadmap, and the block labels survive only as references inside the textbooks and `schet_korpus_resheniya`. Course sequence: СЛАУ → Перевод → Фигуры → Счёт → боевая фаза (working the real bank).

**Corpus finding on №1 techniques (July 2026 audit of ~68 Nivel-1 papers):** «вычти сценарий» (subtracting two near-twin equations) is THE dominant opening move of the regional №1 — 7 of 14 years 2012–2025, including **all five of 2021–2025** (2025 is literally the textbook's `x + y/2` shape); it also appears at zonal (1997, 2002, 2007, 2016, 2023). Drill it to automatism. «Сложи всё» in its pure circular form (`a+b, b+c, a+c` — build the total by adding all equations) has **zero hits** in the №1 Nivel-1 corpus across all stages (zonal 1996–2025, provincial 2000–2025, regional 2012–2025); only its second half (subtract an equation from a *given* total, e.g. zonal 2007, provincial 2025) occurs — and that is again «вычти». The pure circular shape exists in Ñandú but at Tercer Nivel (zonal 2025). So «сложи всё» is taught once as a bridge idea, not drilled. Provincial №1 is a different genre altogether: mostly working-backwards/process problems, almost never dense systems (covered by the doski appendix on working backwards).

## Hard rules when authoring or editing materials

These conventions are load-bearing across all existing pairs — keep them:

1. **The roadmap's problem bank is untouchable.** Real problems from the bank are reserved for the боевая фаза; never copy them (numbers or plots) into textbook examples or reshebnik problems.
2. Textbook examples must not duplicate reshebnik problems, and vice versa — neither in numbers nor in plot.
3. One chapter = one new technique; a problem block's difficulty comes only from that chapter's titular skill; tools only from already-covered chapters.
4. Every reshebnik answer must be computed and independently re-verified (e.g., brute-force enumeration vs. the technique). No unchecked answers.
5. Language is Russian; no formal terminology the child hasn't been given (e.g., in combinatorics no «сочетания/размещения/факториал» — everything through counting principles, case analysis, trees).
6. Each textbook opens with «ритуалы» (standing habits) and each chapter includes typical mistakes; worked examples use «что делаем | что получается» tables. Match the tone and structure of the existing linsys/perevod pairs.
7. When adding a new topic pair, follow the staged workflow from `combinatorics_v1/nandu_n1_regional_schet_session_prompt.md`: research corpus → derive techniques from the corpus (not from textbooks) → propose chapter ladder + coverage map → **stop for approval** → write the pair; then update the plan/tracker files.

## Progress tracking

`nandu_n1_plan_2026.md` is the source of truth for dates, pace and progress (printed on paper, ticked by hand). `nandu_n1_regional_plan.md` is the reference for course composition: ☐ → ✅ per completed day, ⚠ for blocks with ≥2 mistakes (repeated on day 44). Keep `plan_short.md` and the plan's material list in sync when materials change.
