# Test-Case Syntax
Here a guide to write syntax for test-cases. Refer examples for better understanding.

## General format
Every line consist of minimum 2 parts

1. Type of data to be generated
2. Variable name (should contain alphabets only)

The other parts can be

3. Minimum value of data elements
4. Maximum value of data elements

For string:

3. Content of string (lowercase, uppercase, digits, etc.)

A semicolon at end of line indicates a new line in generated cases.
If it is not placed output is generated on single line.

***
#### Generate single Integer

```
int variable-name min-value max-value
```
Example: 
```
int mx 0 1000;
int n 0 mx;
```
Generates,<br>
a single integer between 0 and 1000 -> mx (0th line)<br>
a single integer between 0 and mx -> n (1st line)<br>

---
#### Generate row array of integers
```
rarray_size variable-name min-value max-value
```
Example: 
```
rarray_10 ar 0 100;
int sz 0 20;
rarray_sz arr 0 1000;
```
Generates,<br>
a row array of size 10 of integers between 0 and 100 -> arr1 (0th line)<br>
a single integer between 0 and 20 -> sz (1st line)<br>
a row array of size sz of integers between 0 and 1000 -> arr2 (2nd line)<br>

---
#### Generate fixed length string
```
flstring_size variable-name content
```
Content (single or any combination):

- u - uppercase
- l - lowercase
- d - digits
- ? - custom character string (See example)

Example: 
```
flstring_10 str ul;
flstring_100 strr ? $#&;
```
Generates,<br>
a string of length 10 containing lowercase and uppercase characters  -> str1 (0th line)<br>
a string of length 100 containing $#& characters  -> str2 (1st line)<br>

---
#### Generate variable length string
```
rlstring_minsize_maxsize variable-name content
```
Content (single or any combination):

- u - uppercase
- l - lowercase
- d - digits
- ? - custom character string (See example)

Example: 
```
int n 1 15 20;
rlstring_10_20 str d;
rlstring_10_n strr ? *+.;
```
Generates,<br>
a single integer between 15 and 20 -> n (0th line)<br>
a string containing digits whose length is between 10 and 20  -> str1 (1st line)<br>
a string containing \*+. characters whose length is between 10 and n -> str2 (2nd line)<br>

---
#### Looping
```
loop variable-name no-of-itterations
```

Lines to be looped are to be indented by 4 spaces.

Example: 
```
int t 1 50;
loop lp t
    rlstring_10_20 str d;
    int n 1 100;
int k 1 10;
```
Generates,
a single integer between 1 and 50 -> t (0th line)<br>
generate t times string containing digits whose length is between 10 and 20  -> str1 (2nd line)<br>
generate t times single integer between 1 and 100 -> n (3rd line)<br>
a single integer between 1 and 10 -> k (after loop)<br>
