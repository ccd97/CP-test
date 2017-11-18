import subprocess
import sys
import time
import re


def cpp_code_to_fileio(inp, out_name):
    out_code = '#include <fstream>\n'
    file_io_lines = "int main(int argc, char const *argv[]) {"
    file_io_lines += "\n\tstd::ifstream fin(argv[1]);"
    file_io_lines += "\n\tstd::ofstream fout(argv[2]);"

    with open(inp, 'r') as in_f:
        out_code += in_f.read()

    out_code = re.sub('int[\s]*main[\s]*\([^\)]*\)[\s]*{', file_io_lines, out_code)
    out_code = re.sub('cin[\s]*>>', 'fin>>', out_code)
    out_code = re.sub('cout[\s]*<<', 'fout<<', out_code)

    with open(out_name + ".cpp", 'w') as op_f:
        op_f.write(out_code)

    return out_name + ".cpp"


def py_code_to_fileio(inp, out_name):
    out_code = 'import sys\n'
    out_code += "fin = open(sys.argv[1], 'r')\n"
    out_code += "fout = open(sys.argv[2], 'w+')\n"

    with open(inp, 'r') as in_f:
        out_code += in_f.read()

    inp_pattern = r'input[\s]*\([\s]*\)([\s]*\.[\s]*[lr]?strip[\s]*\([\s]*\))*'
    out_patter = r'print[^\S\r\n]*\((.*)\)'

    out_code = re.sub(inp_pattern, 'fin.readline().strip()', out_code)
    out_code = re.sub(out_patter, 'fout.write(str(\\1))', out_code)

    with open(out_name + ".py", 'w') as op_f:
        op_f.write(out_code)

    return out_name + ".py"


def compile_cpp_code(inp, out_bin):
    try:
        start_time = time.time()
        subprocess.check_call([r"/usr/bin/g++", "--std=c++14", "-Wall",
                               "-o", out_bin, inp + ".cpp"])
        end_time = time.time()
        return (end_time - start_time)
    except subprocess.CalledProcessError as e:
        print("Compilation Error in file : " + inp)
        sys.exit(1)


def run_cpp_bin(bin, in_tc, out_res):
    try:
        start_time = time.time()
        subprocess.check_call(["./" + bin, in_tc, out_res])
        end_time = time.time()
        return (end_time - start_time)
    except subprocess.CalledProcessError as e:
        print("Runtime Error in binary_file : " + bin)
        sys.exit(1)


def run_py_code(inp, in_tc, out_res):
    try:
        inp = inp + ".py"
        start_time = time.time()
        subprocess.check_call([r"/usr/bin/python3", inp, in_tc, out_res])
        end_time = time.time()
        return (end_time - start_time)
    except subprocess.CalledProcessError as e:
        print("Runtime Error in python_file : " + inp)
        sys.exit(1)
