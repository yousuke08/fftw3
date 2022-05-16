import os,shutil,locale,json,io,csv
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pyfftw
import matplotlib.ticker as ptick
from matplotlib.ticker import ScalarFormatter

freq = 5

class data:
    dataLen = 0
    samplingTime = 0.0

    def __init__(self, dataFilePath):
        self.waveData = np.loadtxt(dataFilePath, encoding='utf_8_sig')
        self.dataLen = len(self.waveData)

    def refreshTimeData(self):
        self.timeData = [self.samplingTime * i for i in range(self.dataLen)]

    def refreshFreqData(self):
        #self.ordeData = [self.samplingTime * i for i in range(self.dataLen)]
        self.freqData = [1.0/self.samplingTime/self.dataLen * i for i in range(self.dataLen)]

    def makeWaveFig(self):
        self.waveFig = plt.figure(dpi=100, figsize=(4, 3))
        self.waveFig.subplots_adjust(top=0.98, right=0.98, bottom=0.15)
        self.waveAx = self.waveFig.add_subplot(111)
        #self.waveAx.plot(self.timeData, self.waveData, marker='.')
        self.waveAx.scatter(self.timeData, self.waveData, marker='.')
        self.waveAx.set_xlim(0, self.dataLen * self.samplingTime)
        self.waveAx.xaxis.set_major_locator(ptick.MaxNLocator(5))
        self.waveAx.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
        self.waveAx.ticklabel_format(style="sci", axis="x", scilimits=(0, 0))

    def makeFreqFig(self):
        self.freqFig = plt.figure(dpi=100, figsize=(4, 3))
        self.freqFig.subplots_adjust(top=0.98, right=0.98, bottom=0.15)
        self.freqAx = self.freqFig.add_subplot(111)
        self.freqAx.xaxis.set_major_locator(ptick.MaxNLocator(5))
        self.freqAx.set_xlim(0, (self.dataLen) / 2.0)
        self.freqAx.scatter(self.freqData, self.freqDataAbs, marker='.')

    def drawWaveFig(self):
        if window['-waveCanvas-'].TKCanvas.children:
            for child in window['-waveCanvas-'].TKCanvas.winfo_children():
                child.destroy()
        figureCanvasAgg = FigureCanvasTkAgg(self.waveFig, master=window['-waveCanvas-'].TKCanvas)
        figureCanvasAgg.draw()
        figureCanvasAgg.get_tk_widget().pack(side='left', fill='both', expand=2)

    def drawFreqFig(self):
        if window['-freqCanvas-'].TKCanvas.children:
            for child in window['-freqCanvas-'].TKCanvas.winfo_children():
                child.destroy()
        figureCanvasAgg = FigureCanvasTkAgg(self.freqFig, master=window['-freqCanvas-'].TKCanvas)
        figureCanvasAgg.draw()
        figureCanvasAgg.get_tk_widget().pack(side='left', fill='both', expand=2)

    def runFFT(self):
        a = pyfftw.empty_aligned(self.dataLen, dtype='complex128', n=16)
        #変数に値を代入
        a[:] = self.waveData
        b  = pyfftw.interfaces.numpy_fft.fft(a)
        self.compFreqData = np.fft.fft(a)
        self.freqDataAbs = np.abs(self.compFreqData)/(self.dataLen)
        self.freqDataAng = np.angle(self.compFreqData, deg=True)
    
    def exportCSV(self):
        np.savetxt('./output.csv', np.stack([np.array(self.freqData), self.freqDataAbs]).T, delimiter=',')
        



sg.theme('Light Blue 2')

#frameTime = [[sg.Image(filename='', key='-imageTime-', size=(400, 300))]]
frameTime = [[sg.Canvas(key='-waveCanvas-', size=(400, 300))]]
frameFreq = [[sg.Canvas(key='-freqCanvas-', size=(400, 300))],[sg.Text('表示最大振幅'), sg.InputText(key='-ampRange-', enable_events=True, justification='right', size=(5,1)), sg.Button('Apply', key='-reloadAmpRange-', disabled=True), sg.Text('表示最大周波数'), sg.InputText(key='-freqRange-', enable_events=True, justification='right', size=(5,1)), sg.Button('Apply', key='-reloadFreqRange-', disabled=True)]]

layout = [[sg.Text('Ver_0.1', justification='right')],
          [sg.Text("ファイル選択"), sg.InputText(key="-FILEPATH-", enable_events=True), sg.FileBrowse()],
          [sg.Text('サンプリング周波数[us]'), sg.InputText(key='-SETTS-', enable_events=True, disabled=True), sg.Button('Run', key='-RUN-', disabled=True)],
          [sg.Table([[0, 0], [0, 0]], ['Time', 'Data'], num_rows=18), sg.Frame(title='Waveform', layout=frameTime, border_width=7), sg.Frame(title='FFT', layout=frameFreq, border_width=7)],
          [sg.Button('CSVで保存', disabled=True, key='-saveCSV-'), sg.Cancel('Close',key='Cancel')],
         ]

window = sg.Window('FFT', layout, size=(1000,600), return_keyboard_events=True)

while True:
    event, values = window.read()

    if event in (None, 'Cancel'):
        break
    
    elif event == '-FILEPATH-':
        print(values['-FILEPATH-'])
        simpleSin = data(values['-FILEPATH-'])
        window.find_element('-SETTS-').Update(disabled=False)

    elif event == '-SETTS-':
        simpleSin.samplingTime = values['-SETTS-']
        window.find_element('-RUN-').Update(disabled=False)
    
    elif event == '-RUN-':
        simpleSin.samplingTime = float(values['-SETTS-'])*1e-6
        simpleSin.refreshTimeData()
        simpleSin.refreshTimeData()
        simpleSin.makeWaveFig()
        simpleSin.runFFT()
        simpleSin.refreshFreqData()
        simpleSin.makeFreqFig()
        window['-waveCanvas-'].update(data=simpleSin.drawWaveFig())
        window['-freqCanvas-'].update(data=simpleSin.drawFreqFig())
        window.find_element('-saveCSV-').Update(disabled=False)
    
    elif event == '-freqRange-':
        window.find_element('-reloadFreqRange-').Update(disabled=False)

    elif event == '-ampRange-':
        window.find_element('-reloadAmpRange-').Update(disabled=False)

    elif event == '-reloadFreqRange-':
        simpleSin.freqAx.set_xlim(0, int(values['-freqRange-']))
        window['-freqCanvas-'].update(data=simpleSin.drawFreqFig())

    elif event == '-reloadAmpRange-':
        simpleSin.freqAx.set_ylim(0, int(values['-ampRange-']))
        window['-freqCanvas-'].update(data=simpleSin.drawFreqFig())

    elif event == '-saveCSV-':
        simpleSin.exportCSV()


window.close()