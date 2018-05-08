from random import randint, choice, sample
import string
import time
import re

values = {}


def get_value(s_val):
    numptn = re.compile(r'^-?([0-9]+)$')
    varptn = re.compile(r'^([a-zA-Z]+)$')
    arrptn = re.compile(r'^([a-zA-Z]+)([0-9]+)$')

    if numptn.match(s_val):
        return int(s_val)
    elif varptn.match(s_val):
        return values[s_val]
    elif arrptn.match(s_val):
        ptnsch = re.search(arrptn, s_val)
        return values[ptnsch.group(1)][int(ptnsch.group(2))]


def generate_int(line):
    minv = get_value(line[3])
    maxv = get_value(line[4])
    randn = randint(minv, maxv)
    values[line[2]] = randn
    return str(randn)


def generate_drarray(line):
    output = ""
    ssize = line[1].split('_')[1]
    size = get_value(ssize)
    minv = get_value(line[3])
    maxv = get_value(line[4])
    rns = sample(range(minv, maxv+1), size)
    values[line[2]] = rns

    for val in rns:
        output += str(val) + " "

    return output


def generate_rarray(line):
    output = ""
    ssize = line[1].split('_')[1]
    size = get_value(ssize)
    minv = get_value(line[3])
    maxv = get_value(line[4])
    rns = [randint(minv, maxv) for _ in range(size)]
    values[line[2]] = rns

    for val in rns:
        output += str(val) + " "

    return output


def generate_rlstring(line):
    output = ""
    minlen = line[1].split('_')[1]
    maxlen = line[1].split('_')[2]
    minlen = get_value(minlen)
    maxlen = get_value(maxlen)
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
    flen = get_value(flen)
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
    ittrs = get_value(ittrs)

    nll = 0
    for ln in range(i+1, len(synlist)):
        nspaces = synlist[ln][0] - line[0]
        if nspaces > 0 and nspaces % 4 == 0:
            nll += 1
        else:
            break

    for _ in range(ittrs-1):
        output += generate_tc(synlist[i+1:i+1+nll])

    return output


def generate_tc(synlist):
    output = ""

    i = 0
    while True:
        if i >= len(synlist):
            break

        line = synlist[i]

        if line[1] == 'int':
            output += generate_int(line)

        elif "drarray" in line[1]:
            output += generate_drarray(line)

        elif "rarray" in line[1]:
            output += generate_rarray(line)

        elif "rlstring" in line[1]:
            output += generate_rlstring(line)

        elif "flstring" in line[1]:
            output += generate_flstring(line)

        elif "loop" in line[1]:
            output += generate_loop(i, synlist)

        if output and output[-1] != '\n':
            if line[-1] == ';':
                output += "\n"
            elif output[-1] != " ":
                output += " "

        i += 1

    return output


def get_tokens(line):
    synline = line.strip().split()
    if not synline:
        return None
    indentspace = len(line) - len(line.lstrip())
    tokens = [indentspace]
    tokens.extend(synline)

    if tokens[-1][-1] == ';':
        tokens[-1] = tokens[-1][:-1]
        tokens.append(';')

    return tokens


def get_tcs(tc_syntax, tc_output):
    with open(tc_syntax, 'r') as syntax_file:
        synlist = []
        for line in syntax_file.readlines():
            tkns = get_tokens(line)
            if tkns:
                synlist.append(tkns)
        start_time = time.time()
        tc_out = generate_tc(synlist)
        end_time = time.time()

    with open(tc_output, 'w') as out_file:
        out_file.write(tc_out)

    return end_time - start_time
