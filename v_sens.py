import sys
import numpy as np

fft_lines = []
fft_count=64

out_file = ["fft_x_20", "fft_y_20", "fft_z_20"]

def fft_genFilename(filename):
    out_file[0] = out_file[0] + filename
    out_file[1] = out_file[1] + filename
    out_file[2] = out_file[2] + filename

    #print(out_file)

def fft_readDataSource():
    f = open(sys.argv[1], 'r')
    lines = f.readlines()
    f.close()

    return lines

def fft_getDataCount(lines):
    count=0
    for line in lines:
        if line.find("F=0") > -1:
            count = count+1

        if line[0] == 'F' and line[1] == '=':
            fft_lines.append(line)

    return count

def fft_extractFFT(count, filename):
    fft_x = np.zeros((fft_count, count), dtype=np.int32)
    fft_y = np.zeros((fft_count, count), dtype=np.int32)
    fft_z = np.zeros((fft_count, count), dtype=np.int32)

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

    fft_genFilename(sys.argv[1])

    np.savetxt(out_file[0], fft_x, fmt='%d', delimiter=' ')
    np.savetxt(out_file[1], fft_y, fmt='%d', delimiter=' ')
    np.savetxt(out_file[2], fft_z, fmt='%d', delimiter=' ')


if __name__ == '__main__':
    print(sys.argv[1])

    src = fft_readDataSource()

    count = fft_getDataCount(src)
    print(count)

    fft_extractFFT(count, sys.argv[1])

