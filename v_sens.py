import sys
import os
import glob
import numpy as np

fft_count=64
sens_count=128

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

def fft_readDataSource(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    return lines

#separate FFT data for 13kg and 27kg, store data at separate file
#generate output filename with TOP, SIDE and index
def preprocess_files(flist):

    side_cnt = -1
    top_cnt = -1
    right_cnt = -1
    left_cnt = -1
    gen_file_list = []

    for name in flist:
        pos = []
        f_gen_name = []
        f_date = name.split('-')[0]

        if name.find("SIDE") != -1:
            side_cnt = side_cnt + 1
            f_name = "SIDE_$_" + f_date + "_" + str(side_cnt)
        elif name.find("TOP") != -1:
            top_cnt = top_cnt + 1
            f_name = "TOP_$_" + f_date + "_" + str(top_cnt)
        elif name.find("RIGHT") != -1:
            right_cnt = right_cnt + 1
            f_name = "RIGHT_$_" + f_date + "_" + str(right_cnt)
        elif name.find("LEFT") != -1:
            left_cnt = left_cnt + 1
            f_name = "LEFT_$_" + f_date + "_" + str(left_cnt)

        #print(f_name)

        # find >LOAD and KGF in line
        lines = fft_readDataSource(name)
        for line in lines:
            #if line.find("LOAD ") != -1:
            if "LOAD" in line:
                pos.append(lines.index(line))
                gen_file_list.append(f_name + "_" + line.split(' ')[-1].strip() + ".txt")
                f_gen_name.append(gen_file_list[-1])

        pos.append(len(lines)) # add last line of file
        # print(pos)
        # print(len(pos))

        #print(f_gen_name)
        # if len(pos) != 2:
        #     print("LOAD is not enough!")
        #     return []

        index=0
        for f_gen in f_gen_name:
            fp = open(f_gen, 'w')
            for line in lines[pos[index]:pos[index+1]]:
                fp.write(line)
            fp.close()
            print(f_gen, index)
            if index == len(pos)-1:
                break
            index += 1

        # index = len(pos)-1
        # fp = open(f_gen_name[index], 'w')
        # for line in lines[pos[index]:]:
        #     fp.write(line)
        # fp.close()
        # print(f_gen, index)

    return gen_file_list


def fft_genFilename(filename):
    out_file = []
    out_file.append(filename.replace("$_", "x_20"))
    out_file.append(filename.replace("$_", "y_20"))
    out_file.append(filename.replace("$_", "z_20"))

    #print(out_file)
    return out_file


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

def sens_getDataCount(lines):
    count=0
    sens_lines = []
    for line in lines:
        if line.find("D=0") > -1:
            count = count+1

        if line[0] == 'D' and line[1] == '=':
            sens_lines.append(line)

    #print(len(fft_lines))
    return count, sens_lines

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


def sens_extractData(cnt, sens_lines, filename):
    sens_x = np.zeros((sens_count, cnt), dtype=np.int32)
    sens_y = np.zeros((sens_count, cnt), dtype=np.int32)
    sens_z = np.zeros((sens_count, cnt), dtype=np.int32)

    col = -1
    for line in sens_lines:
        if line[2] == '0' :
            col = col + 1

        s_data = line.split('\t')
        #print(fft)
        s_data[0] = s_data[0].replace("D=", " ").strip()
        row = int(s_data[0])
        s_data[3] = s_data[3].strip()
        #print(fft, col)

        sens_x[row, col] = int(s_data[1])
        sens_y[row, col] = int(s_data[2])
        sens_z[row, col] = int(s_data[3])

    sens_file = "AS_" + filename
    out_filename = fft_genFilename(sens_file)
    #print(out_filename)
    np.savetxt(out_filename[0], sens_x, fmt='%d', delimiter=' ')
    np.savetxt(out_filename[1], sens_y, fmt='%d', delimiter=' ')
    np.savetxt(out_filename[2], sens_z, fmt='%d', delimiter=' ')

if __name__ == '__main__':

    input_list = get_inputfile()
    process_list = preprocess_files(input_list)

    if process_list == []:
        exit(1)

    print(process_list)
    for input in process_list:
        #input = input_list[1]
        print(input)
        src = fft_readDataSource(input)

        count, fft_list = fft_getDataCount(src)
        print(count)

        fft_extractFFT(count, fft_list, input)

        count, sens_list = sens_getDataCount(src)
        print(count)

        sens_extractData(count, sens_list, input)

