import subprocess
import sys
import time


def cpp_code_to_fileio(inp, out_name, in_tc, out_res):
    output_code = '#include <fstream>\n'
    output_code += 'std::ifstream fin("' + in_tc + '");\n'
    output_code += 'std::ofstream fout("' + out_res + '");\n\n'

    with open(inp, 'r') as in_f:
        for line in in_f:
            repl_line = line.replace("cin>>", "fin>>")
            repl_line = repl_line.replace("cout<<", "fout<<")
            output_code += repl_line

    with open(out_name + ".cpp", 'w') as op_f:
        op_f.write(output_code)

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


def run_cpp_bin(bin):
    try:
        start_time = time.time()
        subprocess.check_call("./" + bin)
        end_time = time.time()
        return (end_time - start_time)
    except subprocess.CalledProcessError as e:
        print("Runtime Error in binary_file : " + bin)
        sys.exit(1)
