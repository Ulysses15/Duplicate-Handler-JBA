import sys
import os
import hashlib
args = sys.argv


def files_list(arg_path):  # the function returns a dictionary (key = path : value = size) and the sorting option
    files_dictionary = {}
    s_options = ''
    options = ["1. Descending", "2. Ascending"]
    if len(arg_path) != 2:
        print("Directory is not specified")
    else:
        path = str(arg_path[1])
        print("Enter file format:")
        f_format = input()
        print("Size sorting options:")
        print(options[0])
        print(options[1])
        print()
        print("Enter a sorting option:")
        cycle = True
        while cycle:
            s_options = input()
            if s_options not in ("1", "2"):
                print("Wrong option")
                print()
                print("Enter a sorting option:")
            else:
                for root, dirs, files in os.walk(path, topdown=True):  # get the full path of files in the directory
                    for name in files:
                        if ('.' + f_format) in name:
                            size_f = os.path.getsize(os.path.join(root, name))
                            path_f = os.path.join(root, name)
                            new_entry = {path_f: size_f}
                            files_dictionary.update(new_entry)
                cycle = False  # cycle control
    return files_dictionary, s_options


def duplicate_set(my_files):
    my_files_list = []
    duplicates = []
    for si in my_files.values():
        my_files_list.append(si)
    for ik in my_files_list:
        if my_files_list.count(ik) > 1:
            duplicates.append(ik)
    return set(duplicates)


def file_hashing(file):
    with open(file, 'rb') as file_test:
        m = hashlib.md5()
        content = file_test.read()
        m.update(content)
        return m.hexdigest()


def asking_for_check():
    chi = True
    yes_no = ['yes', 'no']
    while chi:
        print()
        print("Check for duplicates?")
        check = input()
        # check = 'yes'
        if check not in yes_no:
            print('Wrong option')
            print()
        elif check == yes_no[1]:
            chi = False
        else:
            return True


def asking_for_delete():
    chi = True
    yes_no = ['yes', 'no']
    while chi:
        print()
        print("Delete files?")
        check = input()
        if check not in yes_no:
            print('Wrong option')
            print()
        elif check == yes_no[1]:
            chi = False
        else:
            print()
            return True


def flipping(ini_dict):
    flipped_total = {}
    for xk, y in ini_dict.items():
        flipped = {}
        new_item1 = {xk: flipped}
        flipped_total.update(new_item1)
        for key1, value1 in y.items():
            if value1 not in flipped:
                flipped[value1] = [key1]
            else:
                flipped[value1].append(key1)
    return flipped_total


def format_checking(list_to_delete):
    while True:
        print()
        print("Enter file numbers to delete:")
        files_to_delete = list(input().split())
        if all([item.isdigit() for item in files_to_delete]) is False:
            print("Wrong format")
        elif len(files_to_delete) > len(list_to_delete):
            print("Wrong format")
        elif all([int(jj) <= len(list_to_delete) for jj in files_to_delete]) is False:
            print("Wrong format")
        elif all([int(ll) > 0 for ll in files_to_delete]) is False:
            print("Wrong format")
        elif len(set(files_to_delete)) != len(files_to_delete):
            print("Wrong format")
        elif len(files_to_delete) == 0:
            print("Wrong format")
        else:
            return files_to_delete


dic_files, sorting = files_list(args)  # the dictionary {path: size}
duplicates_1 = list(duplicate_set(dic_files))
if sorting == '2':
    duplicates_1.sort()
else:
    duplicates_1.sort(reverse=True)
file_hash = {}
for ii in duplicates_1:
    print(ii, 'bytes')
    file_hash_1 = {}
    new_item_total = {ii: file_hash_1}
    file_hash.update(new_item_total)
    for key, value in dic_files.items():
        if value == ii:
            new_item = {key: file_hashing(key)}
            file_hash_1.update(new_item)
            print(key)

duplicate_list = []
if asking_for_check() is True:
    k = flipping(file_hash)
    i = 1
    for key_1, val_1 in k.items():
        print()
        print(key_1, 'bytes')
        for key_2, val_2 in val_1.items():
            if len(val_2) > 1:
                print("Hash:", key_2)
                for x in val_2:
                    print(str(i) + '.', x)
                    duplicate_list.append(x)
                    i += 1

if asking_for_delete() is True:
    numbers_file = format_checking(duplicate_list)
    size = 0
    for h in numbers_file:
        size += int(os.path.getsize(duplicate_list[int(h) - 1]))
        os.remove(duplicate_list[int(h) - 1])
    print()
    print("Total freed up space:", size, "bytes")
