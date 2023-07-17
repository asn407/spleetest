import os
import subprocess as cmd
import tkinter
import threading
from tkinter import ttk
from tkinter import filedialog
from yt_dlp import YoutubeDL
from spleeter.separator import Separator
import tkinter.font as f

def local_clicked():
    fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    txt_1.insert(tkinter.END, "local_song")
    txt_2.insert(tkinter.END, filepath)
    
def running():
    subwin = tkinter.Toplevel()
    subwin.geometry("600x30")
    subwin.title('なうろ～でぃんぐ...（数分かかる場合があります）')
    pb=ttk.Progressbar(subwin,maximum=100,mode="indeterminate",variable=tkinter.IntVar())
    pb.pack()
    pb.start(interval=10)

    def download():
        url = txt_1.get()
        name = txt_2.get()
        filename = name + '.mp3'
        ydl_opts = {'format':'bestaudio[ext=mp3]/bestaudio[ext=m4a]/bestaudio','outtmpl':filename}
        
        if url != "local_song":
            with YoutubeDL(ydl_opts) as ydl:
                result = ydl.download([url])
                print(result)
        else:
            filename = name

        if bln4.get():
            args = "spleeter separate -o ./ -p spleeter:4stems \"" + filename + "\""
        elif bln5.get():
            args = "spleeter separate -o ./ -p spleeter:5stems \"" + filename + "\""
        else:
            args = "spleeter separate -o ./ \"" + filename + "\""

        p = cmd.Popen(args)

        try:
            outs, errs = p.communicate()
        except cmd.TimeoutExpired:
            pass
        else:
            p.terminate()
            subwin.destroy()
            finbtn = tkinter.Button(tki, text='終了', command=quit)
            finbtn.place(x=340, y=400)

    th1 = threading.Thread(target=download)
    th1.start()

version = "version : beta 1.0.0"

# 画面作成
tki = tkinter.Tk()
tki.geometry('640x480')
tki.title('すぷり～てすと')

# ウィンドウ左側の入力画面設定
title = tkinter.Label(text="すぷり～てすと", font=("MSゴシック", "50", "bold", "italic"))
title.place(x=80, y=30)
lbl_1 = tkinter.Label(text='URL : ')
lbl_1.place(x=30, y=200)
lbl_2 = tkinter.Label(text='Title : ')
lbl_2.place(x=30, y=230)
txt_1 = tkinter.Entry(width=20)
txt_1.place(x=90, y=200)
txt_2 = tkinter.Entry(width=20)
txt_2.place(x=90, y=230)

# ウィンドウ右側のチェックボックス設定
bln2 = tkinter.BooleanVar()
bln2.set(True)
bln4 = tkinter.BooleanVar()
bln4.set(False)
bln5 = tkinter.BooleanVar()
bln5.set(False)
# blnini = tkinter.BooleanVar()
# blnini.set(False)
chk2 = tkinter.Checkbutton(tki, variable=bln2, text='2つの楽器に分類（ボーカル / その他）')
chk2.place(x=280, y=170)
chk4 = tkinter.Checkbutton(tki, variable=bln4, text='4つの楽器に分類（ボーカル / ドラム / ベース / その他）')
chk4.place(x=280, y=200)
chk5 = tkinter.Checkbutton(tki, variable=bln5, text='5つの楽器に分類（ボーカル / ドラム / ベース / ピアノ / その他）')
chk5.place(x=280, y=230)
# chkini = tkinter.Checkbutton(tki, variable=blnini, text='初めて起動する場合はチェックを入れてください')
# chkini.place(x=280, y=260)

# 注意書き
lbl_a = tkinter.Label(text='※注意※')
lbl_a.place(x=30, y=330)
lbl_b = tkinter.Label(text='・当ソフトを使用して生じた不具合、不利益、損害等については、一切の責任を負いません')
lbl_b.place(x=30, y=350)
lbl_c = tkinter.Label(text='・使用する楽曲の著作権を侵害する行為は禁止とします（例 楽曲の違法なダウンロード、違法なアップロード）')
lbl_c.place(x=30, y=370)
lbl_v = tkinter.Label(text=version)
lbl_v.place(x=500, y=450)

# 参照ボタン
local = tkinter.Button(tki, text='ろ～かる', command=local_clicked)
local.place(x=30, y=260)
lbl_local = tkinter.Label(text='ローカルに保存してある楽曲を使用')
lbl_local.place(x=90, y=265)

# 実行ボタン
btn = tkinter.Button(tki, text='Do!!', command=running)
btn.place(x=300, y=400)

# 画面をそのまま表示
tki.mainloop()