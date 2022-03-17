from time import time
import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyfftw

#plot用の変数
CSVpath = ""

# GUIがぼやける現象を防ぐための関数
def make_dpi_aware():
  import ctypes
  import platform
  if int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
#make_dpi_aware()


# 描画用の関数
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def loadCSV(targetCSV):
    npArray = np.genfromtxt(targetCSV, delimiter=",", encoding='utf8', dtype='float')
    x = npArray.T[0]
    y = npArray.T[1]
    ax.plot(x, y, alpha=0.4)
    runFFT(y)

def runFFT(timeData):
    print(len(timeData))
    a = pyfftw.empty_aligned(len(timeData), dtype='complex128', n=16)
    a[:] = timeData + 0j
    b = pyfftw.interfaces.numpy_fft.fft(a)
    c = np.fft.fft(a)
    ax2.plot(abs(c)/len(timeData)*2, alpha=0.4)
    ax2.set_xlim(0, 5)
    np.allclose(b, c)

frameTime = [[sg.Canvas(key='-CANVAS-', size=(400, 300))],
             [sg.Slider(range=(1, 100), default_value=1, resolution=1, orientation='h', size=(34.3, 15), enable_events=True, key='slider')]]
frameFreq = [[sg.Canvas(key='-CANVAS2-', size=(400, 300))],
             [sg.Slider(range=(1, 100), default_value=1, resolution=1, orientation='h', size=(34.3, 15), enable_events=True, key='slider2')]]

# レイアウト作成
mainWindow = [[sg.Text("ファイル選択"), sg.Input(key="-FILEPATH-", enable_events=True), sg.FileBrowse( file_types = (('*.csv', '*.CSV'),))],
              [sg.Frame(title='Waveform', layout=frameTime, border_width=7, element_justification='left'), sg.Frame(title='FFT', layout=frameFreq, border_width=7, element_justification='left')],
              [sg.Button("Run", key='-RUN-', disabled=True), sg.Button("Clear")]]

subWindow = [[sg.Text('Embed Matplotlib Plot')]]

layout = [[sg.Column(mainWindow),
          sg.Column(subWindow)]]

# windowを作成する．finalize=Trueにする必要がある．
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True, element_justification='left', size=(1200, 800))

# 埋め込む用のfigを作成する．
plt.rcParams["font.size"] = 6
plt.tight_layout()
fig = plt.figure(figsize=(4,3))
fig.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.95, wspace=0.15, hspace=0.15)
ax = fig.add_subplot(111)
ax.set_ylim(-2, 2)
fig2 = plt.figure(figsize=(4,3))
fig2.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.95, wspace=0.15, hspace=0.15)
ax2 = fig2.add_subplot(111)
ax2.set_ylim(0, 2)

# figとCanvasを関連付ける．
fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
fig_agg2 = draw_figure(window['-CANVAS2-'].TKCanvas, fig2)

# イベントループ
while True:
    event, values = window.read()
    print(event)

    if event in (None, "Cancel"):
        break

    elif event == "-RUN-":
        loadCSV(values["-FILEPATH-"])
        # 変更を加えたあと，fig_agg.draw()で変更を反映させる．
        fig_agg.draw()
        fig_agg2.draw()
    
    elif event == "Clear":
        ax.cla()
        ax2.cla()
        fig_agg.draw()
        fig_agg2.draw()

    elif event == "-FILEPATH-":
        window.find_element('-RUN-').Update(disabled=False)

    elif event == "slider":
        ax.set_xlim(0, values["slider"])
        fig_agg.draw()

    elif event == "slider2":
        ax2.set_xlim(0, values["slider2"])
        fig_agg2.draw()

# ウィンドウを閉じる．
window.close()