import os
import shutil


def compare_outputs(main_op, bf_op, result):
    with open(main_op) as f:
        main_op_lines = f.readlines()

    with open(bf_op) as f:
        bf_op_lines = f.readlines()

    if len(main_op_lines) != len(bf_op_lines):
        print("Error - both output files dont have same no of lines")
        return -1

    res = open(result, 'w')
    diff = 0

    i = 0
    for ml, bl in zip(main_op_lines, bf_op_lines):
        ml = ml.strip()
        bl = bl.strip()

        i += 1

        if ml != bl:
            res.write("-" * 10 + "  Line - " + str(i) + "  " + "-" * 10 + "\n")
            res.write("main >" + "\n")
            res.write(ml + "\n")
            res.write("bruteforce >" + "\n")
            res.write(bl + "\n")
            res.write("\n")
            diff += 1

    res.close()
    return diff


def copy_file_to_folder_group(i, filename):
    ls = filename.rfind('/') + 1
    if not os.path.exists(filename[:ls] + str(i)):
        os.makedirs(filename[:ls] + str(i))
    new_filename = filename[:ls] + str(i) + '/' + filename[ls:]
    shutil.copyfile(filename, new_filename)


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
