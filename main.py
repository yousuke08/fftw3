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
make_dpi_aware()

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
    a = pyfftw.empty_aligned(len(timeData), dtype='complex128', n=16)
    a[:] = timeData + 0j
    b = pyfftw.interfaces.numpy_fft.fft(a)
    c = np.fft.fft(a)
    ax2.plot(abs(c), alpha=0.4)
    np.allclose(b, c)

# レイアウト作成
mainWindow = [[sg.Text("ファイル選択"), sg.Input(key="-FILEPATH-", enable_events=True), sg.FileBrowse( file_types = (('*.csv', '*.CSV')))],
              [sg.Canvas(key='-CANVAS-'), sg.Canvas(key='-CANVAS2-')],
              [sg.Button("Run", key='-RUN-', disabled=True), sg.Button("Clear")]]

subWindow = [[sg.Text('Embed Matplotlib Plot')]]

layout = [[sg.Column(mainWindow, element_justification='c'),
          sg.Column(subWindow, element_justification='c')]]

# windowを作成する．finalize=Trueにする必要がある．
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True, element_justification='center', font='Monospace 18')

# 埋め込む用のfigを作成する．
fig = plt.figure(figsize=(4, 3))
ax = fig.add_subplot(111)
ax.set_ylim(-2, 2)
fig2 = plt.figure(figsize=(4, 3))
ax2 = fig2.add_subplot(111)
ax2.set_ylim(-10, 10)


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

# ウィンドウを閉じる．
window.close()