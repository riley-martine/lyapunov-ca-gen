#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import os
import plotly.plotly as py

temp_files = []
files = []

py.sign_in("JoshAbrams","5Fre9yLErYpWQyb38zsQ")

for file in os.listdir('.'):
    if file.endswith('errors'):
        temp_files.append(file)
for i in temp_files:
    if files == []:
        files.append([i.split('.')[0]])
    elif i.split('.')[0] != files[-1][0]:
        files.append([i.split('.')[0]])
    else:
        files[-1].append(i)
for i in files:
    i.pop(0)

for fileset in files:
    data = [0 for k in range(2501)]
    for file in fileset:
        input_pipe = open(file,'r')
        errors = input_pipe.readlines()
        err_padded = ['{line:0^{width}}'.format(line=line,width=2501) for line in errors]
        for step in err_padded:
            for k in range(len(step)):
                if step[k] == '1':
                    data[k] += 1
        input_pipe.close()
    temp_array = []
    for i in range(len(data)):
        temp_array.extend([i-1250]*data[i])
    array = np.array(temp_array)
    plt.hist(array, bins=np.arange(-1250,1251,10))
    plt.title("Lyapunov Profile for Rule " + str(fileset[0].split('.')[0]))
    plt.xlabel("Cell Position")
    plt.ylabel("Defect Frequency")

    fig = plt.gcf()

    plot_url = py.plot_mpl(fig)
    print(plot_url)
