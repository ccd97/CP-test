# CP-test

A tool to generate test-cases for competitive programming. With it, you can also execute your code on generated test-cases and compare it with other code automatically.

### What it can do?
* Generate random test-cases
* Auto-generate `.tcs` syntax files from problem statements using the [testcase-syntax skill](skills/testcase-syntax/SKILL.md)
* Run code (supports C11, C++14, Python 3) automatically on these test-cases
* Run two codes simultaneously and compare results to detect corner cases
* Generate HackerRank problem-setting style test-case zip packages

### Why?
* Solely for generating test-cases
* To verify code runs properly and avoid runtime errors
* To compare optimized code against brute-force code on random inputs

## Usage

To generate test-cases (E.g.: 5 test-cases):
```bash
python3 testcode.py -T testcase_syntax.tcs -N 5
```

To generate test-cases and run your code on them:
```bash
python3 testcode.py -T testcase_syntax.tcs -I1 my_code.cpp
```

To generate test-cases, run two codes, and compare output:
```bash
python3 testcode.py -T testcase_syntax.tcs -I1 my_code.cpp -I2 my_bruteforce.py
```

To generate HackerRank style test-cases zip:
```bash
python3 testcode.py -T testcase_syntax.tcs -I1 my_code.cpp -C configs/hackerrank.ini
```

- Default `-N` is 10. Pass `-N <count>` to adjust.
- Default config is `configs/default.ini`. Use `-C` to specify custom config.
- Pass `.tcs` syntax file with `-T`. Refer to [TCSYNTAX.md](TCSYNTAX.md) for reference.
- **Skill**: Use [`skills/testcase-syntax/SKILL.md`](skills/testcase-syntax/SKILL.md) to automatically translate problem statements and constraints into `.tcs` files.
- See [`AGENTS.md`](AGENTS.md) for AI agent testing guidelines and workflows.

### Supported languages

- C11
- C++14
- Python3
