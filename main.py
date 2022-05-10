import os,shutil,locale,json,io
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import pyfftw

freq = 5

def make_data_fig(data, type):

    fig = plt.figure(figsize=(4,3))
    # x = np.linspace(0, 2*np.pi, 500)
    x = np.arange(0, len(data))
    ax = fig.add_subplot(111)
    if type == 'Time':
        ax.plot(x, data, marker='.')
        ax.set_xlim(0,len(data))
    else:
        ax.plot(x, data, marker='.')
        ax.set_xlim(0,len(data)/2)
    return fig

def draw_plot_image(fig):
    item = io.BytesIO()
    plt.savefig(item, format='png')
    plt.clf()
    # plt.close('all')
    return item.getvalue()

sg.theme('Light Blue 2')

a = pyfftw.empty_aligned(128, dtype='complex128', n=16)
a[:] = [np.sin(freq*np.pi*2*i/128)+np.sin(freq*3*np.pi*2*i/128) for i in range(128)]
b = pyfftw.interfaces.numpy_fft.fft(a)
c = np.fft.fft(a)
np.allclose(b, c)

var = [[x + 9 * y for x in range (9)] for y in range (10)]
name = [chr(65+x) for x in range (9)]
aDis = [[0 for i in range(2)] for j in range(len(a))]

for i in range(len(a)):
    aDis[i][0] = i
    aDis[i][1] = round(a.real[i], 2)

frameTime = [[sg.Image(filename='', key='-imageTime-', size=(400,300))]]
frameFreq = [[sg.Image(filename='', key='-imageFreq-', size=(400,300))]]

layout = [[sg.Text('My one-shot window.')],
          [sg.Text("ファイル選択"), sg.InputText(), sg.FileBrowse(key="-FILES-")],
          [sg.Text('入力欄'), sg.In(key='-IN-'), sg.Button('Read', key='-ok-')],
          [sg.Button('Display',key='-display-'), sg.Cancel('Close',key='Cancel')],
          [sg.Table(aDis, ['Time', 'Data'], num_rows=25), sg.Frame(title='Waveform', layout=frameTime, border_width=7), sg.Frame(title='FFT', layout=frameFreq, border_width=7)],
         ]

window = sg.Window('Window Title', layout, size=(1200,800))

while True:
    event, values = window.read()

    if event in (None, 'Cancel'):
        break

    elif event == '-display-':
        figTime = make_data_fig(a.real, 'Time')
        figTimeBytes = draw_plot_image(figTime)
        figFreq = make_data_fig(np.abs(b), 'Freq')
        figFreqBytes = draw_plot_image(figFreq)
        window['-imageTime-'].update(data=figTimeBytes)
        window['-imageFreq-'].update(data=figFreqBytes)
    
    elif event == '-ok-':
        print(values['-IN-'].split)

    elif event == '-FILES-':
        print(values['-FILES-'])

window.close()