#!/usr/bin/env python3
"""Tiny puzzle runner.

Layout per puzzle:
    YYYY/dayNN/
        description1.txt  puzzle description for part 1
        description2.txt  puzzle description for part 2 (add once part 2 is unlocked)
        example.txt       example input (example2.txt optionally overrides it for part 2)
        expected1.txt     expected example answer for part 1
        expected2.txt     expected example answer for part 2 (add once part 2 is unlocked)
        input.txt         real puzzle input
        solution.py       written by the agent: part1(text) and part2(text), each returning a number

Usage:
    python3 aoc.py new 2026 3    scaffold 2026/day03/ with empty puzzle files to fill in
    python3 aoc.py 2026 3        test both parts against the example, then solve input
    python3 aoc.py 2026 3 2      same, but only part 2
"""
import importlib.util
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

GREEN, RED, YELLOW, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[0m"


def day_dir(year: str, day: str) -> Path:
    return ROOT / year / f"day{int(day):02d}"


def read(path: Path) -> str | None:
    if not path.exists():
        return None
    # drop trailing blank (or whitespace-only) lines, but keep trailing spaces on the
    # last real line - some puzzles are column-aligned; an empty file counts as missing
    lines = path.read_text().splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines) or None


def load_solution(folder: Path):
    spec = importlib.util.spec_from_file_location(f"{folder.name}_solution", folder / "solution.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def timed(fn, text):
    start = time.perf_counter()
    result = fn(text)
    return result, time.perf_counter() - start


def run_part(folder: Path, module, part: int) -> bool:
    fn = getattr(module, f"part{part}", None)
    expected = read(folder / f"expected{part}.txt")
    example = read(folder / f"example{part}.txt") if part == 2 else None
    example = example if example is not None else read(folder / "example.txt")

    if fn is None or expected is None or example is None:
        print(f"{YELLOW}part {part}: skipped (missing part{part}, expected{part}.txt or example.txt){RESET}")
        return False

    try:
        got, dt = timed(fn, example)
    except NotImplementedError:
        print(f"{YELLOW}part {part}: not implemented{RESET}")
        return False
    if str(got) != expected.strip():
        print(f"{RED}part {part}: example FAIL  expected {expected.strip()}, got {got}{RESET}")
        return False
    print(f"{GREEN}part {part}: example ok    {got}  ({dt * 1000:.1f} ms){RESET}")

    puzzle = read(folder / "input.txt")
    if puzzle is None:
        print(f"{YELLOW}part {part}: no input.txt{RESET}")
        return False
    answer, dt = timed(fn, puzzle)
    print(f"part {part}: ANSWER        {answer}  ({dt * 1000:.1f} ms)")
    return True


def new(year: str, day: str) -> None:
    folder = day_dir(year, day)
    folder.mkdir(parents=True, exist_ok=True)
    files = ["description1.txt", "example.txt", "expected1.txt", "input.txt"]
    for name in files:
        (folder / name).touch()
    print(f"created {folder.relative_to(ROOT)}/ with {', '.join(files)}")


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[0] == "new" and argv[1].isdigit() and argv[2].isdigit():
        new(argv[1], argv[2])
        return 0
    if len(argv) not in (2, 3) or not all(a.isdigit() for a in argv):
        print(__doc__)
        return 1

    year, day = argv[:2]
    folder = day_dir(year, day)
    if not (folder / "solution.py").exists():
        print(f"{folder.relative_to(ROOT)}/solution.py not found - solve it with: /solve {year} {day}")
        return 1
    module = load_solution(folder)
    parts = [int(argv[2])] if len(argv) > 2 else [1, 2]
    ok = [run_part(folder, module, p) for p in parts]
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
