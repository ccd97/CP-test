# AGENTS.md — Workspace Rules & Agent Guidelines

## 1. Project Overview & Core Purpose

**CP-test** is an automated testing and testcase generation tool for Competitive Programming.

### Key Capabilities
- **Testcase Generation**: Creates random inputs from declarative `.tcs` (testcase syntax) files.
- **Differential Testing**: Runs two solutions (e.g. optimized vs. brute-force) side-by-side to find edge-case failures.
- **Benchmarking**: Measures execution times (min, max, avg) across $N$ test cases to detect TLE.
- **Contest Packaging**: Generates zero-padded HackerRank-style `.zip` test bundles.

---

## 2. Available Skill: `testcase-syntax`

This repository includes a dedicated skill for authoring and debugging testcase syntax files:

- **Path**: [`skills/testcase-syntax/SKILL.md`](skills/testcase-syntax/SKILL.md)
- **When to Use**: Whenever converting problem statements into `.tcs` format, formulating test constraints, or troubleshooting syntax errors.
- **What It Covers**:
  - Full directive grammar: `int`, `rarray`, `drarray`, `flstring`, `rlstring`, `loop`.
  - Output formatting rules (semicolon for newline vs. space continuation).
  - Variable scoping and array indexing (`arr0`, `arr1`).
  - Common CP pattern recipes (multi-testcase loops, 2D grids, graphs, trees, queries, permutations).

---

## 3. Architecture & File Roles

- [`testcode.py`](testcode.py): CLI runner coordinating compilation, test generation, execution, diffing, and reporting.
- [`tcgen.py`](tcgen.py): Parser and generator engine for `.tcs` syntax files.
- [`executer.py`](executer.py): Preprocessor and runner (injects file-I/O into C, C++, Python and executes).
- [`utils.py`](utils.py): Comparison and formatting utilities (line-by-line diffs, statistics, ZIP packaging).
- [`configs/`](configs/): Configuration presets (`default.ini`, `hackerrank.ini`).
- [`TCSYNTAX.md`](TCSYNTAX.md): Reference doc for testcase syntax.

---

## 4. Essential CLI Commands

```bash
# Generate testcases only
python3 testcode.py -T <syntax.tcs> -N <count>

# Run single solution
python3 testcode.py -T <syntax.tcs> -I1 <solution.cpp|.c|.py> -N <count>

# Differential testing (Compare against brute-force)
python3 testcode.py -T <syntax.tcs> -I1 <optimal_code> -I2 <bruteforce_code> -N 50

# Export HackerRank contest package
python3 testcode.py -T <syntax.tcs> -I1 <model_solution.cpp> -C configs/hackerrank.ini -N 20
```

### CLI Parameters
| Flag | Description | Default |
| :--- | :--- | :--- |
| `-T` | Path to `.tcs` testcase syntax file (**Required**) | — |
| `-I1` | Path to primary code file (`.cpp`, `.c`, `.py`) | `None` |
| `-I2` | Path to secondary code / brute-force file | `None` |
| `-C` | Path to `.ini` config file | `configs/default.ini` |
| `-N` | Number of test runs to execute | `10` |

---

## 5. Agent Operating Guidelines

### When Testing CP Problems / Finding Bugs
1. **Analyze Constraints**: Extract input formats, types, and bounds from problem statement.
2. **Author `.tcs` File**: Consult the [`testcase-syntax`](skills/testcase-syntax/SKILL.md) skill to craft the `.tcs` file.
3. **Write Naive Solution**: Create a small, correct brute-force script (e.g. `brute.py`).
4. **Run Stress Test**: `python3 testcode.py -T <syntax.tcs> -I1 <solution> -I2 brute.py -N 50`.
5. **Diagnose Failures**: Inspect `intermediate/diff_result.tmp` on mismatches to find minimal failing cases.

### When Modifying the Codebase
1. **Language Compatibility**: Maintain support for C11, C++14, and Python 3.
2. **File I/O Regex**: Exercise care when modifying regex transformations in `executer.py`.
3. **Configurations**: Keep `configs/*.ini` synchronized with options parsed in `testcode.py`.
