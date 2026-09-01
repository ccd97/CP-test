---
name: testcase-syntax
description: >-
  Converts any competitive programming problem description (Codeforces, LeetCode,
  CodeChef, AtCoder, HackerRank) into an exact, runnable .tcs (testcase syntax) file for CP-test.
  Use whenever given a problem statement, input specification, or constraints.
---

# Problem Statement to `.tcs` Conversion Skill

This skill teaches agents how to parse any competitive programming problem statement, extract its input structure and constraints, and generate a 100% valid `.tcs` testcase syntax file.

---

## 🎯 Extraction & Conversion Protocol

When given a problem description:

### 1. Locate and Focus on the "Input" and "Example" Sections
Ignore the story, backstory, problem mechanics, and output details. Extract only:
- **Testcase Header**: Does it say `"The first line contains $t$ (the number of test cases)..."`?
- **Per-Testcase Lines**: What is on Line 1? Line 2? Line 3?
- **Variable Constraints**: What are the min/max bounds for each variable?
- **Layout & Spacing**: Which tokens are on the same line (space-separated) vs on separate lines (newlines)?

---

### 2. Map Problem Input to `.tcs` Directives

| Problem Input Pattern | Example Problem Description | Translated `.tcs` Statement |
| :--- | :--- | :--- |
| **Number of testcases** | `t (1 <= t <= 500)` | `int t 1 500;` followed by `loop lp t` |
| **Single integer on a line** | `n (1 <= n <= 100)` | `int n 1 100;` |
| **Multiple ints on same line** | `n and m (1 <= n, m <= 50)` | `int n 1 50`<br>`int m 1 50;` *(no `;` on first)* |
| **Array of $n$ integers** | `n integers a1, a2, ..., an (1 <= ai <= 10^9)` | `rarray_n a 1 1000000000;` |
| **Distinct array / Permutation** | `permutation p of length n (1 <= pi <= n)` | `drarray_n p 1 n;` |
| **String of length $n$** | `string s of length n consisting of lowercase` | `flstring_n s l;` |
| **Binary string of length $n$** | `binary string s of length n` | `flstring_n s ? 01;` |
| **$n$ rows of $m$ integers (Grid)** | `n lines each containing m integers` | `loop rowlp n`<br>`    rarray_m row 0 1000;` |
| **$m$ graph edges** | `m lines each with u, v (1 <= u, v <= n)` | `loop edgelp m`<br>`    int u 1 n`<br>`    int v 1 n;` |
| **$q$ queries** | `q queries: type, l, r` | `loop qlp q`<br>`    int type 1 2`<br>`    int l 1 n`<br>`    int r 1 n;` |

---

### 3. Apply the 4 Golden `.tcs` Rules

1. **Variables Must Be Letters Only**:
   - `a`, `b`, `n`, `m`, `k`, `t`, `arr`, `len`, `perm`, `grid` are valid.
   - `a_1`, `a1`, `arr_size` are **INVALID** (regex parser only matches `^[a-zA-Z]+$`).
2. **Semicolon `;` = Newline (`\n`)**:
   - Every line of output **must end with `;` on the last token**.
   - Tokens preceding it on the same line **must omit `;`**.
3. **Loop Indentation = Exactly 4 Spaces**:
   - All lines inside a `loop <var> <count>` block must be indented with 4 spaces (`    `).
   - Do **NOT** put a semicolon on the `loop` line itself.
4. **Distinct Arrays (`drarray`) Requirement**:
   - `drarray_<size> <var> <min> <max>;` requires `(max - min + 1) >= size`.

---

## 📚 Worked Mini-Examples (Problem Input $\to$ `.tcs`)

### Example 1: Multi-Testcase Array ($T$ testcases)
**Problem Input:**
> First line contains $t$ ($1 \le t \le 10$). Each testcase has:
> - Line 1: integer $n$ ($1 \le n \le 100$)
> - Line 2: $n$ space-separated integers $a_1, \dots, a_n$ ($1 \le a_i \le 10^9$)

**Generated `.tcs`:**
```tcs
int t 1 10;
loop lp t
    int n 1 100;
    rarray_n a 1 1000000000;
```

---

### Example 2: Same-Line Tokens + Array
**Problem Input:**
> First line contains two integers $n$ and $k$ ($1 \le n \le 100, 1 \le k \le 10^5$).
> Second line contains array of $n$ integers ($-10^4 \le a_i \le 10^4$).

**Generated `.tcs`:**
```tcs
int n 1 100
int k 1 100000;
rarray_n a -10000 10000;
```

---

### Example 3: 2D Grid / Matrix ($N \times M$)
**Problem Input:**
> First line contains $r$ and $c$ ($1 \le r, c \le 50$) — rows and columns.
> Next $r$ lines each contain $c$ space-separated integers ($0 \le v \le 1000$).

**Generated `.tcs`:**
```tcs
int r 1 50
int c 1 50;
loop rowlp r
    rarray_c row 0 1000;
```

---

### Example 4: Character Map / Binary Maze
**Problem Input:**
> First line contains $n$ and $m$ ($2 \le n, m \le 20$).
> Next $n$ lines each contain a string of length $m$ of `.` and `#`.

**Generated `.tcs`:**
```tcs
int n 2 20
int m 2 20;
loop rowlp n
    flstring_m row ? .#;
```

---

### Example 5: Graph / Tree ($N$ vertices, $M$ edges)
**Problem Input:**
> First line contains $n$ and $m$ ($2 \le n \le 100, 1 \le m \le 200$).
> Next $m$ lines each contain $u, v, w$ ($1 \le u, v \le n, 1 \le w \le 10^4$).

**Generated `.tcs`:**
```tcs
int n 2 100
int m 1 200;
loop edgelp m
    int u 1 n
    int v 1 n
    int w 1 10000;
```

---

### Example 6: Queries on an Array
**Problem Input:**
> First line has $n$ and $q$ ($1 \le n, q \le 500$).
> Second line has array $a$ of $n$ integers ($1 \le a_i \le 10^6$).
> Next $q$ lines each have a query `type l r` ($type \in \{1, 2\}, 1 \le l \le r \le n$).

**Generated `.tcs`:**
```tcs
int n 1 500
int q 1 500;
rarray_n a 1 1000000;
loop qlp q
    int type 1 2
    int l 1 n
    int r 1 n;
```

---

### Example 7: Distinct Permutation
**Problem Input:**
> First line has integer $n$ ($1 \le n \le 50$).
> Second line has a permutation of numbers $1$ to $n$.

**Generated `.tcs`:**
```tcs
int n 1 50;
drarray_n perm 1 n;
```

---

## ⚡ Agent Response Format When User Provides a Problem

Whenever the user provides a problem statement, reply with:

1. **Extracted Input Structure**: Brief summary of the lines and constraints.
2. **The `.tcs` Code Block**: Clean, copy-pasteable (or written directly to a `.tcs` file).
3. **Execution Command**:
   ```bash
   python3 testcode.py -T testcases.tcs -I1 my_code.cpp -N 10
   ```
