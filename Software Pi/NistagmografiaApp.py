import tkinter
import os
import platform
from builtins import print

import util
import RPi.GPIO as gpio
from picamera import PiCamera

from tkinter import *

from startContainer import StartContainer
from previewConfiguration import PreviewConfiguration
from listarPacientesContainer import ListarPacientesContainer
from novoPacientePopup import NovoPacientePopup
from anamneseContainer import AnamneseContainer
from gravarContainer import GravarContainer
from preProcessamentoContainer import PreProcessamentoContainer
from resultadoContainer import ResultadoContainer
from sobrePopup import SobrePopup


class App:

    global config
    global exam

    def __init__(self, window, window_title):
        global exam

        # __________________________________________________________________________________________________________
        #verifica se existe pasta de pacientes, se não existe cria
        if not os.path.exists(os.getcwd() + '/pacientes'):
            os.mkdir(os.getcwd() + '/pacientes')

        # __________________________________________________________________________________________________________
        # Configuração dos pinos de IO do Raspberry
        # Configura para não mostrar alertas
        gpio.setwarnings(False)

        # Configurando GPIO
        gpio.setmode(gpio.BOARD)
        gpio.setup(33, gpio.IN, pull_up_down=gpio.PUD_DOWN)  # Botão
        gpio.setup(35, gpio.OUT)  # LEDVD
        gpio.setup(37, gpio.OUT)  # LEDVM
        gpio.setup(38, gpio.OUT)  # LEDIR
        gpio.setup(40, gpio.OUT)  # LEDBR

        # Configurando o PWM com os valores iniciais de frequencia e dutycicle
        self.pwmIr = gpio.PWM(38, 180)
        self.pwmIr.start(0)
        self.pwmWhite = gpio.PWM(40, 180)
        self.pwmWhite.start(0)

        # __________________________________________________________________________________________________________
        # inicia a camera
        self.picam = PiCamera()

        # __________________________________________________________________________________________________________
        # para pegar o tamanho da tela
        width_value = window.winfo_screenwidth()
        height_value = window.winfo_screenheight() - 100

        exam = util.getExam()
        exam['monitorHeight'] = width_value
        exam['monitorWidth'] = height_value
        util.setExam(exam)

        self.window = window
        self.window.title(window_title)
        #self.window.wm_iconbitmap("resources/icone.ico")
        self.window.geometry("%dx%d+0+0" % (width_value, height_value))
        self.window.resizable(0, 0)  # se quiser deixar sem poder redimencioar a janela

        # Variável de popup
        self.flagPopup = FALSE

        # Barra de menus
        menuBar = Menu(self.window)
        self.window.config(menu=menuBar)
        fileMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Arquivo", menu=fileMenu)
        fileMenu.add_command(label="Ajustar câmera...", command=self._ajustarCamera)
        fileMenu.add_separator()
        fileMenu.add_command(label="Sair", command=self._close)
        pacienteMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Pacientes", menu=pacienteMenu)
        pacienteMenu.add_command(label="Adicionar...", command=self._adicionarPaciente)
        pacienteMenu.add_command(label="Listar", command=self._listarPacientes)
        # exameMenu = Menu(menuBar, tearoff=0)
        # menuBar.add_cascade(label="Exame", menu=exameMenu)
        # exameMenu.add_command(label="Adicionar...", command=self._sobre)
        # exameMenu.add_command(label="Listar", command=self._sobre)
        helpMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Ajuda", menu=helpMenu)
        helpMenu.add_command(label="Sobre...", command=self._sobre)

        # Container
        self.container = StartContainer()
        self.container.pack(fill='both', expand=True)

        #self.window.protocol("WM_DELETE_WINDOW", self._close())
        #self.window.bind("<Destroy>", self._close())

        self.window.mainloop()

    def _ajustarCamera(self):
        self.container.destroy()
        self.container = PreviewConfiguration(self, self.picam, self.pwmIr, self.pwmWhite)
        self.container.pack(fill='both', expand=True)

    def _listarPacientes(self):
        self.container.destroy()
        self.container = ListarPacientesContainer(self)
        self.container.pack(fill='both', expand=True)

    def _adicionarPaciente(self, nomePacinete = None):
        if (not self.flagPopup):
            self.flagPopup = True
            NovoPacientePopup(self, nomePacinete)

    def _anamnese(self, nome, dir=None):
        self.container.destroy()
        self.container = AnamneseContainer(self, nome, dir)
        self.container.pack(fill='both', expand=True)

    def _gravar(self, exame, dir):
        self.container.destroy()
        self.container = GravarContainer(self, exame, self.picam, self.pwmIr, self.pwmWhite, dir)
        self.container.pack(fill='both', expand=True)

    def _preProcessamento(self, dir):
        self.container.destroy()
        self.container = PreProcessamentoContainer(self, dir)
        self.container.pack(fill='both', expand=True)

    def _resultado(self, dir):
        self.container.destroy()
        self.container = ResultadoContainer(self, dir)
        self.container.pack(fill='both', expand=True)

    def _sobre(self):
        if (not self.flagPopup):
            self.flagPopup = True
            SobrePopup(self)

    def _empty(self):
        self.container.destroy()
        self.container = StartContainer()
        self.container.pack(fill='both', expand=True)

    def _close(self):
        gpio.output(35, gpio.LOW)  # LEDVD
        gpio.output(37, gpio.LOW)  # LEDVM
        gpio.output(38, gpio.LOW)  # LEDIR
        gpio.output(40, gpio.LOW)  # LEDBR
        gpio.cleanup()

        self.window.quit()
        self.window.destroy()
        exit(0)

def run():
    global config
    global exam

    location = os.getcwd() + '/'

    if not os.path.isfile(location + "exam.json"):
        print("Criando arquivo exam.json")
        exam = {
            "monitorHeight": 0,
            "monitorWidth": 0,
            "ledIr": 100,
            "ledBr": 100,
            "contraste": 0,
            "saturacao": 0,
            "nitidez": 0,
            "brilho": 50,
            "cameraMode": 7,
            "fps": 90,
            "t1": 2,
            "t2": 7,
            "t3": 10,
            "saveLocation": os.getcwd(),
            "colorEfect": False,
            "rColor": 128,
            "bColor": 128,
            "gColor": 128
        }
        util.setExam(exam)

    if not os.path.isfile(location + "configs.json"):
        print("Criando arquivo configs.json")
        res = {}
        res['resolutions'] = []
        res['resolutions'].append({
            "resName": "Mode 1",
            "minfps": 1,
            "maxfps": 30,
            "width": 1920,
            "height": 1080
        })
        res['resolutions'].append({
            "resName": "Mode 2",
            "minfps": 1,
            "maxfps": 15,
            "width": 2592,
            "height": 1944
        })
        res['resolutions'].append({
            "resName": "Mode 3",
            "minfps": 0.17,
            "maxfps": 1,
            "width": 2592,
            "height": 1944
        })
        res['resolutions'].append({
            "resName": "Mode 4",
            "minfps": 1,
            "maxfps": 42,
            "width": 1296,
            "height": 972
        })
        res['resolutions'].append({
            "resName": "Mode 5",
            "minfps": 1,
            "maxfps": 49,
            "width": 640,
            "height": 480
        })
        res['resolutions'].append({
            "resName": "Mode 6",
            "minfps": 42.1,
            "maxfps": 60,
            "width": 1920,
            "height": 1080
        })
        res['resolutions'].append({
            "resName": "Mode 7",
            "minfps": 60.1,
            "maxfps": 90,
            "width": 640,
            "height": 480
        })

        ext = {}
        ext['extensions'] = []
        ext['extensions'].append({
            "extension": "MP4",
            "archive": ".mp4",
            "text": "Arquivos MP4"
        })

        configs = {
            'resolutions': res['resolutions'],
            'extensions': ext['extensions']
        }

        util.setConfig(configs)
      

    # Comando para poder usar a camera do raspberry como camera normal
    if (platform.system() == "Linux"):
        os.system('sudo modprobe bcm2835-v4l2')

    # Cria a janela e passa como parametro o objeto da aplicação
    App(tkinter.Tk(), "Sistema Hórus")

if __name__ == '__main__':
    print('running....')
    run()
