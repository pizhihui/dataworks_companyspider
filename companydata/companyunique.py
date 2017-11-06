# -*- coding: utf-8
import os
import locale


def main():
    file_path_src = os.getcwd() + "/allcompaydata_origin.txt"
    file_path_trg = os.getcwd() + "/allcompaydata_final.txt"

    file_trg = open(file_path_trg, 'w')

    locale.setlocale(locale.LC_COLLATE, 'zh_CN.UTF-8')

    with open(file_path_src, 'r') as f:
        proxies = f.readlines()
        s = set(proxies)
        li = list(s)
        li.sort()
        file_trg.writelines(li)


if __name__ == "__main__":
    main()
