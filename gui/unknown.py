#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.22
#  in conjunction with Tcl version 8.6
#    May 20, 2019 11:32:16 PM +0800  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import unknown_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    unknown_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    unknown_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("667x730+321+0")
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.Tulpa = tk.Button(top)
        self.Tulpa.place(relx=0.015, rely=0.89, height=68, width=320)
        self.Tulpa.configure(activebackground="#ececec")
        self.Tulpa.configure(activeforeground="#000000")
        self.Tulpa.configure(background="#d9d9d9")
        self.Tulpa.configure(command=unknown_support.onBtnTulpaSays)
        self.Tulpa.configure(disabledforeground="#a3a3a3")
        self.Tulpa.configure(foreground="#000000")
        self.Tulpa.configure(highlightbackground="#d9d9d9")
        self.Tulpa.configure(highlightcolor="black")
        self.Tulpa.configure(pady="0")
        self.Tulpa.configure(text='''Carol''')

        self.Host = tk.Button(top)
        self.Host.place(relx=0.51, rely=0.89, height=68, width=320)
        self.Host.configure(activebackground="#ececec")
        self.Host.configure(activeforeground="#000000")
        self.Host.configure(background="#d9d9d9")
        self.Host.configure(command=unknown_support.onBtnHostSays)
        self.Host.configure(disabledforeground="#a3a3a3")
        self.Host.configure(foreground="#000000")
        self.Host.configure(highlightbackground="#d9d9d9")
        self.Host.configure(highlightcolor="black")
        self.Host.configure(pady="0")
        self.Host.configure(text='''Scrooge''')

        self.TulpaSays = tk.Entry(top)
        self.TulpaSays.place(relx=0.015, rely=0.808,height=47, relwidth=0.48)
        self.TulpaSays.configure(background="white")
        self.TulpaSays.configure(disabledforeground="#a3a3a3")
        self.TulpaSays.configure(font="TkFixedFont")
        self.TulpaSays.configure(foreground="#000000")
        self.TulpaSays.configure(highlightbackground="#d9d9d9")
        self.TulpaSays.configure(highlightcolor="black")
        self.TulpaSays.configure(insertbackground="black")
        self.TulpaSays.configure(selectbackground="#c4c4c4")
        self.TulpaSays.configure(selectforeground="black")

        self.HostSays = tk.Entry(top)
        self.HostSays.place(relx=0.51, rely=0.808,height=47, relwidth=0.48)
        self.HostSays.configure(background="white")
        self.HostSays.configure(disabledforeground="#a3a3a3")
        self.HostSays.configure(font="TkFixedFont")
        self.HostSays.configure(foreground="#000000")
        self.HostSays.configure(highlightbackground="#d9d9d9")
        self.HostSays.configure(highlightcolor="black")
        self.HostSays.configure(insertbackground="black")
        self.HostSays.configure(selectbackground="#c4c4c4")
        self.HostSays.configure(selectforeground="black")

        self.Dialog = tk.Text(top)
        self.Dialog.place(relx=0.015, rely=0.137, relheight=0.647
                , relwidth=0.975)
        self.Dialog.configure(background="white")
        self.Dialog.configure(font="TkTextFont")
        self.Dialog.configure(foreground="black")
        self.Dialog.configure(highlightbackground="#d9d9d9")
        self.Dialog.configure(highlightcolor="black")
        self.Dialog.configure(insertbackground="black")
        self.Dialog.configure(selectbackground="#c4c4c4")
        self.Dialog.configure(selectforeground="black")
        self.Dialog.configure(state='disabled')
        self.Dialog.configure(width=650)
        self.Dialog.configure(wrap="word")

        self.Export = tk.Button(top)
        self.Export.place(relx=0.015, rely=0.014, height=80, width=140)
        self.Export.configure(activebackground="#ececec")
        self.Export.configure(activeforeground="#000000")
        self.Export.configure(background="#d9d9d9")
        self.Export.configure(command=unknown_support.onExport)
        self.Export.configure(disabledforeground="#a3a3a3")
        self.Export.configure(foreground="#000000")
        self.Export.configure(highlightbackground="#d9d9d9")
        self.Export.configure(highlightcolor="black")
        self.Export.configure(pady="0")
        self.Export.configure(text='''Export As Txt''')

        self.Seq2Seq = tk.Button(top)
        self.Seq2Seq.place(relx=0.27, rely=0.014, height=40, width=140)
        self.Seq2Seq.configure(activebackground="#ececec")
        self.Seq2Seq.configure(activeforeground="#000000")
        self.Seq2Seq.configure(background="#d9d9d9")
        self.Seq2Seq.configure(command=unknown_support.onSeq2Seq)
        self.Seq2Seq.configure(disabledforeground="#a3a3a3")
        self.Seq2Seq.configure(foreground="#000000")
        self.Seq2Seq.configure(highlightbackground="#d9d9d9")
        self.Seq2Seq.configure(highlightcolor="black")
        self.Seq2Seq.configure(pady="0")
        self.Seq2Seq.configure(text='''AI Test''')

        self.CleanScreen = tk.Button(top)
        self.CleanScreen.place(relx=0.78, rely=0.014, height=40, width=140)
        self.CleanScreen.configure(activebackground="#ececec")
        self.CleanScreen.configure(activeforeground="#000000")
        self.CleanScreen.configure(background="#d9d9d9")
        self.CleanScreen.configure(command=unknown_support.onClean)
        self.CleanScreen.configure(disabledforeground="#a3a3a3")
        self.CleanScreen.configure(foreground="#000000")
        self.CleanScreen.configure(highlightbackground="#d9d9d9")
        self.CleanScreen.configure(highlightcolor="black")
        self.CleanScreen.configure(pady="0")
        self.CleanScreen.configure(text='''Clean Screen''')
        self.CleanScreen.configure(width=140)

        self.Data = tk.Button(top)
        self.Data.place(relx=0.27, rely=0.068, height=40, width=140)
        self.Data.configure(activebackground="#ececec")
        self.Data.configure(activeforeground="#000000")
        self.Data.configure(background="#d9d9d9")
        self.Data.configure(command=unknown_support.onDataGen)
        self.Data.configure(disabledforeground="#a3a3a3")
        self.Data.configure(foreground="#000000")
        self.Data.configure(highlightbackground="#d9d9d9")
        self.Data.configure(highlightcolor="black")
        self.Data.configure(pady="0")
        self.Data.configure(text='''Gen Data''')

        self.Answer = tk.Button(top)
        self.Answer.place(relx=0.525, rely=0.014, height=80, width=140)
        self.Answer.configure(activebackground="#ececec")
        self.Answer.configure(activeforeground="#000000")
        self.Answer.configure(background="#d9d9d9")
        self.Answer.configure(command=unknown_support.onAnswers)
        self.Answer.configure(disabledforeground="#a3a3a3")
        self.Answer.configure(foreground="#000000")
        self.Answer.configure(highlightbackground="#d9d9d9")
        self.Answer.configure(highlightcolor="black")
        self.Answer.configure(pady="0")
        self.Answer.configure(text='''Answers''')

        self.Soliloquize = tk.Button(top)
        self.Soliloquize.place(relx=0.78, rely=0.068, height=40, width=140)
        self.Soliloquize.configure(activebackground="#ececec")
        self.Soliloquize.configure(activeforeground="#000000")
        self.Soliloquize.configure(background="#d9d9d9")
        self.Soliloquize.configure(command=unknown_support.onSoliloquize)
        self.Soliloquize.configure(disabledforeground="#a3a3a3")
        self.Soliloquize.configure(foreground="#000000")
        self.Soliloquize.configure(highlightbackground="#d9d9d9")
        self.Soliloquize.configure(highlightcolor="black")
        self.Soliloquize.configure(pady="0")
        self.Soliloquize.configure(text='''Soliloquize''')

if __name__ == '__main__':
    vp_start_gui()





