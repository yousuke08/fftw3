import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

# レイアウト作成
layout = [[sg.Text('Embed Matplotlib Plot')],
          [sg.Canvas(key='-CANVAS-')],
          [sg.Button("Add"), sg.Button("Clear")]]

# windowを作成する．finalize=Trueにする必要がある．
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True, element_justification='center', font='Monospace 18')

# 埋め込む用のfigを作成する．
fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111)
ax.set_ylim(-10, 10)

# figとCanvasを関連付ける．
fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

# イベントループ
while True:
    event, values = window.read()
    print(event, values)
    # sg.Print(event, values)

    if event in (None, "Cancel"):
        break

    elif event == "Add":
        # 適当なプロット用データ作成
        t = np.linspace(0, 7, 100)
        afreq = np.random.randint(1, 10)
        amp = np.random.randint(1, 10)
        y = amp * np.sin(afreq * t)

        # プロット
        ax.plot(t, y, alpha=0.4)

        # 変更を加えたあと，fig_agg.draw()で変更を反映させる．
        fig_agg.draw()

    elif event == "Clear":
        ax.cla()
        fig_agg.draw()

# ウィンドウを閉じる．
window.close()