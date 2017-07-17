#!/usr/bin/env pysketch

""" Cut the lines of very long files """

fin = None
fout = None
l = 0

def setup(filename, length: int, output = None):
    global fin, fout, l
    fin = open(filename, 'r')
    if not output:
        output = "{}.{}.cut".format(filename,length)
    fout = open(output, 'w')
    l = length

def loop():
    global fin, fout, l
    line = fin.readline()[:l]
    if line == '':
        exit()
    if line[-1] != '\n':
        line += '\n'
    fout.write(line)

def cleanup():
    global fin, fout
    fin.close()
    fout.close()
