#!/usr/bin/env python3

from hashlib import md5, sha1, sha256
from os import listdir, path

import argparse as ap

def find_all_files(file_lst):
    acc = list()
    children = list()

    for f in file_lst:
        if not (f == '.' or f == '..'): 
            if path.isfile(f):
                acc.append(f)
            elif path.isdir(f):
                children += [ "{}/{}".format(f, subf) for subf in listdir(f) ]
    
    if children:
        return acc + find_all_files(children)
    else:
        return acc
            
def hashlist(file_lst):
    h_lst = list()
    BUFF = 65536

    for f in file_lst:
        m = md5()
        s1 = sha1()
        s256 = sha256()

        with open(f, 'rb') as f_bytes:
            while True:
                data = f_bytes.read(BUFF)

                if not data:
                    break
                m.update(data)
                s1.update(data)
                s256.update(data)
        h_lst.append((m.hexdigest(), s1.hexdigest(), s256.hexdigest()))
    return h_lst
