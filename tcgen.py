from random import randint, choice
import string
import time

values = {}


def generate_int(line):
    minv = int(line[2]) if line[2].isdecimal() else values[line[2]]
    maxv = int(line[3]) if line[3].isdecimal() else values[line[3]]
    randn = randint(minv, maxv)
    values[line[1]] = randn
    return str(randn)


def generate_rarray(line):
    output = ""
    ssize = line[0].split('_')[1]
    size = int(ssize) if ssize.isdecimal() else values[ssize]
    minv = int(line[2]) if line[2].isdecimal() else values[line[2]]
    maxv = int(line[3]) if line[3].isdecimal() else values[line[3]]
    rns = [randint(minv, maxv) for _ in range(size)]
    values[line[1]] = rns

    for val in rns:
        output += str(val) + " "

    return output


def generate_rlstring(line):
    output = ""
    minlen = line[0].split('_')[1]
    maxlen = line[0].split('_')[2]
    minlen = int(minlen) if minlen.isdecimal() else values[minlen]
    maxlen = int(maxlen) if maxlen.isdecimal() else values[maxlen]
    rnlen = randint(minlen, maxlen)

    letters = ""
    if line[2] == "?":
        letters += line[3].strip()
    else:
        if "u" in line[2]:
            letters += string.ascii_uppercase
        if "l" in line[2]:
            letters += string.ascii_lowercase
        if "d" in line[2]:
            letters += string.digits

    for _ in range(rnlen):
        output += choice(letters)

    return output


def generate_flstring(line):
    output = ""
    flen = line[0].split('_')[1]
    flen = int(flen) if flen.isdecimal() else values[flen]
    letters = ""
    if line[2] == "?":
        letters += line[3].strip()
    else:
        if "u" in line[2]:
            letters += string.ascii_uppercase
        if "l" in line[2]:
            letters += string.ascii_lowercase
        if "d" in line[2]:
            letters += string.digits

    for _ in range(flen):
        output += choice(letters)

    return output


def generate_loop(i, synlist):
    output = ""
    line = synlist[i]

    ittrs = line[2]
    ittrs = int(ittrs) if ittrs.isdecimal() else values[ittrs]

    nll = int(line[0].split('_')[1]) + 1

    for _ in range(ittrs-1):
        output += generate_tc(synlist[i+1:i+1+nll])
        if output[-1] != '\n':
            output += "\n"

    return output


def generate_tc(synlist):
    output = ""

    i = 0
    while True:
        if i >= len(synlist):
            break

        line = synlist[i]

        if output and output[-1] != '\n':
            output += "\n"

        if line[0] == 'int':
            output += generate_int(line)

        elif "rarray" in line[0]:
            output += generate_rarray(line)

        elif "rlstring" in line[0]:
            output += generate_rlstring(line)

        elif "flstring" in line[0]:
            output += generate_flstring(line)

        elif "loop" in line[0]:
            output += generate_loop(i, synlist)

        i += 1

    return output + "\n"


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
