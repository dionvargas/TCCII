import cv2
import numpy
import json
import os
from PIL import Image, ImageTk

def findPupila(frame, line=1):

    matriz = frame
    original = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #converte para escala de cinza

    # Filtro de média para remover ruídos
    im2 = cv2.medianBlur(original, 13)

    # Binarização identificar a pupila
    ret, im3 = cv2.threshold(im2, 35, 255, cv2.THRESH_BINARY_INV)  # extrai o pupila

    # Morfologia
    im4 = im3.copy()
    elementoEstruturanteAbertura = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23))
    for x in range(0, 1):
        im4 = cv2.morphologyEx(im4, cv2.MORPH_OPEN, elementoEstruturanteAbertura)

    # Binarização identificar o reflexo da pupila
    ret, im5 = cv2.threshold(im2, 200, 255, cv2.THRESH_BINARY)  # extrai o pupila

    im6 = cv2.add(im4, im5)

    # Morfologia
    im7 = im6.copy()
    elementoEstruturanteFechamento = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35))
    for x in range(0, 1):
        im7 = cv2.morphologyEx(im7, cv2.MORPH_CLOSE, elementoEstruturanteFechamento)
    for x in range(0, 1):
        im7 = cv2.morphologyEx(im7, cv2.MORPH_OPEN, elementoEstruturanteAbertura)

    # Calculando a circularidade
    modo = cv2.RETR_TREE
    metodo = cv2.CHAIN_APPROX_SIMPLE
    _, contornos, hierarquia = cv2.findContours(im7, modo, metodo)

    maiorCirc = 0
    maiorArea = 0
    circularidade = 0
    area = 0
    pupila = None

    for c in contornos:
        if (int(len(c) > 5)):

            area = cv2.contourArea(c)
            perimetro = cv2.arcLength(c, True)
            circularidade = (4 * numpy.pi * area) / (perimetro * perimetro)

            if ((area > maiorArea) and (circularidade > 0.57) and (area > 5000)):
                maiorArea = area
                maiorCirc = circularidade
                pupila = c

        else:
            print("Elipse muito pequena")

    final = matriz.copy()
    width, height = final.shape[:2]

    if (pupila is None):
        centroX = 0
        centroY = 0

    else:
        ellipse = cv2.fitEllipse(pupila)
        cv2.ellipse(final, ellipse, (0, 0, 255), line)

        centroX = int(ellipse[0][0])
        centroY = int(ellipse[0][1])

        # linha horizontal
        cv2.line(final, (centroX, 0), (centroX, width), (0, 0, 255), line)
        # linha vertical
        cv2.line(final, (0, centroY), (height, centroY), (0, 0, 255), line)

    angulo = 1

    return area, circularidade, centroX, centroY, angulo, final

def convertToExibe(frame, x=0, y=0):
    if ((x == 0) or (y == 0)):
        y = numpy.size(frame, 0)
        x = numpy.size(frame, 1)
    frame = cv2.resize(frame, (int(x), int(y)))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    return frame

def setPaciente(paciente):
    diretorio = os.getcwd() + "\\pacientes\\" + paciente["nome"]
    with open(diretorio + '\\paciente.json', 'w') as outfile:
        json.dump(paciente, outfile)

def getPaciente(nomePaciente):
    global paciente
    diretorio = os.getcwd() + "\\pacientes\\" + nomePaciente + '\\paciente.json'
    with open(diretorio) as json_file:
        paciente = json.load(json_file)
    return paciente

def setExame(exame, dir):
    with open(dir + '\\anamnese.json', 'w') as outfile:
        json.dump(exame, outfile)

def getExame(dir):
    global exame
    dir = dir + '\\anamnese.json'
    with open(dir) as json_file:
        exame = json.load(json_file)
    return exame

def getConfig():
    global config
    with open('configs.json') as json_file:
        config = json.load(json_file)
    return config

def setConfig(config):
    with open('configs.json', 'w') as outfile:
        json.dump(config, outfile)

def getExam():
    global exam
    with open('exam.json') as json_file:
        exam = json.load(json_file)
    return exam

def setExam(exam):
    with open('exam.json', 'w') as outfile:
        json.dump(exam, outfile)

def setDados(location, dados):
    with open(location + 'dados.json', 'w') as outfile:
        json.dump(dados, outfile)

def getDados(location):
    global dados
    with open(location+'\\dados.json') as json_file:
        dados = json.load(json_file)
    return dados

def validateInt(value):
    try:
        v = int(value)
        return True
    except ValueError:
        return False

def validateFloat(value):
    try:
        v = float(value)
        return value
    except ValueError:
        return None
