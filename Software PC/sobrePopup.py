import util
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class SobrePopup:

    def __init__(self, father):

        self.father = father

        exam = util.getExam()

        widthWindowControl = 300
        heightWindowControl = 200
        yControl = 100
        xControl = int(exam['monitorWidth']/2)

        self.window = Toplevel()
        self.window.title("Sobre")
        self.window.minsize(widthWindowControl, heightWindowControl)
        self.window.geometry('{}x{}+{}+{}'.format(widthWindowControl, heightWindowControl, xControl, yControl))
        self.window.resizable(False, False)
        self.window.config(padx=5, pady=5)

        # Para deixar a janela principal inativa
        self.window.transient(self.father.window)
        self.window.focus_force()
        self.window.grab_set()

        root = Frame(self.window)
        root.pack(fill="both", expand="True")

        Label(root, text="Sonre").pack()

        self.window.protocol("WM_DELETE_WINDOW", self._close)
        self.window.mainloop()

    def _close(self):

        self.father.flagPopup = False

        # Fecha a janela
        self.window.destroy()