import os
import shutil


def compare_outputs(code1_op, code2_op, result_file):
    with open(code1_op) as code_file:
        code1_op_lines = code_file.readlines()

    with open(code2_op) as code_file:
        code2_op_lines = code_file.readlines()

    if len(code1_op_lines) != len(code2_op_lines):
        print("Error - both output files dont have same no of lines")
        return -1

    res = open(result_file, 'w')
    diff = 0

    i = 0
    for c1l, c2l in zip(code1_op_lines, code2_op_lines):
        c1l = c1l.strip()
        c2l = c2l.strip()

        i += 1

        if c1l != c2l:
            res.write("-" * 10 + "  Line - " + str(i) + "  " + "-" * 10 + "\n")
            res.write("code1 >" + "\n")
            res.write(c1l + "\n")
            res.write("code2 >" + "\n")
            res.write(c2l + "\n")
            res.write("\n")
            diff += 1

    res.close()
    return diff


def write_stats(stats, report_file, single_file):
    res = open(report_file, 'w')

    stat_size = len(stats)

    max_code1_time = max(stats,
                         key=lambda x: x['code1_time'])['code1_time']
    min_code1_time = min(stats,
                         key=lambda x: x['code1_time'])['code1_time']
    avg_code1_time = sum(s['code1_time'] for s in stats)/stat_size

    res.write("-" * 10 + "  Code1 File  " + "-" * 10 + "\n")
    res.write("Minimum time : " + str(min_code1_time) + " sec" + "\n")
    res.write("Maximum time : " + str(max_code1_time) + " sec" + "\n")
    res.write("Average time : " + str(avg_code1_time) + " sec" + "\n")
    res.write("\n")

    if not single_file:
        max_code2_time = max(stats,
                             key=lambda x: x['code2_time'])['code2_time']
        min_code2_time = min(stats,
                             key=lambda x: x['code2_time'])['code2_time']
        avg_code2_time = sum(s['code2_time'] for s in stats)/stat_size

        res.write("-" * 10 + "  Code2 File  " + "-" * 10 + "\n")
        res.write("Minimum time : " + str(min_code2_time) + " sec" + "\n")
        res.write("Maximum time : " + str(max_code2_time) + " sec" + "\n")
        res.write("Average time : " + str(avg_code2_time) + " sec" + "\n")
        res.write("\n")

        is_wrong = False

        res.write("-" * 10 + "  Wrong Testcases  " + "-" * 10 + "\n")
        for i in range(stat_size):
            if stats[i]['diff'] == -1:
                res.write("Testcase " + str(i) + " produced invalid output"
                          + "\n")
                is_wrong = True
            elif stats[i]['diff'] != 0:
                res.write("Testcase " + str(i) + " different at "
                          + str(stats[i]['diff']) + " positions" + "\n")
                is_wrong = True

        if not is_wrong:
            res.write("No wrong testcase" + "\n")

    res.close()


def copy_file_to_folder_group(i, filename):
    idx = filename.rfind('/') + 1
    if not os.path.exists(filename[:idx] + str(i)):
        os.makedirs(filename[:idx] + str(i))
    new_filename = filename[:idx] + str(i) + '/' + filename[idx:]
    shutil.copyfile(filename, new_filename)


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
