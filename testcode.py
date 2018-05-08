import argparse
import configparser

import tcgen
import executer
import utils

parser = argparse.ArgumentParser()
config = configparser.RawConfigParser(allow_no_value=False)


parser.add_argument('-T', metavar='--testcases', type=str, required=True,
                    help='file containg testcase syntax')
parser.add_argument('-I1', metavar='--input1', type=str, required=False,
                    help='file containg code1')
parser.add_argument('-I2', metavar='--input2', type=str, required=False,
                    help='file containg code2')
parser.add_argument('-C', metavar='--config', type=str, default='config.cfg',
                    help='config file')
parser.add_argument('-N', metavar='--no_test', type=int, default=10,
                    help='no of times to run test')

args = parser.parse_args()
config.read(args.C)

interm = "intermediate/"

code1_file = args.I2 if args.I1 is None and args.I2 is not None else args.I1
code1_fio = interm + config['code1']['fileio']
code1_out = interm + config['code1']['output']
code1_bin = interm + config['code1']['binary']

code2_file = None if args.I1 is None and args.I2 is not None else args.I2
code2_fio = interm + config['code2']['fileio']
code2_out = interm + config['code2']['output']
code2_bin = interm + config['code2']['binary']

tc_syntax = args.T
tc_nos = args.N
tc_out = interm + config['testcases']['output']

result = interm + config['result']['output']
report = interm + config['result']['report']

clean_fileio = config['cleanup'].getboolean('clean_fileio')
clean_binary = config['cleanup'].getboolean('clean_binary')
clean_all = config['cleanup'].getboolean('clean_all')


if __name__ == "__main__":

    print("-" * 10 + "  Compiling  " + "-" * 10)

    if code1_file is not None:
        if ".cpp" in code1_file:
            executer.c_cpp_code_to_fileio(code1_file, code1_fio, isplus=True)
            c1_time = executer.compile_cpp_code(code1_fio, code1_bin)
            print("Code1 CPP compiled in %.5f sec" % c1_time)
        elif ".c" in code1_file:
            executer.c_cpp_code_to_fileio(code1_file, code1_fio, isplus=False)
            c1_time = executer.compile_c_code(code1_fio, code1_bin)
            print("Code1 C compiled in %.5f sec" % c1_time)
        elif ".py" in code1_file:
            executer.py_code_to_fileio(code1_file, code1_fio)
            print("Code1 PY converted")

    if code2_file is not None:
        if ".cpp" in code2_file:
            executer.c_cpp_code_to_fileio(code2_file, code2_fio, isplus=True)
            c2_time = executer.compile_cpp_code(code2_fio, code2_bin)
            print("Code2 CPP compiled in %.5f sec" % c2_time)
        elif ".c" in code2_file:
            executer.c_cpp_code_to_fileio(code2_file, code2_fio, isplus=False)
            c2_time = executer.compile_c_code(code2_fio, code2_bin)
            print("Code1 C compiled in %.5f sec" % c2_time)
        elif ".py" in code2_file:
            executer.py_code_to_fileio(code2_file, code2_fio)
            print("Code2 PY converted")

    print()

    try:
        stats = []

        for i in range(tc_nos):

            print("-" * 10 + "  Test - " + str(i) + "  " + "-" * 10)

            tc_time = tcgen.get_tcs(tc_syntax, tc_out)
            print("Testcases generated in %.5f sec" % tc_time)

            utils.copy_file_to_folder_group(i, tc_out)

            if code1_file is not None:
                if ".cpp" in code1_file or ".c" in code1_file:
                    c1tm = executer.run_c_cpp_bin(code1_bin, tc_out, code1_out)
                elif ".py" in code1_file:
                    c1tm = executer.run_py_code(code1_fio, tc_out, code1_out)
                print("Code1 executed in %.5f sec" % c1tm)
                utils.copy_file_to_folder_group(i, code1_out)
                stats.append({'code1_time': c1tm})

            if code2_file is not None:
                if ".cpp" in code2_file or ".c" in code2_file:
                    c2tm = executer.run_c_cpp_bin(code2_bin, tc_out, code2_out)
                elif ".py" in code2_file:
                    c2tm = executer.run_py_code(code2_fio, tc_out, code2_out)
                print("Code2 executed in %.5f sec" % c2tm)
                utils.copy_file_to_folder_group(i, code2_out)

                diffs = utils.compare_outputs(code1_out, code2_out, result)
                if diffs == 0:
                    print("Success : both outputs are same")
                elif diffs == -1:
                    print("Failure : invalid output generated")
                else:
                    print("Failure : output different at %d positions" % diffs)

                if diffs != -1:
                    utils.copy_file_to_folder_group(i, result)

                stats[-1].update({'code2_time': c2tm, 'diff': diffs})

            print()

    except KeyboardInterrupt as _:
        i = i-1
        print("Error : KeyboardInterrupt")

    finally:
        if stats:
            utils.write_stats(stats, report, code2_file is None)

            print()
            print("Tests done : " + str(i+1) + "/" + str(tc_nos))
            print("Report written to " + report)
            print()

        if code1_file is not None:
            if clean_fileio:
                if ".py" in code1_file:
                    utils.delete_file(code1_fio + ".py")
                elif ".cpp" in code1_file:
                    utils.delete_file(code1_fio + ".cpp")
                elif ".c" in code1_file:
                    utils.delete_file(code1_fio + ".c")

            if clean_binary:
                if ".cpp" in code1_file or ".c" in code1_file:
                    utils.delete_file(code1_bin)

            utils.delete_file(code1_out)

        if code2_file is not None:
            if clean_fileio:
                if ".py" in code2_file:
                    utils.delete_file(code2_fio + ".py")
                elif ".cpp" in code2_file:
                    utils.delete_file(code2_fio + ".cpp")
                elif ".c" in code2_file:
                    utils.delete_file(code2_fio + ".c")

            if clean_binary:
                if ".cpp" in code2_file or ".c" in code2_file:
                    utils.delete_file(code2_bin)

            utils.delete_file(code2_out)

        utils.delete_file(tc_out)
        utils.delete_file(result)

        if clean_all:
            print("**WARNING**")
            print("Cleaning everything except report.")
            print("To avoid this set 'clean_all' flag to 'no' in your config")
            print()
            for i in range(tc_nos):
                utils.delete_folder_group(i, interm)
