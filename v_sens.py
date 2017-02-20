import sys
import os
import glob
import numpy as np

fft_count=64

file_prefix = ["fft_x_20", "fft_y_20", "fft_z_20"]

def get_inputfile():
    flist = []
    path = os.getcwd()
    pathname =  path + "\*.txt"
    #print(pathname)
    txt_list = glob.glob(pathname)
    #print(txt_list)
    for name in txt_list:
        txt_name = name.replace(path + "\\", " ").strip()
        flist.append(txt_name)

    #print(flist)
    return flist

def fft_genFilename(filename):
    out_file = []
    out_file.append(file_prefix[0] + filename)
    out_file.append(file_prefix[1] + filename)
    out_file.append(file_prefix[2] + filename)

    #print(out_file)
    return out_file

def fft_readDataSource(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    return lines

def fft_getDataCount(lines):
    count=0
    fft_lines = []
    for line in lines:
        if line.find("F=0") > -1:
            count = count+1

        if line[0] == 'F' and line[1] == '=':
            fft_lines.append(line)

    #print(len(fft_lines))
    return count, fft_lines

def fft_extractFFT(cnt, fft_lines, filename):
    fft_x = np.zeros((fft_count, cnt), dtype=np.int32)
    fft_y = np.zeros((fft_count, cnt), dtype=np.int32)
    fft_z = np.zeros((fft_count, cnt), dtype=np.int32)

    col = -1
    for line in fft_lines:
        if line[2] == '0' :
            col = col + 1

        fft = line.split('\t')
        #print(fft)
        fft[0] = fft[0].replace("F=", " ").strip()
        row = int(fft[0])
        fft[3] = fft[3].strip()
        #print(fft, col)

        fft_x[row, col] = int(fft[1])
        fft_y[row, col] = int(fft[2])
        fft_z[row, col] = int(fft[3])

    out_filename = fft_genFilename(filename)
    #print(out_filename)
    np.savetxt(out_filename[0], fft_x, fmt='%d', delimiter=' ')
    np.savetxt(out_filename[1], fft_y, fmt='%d', delimiter=' ')
    np.savetxt(out_filename[2], fft_z, fmt='%d', delimiter=' ')


if __name__ == '__main__':

    input_list = get_inputfile()
    #print(input_list)
    for input in input_list:
        #input = input_list[1]
        print(input)
        src = fft_readDataSource(input)

        count, fft_list = fft_getDataCount(src)
        print(count)

        fft_extractFFT(count, fft_list, input)

