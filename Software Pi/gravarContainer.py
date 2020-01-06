import util
import shutil
import os
import subprocess
import cv2

from clock import Clock
from datetime import datetime
from emptyContainer import EmptyContainer
from tkinter import *
from tkinter import messagebox
import RPi.GPIO as gpio

class GravarContainer(EmptyContainer):

    gravando = False

    def __init__(self, father, exame, picam, pwmIr, pwmWhite, dir):
        super().__init__()

        exam = util.getExam()
        config = util.getConfig()

        self.father = father
        self.exame = exame
        self.picam = picam
        self.dir = dir
        self.endExame = False
        self.manobra = False
        self.fimManobra = False

        self.pwmIr = pwmIr
        self.pwmWhite = pwmWhite
        self.camera = picam

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

        Label(self.frameLeft, font=("Helvetica", 18, "bold"), text="Status").grid(row=2, column=0, columnspan=2,
                                                                                  sticky=W + E + N, padx=5, pady=5)
        self.varExame = BooleanVar()
        self.varExame.set(False)
        self.checkExame = Checkbutton(self.frameLeft, var=self.varExame, state=DISABLED, offvalue=False, onvalue=True)
        self.checkExame.grid(row=3, column=0, sticky=N + S + E, padx=3, pady=3)
        Label(self.frameLeft, font=("Helvetica", 18), justify=LEFT, text="Exame").grid(row=3, column=1,
                                                                                       sticky=N + S + W)
        self.varProcessamento = BooleanVar()
        self.varProcessamento.set(False)
        self.checkProcessamento = Checkbutton(self.frameLeft, var=self.varProcessamento, state=DISABLED, offvalue=False,
                                              onvalue=True)
        self.checkProcessamento.grid(row=6, column=0, sticky=N + S + E, padx=3, pady=3)
        Label(self.frameLeft, font='bold', justify=LEFT, text="Processamento").grid(row=6, column=1, sticky=N + S + W)

        self.varResultados = BooleanVar()
        self.varResultados.set(False)
        self.checkResultados = Checkbutton(self.frameLeft, var=self.varResultados, state=DISABLED, offvalue=False,
                                           onvalue=True)
        self.checkResultados.grid(row=7, column=0, sticky=N + S + E, padx=3, pady=3)
        Label(self.frameLeft, font='bold', justify=LEFT, text="Resultados").grid(row=7, column=1, sticky=N + S + W)

        Label(self.frameLeft, height=24, text=" ").grid(row=13, column=0, sticky=N + S + W + E)

        # ____ FRAME DA DIREITA
        self.frameRight = Frame(self.root, relief="groove", border=1)
        self.frameRight.grid(column=1, row=0, sticky=N + S + E + W)

        self.tempos = Frame(self.frameRight, height=40)
        self.tempos.pack(side="top", fill="x")
        self.tempos.configure(relief="groove", border=3, padx=5, pady=5)

        Label(self.tempos, text="Tempos de exame", font="bold").grid(column=0, row=0, columnspan=2)

        Label(self.tempos, text="Tempo de espera").grid(column=0, row=1, columnspan=2)
        self.eT1 = Entry(self.tempos, width=2)
        self.eT1.delete(0, END)
        self.eT1.insert(0, str(exam['t1']))
        self.eT1.grid(column=0, row=2, sticky=E)
        Label(self.tempos, text="segundos").grid(column=1, row=2, sticky=W)

        Label(self.tempos, text="Tempo de miose").grid(column=0, row=3, columnspan=2)
        self.eT2 = Entry(self.tempos, width=2)
        self.eT2.delete(0, END)
        self.eT2.insert(0, str(exam['t2']))
        self.eT2.grid(column=0, row=4, sticky=E)
        Label(self.tempos, text="segundos").grid(column=1, row=4, sticky=W)

        Label(self.tempos, text="Tempo de midriase").grid(column=0, row=5, columnspan=2)
        self.eT3 = Entry(self.tempos, width=2)
        self.eT3.delete(0, END)
        self.eT3.insert(0, str(exam['t3']))
        self.eT3.grid(column=0, row=6, sticky=E)
        Label(self.tempos, text="segundos").grid(column=1, row=6, sticky=W)

        self.temposMovimento = Frame(self.frameRight, height=40)
        self.temposMovimento.pack(side="top", fill="x")
        self.temposMovimento.configure(relief="groove", border=3, padx=5, pady=5)

        self.lMT1 = StringVar()
        self.lMT1.set("Inicio do movimento")
        Label(self.temposMovimento, textvariable=self.lMT1).grid(column=0, row=0)

        self.lMT2 = StringVar()
        self.lMT2.set("Fim do movimento")
        Label(self.temposMovimento, textvariable=self.lMT2).grid(column=0, row=1)

        self.lMT3 = StringVar()
        self.lMT3.set("Fim do movimento")
        Label(self.temposMovimento, textvariable=self.lMT3).grid(column=0, row=2)

        controle = Frame(self.frameRight, height=40)
        controle.pack(side="bottom", fill="x")
        controle.configure(relief="groove", border=3, padx=5, pady=5)

        self.varBtnGravar = StringVar()
        self.varBtnGravar.set("Iniciar exame")
        self.btnGravar = Button(controle, textvariable=self.varBtnGravar, command=self._gravar).pack(side="bottom", fill="y")

        self.cl = Clock(self)

        self.eNome["state"] = NORMAL
        self.eNome.delete(0, END)
        self.eNome.insert(0, exame['nome'])
        self.eNome["state"] = DISABLED

        # ____ JANELA DE PREVIEW
        self.camera = picam

        self.camera.sensor_mode = exam["cameraMode"]
        for key in config['resolutions']:
            if key['resName'] == "Mode " + str(exam["cameraMode"]):
                self.camera.resolution = (key['width'], key['height'])

        self.camera.framerate = exam['fps']

        self.camera.brightness = exam['brilho']
        self.camera.contrast = exam['contraste']
        self.camera.sharpness = exam['nitidez']
        self.camera.saturation = exam['saturacao']
        if exam['colorEfect']:
            red = exam['rColor']
            green = exam['gColor']
            blue = exam['bColor']

            y = float(0.299 * red) + float(0.587 * green) + float(0.114 * blue)
            u = float(0.492 * (blue - y))
            v = float(0.877 * (red - y))

            self.camera.color_effects = (u, v)

        self.widthWindowPreview = 640
        self.heightWindowPreview = 480
        self.xControl = int(555)
        self.yControl = int(155)

        for key in config['resolutions']:
            if key['resName'] == "Mode " + str(exam["cameraMode"]):
                self.camera.sensor_mode = exam["cameraMode"]
                self.camera.resolution = (key['width'], key['height'])
        self.camera.start_preview(fullscreen=False, window=(self.xControl, self.yControl, self.widthWindowPreview, self.heightWindowPreview))

    def _validate(self):
        if(self.eT1.get() == ""): #verifica se o campo está em branco
            messagebox.showerror("Erro", "Preencha o tempo de espera")
            self.eT1.focus_set()
            return False
        else:
            if(util.validateInt(self.eT1.get()) == False):
                messagebox.showerror("Erro", "O tempo de espera deve ser inteiro")
                self.eT1.focus_set()
                return False
            else:
                if(int(self.eT1.get()) < 1):
                    messagebox.showerror("Erro", "O tempo de espera deve ser ao menos um segundo")
                    self.eT1.focus_set()
                    return False
        if(self.eT2.get() == ""):
            messagebox.showerror("Erro", "Preencha o tempo de miose")
            self.eT2.focus_set()
            return False
        else:
            if(util.validateInt(self.eT2.get()) == False):
                messagebox.showerror("Erro", "O tempo de miose deve ser inteiro")
                self.eT2.focus_set()
                return False
            else:
                if(int(self.eT2.get()) < 1):
                    messagebox.showerror("Erro", "O tempo de miose deve ser ao menos um segundo")
                    self.eT2.focus_set()
                    return False
        if(self.eT3.get() == ""):
            messagebox.showerror("Erro", "Preencha o tempo de midriase")
            self.eT3.focus_set()
            return False
        else:
            if(util.validateInt(self.eT3.get()) == False):
                messagebox.showerror("Erro", "O tempo de midriase deve ser inteiro")
                self.eT3.focus_set()
                return False
            else:
                if(int(self.eT3.get()) < 1):
                    messagebox.showerror("Erro", "O tempo de midriase deve ser ao menos um segundo")
                    self.eT3.focus_set()
                    return False
        return True

    def _gravar(self):
        global exam

        if(self._validate()):
            exam = util.getExam()

            if(not self.gravando):
                self.gravando = True
                self.eT1['state'] = DISABLED
                self.eT2['state'] = DISABLED
                self.eT3['state'] = DISABLED
                self.pwmWhite.ChangeDutyCycle(exam['ledBr'])
                self.picam.start_recording('temp.h264')
                self.cl.start()
                self.varBtnGravar.set("Encerrar Exame")
            else:
                self.endExame = True

    def cbClock(self, i):
        if(self.gravando):

            # 35 LED Verde
            # 37 LED Vermelho

            if(i == 200): # 2 segundos
                self.exame['t1'] = i
                gpio.output(35, gpio.HIGH)

            if(i == 700): # 7 segundos
                self.exame['t2'] = i
                gpio.output(35, gpio.LOW)
                self.pwmIr.ChangeDutyCycle(exam['ledIr'])
                self.pwmWhite.ChangeDutyCycle(0)

            if(i == 1000): # 10 segundos
                self.exame['t3'] = i
                gpio.output(37, gpio.HIGH)

            if(i > 1000 and gpio.input(33) == 0 and self.manobra == False): # mais que 10 segundos
                self.lMT1.set("-> Início do movimento")
                self.exame['t4'] = i
                self.manobra = True
                gpio.output(37, gpio.LOW)

            if(self.manobra == True and gpio.input(33) == 1 and self.fimManobra == False):
                self.lMT2.set("-> Fim do movimento")
                self.fimManobra = True
                self.exame['t5'] = i
                gpio.output(37, gpio.HIGH)
                self.pwmIr.ChangeDutyCycle(0)
                self.pwmWhite.ChangeDutyCycle(exam['ledBr'])

            if(self.endExame):
                self.cl.stop()

                self.lMT3.set("-> Fim do exame")

                self.picam.stop_recording()
                self.gravando = False
                self.exame['t6'] = i

                gpio.output(35, gpio.LOW)           # LEDVD
                gpio.output(37, gpio.LOW)           # LEDVM
                self.pwmWhite.ChangeDutyCycle(0)    # LEDIR
                self.pwmIr.ChangeDutyCycle(0)       # LEDBR

                now = datetime.now()
                nowstr = now.strftime("%Y-%m-%d-%H-%M")

                command = "MP4Box -fps %d -add temp.h264 exame.mp4" % (exam['fps'])

                subprocess.check_output(command, shell=True)
                os.remove(os.getcwd() + "/temp.h264")  # remove o arquivo temporario

                if os.path.isfile("exame.mp4"):

                    destino = os.getcwd() + "/pacientes/" + self.exame["nome"] + "/" + nowstr
                    os.mkdir(destino)
                    shutil.copyfile("exame.mp4", destino + "/exame.mp4")

                    captura = cv2.VideoCapture(destino + "/exame.mp4")

                    self.exame['data'] = now.strftime("%d/%m/%Y")
                    self.exame['hora'] = now.strftime("%H:%M")
                    self.exame['numero'] = now.strftime("%Y%m%d%H%M")
                    self.exame['exame'] = "S"
                    self.exame['frames'] = captura.get(cv2.CAP_PROP_FRAME_COUNT)
                    self.exame['fps'] = captura.get(cv2.CAP_PROP_FPS)

                    self.exame['t1'] = int((int(self.exame['t1']) - 0.05) / 1.11)
                    self.exame['t2'] = int((int(self.exame['t2']) - 0.05) / 1.11)
                    self.exame['t3'] = int((int(self.exame['t3']) - 0.05) / 1.11)
                    self.exame['t4'] = int((int(self.exame['t4']) - 0.05) / 1.11)
                    self.exame['t5'] = int((int(self.exame['t5']) - 0.05) / 1.11)
                    self.exame['t6'] = int((int(self.exame['t6']) - 0.05) / 1.11)

                    util.setExame(self.exame, destino)

                    os.remove("exame.mp4")  # remove o arquivo de exame da pasta raiz
                    self.camera.stop_preview()

                    self.father._preProcessamento(destino)

                else:
                    messagebox.showerror("Erro", "Algo deu errado na gravação do arquivo")