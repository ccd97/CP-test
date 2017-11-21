import argparse
import configparser

import tcgen
import executer
import utils

parser = argparse.ArgumentParser()
config = configparser.RawConfigParser(allow_no_value=False)


parser.add_argument('-T', metavar='--testcases', type=str, required=True,
                    help='file containg testcase syntax')
parser.add_argument('-I', metavar='--input', type=str, required=False,
                    help='file containg input code')
parser.add_argument('-B', metavar='--bruteforce', type=str, required=False,
                    help='file containg bruteforce code')
parser.add_argument('-C', metavar='--config', type=str, default='config.cfg',
                    help='config file')
parser.add_argument('-N', metavar='--no_test', type=int, default=10,
                    help='no of times to run test')

args = parser.parse_args()
config.read(args.C)

interm = "intermediate/"

main_file = args.I
main_fileio = interm + config['main_file']['fileio']
main_out = interm + config['main_file']['output']
main_binary = interm + config['main_file']['binary']

bf_file = args.B
bf_fileio = interm + config['bruteforce_file']['fileio']
bf_output = interm + config['bruteforce_file']['output']
bf_binary = interm + config['bruteforce_file']['binary']

tc_syntax = args.T
tc_nos = args.N
tc_out = interm + config['testcases']['output']

result = interm + config['result']['output']
report = interm + config['result']['report']


if __name__ == "__main__":

    print("-" * 10 + "  Compiling  " + "-" * 10)

    if main_file is not None:
        if ".cpp" in main_file:
            executer.cpp_code_to_fileio(main_file, main_fileio)
            mc_time = executer.compile_cpp_code(main_fileio, main_binary)
            print("Main CPP compiled in %.5f sec" % mc_time)
            utils.delete_file(main_fileio + ".cpp")
        elif ".py" in main_file:
            executer.py_code_to_fileio(main_file, main_fileio)
            print("Main PY converted")

    if bf_file is not None:
        if ".cpp" in bf_file:
            executer.cpp_code_to_fileio(bf_file, bf_fileio)
            bfc_time = executer.compile_cpp_code(bf_fileio, bf_binary)
            print("Bruteforce CPP compiled in %.5f sec" % bfc_time)
            utils.delete_file(bf_fileio + ".cpp")
        elif ".py" in bf_file:
            executer.py_code_to_fileio(bf_file, bf_fileio)
            print("Bruteforce PY converted")

    print()

    try:
        stats = []

        for i in range(tc_nos):

            print("-" * 10 + "  Test - " + str(i) + "  " + "-" * 10)

            tc_time = tcgen.get_tcs(tc_syntax, tc_out)
            print("Testcases generated in %.5f sec" % tc_time)

            utils.copy_file_to_folder_group(i, tc_out)

            if main_file is not None:
                if ".cpp" in main_file:
                    mtm = executer.run_cpp_bin(main_binary, tc_out, main_out)
                elif ".py" in main_file:
                    mtm = executer.run_py_code(main_fileio, tc_out, main_out)
                print("Main executed in %.5f sec" % mtm)
                utils.copy_file_to_folder_group(i, main_out)

            if bf_file is not None:
                if ".cpp" in bf_file:
                    btm = executer.run_cpp_bin(bf_binary, tc_out, bf_output)
                elif ".py" in bf_file:
                    btm = executer.run_py_code(bf_fileio, tc_out, bf_output)
                print("Bruteforce executed in %.5f sec" % btm)
                utils.copy_file_to_folder_group(i, bf_output)

                diffs = utils.compare_outputs(main_out, bf_output, result)
                if diffs == 0:
                    print("Success : both outputs are same")
                else:
                    print("Failure : output different at %d positions" % diffs)

                utils.copy_file_to_folder_group(i, result)
                stats.append({'main_time': mtm, 'bf_time': btm, 'diff': diffs})

            print()

    except KeyboardInterrupt as e:
        i = i-1
        print("Error : KeyboardInterrupt")

    finally:
        utils.write_stats(stats, report)

        print()
        print("Tests done : " + str(i+1) + "/" + str(tc_nos))
        print("Report written to " + report)
        print()

        if main_file is not None and ".py" in main_file:
            utils.delete_file(main_fileio + ".py")
        utils.delete_file(main_out)
        utils.delete_file(main_binary)

        if bf_file is not None and ".py" in bf_file:
            utils.delete_file(bf_fileio + ".py")
        utils.delete_file(bf_output)
        utils.delete_file(bf_binary)

        utils.delete_file(tc_out)
        utils.delete_file(result)
