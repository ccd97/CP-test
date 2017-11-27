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

code1_file = args.I1
code1_fio = interm + config['code1']['fileio']
code1_out = interm + config['code1']['output']
code1_bin = interm + config['code1']['binary']

code2_file = args.I2
code2_fio = interm + config['code2']['fileio']
code2_out = interm + config['code2']['output']
code2_bin = interm + config['code2']['binary']

tc_syntax = args.T
tc_nos = args.N
tc_out = interm + config['testcases']['output']

result = interm + config['result']['output']
report = interm + config['result']['report']


if __name__ == "__main__":

    print("-" * 10 + "  Compiling  " + "-" * 10)

    if code1_file is not None:
        if ".cpp" in code1_file:
            executer.cpp_code_to_fileio(code1_file, code1_fio)
            c1_time = executer.compile_cpp_code(code1_fio, code1_bin)
            print("Code1 CPP compiled in %.5f sec" % c1_time)
            utils.delete_file(code1_fio + ".cpp")
        elif ".py" in code1_file:
            executer.py_code_to_fileio(code1_file, code1_fio)
            print("Code1 PY converted")

    if code2_file is not None:
        if ".cpp" in code2_file:
            executer.cpp_code_to_fileio(code2_file, code2_fio)
            c2_time = executer.compile_cpp_code(code2_fio, code2_bin)
            print("Code2 CPP compiled in %.5f sec" % c2_time)
            utils.delete_file(code2_fio + ".cpp")
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
                if ".cpp" in code1_file:
                    c1tm = executer.run_cpp_bin(code1_bin, tc_out, code1_out)
                elif ".py" in code1_file:
                    c1tm = executer.run_py_code(code1_fio, tc_out, code1_out)
                print("Code1 executed in %.5f sec" % c1tm)
                utils.copy_file_to_folder_group(i, code1_out)

            if code2_file is not None:
                if ".cpp" in code2_file:
                    c2tm = executer.run_cpp_bin(code2_bin, tc_out, code2_out)
                elif ".py" in code2_file:
                    c2tm = executer.run_py_code(code2_fio, tc_out, code2_out)
                print("Code2 executed in %.5f sec" % c2tm)
                utils.copy_file_to_folder_group(i, code2_out)

                diffs = utils.compare_outputs(code1_out, code2_out, result)
                if diffs == 0:
                    print("Success : both outputs are same")
                else:
                    print("Failure : output different at %d positions" % diffs)

                utils.copy_file_to_folder_group(i, result)
                stats.append({'code1_time': c1tm,
                              'code2_time': c2tm,
                              'diff': diffs})

            print()

    except KeyboardInterrupt as _:
        i = i-1
        print("Error : KeyboardInterrupt")

    finally:
        utils.write_stats(stats, report)

        print()
        print("Tests done : " + str(i+1) + "/" + str(tc_nos))
        print("Report written to " + report)
        print()

        if code1_file is not None and ".py" in code1_file:
            utils.delete_file(code1_fio + ".py")
        utils.delete_file(code1_out)
        utils.delete_file(code1_bin)

        if code2_file is not None and ".py" in code2_file:
            utils.delete_file(code2_fio + ".py")
        utils.delete_file(code2_out)
        utils.delete_file(code2_bin)

        utils.delete_file(tc_out)
        utils.delete_file(result)
