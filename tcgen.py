from random import randint, choice
import string
import time

values = {}


def generate_int(line):
    minv = int(line[3]) if line[3].isdecimal() else values[line[3]]
    maxv = int(line[4]) if line[4].isdecimal() else values[line[4]]
    randn = randint(minv, maxv)
    values[line[2]] = randn
    return str(randn)


def generate_carray(i, cidx, synlist):
    output = ""
    ssize = synlist[i][1].split('_')[1]
    size = int(ssize) if ssize.isdecimal() else values[ssize]
    cols = []
    while True:
        if i >= len(synlist):
            break

        line = synlist[i]

        if int(line[0]) != cidx:
            i = i - 1
            break

        minv = int(line[3]) if line[3].isdecimal() else values[line[3]]
        maxv = int(line[4]) if line[4].isdecimal() else values[line[4]]
        rns = [randint(minv, maxv) for _ in range(size)]
        cols.append(line[2])
        values[line[2]] = rns

        i = i + 1

    for j in range(len(values[cols[0]])):
        for col in cols:
            output += str(values[col][j]) + " "
        output += "\n"

    return i, output


def generate_rarray(line):
    output = ""
    ssize = line[1].split('_')[1]
    size = int(ssize) if ssize.isdecimal() else values[ssize]
    minv = int(line[3]) if line[3].isdecimal() else values[line[3]]
    maxv = int(line[4]) if line[4].isdecimal() else values[line[4]]
    rns = [randint(minv, maxv) for _ in range(size)]
    values[line[2]] = rns

    for val in rns:
        output += str(val) + " "

    return output


def generate_rlstring(line):
    output = ""
    minlen = line[1].split('_')[1]
    maxlen = line[1].split('_')[2]
    minlen = int(minlen) if minlen.isdecimal() else values[minlen]
    maxlen = int(maxlen) if maxlen.isdecimal() else values[maxlen]
    rnlen = randint(minlen, maxlen)

    letters = ""
    if line[3] == "?":
        letters += line[4].strip()
    else:
        if "u" in line[3]:
            letters += string.ascii_uppercase
        if "l" in line[3]:
            letters += string.ascii_lowercase
        if "d" in line[3]:
            letters += string.digits

    for _ in range(rnlen):
        output += choice(letters)

    return output


def generate_flstring(line):
    output = ""
    flen = line[1].split('_')[1]
    flen = int(flen) if flen.isdecimal() else values[flen]
    letters = ""
    if line[3] == "?":
        letters += line[4].strip()
    else:
        if "u" in line[3]:
            letters += string.ascii_uppercase
        if "l" in line[3]:
            letters += string.ascii_lowercase
        if "d" in line[3]:
            letters += string.digits

    for _ in range(flen):
        output += choice(letters)

    return output


def generate_loop(i, synlist):
    output = ""
    line = synlist[i]

    ittrs = line[3]
    ittrs = int(ittrs) if ittrs.isdecimal() else values[ittrs]

    nll = int(line[1].split('_')[1]) + 1

    for _ in range(ittrs-1):
        output += generate_tc(synlist[i+1:i+1+nll])
        if output[-1] != '\n':
            output += "\n"

    return output


def generate_tc(synlist):
    output = ""
    cidx = int(synlist[0][0])

    i = 0
    while True:
        if i >= len(synlist):
            break

        line = synlist[i]

        if int(line[0]) != cidx:
            cidx = int(line[0])
            if output[-1] != '\n':
                output += "\n"

        if line[1] == 'int':
            output += generate_int(line) + " "

        if "rarray" in line[1]:
            output += generate_rarray(line) + " "

        if 'carray' in line[1]:
            i, out = generate_carray(i, cidx, synlist)
            output += out

        if "rlstring" in line[1]:
            output += generate_rlstring(line)

        if "flstring" in line[1]:
            output += generate_flstring(line)

        if "loop" in line[1]:
            output += generate_loop(i, synlist)

        i += 1

    return output


def get_tcs(tc_syntax, tc_output):
    with open(tc_syntax, 'r') as syntax_file:
        synlist = []
        for line in syntax_file.readlines():
            synlist.append(line.strip().split())
        start_time = time.time()
        tc_out = generate_tc(synlist)
        end_time = time.time()

    with open(tc_output, 'w') as out_file:
        out_file.write(tc_out)

    return end_time - start_time
