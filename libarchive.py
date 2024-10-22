import os
from datetime import datetime
import shutil
import zipfile
import re


def check_counter(path):
    filename = 'counter_' + datetime.now().strftime('%d%m%Y') + '.txt'
    print(f"Путь: {path}")

    try:
        os.chdir(path)
        os.chdir("..//")
        with open(filename, 'a') as f:
            f.write(str(datetime.now()) + ' Архив создан по пути: ' + path + '\n')
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
        return -1

    # количество строк в файле
    counter = sum(1 for line in open(filename, 'r'))
    os.chdir(path)
    return counter


def archive(path, arh_date):
    os.chdir(path)
    mydir = os.path.abspath(os.curdir)
    print(mydir + " step 1")

    listdir_r = [rootdirs for rootdirs in os.listdir(mydir) if os.path.isdir(rootdirs)]
    for rootdirs in listdir_r:
        s = rootdirs.split()
        if s[0].isdigit() == True:
            print("Инн извлечен" + "\n" + s[0])
            inn2 = s[0]

            os.chdir(mydir + "\\" + rootdirs)
            rootdirs = mydir + "\\" + rootdirs
            rootdirs = os.path.abspath(os.curdir)

            res = RenameFiles(inn2, rootdirs)
            if res != 0:
                os.chdir(path)
                return res

    # Формирование конечного архива
    arh_name = "2551_" + str(arh_date) + "_" + str(check_counter(path)) + ".zip"
    z = zipfile.ZipFile(mydir + "\\" + arh_name, 'w')

    for root, dirs, files in os.walk(mydir):
        for file in files:
            if file.endswith('.zip') and root != mydir:
                print(root)
                os.chdir(root)
                z.write(file)
                os.remove(file)

    z.close()
    os.chdir(path)
    return 0


def RenameFiles(inn, mydir):
    cb_codes = ['kd', 'ps', 'ur', 'bl', 'pu', 'rs', 'cd', 'ov', 'zb', 'vs', 'ss', 'vd', 'dc', 'cl', 'di', 'ds']
    cb_codes2 = ['kd', 'ps', 'ur', 'bl', 'pu', 'rs', 'cd', 'ov', 'zb', 'vs', 'vd', 'dc', 'cl', 'di', 'ds']

    mle = len(inn)
    list_inn = list(inn)

    print(mle)
    print(mydir)
    listfiles = [f for f in os.listdir(mydir) if os.path.isfile(f)]
    for f in listfiles:
        count_dot = f.count('.')
        print(f)
        z = list(f)
        y = z[0:mle]
        #Добавлем инн, если нет
        if y != list_inn:
            new_filename = inn + "_" + f
            new_filename_2 = new_filename
            new_filename = os.path.join(mydir, new_filename)
            old_filename = os.path.join(mydir, f)
            os.rename(old_filename, new_filename)
            f = new_filename_2
        #Замена точки на _
        if count_dot == 2:
            old_filename = os.path.join(mydir, f)
            f = f.replace(".", "_", 1)
            new_filename = os.path.join(mydir, f)
            os.rename(old_filename, new_filename)
    listfiles = [f for f in os.listdir(mydir) if os.path.isfile(f)]
    for cb_code in cb_codes:
        counter_code = 1
        print("step1_")
        for f in listfiles:
            print("step_x " + f)

            if f.endswith('.zip'):
                return -1

            try:
                inn_ind = f.index("_")
            except ValueError:
                return -2
            part_inn = f[0:inn_ind]
            print(part_inn)
            print(inn_ind)
            print(f)
            part_after_inn = f[inn_ind + 1:]
            print(part_after_inn)

            dot_ind = part_after_inn.index(".")
            part_after_dot = part_after_inn[dot_ind:]
            print("step2_" + part_after_inn[:2] + " " + cb_code)
            if part_after_inn[:2] == cb_code:
                print("step3_in cicle")
                new_filename = part_inn + "_" + cb_code + "_zzz_" + str('{0:02}'.format(counter_code)) + part_after_dot
                print("step3" + new_filename)
                old_filename = os.path.join(mydir, f)
                new_filename = os.path.join(mydir, new_filename)
                os.rename(old_filename, new_filename)
                counter_code = counter_code + 1

    listfiles = [f for f in os.listdir(mydir) if os.path.isfile(f)]
    for f in listfiles:
        old_filename = os.path.join(mydir, f)
        f = f.replace("_zzz_", "_")
        new_filename = os.path.join(mydir, f)
        os.rename(old_filename, new_filename)

    listfiles = [f for f in os.listdir(mydir) if os.path.isdir(f)]
    couner_ss = 0
    for f in listfiles:
        # print (f)
        len_f = len(f)
        mysybdir = mydir + "\\" + f
        # print(f)
        #print(mysybdir)
        listfiles_sub = [f_subfile for f_subfile in os.listdir(mysybdir)]
        for f_subfile in listfiles_sub:
            # print(f_subfile)
            count_dot = f_subfile.count('.')
            #проверяем первые три цифры и переименовываем
            if re.match(r'\d\d\d.*', f_subfile):
                print(f_subfile + "matched")
                old_filename = os.path.join(mysybdir, f_subfile)
                print("zero_step " + f_subfile[0:4])
                f_subfile = f_subfile.replace(f_subfile[0:4], f)
                if re.match(r'.*\D\D\d.*', f_subfile):  #ищем с одной цифрой после двух и более не цифр
                    f_subfile = "-yyy-" + f_subfile
                    print("result file" + f_subfile)

                new_filename = os.path.join(mysybdir, f_subfile)
                os.rename(old_filename, new_filename)
                #print("odin_step "+ f_subfile)
            if count_dot == 2:
                #f_subfile.find('.')
                old_filename = os.path.join(mysybdir, f_subfile)
                f_subfile_repl = f_subfile.replace(".", "_", 1)
                new_filename = os.path.join(mysybdir, f_subfile_repl)
                os.rename(old_filename, new_filename)
                f_subfile = f_subfile_repl

            #замена цифр на двухзначные
            if re.match(r'.*_\d\.', f_subfile):
                print("this is file" + f_subfile)
                old_filename = os.path.join(mysybdir, f_subfile)
                count_ = f_subfile.count("_")
                if count_ > 1:
                    print("that is file" + f_subfile)
                    first_ = f_subfile.index("_", )
                    right_side = f_subfile[first_ + 1:]
                    left_side = f_subfile[:first_]
                    print(left_side, "+", right_side)
                    right_side = right_side.replace("_", "_0")
                    f_subfile = left_side + "_" + right_side
                if count_ == 1:
                    f_subfile = f_subfile.replace("_", "_0")

                new_filename = os.path.join(mysybdir, f_subfile)
                os.rename(old_filename, new_filename)

            if re.match(r'ss_.*', f_subfile):
                #  print("hi")
                couner_ss = 1 + couner_ss
                new_f_subfile = inn + "_ss_" + str('{0:02}'.format(couner_ss)) + ".xlsx"
                # print(new_f_subfile)
                old_filename = os.path.join(mysybdir, f_subfile)
                new_filename = os.path.join(mysybdir, new_f_subfile)
                os.rename(old_filename, new_filename)
                shutil.move(new_filename, mydir)

        listfiles_sub2 = [f_subfile for f_subfile in os.listdir(mysybdir)]
        for cb_code in cb_codes2:
            counter_code2 = 1
            for files in listfiles_sub2:
                dot_ind2 = files.index(".")
                part_after_dot2 = files[dot_ind2:]
                if files[0:2] == cb_code:
                    if re.match(r'.*\d.*', files):
                        new_filename = f + "_" + cb_code + "_zzz_" + str(
                            '{0:02}'.format(counter_code2)) + part_after_dot2
                        old_filename = os.path.join(mysybdir, files)
                        new_filename = os.path.join(mysybdir, new_filename)
                        os.rename(old_filename, new_filename)
                        counter_code2 = counter_code2 + 1
                    else:
                        new_filename = f + "_" + files
                        old_filename = os.path.join(mysybdir, files)
                        new_filename = os.path.join(mysybdir, new_filename)
                        os.rename(old_filename, new_filename)

        listfiles_sub2 = [f_subfile for f_subfile in os.listdir(mysybdir)]
        for files in listfiles_sub2:
            old_filename = os.path.join(mysybdir, files)
            files = files.replace("_zzz_", "_")
            new_filename = os.path.join(mysybdir, files)
            os.rename(old_filename, new_filename)

        listfiles_sub3 = [f_subfile for f_subfile in os.listdir(mysybdir)]
        for cb_code in cb_codes2:
            counter_code3 = 1
            for files in listfiles_sub3:
                if files[0:5] == "-yyy-":
                    code_ind = files.index("_", )
                    part_code = files[0:code_ind]
                    part_after_code = files[code_ind + 1:]
                    print("part after code" + part_after_code)
                    dot_ind2 = part_after_code.index(".")
                    part_after_dot = part_after_code[dot_ind2:]
                    if part_after_code[:2] == cb_code:
                        new_filename = part_code + "_" + cb_code + "_" + str(
                            '{0:02}'.format(counter_code3)) + part_after_dot
                        new_filename = new_filename[5:]
                        old_filename = os.path.join(mysybdir, files)
                        new_filename = os.path.join(mysybdir, new_filename)
                        os.rename(old_filename, new_filename)
                        counter_code3 = counter_code3 + 1

    os.chdir(mydir)
    listfiles = [f for f in os.listdir(mydir) if os.path.isfile(f)]
    z = zipfile.ZipFile(mydir + "\\" + inn + ".zip", 'w')

    for f in listfiles:
        print(f)
        z.write(f)
    z.close()

    listfiles = [f for f in os.listdir(mydir) if os.path.isdir(f)]

    for f in listfiles:
        mysybdir = mydir + "\\" + f
        z = zipfile.ZipFile(mydir + "\\" + f + ".zip", 'w')
        print(z)
        print(mysybdir)
        os.chdir(mysybdir)
        for root, dirs, files in os.walk(mysybdir):
            for file in files:
                print(file)
                z.write(file)
        z.close()

    return 0
