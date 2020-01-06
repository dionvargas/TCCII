from builtins import print

import cv2
import util
import numpy as np

from emptyContainer import EmptyContainer
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from VerticalScrolledFrame import *

import matplotlib.pyplot as plt

class ResultadoContainer(EmptyContainer):

    cont = 0
    play = False

    def __init__(self, father, dir):
        super().__init__()

        self.father = father
        self.dir = dir

        self.exame = util.getExame(dir)

        self.relacao = 0.3

        # Array dos gráficos
        self.aChart1 = []
        self.aChart2 = []
        self.aChart3 = []

        self.pos = []
        self.area = []
        self.circularidade = []
        self.posX = []
        self.velX = []
        self.acelX = []
        self.posY = []
        self.velY = []
        self.acelY = []
        self.desEscalar = []
        self.velEscalar = []
        self.acelEscalar = []
        self.posA = []
        self.velA = []
        self.acelA = []

        self.numFrame = int(self.exame['t5'])
        self.frame_seq = int(self.exame["frames"])
        self.fps = int(self.exame["fps"])

        self.cap = cv2.VideoCapture(dir + "/exame.mp4")

        self.width = self.cap.get(3)
        self.height = self.cap.get(4)

        procDados = open(self.dir + "/dados.exa", "r")
        for linha in procDados:
            tmp = linha.split(";")
            self.pos.append(int(tmp[0]))
            self.area.append(float(tmp[1]))
            self.circularidade.append(float(tmp[2]))
            self.posX.append(int(tmp[3]))
            self.velX.append(int(tmp[4]))
            self.acelX.append(int(tmp[5]))
            self.posY.append(int(tmp[6]))
            self.velY.append(int(tmp[7]))
            self.acelY.append(int(tmp[8]))
            self.desEscalar.append(float(tmp[9]))
            self.velEscalar.append(float(tmp[10]))
            self.acelEscalar.append(float(tmp[11]))
            self.posA.append(int(tmp[12]))
            self.velA.append(int(tmp[13]))
            self.acelA.append(int(tmp[14]))

        procDados.close()

        # ____ FRAME PRINCIPAL
        self.root = Frame(self)
        self.root.pack(fill="both", expand="True")

        # ____ FRAME DA ESQUERDA
        self.frameLeft = Frame(self.root, border=1, relief="groove")
        self.frameLeft.grid(column=0, row=0, sticky=N + S + E + W)

        # NOME
        Label(self.frameLeft, font='bold', text="Nome").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.eNome = Entry(self.frameLeft, width=20, font='bold')
        self.eNome.grid(row=0, column=1, sticky=W + E, padx=5, pady=5)
        self.labelExame = Label(self.frameLeft, font='bold', text="Exame")
        self.labelExame.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.eExame = Entry(self.frameLeft, width=13, font='bold')
        self.eExame.insert(0, self.exame['numero'])
        self.eExame["state"] = DISABLED
        self.eExame.grid(row=1, column=1, sticky=W + E, padx=5, pady=5)

        Label(self.frameLeft, font=("Helvetica", 18, "bold"), text="Status").grid(row=2, column=0, columnspan=2, sticky=W + E + N, padx=5, pady=5)
        self.varExame = BooleanVar()
        self.varExame.set(True)
        self.checkExame = Checkbutton(self.frameLeft, var=self.varExame, state=DISABLED, offvalue=False, onvalue=True)
        self.checkExame.grid(row=3, column=0, sticky=N + S + E, padx=3, pady=3)
        Label(self.frameLeft, font='bold', justify=LEFT, text="Exame").grid(row=3, column=1, sticky=N + S + W)
        self.varProcessamento = BooleanVar()
        self.varProcessamento.set(True)
        self.checkProcessamento = Checkbutton(self.frameLeft, var=self.varProcessamento, state=DISABLED, offvalue=False,
                                              onvalue=True)
        self.checkProcessamento.grid(row=6, column=0, sticky=N + S + E, padx=3, pady=3)
        Label(self.frameLeft, font='bold', justify=LEFT, text="Processamento").grid(row=6, column=1, sticky=N + S + W)

        self.varResultados = BooleanVar()
        self.varResultados.set(True)
        self.checkResultados = Checkbutton(self.frameLeft, var=self.varResultados, state=DISABLED, offvalue=False,
                                           onvalue=True)
        self.checkResultados.grid(row=7, column=0, sticky=N + S + E, padx=3, pady=3)
        Label(self.frameLeft, font=("Helvetica", 18), justify=LEFT, text="Resultados").grid(row=7, column=1, sticky=N + S + W)

        Label(self.frameLeft, height=19, text=" ").grid(row=12, column=0, sticky=N + S + W + E)

        self.frameButtons = Frame(self.frameLeft)
        self.frameButtons.grid(column=0, row=10, columnspan=2, sticky=N + S + E + W)

        # Botão de próxima etapa e etapa anterior
        self.btnAnterior = Button(self.frameButtons, text="Etapa anterior", command=lambda: self._etapaAnterior())
        self.btnAnterior.grid(column=0, row=0, padx=15, pady=5, sticky=N + S + W)
        self.btnProxima = Button(self.frameButtons, text="Próxima etapa", state=DISABLED)
        self.btnProxima.grid(column=1, row=0, padx=15, pady=5, sticky=N + S + W)

        # ____ FRAME DO CENTRO
        self.frameCenter = Frame(self.root)
        self.frameCenter.grid(column=1, row=0, sticky=N + S + E + W)

        figureChart = plt.figure(figsize=(7.5, 5.5), facecolor='white')

        # --------------- GRÁFICO A -------------------

        self.aAxis = figureChart.add_subplot(3, 1, 1)  # 1 row, 1 column
        self.aTValues = self.pos
        self.aValues = self.posX
        self.aTimeBar = [np.min(self.aValues), np.max(self.aValues)]
        self.aAxis.plot(self.aTValues, self.aValues)
        self.aAxis.plot([self.numFrame, self.numFrame], self.aTimeBar)

        self.aAxis.set_ylabel('Posição X')
        self.aAxis.set_xlabel('Frame')
        self.aAxis.grid()

        # --------------- GRÁFICO B -------------------

        self.bAxis = figureChart.add_subplot(3, 1, 2)  # 1 row, 1 column
        self.bTValues = self.pos
        self.bValues = self.posY
        self.bTimeBar = [np.min(self.bValues), np.max(self.bValues)]
        self.bAxis.plot(self.bTValues, self.bValues)
        self.bAxis.plot([self.numFrame, self.numFrame], self.bTimeBar)

        self.bAxis.set_ylabel('Posição Y')
        self.bAxis.set_xlabel('Frame')
        self.bAxis.grid()

        # --------------- GRÁFICO C -------------------

        self.cAxis = figureChart.add_subplot(3, 1, 3)  # 1 row, 1 column
        self.cTValues = self.pos
        self.cValues = self.velEscalar
        self.cTimeBar = [np.min(self.cValues), np.max(self.cValues)]
        self.cAxis.plot(self.cTValues, self.cValues)
        self.cAxis.plot([self.numFrame, self.numFrame], self.cTimeBar)

        self.cAxis.set_ylabel('Deslocamento escalar')
        self.cAxis.set_xlabel('Frame')
        self.cAxis.grid()

        self.canvasChart = FigureCanvasTkAgg(figureChart, master=self.frameCenter)
        self.canvasChart._tkcanvas.pack(side="bottom", fill="x")

        # # Toolbar
        toolbar = NavigationToolbar2Tk(self.canvasChart, self.frameCenter)
        toolbar.update()
        toolbar.pack(side="top", fill="x")

        frameSelectChart = Frame(self.frameCenter)
        frameSelectChart.pack(side="bottom", fill="x")

        Label(frameSelectChart, text="Gráfico 1").grid(column=0, row=0)
        self.comboChart1 = ttk.Combobox(frameSelectChart, width=22, state="readonly")
        self.comboChart1.grid(column=1, row=0)
        self.comboChart1['values'] = [ \
            'Posição em X',
            'Posição em Y',
            'Deslocamento escalar',
            'Ângulo',
            'Área da pupila',
            'Circularidade da pupila',
            'Velocidade em X',
            'Velocidade em Y',
            'Velocidade angular',
            'Velocidade escalar',
            'Aceleração em X',
            'Aceleração em Y',
            'Aceleração angular',
            'Aceleração escalar',
        ]
        self.comboChart1.set("Posição em X")

        Label(frameSelectChart, text="Gráfico 2").grid(column=2, row=0)
        self.comboChart2 = ttk.Combobox(frameSelectChart, width=22, state="readonly")
        self.comboChart2.grid(column=3, row=0)
        self.comboChart2['values'] = [ \
            'Posição em X',
            'Posição em Y',
            'Deslocamento escalar',
            'Ângulo',
            'Área da pupila',
            'Circularidade da pupila',
            'Velocidade em X',
            'Velocidade em Y',
            'Velocidade angular',
            'Velocidade escalar',
            'Aceleração em X',
            'Aceleração em Y',
            'Aceleração angular',
            'Aceleração escalar',        ]
        self.comboChart2.set("Posição em Y")
        Label(frameSelectChart, text="Gráfico 3").grid(column=4, row=0)
        self.comboChart3 = ttk.Combobox(frameSelectChart, width=22, state="readonly")
        self.comboChart3.grid(column=5, row=0)
        self.comboChart3['values'] = [ \
            'Posição em X',
            'Posição em Y',
            'Deslocamento escalar',
            'Ângulo',
            'Área da pupila',
            'Circularidade da pupila',
            'Velocidade em X',
            'Velocidade em Y',
            'Velocidade angular',
            'Velocidade escalar',
            'Aceleração em X',
            'Aceleração em Y',
            'Aceleração angular',
            'Aceleração escalar',
        ]
        self.comboChart3.set("Velocidade escalar")

        # Põe os callbacks dos combobox
        self.comboChart1.bind("<<ComboboxSelected>>", self._selectChartA)
        self.comboChart2.bind("<<ComboboxSelected>>", self._selectChartB)
        self.comboChart3.bind("<<ComboboxSelected>>", self._selectChartC)

        # ____ FRAME DA DIREITA
        self.frameRight = Frame(self.root)
        self.frameRight.grid(column=2, row=0, sticky=N + S + E + W)

        display = Frame(self.frameRight, padx=3, pady=3, relief="groove", border=3)
        display.pack(side="top", fill="x")
        self.imgDisplay = Canvas(display, width=int(640 * self.relacao), height=int(480 * self.relacao))
        self.imgDisplay.grid(column=0, row=0, columnspan=3, sticky=W)
        btnBefore = Button(display, text="<", width=5, command=self._frameBefore)
        btnBefore.grid(column=0, row=1, rowspan=2, sticky=W)
        self.frameCont = StringVar()
        self.frameCont.set(self.numFrame)
        self.vLabelTempo = StringVar()
        self.vLabelTempo.set("00:00:00")
        self.lTempo = Label(display, textvariable=self.vLabelTempo)
        self.lTempo.grid(column=1, row=1, sticky=W)
        eTempo = Entry(display, textvariable=self.frameCont, width=6)
        eTempo.bind("<Return>", self._setTempo)
        eTempo.grid(column=1, row=2, sticky=E + W)
        btnAfter = Button(display, text=">", width=5, command=self._frameAfter)
        btnAfter.grid(column=2, row=1, rowspan=2, sticky=E)

        # Frame que mostra os valores do cursor

        fonte = ("Arial", 8)
        frameDados = Frame(self.frameRight)
        frameDados.pack(fill=BOTH, expand=TRUE)

        # Label(frameDados, text="Frames").grid(row=0, column=1, padx=5, sticky=W)

        Label(frameDados, text="Espera:", font=fonte).grid(row=1, column=0, padx=5, sticky=W)
        sEspera = StringVar()
        sEspera.set(self.exame["t1"])
        Label(frameDados, text="Frame", font=fonte).grid(row=1, column=1, sticky=W)
        Label(frameDados, textvariable=sEspera, font=fonte).grid(row=1, column=2, sticky=W)

        Label(frameDados, text="Miose:", font=fonte).grid(row=2, column=0, padx=5, sticky=W)
        sMiose = StringVar()
        sMiose.set(self.exame["t2"])
        Label(frameDados, text="Frame", font=fonte).grid(row=2, column=1, sticky=W)
        Label(frameDados, textvariable=sMiose, font=fonte).grid(row=2, column=2, sticky=W)

        Label(frameDados, text="Midriase:", font=fonte).grid(row=3, column=0, padx=5, sticky=W)
        sMidriase = StringVar()
        sMidriase.set(self.exame["t3"])
        Label(frameDados, text="Frame", font=fonte).grid(row=3, column=1, sticky=W)
        Label(frameDados, textvariable=sMidriase, font=fonte).grid(row=3, column=2, sticky=W)

        Label(frameDados, text="Ini. do mov.:", font=fonte).grid(row=4, column=0, padx=5, sticky=W)
        sIMovimento = StringVar()
        sIMovimento.set(self.exame["t4"])
        Label(frameDados, text="Frame", font=fonte).grid(row=4, column=1, sticky=W)
        Label(frameDados, textvariable=sIMovimento, font=fonte).grid(row=4, column=2, sticky=W)

        Label(frameDados, text="Fim do mov.:", font=fonte).grid(row=5, column=0, padx=5, sticky=W)
        sFMovimento = StringVar()
        sFMovimento.set(self.exame["t5"])
        Label(frameDados, text="Frame", font=fonte).grid(row=5, column=1, sticky=W)
        Label(frameDados, textvariable=sFMovimento, font=fonte).grid(row=5, column=2, sticky=W)

        Label(frameDados, text="Ini. do corte:", font=fonte).grid(row=6, column=0, padx=5, sticky=W)
        sICorte = StringVar()
        sICorte.set(self.exame["t7"])
        Label(frameDados, text="Frame", font=fonte).grid(row=6, column=1, sticky=W)
        Label(frameDados, textvariable=sICorte, font=fonte).grid(row=6, column=2, sticky=W)

        Label(frameDados, text="Fim do corte:", font=fonte).grid(row=7, column=0, padx=5, sticky=W)
        sFCorte = StringVar()
        sFCorte.set(self.exame["t8"])
        Label(frameDados, text="Frame", font=fonte).grid(row=7, column=1, sticky=W)
        Label(frameDados, textvariable=sFCorte, font=fonte).grid(row=7, column=2, sticky=W)

        Label(frameDados, text="Fim do exame:", font=fonte).grid(row=8, column=0, padx=5, sticky=W)
        sFExame = StringVar()
        sFExame.set(self.exame["t6"])
        Label(frameDados, text="Frame", font=fonte).grid(row=8, column=1, sticky=W)
        Label(frameDados, textvariable=sFExame, font=fonte).grid(row=8, column=2, sticky=W)

        # Label(frameDados, text="Cursor").grid(row=9, column=1, padx=5, sticky=W)

        # Posição em X
        Label(frameDados, text="Pos. em X:", font=fonte).grid(row=10, column=0, padx=5, sticky=W)
        self.sPosX = StringVar()
        self.sPosX.set(self.posX[self.numFrame - int(self.exame['t5'])])
        Label(frameDados, textvariable=self.sPosX, font=fonte).grid(row=10, column=1, sticky=W)
        Label(frameDados, text="px", font=fonte).grid(row=10, column=2, sticky=W)

        # Posição em Y
        Label(frameDados, text="Pos. em Y:", font=fonte).grid(row=11, column=0, padx=5, sticky=W)
        self.sPosY = StringVar()
        self.sPosY.set(self.posY[self.numFrame - int(self.exame['t5'])])
        Label(frameDados, textvariable=self.sPosY, font=fonte).grid(row=11, column=1, sticky=W)
        Label(frameDados, text="px", font=fonte).grid(row=11, column=2, sticky=W)

        # Deslocamento escalar
        # Label(frameDados, text="Desl. escalar:", font=fonte).grid(row=12, column=0, padx=5, sticky=W)
        self.sDesEsc = StringVar()
        self.sDesEsc.set(self.desEscalar[self.numFrame - int(self.exame['t5'])])
        # Label(frameDados, textvariable=self.sDesEsc, font=fonte).grid(row=12, column=1, sticky=W)
        # Label(frameDados, text="px", font=fonte).grid(row=12, column=2, sticky=W)

        # Ângulo
        # Label(frameDados, text="Ângulo:", font=fonte).grid(row=13, column=0, padx=5, sticky=W)
        self.sPosAngulo = StringVar()
        self.sPosAngulo.set(self.posA[self.numFrame - int(self.exame['t5'])])
        # Label(frameDados, textvariable=self.sPosAngulo, font=fonte).grid(row=13, column=1, sticky=W)
        # Label(frameDados, text="graus", font=fonte).grid(row=13, column=2, sticky=W)

        # Área da pupila
        Label(frameDados, text="Área da pupila:", font=fonte).grid(row=14, column=0, padx=5, sticky=W)
        self.sArea = StringVar()
        self.sArea.set(self.area[self.numFrame - int(self.exame['t5'])])
        Label(frameDados, textvariable=self.sArea, font=fonte).grid(row=14, column=1, sticky=W)
        Label(frameDados, text="px²", font=fonte).grid(row=14, column=2, sticky=W)

        # Circularidade da pupila
        # Label(frameDados, text="Circ. da pupila:", font=fonte).grid(row=15, column=0, padx=5, sticky=W)
        self.sCircularidade = StringVar()
        self.sCircularidade.set(self.circularidade[self.numFrame - int(self.exame['t5'])])
        # Label(frameDados, textvariable=self.sCircularidade, font=fonte).grid(row=15, column=1, sticky=W)
        # Label(frameDados, text="%", font=fonte).grid(row=15, column=2, sticky=W)
        #
        # Velocidade em X
        Label(frameDados, text="Vel. em X:", font=fonte).grid(row=16, column=0, padx=5, sticky=W)
        self.sVelX = StringVar()
        self.sVelX.set(self.velX[self.numFrame - int(self.exame['t5'])])
        Label(frameDados, textvariable=self.sVelX, font=fonte).grid(row=16, column=1, sticky=W)
        Label(frameDados, text="px/frame", font=fonte).grid(row=16, column=2, sticky=W)

        # Velocidade em Y
        Label(frameDados, text="Vel. em Y:", font=fonte).grid(row=17, column=0, padx=5, sticky=W)
        self.sVelY = StringVar()
        self.sVelY.set(self.velX[self.numFrame - int(self.exame['t5'])])
        Label(frameDados, textvariable=self.sVelY, font=fonte).grid(row=17, column=1, sticky=W)
        Label(frameDados, text="px/frame", font=fonte).grid(row=17, column=2, sticky=W)

        # Velocidade escalar
        Label(frameDados, text="Vel. Escalar:").grid(row=18, column=0, padx=5, sticky=W)
        self.sVelEscalar = StringVar()
        self.sVelEscalar.set(self.velEscalar[self.numFrame - int(self.exame['t5'])])
        Label(frameDados, textvariable=self.sVelEscalar, font=fonte).grid(row=18, column=1, sticky=W)
        Label(frameDados, text="px/frame", font=fonte).grid(row=18, column=2, sticky=W)

        # Velocidade angular
        # Label(frameDados, text="Vel. Angular:", font=fonte).grid(row=19, column=0, padx=5, sticky=W)
        self.sVelA = StringVar()
        self.sVelA.set(self.velA[self.numFrame - int(self.exame['t5'])])
        # Label(frameDados, textvariable=self.sVelA, font=fonte).grid(row=19, column=1, sticky=W)
        # Label(frameDados, text="graus/frame", font=fonte).grid(row=19, column=2, sticky=W)

        # Aceleração em X
        Label(frameDados, text="Acel. em X:", font=fonte).grid(row=20, column=0, padx=5, sticky=W)
        self.sAcelX = StringVar()
        self.sAcelX.set(self.acelX[self.numFrame - int(self.exame['t5'])])
        Label(frameDados, textvariable=self.sAcelX, font=fonte).grid(row=20, column=1, sticky=W)
        Label(frameDados, text="px/frame²", font=fonte).grid(row=20, column=2, sticky=W)

        # Aceleração em Y
        Label(frameDados, text="Acel. em Y:", font=fonte).grid(row=21, column=0, padx=5, sticky=W)
        self.sAcelY = StringVar()
        self.sAcelY.set(self.acelY[self.numFrame - int(self.exame['t5'])])
        Label(frameDados, textvariable=self.sAcelY, font=fonte).grid(row=21, column=1, sticky=W)
        Label(frameDados, text="px/frame²", font=fonte).grid(row=21, column=2, sticky=W)

        # Aceleração escalar
        Label(frameDados, text="Acel. escalar:", font=fonte).grid(row=22, column=0, padx=5, sticky=W)
        self.sAcelEscalar = StringVar()
        self.sAcelEscalar.set(self.acelEscalar[self.numFrame - int(self.exame['t5'])])
        Label(frameDados, textvariable=self.sAcelEscalar, font=fonte).grid(row=22, column=1, sticky=W)
        Label(frameDados, text="px/frame²", font=fonte).grid(row=22, column=2, sticky=W)

        # Aceleração angular
        # Label(frameDados, text="Acel. angular:", font=fonte).grid(row=23, column=0, padx=5, sticky=W)
        self.sAcelA = StringVar()
        self.sAcelA.set(self.acelA[self.numFrame - int(self.exame['t5'])])
        # Label(frameDados, textvariable=self.sAcelA, font=fonte).grid(row=23, column=1, sticky=W)
        # Label(frameDados, text="graus/frame²", font=fonte).grid(row=23, column=2, sticky=W)

        Label(frameDados, text="Tempo até o cursor:", font=("Arial", 9)).grid(row=24, column=0, columnspan=3, padx=5, sticky=W)
        self.sTempo = StringVar()
        self.sTempo.set("00:00:00")
        Label(frameDados, textvariable=self.sTempo, font=("Arial", 9)).grid(row=25, column=1, padx=5, sticky=W)

        self.btnReprocessar = Button(frameDados, text="Mostrar traçado", command=self._mostraTracado)
        self.btnReprocessar.grid(row=26, column=0, columnspan=3, sticky=W + E, padx=3, pady=5)

        # ____ Setando parâmetros
        self.eNome["state"] = NORMAL
        self.eNome.delete(0, END)
        self.eNome.insert(0, self.exame['nome'])
        self.eNome["state"] = DISABLED

        self.changeFrame()

    def _frameBefore(self):
        self.numFrame -= 1
        if self.numFrame < 0:
            self.numFrame = 0
        self.changeFrame()

    def _frameAfter(self):
        self.numFrame += 1
        if self.numFrame > self.frame_seq:
            self.numFrame = self.frame_seq
        self.changeFrame()

    def changeFrame(self):
        self.showFrame()
        self.frameCont.set(self.numFrame)
        self.atualizaValores()
        self.replot()

    def replot(self):

        # Gráfico A
        self.aAxis.cla()
        self.aAxis.grid()

        self.aTimeBar = [np.min(self.aValues), np.max(self.aValues)]
        self.aAxis.plot([int(self.exame["t7"]), int(self.exame["t7"])], self.aTimeBar, "k", label="Corte")
        self.aAxis.plot([int(self.exame["t8"]), int(self.exame["t8"])], self.aTimeBar, "k")

        if (self.comboChart1.get() == "Posição em X"):
            self.aAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaX"]) + int(self.exame["desvioY"]),
                             int(self.exame["mediaX"]) + int(self.exame["desvioY"])], "y", label="Média")
            self.aAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaX"]) - int(self.exame["desvioY"]),
                             int(self.exame["mediaX"]) - int(self.exame["desvioY"])], "y")
        elif (self.comboChart1.get() == "Posição em Y"):
            self.aAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaY"]) + int(self.exame["desvioY"]),
                             int(self.exame["mediaY"]) + int(self.exame["desvioY"])], "y", label="Média")
            self.aAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaY"]) - int(self.exame["desvioY"]),
                             int(self.exame["mediaY"]) - int(self.exame["desvioY"])], "y")
        elif (self.comboChart1.get() == "Área da pupila"):
            self.aAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaArea"]) + int(self.exame["desvioArea"]),
                             int(self.exame["mediaArea"]) + int(self.exame["desvioArea"])], "y", label="Média")
            self.aAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaArea"]) - int(self.exame["desvioArea"]),
                             int(self.exame["mediaArea"]) - int(self.exame["desvioArea"])], "y")
        elif (self.comboChart1.get() == "Ângulo"):
            self.aAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaAngulo"]) + int(self.exame["desvioAngulo"]),
                             int(self.exame["mediaAngulo"]) + int(self.exame["desvioAngulo"])], "y", label="Média")
            self.aAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaAngulo"]) - int(self.exame["desvioAngulo"]),
                             int(self.exame["mediaAngulo"]) - int(self.exame["desvioAngulo"])], "y")

        self.aAxis.plot(self.aTValues, self.aValues, label="Íris")
        self.aAxis.plot([self.numFrame, self.numFrame], self.aTimeBar, label="Cursor")

        self.aAxis.set_ylabel(self.comboChart1.get())
        # legendaCursor = mpatches.Patch(color='orange', label='Cursor')
        # legendaIris = mpatches.Patch(color='blue', label='Íris')
        # legendaCorte = mpatches.Patch(color='k', label='Corte')
        # legendaMedia = mpatches.Patch(color='y', label='Média')
        # self.aAxis.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='upper center',
        #    ncol=2, mode="expand", borderaxespad=0.,handles=[legendaCursor, legendaIris, legendaCorte, legendaMedia])
        # self.aAxis.legend(loc='right', ncol=2, mode="expand", borderaxespad=0.)
        self.aAxis.set_xlabel('Frame')

        # Gráfico B
        self.bAxis.cla()
        self.bAxis.grid()

        self.bTimeBar = [np.min(self.bValues), np.max(self.bValues)]
        self.bAxis.plot([int(self.exame["t7"]), int(self.exame["t7"])], self.bTimeBar, "k")
        self.bAxis.plot([int(self.exame["t8"]), int(self.exame["t8"])], self.bTimeBar, "k")

        if (self.comboChart2.get() == "Posição em X"):
            self.bAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaX"]) + int(self.exame["desvioY"]),
                             int(self.exame["mediaX"]) + int(self.exame["desvioY"])], "y")
            self.bAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaX"]) - int(self.exame["desvioY"]),
                             int(self.exame["mediaX"]) - int(self.exame["desvioY"])], "y")
        elif (self.comboChart2.get() == "Posição em Y"):
            self.bAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaY"]) + int(self.exame["desvioY"]),
                             int(self.exame["mediaY"]) + int(self.exame["desvioY"])], "y")
            self.bAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaY"]) - int(self.exame["desvioY"]),
                             int(self.exame["mediaY"]) - int(self.exame["desvioY"])], "y")
        elif (self.comboChart1.get() == "Área da pupila"):
            self.bAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaArea"]) + int(self.exame["desvioArea"]),
                             int(self.exame["mediaArea"]) + int(self.exame["desvioArea"])], "y")
            self.bAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaArea"]) - int(self.exame["desvioArea"]),
                             int(self.exame["mediaArea"]) - int(self.exame["desvioArea"])], "y")
        elif (self.comboChart1.get() == "Ângulo"):
            self.bAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaAngulo"]) + int(self.exame["desvioAngulo"]),
                             int(self.exame["mediaAngulo"]) + int(self.exame["desvioAngulo"])], "y")
            self.bAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaAngulo"]) - int(self.exame["desvioAngulo"]),
                             int(self.exame["mediaAngulo"]) - int(self.exame["desvioAngulo"])], "y")

        self.bAxis.plot(self.bTValues, self.bValues)
        self.bAxis.plot([self.numFrame, self.numFrame], self.bTimeBar)

        self.bAxis.set_ylabel(self.comboChart2.get())
        self.bAxis.set_xlabel('Frame')

        # Gráfico C
        self.cAxis.cla()
        self.cAxis.grid()

        self.cTimeBar = [np.min(self.cValues), np.max(self.cValues)]
        self.cAxis.plot([int(self.exame["t7"]), int(self.exame["t7"])], self.cTimeBar, "k")
        self.cAxis.plot([int(self.exame["t8"]), int(self.exame["t8"])], self.cTimeBar, "k")

        if (self.comboChart3.get() == "Posição em X"):
            self.cAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaX"]) + int(self.exame["desvioY"]),
                             int(self.exame["mediaX"]) + int(self.exame["desvioY"])], "y")
            self.cAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaX"]) - int(self.exame["desvioY"]),
                             int(self.exame["mediaX"]) - int(self.exame["desvioY"])], "y")
        elif (self.comboChart3.get() == "Posição em Y"):
            self.cAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaY"]) + int(self.exame["desvioY"]),
                             int(self.exame["mediaY"]) + int(self.exame["desvioY"])], "y")
            self.cAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaY"]) - int(self.exame["desvioY"]),
                             int(self.exame["mediaY"]) - int(self.exame["desvioY"])], "y")
        elif (self.comboChart1.get() == "Área da pupila"):
            self.cAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaArea"]) + int(self.exame["desvioArea"]),
                             int(self.exame["mediaArea"]) + int(self.exame["desvioArea"])], "y")
            self.cAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaArea"]) - int(self.exame["desvioArea"]),
                             int(self.exame["mediaArea"]) - int(self.exame["desvioArea"])], "y")
        elif (self.comboChart1.get() == "Ângulo"):
            self.cAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaAngulo"]) + int(self.exame["desvioAngulo"]),
                             int(self.exame["mediaAngulo"]) + int(self.exame["desvioAngulo"])], "y")
            self.cAxis.plot([int(self.exame["t5"]), int(self.exame["t6"])],
                            [int(self.exame["mediaAngulo"]) - int(self.exame["desvioAngulo"]),
                             int(self.exame["mediaAngulo"]) - int(self.exame["desvioAngulo"])], "y")

        self.cAxis.plot(self.cTValues, self.cValues)
        self.cAxis.plot([self.numFrame, self.numFrame], self.cTimeBar)

        self.cAxis.set_ylabel(self.comboChart3.get())
        self.cAxis.set_xlabel('Frame')

        self.canvasChart.draw()

    def _selectChartA(self, event):
        if (self.comboChart1.get() == "Área da pupila"):
            self.aValues = self.area
        elif (self.comboChart1.get() == "Circularidade da pupila"):
            self.aValues = self.circularidade
        elif(self.comboChart1.get() == "Posição em X"):
            self.aValues = self.posX
        elif (self.comboChart1.get() == "Velocidade em X"):
            self.aValues = self.velX
        elif (self.comboChart1.get() == "Aceleração em X"):
            self.aValues = self.acelX
        elif (self.comboChart1.get() == "Posição em Y"):
            self.aValues = self.posY
        elif (self.comboChart1.get() == "Velocidade em Y"):
            self.aValues = self.velY
        elif (self.comboChart1.get() == "Aceleração em Y"):
            self.aValues = self.acelY
        elif (self.comboChart1.get() == "Deslocamento escalar"):
            self.aValues = self.desEscalar
        elif (self.comboChart1.get() == "Velocidade escalar"):
            self.aValues = self.velEscalar
        elif (self.comboChart1.get() == "Aceleração escalar"):
            self.aValues = self.acelEscalar
        elif (self.comboChart1.get() == "Ângulo"):
            self.aValues = self.posA
        elif (self.comboChart1.get() == "Velocidade angular"):
            self.aValues = self.velA
        elif (self.comboChart1.get() == "Aceleração angular"):
            self.aValues = self.acelA

        self.replot()

    def _selectChartB(self, event):
        if (self.comboChart2.get() == "Área da pupila"):
            self.bValues = self.area
        elif (self.comboChart2.get() == "Circularidade da pupila"):
            self.bValues = self.circularidade
        elif(self.comboChart2.get() == "Posição em X"):
            self.bValues = self.posX
        elif (self.comboChart2.get() == "Velocidade em X"):
            self.bValues = self.velX
        elif (self.comboChart2.get() == "Aceleração em X"):
            self.bValues = self.acelX
        elif (self.comboChart2.get() == "Posição em Y"):
            self.bValues = self.posY
        elif (self.comboChart2.get() == "Velocidade em Y"):
            self.bValues = self.velY
        elif (self.comboChart2.get() == "Aceleração em Y"):
            self.bValues = self.acelY
        elif (self.comboChart2.get() == "Deslocamento escalar"):
            self.bValues = self.desEscalar
        elif (self.comboChart2.get() == "Velocidade escalar"):
            self.bValues = self.velEscalar
        elif (self.comboChart2.get() == "Aceleração escalar"):
            self.bValues = self.acelEscalar
        elif (self.comboChart2.get() == "Ângulo"):
            self.bValues = self.posA
        elif (self.comboChart2.get() == "Velocidade angular"):
            self.bValues = self.velA
        elif (self.comboChart2.get() == "Aceleração angular"):
            self.bValues = self.acelA

        self.replot()

    def _selectChartC(self, event):
        if (self.comboChart3.get() == "Área da pupila"):
            self.cValues = self.area
        elif (self.comboChart3.get() == "Circularidade da pupila"):
            self.cValues = self.circularidade
        elif (self.comboChart3.get() == "Posição em X"):
            self.cValues = self.posX
        elif (self.comboChart3.get() == "Velocidade em X"):
            self.cValues = self.velX
        elif (self.comboChart3.get() == "Aceleração em X"):
            self.cValues = self.acelX
        elif (self.comboChart3.get() == "Posição em Y"):
            self.cValues = self.posY
        elif (self.comboChart3.get() == "Velocidade em Y"):
            self.cValues = self.velY
        elif (self.comboChart3.get() == "Aceleração em Y"):
            self.cValues = self.acelY
        elif (self.comboChart3.get() == "Deslocamento escalar"):
            self.cValues = self.desEscalar
        elif (self.comboChart3.get() == "Velocidade escalar"):
            self.cValues = self.velEscalar
        elif (self.comboChart3.get() == "Aceleração escalar"):
            self.cValues = self.acelEscalar
        elif (self.comboChart3.get() == "Ângulo"):
            self.cValues = self.posA
        elif (self.comboChart3.get() == "Velocidade angular"):
            self.cValues = self.velA
        elif (self.comboChart3.get() == "Aceleração angular"):
            self.cValues = self.acelA

        self.replot()

    def _setTempo(self, event):
        frame = event.widget.get()
        if(util.validateInt(frame)):
            frame = int(frame)
            if(frame >= int(self.exame['t5']) and frame <= int(self.exame['t6'])):
                self.numFrame = frame
            else:
                messagebox.showerror("Erro", "A amostra deve estar entre " + str(self.exame['t5']) + " e " + str(self.exame['t6']))
        self.changeFrame()

    def atualizaValores(self):
        # Atualiza valores do relógio
        iTempo = int((self.numFrame * 1.11) + 0.5)
        minutos = int(iTempo / 6000)
        segundos = int((iTempo - (minutos * 6000)) / 100)
        msegundos = (iTempo - (minutos * 6000 + segundos * 100))
        if(msegundos < 1): msegundos = 0

        if (int(minutos) < 10): minutos = str("0" + str(minutos))
        if (segundos < 10): segundos = str("0" + str(segundos))
        if (msegundos < 10): msegundos = str("0" + str(msegundos))

        self.vLabelTempo.set(str(minutos) + ":" + str(segundos) + ":" + str(msegundos))

        # Atualiza valores do tempo do cursor
        iTempo = int((((self.numFrame - int(self.exame['t5'])) * 1.11) + 0.5))
        minutos = int(iTempo / 6000)
        segundos = int((iTempo - (minutos * 6000)) / 100)
        msegundos = (iTempo - (minutos * 6000 + segundos * 100))
        if(msegundos < 1): msegundos = 0

        if (int(minutos) < 10): minutos = str("0" + str(minutos))
        if (segundos < 10): segundos = str("0" + str(segundos))
        if (msegundos < 10): msegundos = str("0" + str(msegundos))

        self.sTempo.set(str(minutos) + ":" + str(segundos) + ":" + str(msegundos))

        # Atualiza os valores da barra lateral
        self.sPosX.set(self.posX[self.numFrame - int(self.exame['t5'])])
        self.sPosY.set(self.posY[self.numFrame - int(self.exame['t5'])])
        self.sDesEsc.set(self.desEscalar[self.numFrame - int(self.exame['t5'])])
        self.sPosAngulo.set(self.posA[self.numFrame - int(self.exame['t5'])])
        self.sArea.set(self.area[self.numFrame - int(self.exame['t5'])])
        self.sCircularidade.set(self.circularidade[self.numFrame - int(self.exame['t5'])])
        self.sVelX.set(self.velX[self.numFrame - int(self.exame['t5'])])
        self.sVelY.set(self.velY[self.numFrame - int(self.exame['t5'])])
        self.sVelEscalar.set(self.velEscalar[self.numFrame - int(self.exame['t5'])])
        self.sVelA.set(self.velA[self.numFrame - int(self.exame['t5'])])
        self.sAcelX.set(self.acelX[self.numFrame - int(self.exame['t5'])])
        self.sAcelY.set(self.acelY[self.numFrame - int(self.exame['t5'])])
        self.sAcelEscalar.set(self.acelEscalar[self.numFrame - int(self.exame['t5'])])
        self.sAcelA.set(self.acelA[self.numFrame - int(self.exame['t5'])])

    def showFrame(self):
        # Se for um frame que foi processdo
        if ((self.numFrame >= int(self.exame['t7'])) and (self.numFrame <= int(self.exame['t8']))):
            ret, frame = cv2.VideoCapture(self.dir + "/frames/" + str(self.numFrame) + ".png").read()
            if ret:
                self.video = util.convertToExibe(frame, int(640 * self.relacao), int(480 * self.relacao))
                self.imgDisplay.create_image(0, 0, image=self.video, anchor=NW)
        # Se for um frame que não foi processado
        else:
            if (self.cap.isOpened()):
                self.cap.set(1, self.numFrame)
                ret, frame = self.cap.read()

                if ret:
                    self.video = util.convertToExibe(frame, int(640*self.relacao), int(480*self.relacao))
                    self.imgDisplay.create_image(0, 0, image=self.video, anchor=NW)
                else:
                    self.cap.release()

    def _mostraTracado(self):
        self.cap.set(1, self.numFrame)
        ret, frame = self.cap.read()

        # Lê as posições dos percurso e desenha em cima do frame
        xAnterior = self.posX[0]
        yAnterior = self.posY[0]

        # desenha um ponto da média
        frame = cv2.line(frame, (xAnterior, yAnterior), (xAnterior, yAnterior), (0, 0, 255), 3)

        partCor = 255/(int(self.exame['t8']) - int(self.exame['t7']))

        for posicao in range(len(self.posX)):
            if (posicao + int(self.exame['t5']) >= int(self.exame['t7'])) and (posicao + int(self.exame['t5']) <= int(self.exame['t8'])):
                # represents the top left corner of image
                start_point = (xAnterior, yAnterior)
                # End coordinate
                end_point = (self.posX[posicao], self.posY[posicao])
                # Green color in BGR
                cor = (int(self.exame['t7']) - int(self.exame['t5']) - posicao) * partCor
                color = (0, int(cor+255), int(cor))

                # Line thickness of 9 px
                thickness = 1

                frame = cv2.line(frame, start_point, end_point, color, thickness)

                xAnterior = self.posX[posicao]
                yAnterior = self.posY[posicao]

        cv2.imshow("Mostra trageto", frame)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def _etapaAnterior(self):
        self.father._preProcessamento(self.dir)