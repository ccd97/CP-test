import os
import shutil
import tempfile


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


def copy_to_grp(i, filename, grptype, idxfile, idxlen):
    sidx = filename.rfind('/') + 1
    didx = filename.rfind('.')

    if grptype == 1:
        fldrnam = str(i).zfill(idxlen)
    elif grptype == 2:
        idxfile = True
        fldrnam = filename[sidx:didx]
    else:
        fldrnam = str(i)

    fileext = (str(i).zfill(idxlen) if idxfile else "") + ".txt"

    if not os.path.exists(filename[:sidx] + fldrnam):
        os.makedirs(filename[:sidx] + fldrnam)
    new_filename = filename[:sidx] + fldrnam + '/'
    new_filename += filename[sidx:didx] + fileext
    shutil.copyfile(filename, new_filename)

    return fldrnam


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def delete_folder(foldername):
    if os.path.exists(foldername):
        shutil.rmtree(foldername)


def delete_folders(basepath, folder_list):
    for folder in folder_list:
        delete_folder(basepath + "/" + folder)


def make_zip(folder):
    tmpzip = tempfile.gettempdir() + "/" + folder
    shutil.make_archive(tmpzip, 'zip', folder)
    shutil.move(tmpzip + ".zip", folder + "/" + folder + ".zip")
