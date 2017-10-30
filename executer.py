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

    out_code = re.sub('int main\(.*\)[\S\s]*{', file_io_lines, out_code)
    out_code = re.sub('cin>>', 'fin>>', out_code)
    out_code = re.sub('cout<<', 'fout<<', out_code)

    with open(out_name + ".cpp", 'w') as op_f:
        op_f.write(out_code)

    return out_name + ".cpp"


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
