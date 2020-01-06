from builtins import print

import cv2
import tkinter
import util
import os
import shutil

from emptyContainer import EmptyContainer
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class PreProcessamentoContainer(EmptyContainer):

    cont = 0
    play = False

    def __init__(self, father, dir):
        super().__init__()

        self.father = father
        self.dir = dir

        self.exame = util.getExame(dir)

        self.cap = cv2.VideoCapture(dir + "/exame.mp4")

        self.width = self.cap.get(3)
        self.height = self.cap.get(4)

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
        self.varExame.set(False)
        self.checkExame = Checkbutton(self.frameLeft, var=self.varExame, state=DISABLED, offvalue=False, onvalue=True)
        self.checkExame.grid(row=3, column=0, sticky=N + S + E, padx=3, pady=3)
        Label(self.frameLeft, font='bold', justify=LEFT, text="Exame").grid(row=3, column=1, sticky=N + S + W)
        self.varProcessamento = BooleanVar()
        self.varProcessamento.set(False)
        self.checkProcessamento = Checkbutton(self.frameLeft, var=self.varProcessamento, state=DISABLED, offvalue=False,
                                              onvalue=True)
        self.checkProcessamento.grid(row=6, column=0, sticky=N + S + E, padx=3, pady=3)
        Label(self.frameLeft, font=("Helvetica", 18), justify=LEFT, text="Processamento").grid(row=6, column=1, sticky=N + S + W)

        self.varResultados = BooleanVar()
        self.varResultados.set(False)
        self.checkResultados = Checkbutton(self.frameLeft, var=self.varResultados, state=DISABLED, offvalue=False,
                                           onvalue=True)
        self.checkResultados.grid(row=7, column=0, sticky=N + S + E, padx=3, pady=3)
        Label(self.frameLeft, font='bold', justify=LEFT, text="Resultados").grid(row=7, column=1, sticky=N + S + W)

        Label(self.frameLeft, height=19, text=" ").grid(row=9, column=0, sticky=N + S + W + E)

        self.frameButtons = Frame(self.frameLeft)
        self.frameButtons.grid(column=0, row=10, columnspan=2, sticky=N + S + E + W)

        # Botão de próxima etapa e etapa anterior
        self.btnAnterior = Button(self.frameButtons, text="Etapa anterior", command=lambda: self._etapaAnterior())
        self.btnAnterior.grid(column=0, row=0, padx=15, pady=5, sticky=N + S + W)
        self.btnProxima = Button(self.frameButtons, text="Próxima etapa", command=lambda: self._proximaEtapa())
        self.btnProxima.grid(column=1, row=0, padx=15, pady=5, sticky=N + S + W)

        # ____ FRAME CENTRAL
        self.frameCenter = Frame(self.root)
        self.frameCenter.grid(column=1, row=0, sticky=N + S + E + W)

        controle = Frame(self.frameCenter, height=30)
        controle.pack(side="bottom", fill="x")

        self.camera = Canvas(controle, width=self.width, height=self.height)
        self.camera.pack(expand=True)

        self.frame_seq = int(self.exame["frames"])
        self.fps = self.exame["fps"]

        self.progressBar = Scale(controle, from_=0, to=self.frame_seq, orient=HORIZONTAL, command=self._alteradoScale,
                                 showvalue=False)
        self.progressBar.pack(side="left", fill="x", expand=True)

        # ____ FRAME DA DIREITA
        self.frameRight = Frame(self.root)
        self.frameRight.grid(column=2, row=0, sticky=N + S + E + W)

        frameFrames = Frame(self.frameRight)
        frameFrames.pack(side="top", fill="x")

        Label(frameFrames, text="Espera").grid(row=0, column=0, sticky=W)
        self.eEspera = Entry(frameFrames, width=6, font='bold')
        self.eEspera.insert(0, self.exame["t1"])
        self.eEspera["state"] = DISABLED
        self.eEspera.grid(row=0, column=1, sticky=W + E, padx=3, pady=5)

        Label(frameFrames, text="Miose").grid(row=1, column=0, sticky=W)
        self.eMiose = Entry(frameFrames, width=6, font='bold')
        self.eMiose.insert(0, self.exame["t2"])
        self.eMiose["state"] = DISABLED
        self.eMiose.grid(row=1, column=1, sticky=W + E, padx=3, pady=5)

        Label(frameFrames, text="Midriase").grid(row=2, column=0, sticky=W)
        self.eMidriase = Entry(frameFrames, width=6, font='bold')
        self.eMidriase.insert(0, self.exame["t3"])
        self.eMidriase["state"] = DISABLED
        self.eMidriase.grid(row=2, column=1, sticky=W + E, padx=3, pady=5)

        Label(frameFrames, text="Início do movimento").grid(row=3, column=0, sticky=W)
        self.eInicioMovimento = Entry(frameFrames, width=6, font='bold')
        self.eInicioMovimento.insert(0, self.exame["t4"])
        self.eInicioMovimento["state"] = DISABLED
        self.eInicioMovimento.grid(row=3, column=1, sticky=W + E, padx=3, pady=5)

        Label(frameFrames, text="Fim do movimento").grid(row=4, column=0, sticky=W)
        self.eFimMovimento = Entry(frameFrames, width=6, font='bold')
        self.eFimMovimento.insert(0, self.exame["t5"])
        self.eFimMovimento["state"] = DISABLED
        self.eFimMovimento.grid(row=4, column=1, sticky=W + E, padx=3, pady=5)

        Label(frameFrames, text="Fim do exame").grid(row=5, column=0, sticky=W)
        self.eFimExame = Entry(frameFrames, width=6, font='bold')
        self.eFimExame.insert(0, self.exame["t6"])
        self.eFimExame["state"] = DISABLED
        self.eFimExame.grid(row=5, column=1, sticky=W + E, padx=3, pady=5)

        frameCorte = Frame(self.frameRight)
        frameCorte.pack(side="top", fill="x")

        Label(frameCorte, text="Início do corte").grid(row=0, column=0, columnspan=2, sticky=W)
        self.eInicioCorte = Entry(frameCorte, width=6, font='bold')
        self.eInicioCorte.grid(row=1, column=0, sticky=W + E, padx=3, pady=5)
        self.btnInicioCorte = Button(frameCorte, text="Usar quadro exibido", command=self._usarQuadroInicio)
        self.btnInicioCorte.grid(row=1, column=1, sticky=W + E, padx=3, pady=5)

        Label(frameCorte, text="Fim do corte").grid(row=2, column=0, columnspan=2, sticky=W)
        self.eFimCorte = Entry(frameCorte, width=6, font='bold')
        self.eFimCorte.grid(row=3, column=0, sticky=W + E, padx=3, pady=5)
        self.btnFimCorte = Button(frameCorte, text="Usar quadro exibido", command=self._usarQuadroFim)
        self.btnFimCorte.grid(row=3, column=1, sticky=W + E, padx=3, pady=5)

        if(not (self.exame["processamento"] is "N")):
            self.eInicioCorte.insert(0, self.exame["t7"])
            self.eInicioCorte["state"] = DISABLED
            self.eFimCorte.insert(0, self.exame["t8"])
            self.eFimCorte["state"] = DISABLED
            self.btnInicioCorte["state"] = DISABLED
            self.btnFimCorte["state"] = DISABLED
            self.btnReprocessar = Button(frameCorte, text="Processar novamente", command=self._reprocessar)
            self.btnReprocessar.grid(row=5, column=0, columnspan=2, sticky=W + E, padx=3, pady=5)

        frameControles = Frame(self.frameRight)
        frameControles.pack(side="bottom", fill="x")

        self.vLabelFrame = StringVar()
        self.vLabelFrame.set("Frame 0/0")
        self.lFrame = Label(frameControles, textvariable=self.vLabelFrame)
        self.lFrame.pack(side="top", fill="x")
        self.vLabelTempo = StringVar()
        self.vLabelTempo.set("00:00:00")
        self.lTempo = Label(frameControles, textvariable=self.vLabelTempo)
        self.lTempo.pack(side="top", fill="x")

        Button(frameControles, text="<", command=self._frameBefore).pack(side="left", fill="x")
        self.l_play = StringVar()
        self.l_play.set("Play")
        self.btnPlay = Button(frameControles, textvariable=self.l_play, command=self._playMovie).pack(side="left", fill="x", expand=True)
        Button(frameControles, text=">", command=self._frameAfter).pack(side="right", fill="x")

        # ____ Setando parâmetros
        self.eNome["state"] = NORMAL
        self.eNome.delete(0, END)
        self.eNome.insert(0, self.exame['nome'])
        self.eNome["state"] = DISABLED

        # Checks de status
        if self.exame['exame'] is "S":
            self.checkExame["state"] = NORMAL
            self.varExame.set(True)
            self.checkExame["state"] = DISABLED

        if self.exame['processamento'] is "S":
            self.checkProcessamento["state"] = NORMAL
            self.varProcessamento.set(True)
            self.checkProcessamento["state"] = DISABLED

        if self.exame['resultados'] is "S":
            self.checkResultados["state"] = NORMAL
            self.varResultados.set(True)
            self.checkResultados["state"] = DISABLED

        self.showFrame(self.cont)

    def _playMovie(self):
        self.play = not self.play

        if(self.play):
            self.l_play.set("Stop")
            tempo = 1000/self.fps
            self.delay = int(tempo)
            self.exibeVideo()
        else:
            self.l_play.set("Play")

    def _frameBefore(self):
        self.play = False
        self.l_play.set("Play")
        self.cont -= 1
        if self.cont < 0:
            self.cont = 0
        self.progressBar.set(self.cont)
        self.showFrame(self.cont)

    def _frameAfter(self):
        self.play = False
        self.l_play.set("Play")
        self.cont += 1
        if self.cont > self.frame_seq:
            self.cont = self.frame_seq
        self.progressBar.set(self.cont)
        self.showFrame(self.cont)

    def _alteradoScale(self, val):
        self.cont = int(val)
        self.showFrame(val)

    def exibeVideo(self):
        self.cont += 1
        if self.cont > self.frame_seq:
            self.cont = self.frame_seq
            self.play = False
            self.l_play.set("Play")
        self.progressBar.set(self.cont)
        self.showFrame(self.cont)

        if(self.play):
            self.after(self.delay, self.exibeVideo)

    def showFrame(self, valor):
        valor = int(valor)
        if (self.cap.isOpened()):
            self.cap.set(1, valor)
            ret, frame = self.cap.read()

            if ret:
                self.video = util.convertToExibe(frame)
                self.camera.create_image(0, 0, image=self.video, anchor=tkinter.NW)
                self.vLabelFrame.set("Frame " + str(self.cont) + "/" + str(self.frame_seq))

                iTempo = int((self.cont * 1.11) + 0.5)
                minutos = int(iTempo / 6000)
                segundos = int((iTempo - (minutos * 6000)) / 100)
                msegundos = (iTempo - (minutos * 6000 + segundos * 100))

                if (int(minutos) < 10): minutos = str("0" + str(minutos))
                if (segundos < 10): segundos = str("0" + str(segundos))
                if (msegundos < 10): msegundos = str("0" + str(msegundos))

                self.vLabelTempo.set(str(minutos) + ":" + str(segundos) + ":" + str(msegundos))

            else:
                self.cap.release()

    def _validate(self):
        if(self.eInicioCorte.get() == ""): #verifica se o campo está em branco
            messagebox.showerror("Erro", "Preencha o campo Início do corte")
            self.eInicioCorte.focus_set()
            return False
        else:
            if (util.validateInt(self.eInicioCorte.get()) == False):
                messagebox.showerror("Erro", "O campo Início do corte deve ser inteiro")
                self.eInicioCorte.focus_set()
                return False
            else:
                if (int(self.eInicioCorte.get()) < int(self.exame['t5'])):
                    messagebox.showerror("Erro", "O campo Início do corte deve ser maior que o fim do movimento")
                    self.eInicioCorte.focus_set()
                    return False

        if(self.eFimCorte.get() == ""):
            messagebox.showerror("Erro", "Preencha o campo Fim do corte")
            self.eFimCorte.focus_set()
            return False
        else:
            if (util.validateInt(self.eFimCorte.get()) == False):
                messagebox.showerror("Erro", "O campo Fim do corte deve ser inteiro")
                self.eFimCorte.focus_set()
                return False
            else:
                if(int(self.eFimCorte.get()) < int(self.eInicioCorte.get())):
                    messagebox.showerror("Erro", "O campo Fim do corte deve ser maior que o fim do movimento")
                    self.eFimCorte.focus_set()
                    return False
                else:
                    if (int(self.eFimCorte.get()) > int(self.exame['t6'])):
                        messagebox.showerror("Erro", "O campo Fim do corte deve ser menor ou igual que o fim do exame")
                        self.eFimCorte.focus_set()
        return True

    def _usarQuadroInicio(self):
        self.eInicioCorte.delete(0, END)
        self.eInicioCorte.insert(0, str(self.cont))

    def _usarQuadroFim(self):
        self.eFimCorte.delete(0, END)
        self.eFimCorte.insert(0, str(self.cont))

    def _reprocessar(self):
        self.btnReprocessar.grid_remove()
        self.varProcessamento.set(False)

        self.exame["processamento"] = "N"
        self.exame["t7"] = ""
        self.exame["t8"] = ""
        util.setExame(self.exame, self.dir)
        #apagar arquivo processado
        if os.path.exists(self.dir + "/frames"):
            shutil.rmtree(self.dir + "/frames")

        self.eInicioCorte["state"] = "normal"
        self.eInicioCorte.delete(0, END)
        self.eFimCorte["state"] = "normal"
        self.eFimCorte.delete(0, END)
        self.btnInicioCorte["state"] = "normal"
        self.btnFimCorte["state"] = "normal"

    def _deriva(self, vet):
        retorno = []
        for x in range(len(vet)):
            if (x == len(vet)-1):
                retorno.append(-vet[x])
            else:
                retorno.append(vet[int(x+1)] - vet[x])
        return retorno

    def _desEsc(self, vetX, vetY):
        retorno = []

        #Calcula o deslocamento
        for x in range(len(vetX)):
            retorno.append((vetX[x]**2+vetY[x]**2)**0.5)

        return retorno

    def _etapaAnterior(self):
        self.father._anamnese(self.exame['nome'], self.dir)

    def _proximaEtapa(self):
        if(not(self.exame['processamento'] is "S")):
            if(self._validate()):
                # start progress bar
                popup = Toplevel()
                popup.title("Processando...")
                popup.transient(self.father.window)
                popup.focus_force()
                popup.grab_set()

                popup.geometry('{}x{}+{}+{}'.format(300, 50, 500, 300))
                popup.resizable(False, False)
                popup.config(padx=5, pady=5)

                progress = 0
                progressVar = DoubleVar()
                textVar = StringVar()
                textVar.set("0%")
                progressBar = ttk.Progressbar(popup, variable=progressVar, maximum=100)
                progressBar.pack(side="top", fill="x")
                textLabel = Label(popup, textvariable=textVar)
                textLabel.pack(side="bottom")
                popup.pack_slaves()

                pos = []
                posArea = []
                posCircularidade = []
                posX = []
                posY = []
                posA = []


                # Caso houver a pasta de frames exclui
                if os.path.exists(self.dir + "/frames"):
                    shutil.rmtree(self.dir + "/frames")

                # Cria pasta para armazenar as imagens
                os.mkdir(self.dir + "/frames")

                quadrosProc = int(self.exame['t6']) - int(self.exame['t5']) + 1
                progress_step = float(100.0 / quadrosProc)

                if (self.cap.isOpened()):

                    for x in range(quadrosProc):
                        popup.update()

                        self.cap.set(1, (int(self.exame['t5']) + x))
                        ret, frame = self.cap.read()

                        if ret:
                            progress += progress_step
                            progressVar.set(progress)
                            textVar.set(str(int(progress)) + "%")
                            if((x >= (int(self.eInicioCorte.get()) - int(self.exame['t5']))) and (x <= (int(self.eFimCorte.get()) - int(self.exame['t5'])))):
                                #Alterar para os valores de retorno do algoritmo de reconhecimend da pupila
                                area, circularidade, posHor, posVer, ang, frame = util.findPupila(frame, 2)
                                cv2.imwrite(self.dir + "/frames/"+ str(x + int(self.exame['t5'])) + ".png", frame)

                            else:
                                area = 0
                                circularidade = 0
                                posVer = 0
                                posHor = 0
                                ang = 0

                        textVar.set(str(int(progress)) + "%")
                        pos.append(int(self.exame['t5']) + x)
                        posArea.append(area)
                        posCircularidade.append(circularidade)
                        posX.append(posHor)
                        posY.append(posVer)
                        posA.append(ang)

                    # __________    Faz os cálculos
                    # Calcula a velocidade no Eixo X
                    velX = self._deriva(posX)
                    # Calcula a aceleração em X
                    acelX = self._deriva(velX)
                    # Calcula a velocidade no Eixo Y
                    velY = self._deriva(posY)
                    # Calcula a aceleração em Y
                    acelY = self._deriva(velY)
                    # Calcula o deslocamento escalar
                    desEscalar = self._desEsc(posX, posY)
                    # Calcula a velocidade escalar
                    velEscalar = self._deriva(desEscalar)
                    # Calcula a aceleração escalar
                    acelEscalar = self._deriva(velEscalar)
                    # Calcula a velocidade Angular
                    velA = self._deriva(posA)
                    # Calcula a aceleração angular
                    acelA = self._deriva(velA)

                    arq = open(self.dir + "/dados.exa", "w")
                    for i in range(quadrosProc):
                        arq.write(str(pos[i]))
                        arq.write(";")
                        arq.write(str(posArea[i]))
                        arq.write(";")
                        arq.write(str(round(posCircularidade[i]*100, 2)))
                        arq.write(";")
                        arq.write(str(posX[i]))
                        arq.write(";")
                        arq.write(str(velX[i]))
                        arq.write(";")
                        arq.write(str(acelX[i]))
                        arq.write(";")
                        arq.write(str(posY[i]))
                        arq.write(";")
                        arq.write(str(velY[i]))
                        arq.write(";")
                        arq.write(str(acelY[i]))
                        arq.write(";")
                        arq.write(str(round(desEscalar[i],2)))
                        arq.write(";")
                        arq.write(str(round(velEscalar[i],2)))
                        arq.write(";")
                        arq.write(str(round(acelEscalar[i],2)))
                        arq.write(";")
                        arq.write(str(posA[i]))
                        arq.write(";")
                        arq.write(str(velA[i]))
                        arq.write(";")
                        arq.write(str(acelA[i]))
                        arq.write("\n")
                    arq.close()

                else:
                    print("Arquivo não encontrado")

                popup.destroy()

                self.exame['processamento'] = "S"
                self.exame['t7'] = self.eInicioCorte.get()
                self.exame['t8'] = self.eFimCorte.get()

                util.setExame(self.exame, self.dir)
                self.father._resultado(self.dir)

        else:
            self.father._resultado(self.dir)