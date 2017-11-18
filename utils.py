import os
import shutil


def compare_outputs(main_op, bf_op, result_file):
    with open(main_op) as f:
        main_op_lines = f.readlines()

    with open(bf_op) as f:
        bf_op_lines = f.readlines()

    if len(main_op_lines) != len(bf_op_lines):
        print("Error - both output files dont have same no of lines")
        return -1

    res = open(result_file, 'w')
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


def write_stats(stats, report_file):
    res = open(report_file, 'w')

    n = len(stats)

    max_main_time = max(stats, key=lambda x: x['main_time'])['main_time']
    min_main_time = min(stats, key=lambda x: x['main_time'])['main_time']
    avg_main_time = sum(s['main_time'] for s in stats)/n

    max_bf_time = max(stats, key=lambda x: x['bf_time'])['bf_time']
    min_bf_time = min(stats, key=lambda x: x['bf_time'])['bf_time']
    avg_bf_time = sum(s['bf_time'] for s in stats)/n

    res.write("-" * 10 + "  Main File  " + "-" * 10 + "\n")
    res.write("Minimum time required : " + str(min_main_time) + " sec" + "\n")
    res.write("Maximum time required : " + str(max_main_time) + " sec" + "\n")
    res.write("Average time required : " + str(avg_main_time) + " sec" + "\n")
    res.write("\n")

    res.write("-" * 10 + "  Bruteforce File  " + "-" * 10 + "\n")
    res.write("Minimum time required : " + str(min_bf_time) + " sec" + "\n")
    res.write("Maximum time required : " + str(max_bf_time) + " sec" + "\n")
    res.write("Average time required : " + str(avg_bf_time) + " sec" + "\n")
    res.write("\n")

    res.write("-" * 10 + "  Wrong Testcases  " + "-" * 10 + "\n")
    for i in range(n):
        if stats[i]['diffs'] != 0:
            res.write("Testcase " + str(i) + " different at "
                      + str(stats[i]['diffs']) + " positions" + "\n")

    res.close()


def copy_file_to_folder_group(i, filename):
    ls = filename.rfind('/') + 1
    if not os.path.exists(filename[:ls] + str(i)):
        os.makedirs(filename[:ls] + str(i))
    new_filename = filename[:ls] + str(i) + '/' + filename[ls:]
    shutil.copyfile(filename, new_filename)


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
