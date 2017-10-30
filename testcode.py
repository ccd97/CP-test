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
main_output = interm + config['main_file']['output']
main_binary = interm + config['main_file']['binary']

bf_file = args.B
bf_fileio = interm + config['bruteforce_file']['fileio']
bf_output = interm + config['bruteforce_file']['output']
bf_binary = interm + config['bruteforce_file']['binary']

tc_syntax = args.T
tc_nos = args.N if bf_file is not None else 1
tc_output = interm + config['testcases']['output']

result = interm + config['result']['output']


if __name__ == "__main__":
    for i in range(tc_nos):

        print("-" * 10 + "  Test - " + str(i) + "  " + "-" * 10)

        tc_time = tcgen.get_tcs(tc_syntax, tc_output)
        print("Testcases generated in %.5f sec" % tc_time)

        utils.copy_file_to_folder_group(i, tc_output)

        if main_file is not None:
            if ".cpp" in main_file:
                executer.cpp_code_to_fileio(main_file, main_fileio,
                                            tc_output, main_output)
                mc_time = executer.compile_cpp_code(main_fileio, main_binary)
                mr_time = executer.run_cpp_bin(main_binary)
                print("Main CPP compiled in %.5f sec" % mc_time)
                print("Main CPP executed in %.5f sec" % mr_time)

                utils.copy_file_to_folder_group(i, main_output)

        if bf_file is not None:
            if ".cpp" in main_file:
                executer.cpp_code_to_fileio(bf_file, bf_fileio,
                                            tc_output, bf_output)
                bfc_time = executer.compile_cpp_code(bf_fileio, bf_binary)
                bfr_time = executer.run_cpp_bin(bf_binary)
                print("Bruteforce CPP compiled in %.5f sec" % bfc_time)
                print("Bruteforce CPP executed in %.5f sec" % bfr_time)

                utils.copy_file_to_folder_group(i, bf_output)

            diffs = utils.compare_outputs(main_output, bf_output, result)
            if diffs == 0:
                print("Success : both outputs are same")
            else:
                print("Failure : outputs different at %d positions" % diffs)

            utils.copy_file_to_folder_group(i, result)

        print()

    if ".cpp" in main_file:
        utils.delete_file(main_fileio + ".cpp")
    utils.delete_file(main_output)
    utils.delete_file(main_binary)

    if ".cpp" in main_file:
        utils.delete_file(bf_fileio + ".cpp")
    utils.delete_file(bf_output)
    utils.delete_file(bf_binary)

    utils.delete_file(tc_output)
    utils.delete_file(result)
