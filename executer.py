import subprocess
import sys
import time
import re


def c_cpp_code_to_fileio(inp, out_name, isplus):
    if not isplus:
        out_code = '#include <stdio.h>\n'
    else:
        out_code = '#include <cstdio>\n'

    file_io_lines = "int main(int argc, char const *argv[]) {"
    file_io_lines += '\n\tfreopen(argv[1], "r", stdin);'
    file_io_lines += '\n\tfreopen(argv[2], "w", stdout);'
    main_func_pattern = r'int[\s]*main[\s]*\([^\)]*\)[\s]*{'

    with open(inp, 'r') as in_f:
        out_code += in_f.read()

    out_code = re.sub(main_func_pattern, file_io_lines, out_code)

    file_ext = ".c" if not isplus else ".cpp"
    with open(out_name + file_ext, 'w') as op_f:
        op_f.write(out_code)

    return out_name + file_ext


def py_code_to_fileio(inp, out_name):
    out_code = 'import sys\n'
    out_code += "fin = open(sys.argv[1], 'r')\n"
    out_code += "fout = open(sys.argv[2], 'w+')\n"

    with open(inp, 'r') as in_f:
        out_code += in_f.read()

    inp_pattern = r'input[\s]*\([\s]*\)([\s]*\.[\s]*[lr]?strip[\s]*\([\s]*\))*'
    out_pattern = r'print[^\S\r\n]*\((.*)\)'

    out_code = re.sub(inp_pattern, 'fin.readline().strip()', out_code)
    out_code = re.sub(out_pattern, 'print(str(\\1), file=fout)', out_code)

    with open(out_name + ".py", 'w') as op_f:
        op_f.write(out_code)

    return out_name + ".py"


def compile_c_code(inp, out_bin):
    try:
        start_time = time.time()
        subprocess.check_call([r"/usr/bin/gcc", "--std=c11", "-Wall",
                               "-o", out_bin, inp + ".c"])
        end_time = time.time()
        return end_time - start_time
    except subprocess.CalledProcessError as _:
        print("Compilation Error in file : " + inp)
        sys.exit(1)


def compile_cpp_code(inp, out_bin):
    try:
        start_time = time.time()
        subprocess.check_call([r"/usr/bin/g++", "--std=c++14", "-Wall",
                               "-o", out_bin, inp + ".cpp"])
        end_time = time.time()
        return end_time - start_time
    except subprocess.CalledProcessError as _:
        print("Compilation Error in file : " + inp)
        sys.exit(1)


def run_c_cpp_bin(binary, in_tc, out_res):
    try:
        start_time = time.time()
        subprocess.check_call(["./" + binary, in_tc, out_res])
        end_time = time.time()
        return end_time - start_time
    except subprocess.CalledProcessError as _:
        print("Runtime Error in binary_file : " + binary)
        sys.exit(1)


def run_py_code(inp, in_tc, out_res):
    try:
        inp = inp + ".py"
        start_time = time.time()
        subprocess.check_call([r"/usr/bin/python3", inp, in_tc, out_res])
        end_time = time.time()
        return end_time - start_time
    except subprocess.CalledProcessError as _:
        print("Runtime Error in python_file : " + inp)
        sys.exit(1)
