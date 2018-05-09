# CP-test

A tool to generate test-cases for competitive programming. With it, you can also execute your code on generated test-cases and compare it with other code automatically.

### What it can do?
* Generate random test-cases
* Run code (supports various languages) automatically on these test-cases
* Run two code simultaneously and compare the result on these test-cases
* HackerRank problem-setting style test-cases zip

### Why?
* Sometimes solely for generating test-cases
* To check if code written generates proper output and does not give a run-time error
* To compare your code with brute-force code/any other code to check for corner cases

## Usage

To generate test-cases (E.g.: 5 test-cases)

```
python3 testcode.py -T testcase_syntax.tcs -N 5
```

To generate test-cases and run your code on generated test-cases
```
python3 testcode.py -T testcase_syntax.tcs -I1 my_code.cpp
```

To generate test-cases and run two codes and compare output
```
python3 testcode.py -T testcase_syntax.tcs -I1 my_code.cpp -I2 my_bruteforce.py
```

To generate HackerRank style test-cases zip
```
python3 testcode.py -T testcase_syntax.tcs -I1 my_code.cpp -C configs/hackerrank.ini
```
<br>
The default value of `-N` is 10. To generate more/less test-cases pass it as parameter.<br>
The default config used is `configs/default.ini`. Use `-C` flag to pass custom config.<br>

You need to specify syntax of test-cases in a file and pass it with `-T` argument.<br>
This test-case syntax is very simple and can be easily written. Refer to [TCSYNTAX.md](TCSYNTAX.md)

### Supported languages

Currently code files supported are:

- C11
- C++14
- Python3
