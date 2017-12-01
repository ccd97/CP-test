# Test-Case Syntax
Here a guide to write syntax for test-cases. Refer examples for better understanding.

## General format
Every line consist of minimum 3 parts

1. Line number (indexing starts from 0)
2. Type of data to be generated
3. Variable name

The other parts can be

4. Minimum value of data elements
5. Maximum value of data elements

For string:

4. Content of string (lowercase, uppercase, digits, etc.)

***
#### Generate single Integer

```
line int variable-name min-value max-value
```
Example: 
```
0 int mx 0 1000
1 int n 0 mx
```
Generates,<br>
a single integer between 0 and 1000 -> mx (0th line)<br>
a single integer between 0 and mx -> n (1st line)<br>

---
#### Generate row array of integers
```
line rarray_size variable-name min-value max-value
```
Example: 
```
0 rarray_10 arr1 0 100
1 int sz 0 20
2 rarray_sz arr2 0 1000
```
Generates,<br>
a row array of size 10 of integers between 0 and 100 -> arr1 (0th line)<br>
a single integer between 0 and 20 -> sz (1st line)<br>
a row array of size sz of integers between 0 and 1000 -> arr2 (2nd line)<br>

---
#### Generate column array of integers
```
line carray_size variable-name min-value max-value
line carray_size variable-name min-value max-value
.
.
line carray_size variable-name min-value max-value
```
Note - Line number and size should be same for all lines as it is still a single entry


Example: 
```
0 carray_3 n 1 100
0 carray_3 k -10 10
1 int z 99 100
```
Generates,<br>
a column array (horizontal array) of size 3 with integers from 1 to 100 -> n (0th line)<br>
a column array (horizontal array) of size 3 with integers from -10 to 10 -> k (0th line)<br>
a single integer between 99 and 100 -> z (1st line)<br>

One possible output:
```
-2 35
7 89
-10 13
99
```

---
#### Generate fixed length string
```
line flstring_size variable-name content
```
Content (single or any combination):

- u - uppercase
- l - lowercase
- d - digits

Example: 
```
0 flstring_10 str1 ul
1 flstring_100 str2
```
Generates,<br>
a string of length 10 containing lowercase and uppercase characters  -> str1 (0th line)<br>
a string of length 100 containing lowercase, uppercase and digits  -> str2 (1st line)<br>

---
#### Generate variable length string
```
line rlstring_minsize_maxsize variable-name content
```
Content (single or any combination):

- u - uppercase
- l - lowercase
- d - digits

Example: 
```
0 int n 1 15 20
1 rlstring_10_20 str1 d
2 rlstring_10_n str2 u
```
Generates,<br>
a single integer between 15 and 20 -> n (0th line)<br>
a string containing digits whose length is between 10 and 20  -> str1 (1st line)<br>
a string containing uppercase characters whose length is between 10 and n -> str2 (2nd line)<br>

---
#### Looping
```
line loop_no-of-lines min-value max-value
```
Example: 
```
0 loop_2 t 1 50
1 rlstring_10_20 str1 d
2 int n 1 100
3 int k 1 10
```
Generates,
a single integer between 1 and 50 -> t (0th line)<br>
generate t times string containing digits whose length is between 10 and 20  -> str1 (1st line)<br>
generate t times single integer between 1 and 100 -> n (2nd line)<br>
a single integer between 1 and 10 -> k (3th line)<br>
