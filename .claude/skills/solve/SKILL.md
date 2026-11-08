---
name: solve
description: Solve one part of a puzzle in YYYY/dayNN/ by writing its solution.py, verified with the aoc.py runner. Use when asked to solve a puzzle day, e.g. "/solve 2026 3".
argument-hint: <year> <day>
---

# Solve a puzzle

Arguments: `$ARGUMENTS` (year, then day). The puzzle folder is `<year>/dayNN/` (day padded to two digits), relative to the repo root that holds `aoc.py`.

## The rules

- **`solution.py` is the only file you create or edit.** Never touch descriptions, examples, expected values, inputs, `aoc.py`, `requirements.txt` or other days. If one of them looks wrong or is missing, stop and tell the user.
- **The runner is the only judge.** Check every change with `.venv/bin/python aoc.py <year> <day> [part]`, run from the repo root. Don't compute answers another way, and don't call a part solved unless the runner printed `example ok` and then `ANSWER` for it.
- Use the standard library plus whatever is in `requirements.txt`. Don't install anything.

## Folder contents

| File | Meaning |
|---|---|
| `description1.txt`, `description2.txt` | puzzle text for part 1 and part 2 |
| `example.txt` | example input, used for both parts |
| `example2.txt` | optional; replaces `example.txt` for part 2 |
| `expected1.txt`, `expected2.txt` | the example's answer for each part |
| `input.txt` | real input; read it only to learn its format or size |
| `solution.py` | yours; it doesn't exist before part 1 |

## Steps

1. **Pick the part.** Do part 2 if `description2.txt` and `expected2.txt` are both non-empty and `solution.py` already passes part 1. Otherwise do part 1. If the files that part needs are empty or missing, stop and say which ones.
2. **Read** that part's description, the example input and the expected value. For part 2, also read the existing `solution.py`.
3. **Write `solution.py`.** It must define the function `part1(text: str)` for part 1, or `part2(text: str)` for part 2, returning a number. `text` is the whole input file with `\n` line endings and with blank lines at the end removed, so the last line always has content. Do your own parsing, but don't `.strip()` the whole text or every line by reflex: leading and trailing spaces inside lines are kept on purpose, because some puzzles depend on column alignment. Blank lines in the middle (e.g. separating sections) are kept too. Rules for the file:
   - Nothing runs at import time: no file reads, no prints, no calls at module level.
   - For part 1, only define `part1`; the runner reports part 2 as skipped, and that's expected.
   - For part 2, add `part2` and keep `part1` working. Reuse part 1's code by refactoring it into shared helpers when that fits.
4. **Run** `.venv/bin/python aoc.py <year> <day> <part>`. If the example fails, work out why from the description, fix the code and run again. If the example passes but the real input is too slow, find a better algorithm; don't just add special cases for the example.
5. **Finish with a full run:** `.venv/bin/python aoc.py <year> <day>` with no part number. After part 2, both parts must show `example ok`.
6. **Report** the answer from the runner output and a short sentence on the approach.
