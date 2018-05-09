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
parser.add_argument('-C', metavar='--config', type=str,
                    default='configs/default.ini', help='config file')
parser.add_argument('-N', metavar='--no_test', type=int, default=10,
                    help='no of times to run test')

args = parser.parse_args()
config.read(args.C)

tc_syntax = args.T
tc_nos = args.N

interm = config['output']['intermediate'] + '/'

code1_file = args.I2 if args.I1 is None and args.I2 is not None else args.I1
code1_fio = interm + config['code1']['fileio']
code1_bin = interm + config['code1']['binary']

code2_file = None if args.I1 is None and args.I2 is not None else args.I2
code2_fio = interm + config['code2']['fileio']
code2_bin = interm + config['code2']['binary']

tc_out = interm + config['testcases']['output']
code1_out = interm + config['code1']['output']
code2_out = interm + config['code2']['output']
result = interm + config['result']['output']

report = interm + config['result']['report'] + ".txt"
make_report = config['result'].getboolean('make_report')

grp_type = config['output'].getint('group_type')
idx_out = config['output'].getboolean('index_output') or (grp_type != 1)
idx_len = config['output'].getint('index_length')

gen_zip = config['output'].getboolean('zip_output')

clean_fileio = config['cleanup'].getboolean('clean_fileio')
clean_binary = config['cleanup'].getboolean('clean_binary')
clean_compare = config['cleanup'].getboolean('clean_compare')
clean_all = config['cleanup'].getboolean('clean_all')


if __name__ == "__main__":

    utils.create_folder(interm)

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
        created_folders = set()

        ttc_out = tc_out + ".tmp"
        tc1_out = code1_out + ".tmp"
        tc2_out = code2_out + ".tmp"
        tresult = result + ".tmp"

        for i in range(tc_nos):

            print("-" * 10 + "  Test - " + str(i) + "  " + "-" * 10)

            tc_time = tcgen.get_tcs(tc_syntax, ttc_out)
            print("Testcases generated in %.5f sec" % tc_time)

            grp_args = {'grptype': grp_type,
                        'idxfile': idx_out,
                        'idxlen': idx_len}

            foldr = utils.copy_to_grp(i, ttc_out, **grp_args)
            created_folders.add(foldr)

            if code1_file is not None:
                if ".cpp" in code1_file or ".c" in code1_file:
                    c1tm = executer.run_c_cpp_bin(code1_bin, ttc_out, tc1_out)
                elif ".py" in code1_file:
                    c1tm = executer.run_py_code(code1_fio, ttc_out, tc1_out)
                print("Code1 executed in %.5f sec" % c1tm)

                foldr = utils.copy_to_grp(i, tc1_out, **grp_args)
                created_folders.add(foldr)

                stats.append({'code1_time': c1tm})

            if code2_file is not None:
                if ".cpp" in code2_file or ".c" in code2_file:
                    c2tm = executer.run_c_cpp_bin(code2_bin, ttc_out, tc2_out)
                elif ".py" in code2_file:
                    c2tm = executer.run_py_code(code2_fio, ttc_out, tc2_out)
                print("Code2 executed in %.5f sec" % c2tm)

                foldr = utils.copy_to_grp(i, tc2_out, **grp_args)
                created_folders.add(foldr)

                diffs = utils.compare_outputs(tc1_out, tc2_out, tresult)
                if diffs == 0:
                    print("Success : both outputs are same")
                elif diffs == -1:
                    print("Failure : invalid output generated")
                else:
                    print("Failure : output different at %d positions" % diffs)

                if diffs != -1:
                    foldr = utils.copy_to_grp(i, tresult, **grp_args)
                    created_folders.add(foldr)

                stats[-1].update({'code2_time': c2tm, 'diff': diffs})

            print()

    except KeyboardInterrupt as _:
        i = i-1
        print("Error : KeyboardInterrupt")

    finally:
        if stats:
            print()
            print("Tests done : " + str(i+1) + "/" + str(tc_nos))
            if make_report:
                utils.write_stats(stats, report, code2_file is None)
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

            utils.delete_file(tc1_out)

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

            utils.delete_file(tc2_out)

        utils.delete_file(ttc_out)
        utils.delete_file(tresult)

        if clean_compare:
            if grp_type == 2:
                print(created_folders)
                utils.delete_folder(code2_out)
                utils.delete_folder(result)
            elif grp_type == 1:
                fend = (str(i).zfill(idx_len) if idx_out else "") + ".txt"
                c2sidx = code2_out.rfind('/') + 1
                ressidx = code2_out.rfind('/') + 1
                c2fname = code2_out[c2sidx:]
                resfname = result[ressidx:]
                for fld in created_folders:
                    utils.delete_file(interm + fld + "/" + c2fname + fend)
                    utils.delete_file(interm + fld + "/" + resfname + fend)

        if gen_zip:
            utils.delete_file(interm + interm[:-1] + ".zip")
            utils.make_zip(interm[:-1])

        if clean_all:
            print("**WARNING**")
            print("Cleaning everything except report.")
            print("To avoid this set 'clean_all' flag to 'no' in your config")
            utils.delete_folders(interm, created_folders)
            print()
