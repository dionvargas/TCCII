import cv2
import numpy as np
import json
import os
from PIL import Image, ImageTk

def removeReflexos(frame):
    image_in = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)               # Load the glared image
    h, s, v = cv2.split(cv2.cvtColor(image_in, cv2.COLOR_RGB2HSV))  # split into HSV components

    ret, th = cv2.threshold(h, 20, 255, cv2.THRESH_BINARY_INV)

    disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    mascara = cv2.dilate(th.astype(np.uint8), disk)

    corrected = cv2.inpaint(image_in, mascara, 10, cv2.INPAINT_TELEA)

    return corrected

def findIris(frame, posH, posV, line=8):
    matriz = frame
    original = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # converte para escala de cinza

    posCart = (posH**2+posV**2)**(1/2)

    # Filtro de média para remover ruídos
    suavizada = cv2.medianBlur(original, 15)

    cimg = matriz.copy()
    circles = cv2.HoughCircles(suavizada, cv2.HOUGH_GRADIENT, 1, 100, param1=40, param2=30, minRadius=100, maxRadius=400)

    if(circles is not None):

        circles = np.int16(np.around(circles))

        maiorRaio = 0
        pupila = None
        distancia = 0

        for i in circles[0, :]:
            disCar = abs(posCart - (i[0] ** 2 + i[1] ** 2) ** (1 / 2))
            if(posH == 0 and posV == 0):
                if (i[2] > maiorRaio and i[2] > 100 and i[2] < 220):
                    maiorRaio = i[2]
                    distancia = disCar
                    pupila = i
            else:
                if (distancia > disCar and i[2] > 100 and i[2] < 220):
                    maiorRaio = i[2]
                    distancia = disCar
                    pupila = i

        if(pupila is not None):
            # draw the outer circle
            cv2.circle(cimg, (pupila[0], pupila[1]), pupila[2], (0, 255, 0), line)
            # draw the center of the circle
            cv2.circle(cimg, (pupila[0], pupila[1]), 2, (0, 0, 255), line)

            area = float(np.pi * pupila[2]**2)
            circularidade = 1
            centroX = pupila[0]
            centroY = pupila[1]
            angulo = 0

            final = cimg.copy()

        else:
            area = 0
            circularidade = 0
            centroX = 0
            centroY = 0
            angulo = 0

            final = matriz.copy()

    else:
        area = 0
        circularidade = 0
        centroX = 0
        centroY = 0
        angulo = 0

        final = matriz.copy()

    return area, circularidade, centroX, centroY, angulo, final

def findPupila(frame, line=5):

    matriz = frame

    image_in = cv2.cvtColor(matriz, cv2.COLOR_BGR2RGB)              # Load the glared image
    h, s, v = cv2.split(cv2.cvtColor(image_in, cv2.COLOR_RGB2HSV))  # split into HSV components

    ret, s = cv2.threshold(s, 20, 255, cv2.THRESH_BINARY)

    ret, reflexos = cv2.threshold(h, 10, 255, cv2.THRESH_BINARY_INV)
    s = cv2.add(s, reflexos)

    disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (50, 50))
    s = cv2.morphologyEx(s, cv2.MORPH_CLOSE, disk)
    elementReflexos = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    s = cv2.morphologyEx(s, cv2.MORPH_OPEN, elementReflexos)

    # Calculando a circularidade
    modo = cv2.RETR_TREE
    metodo = cv2.CHAIN_APPROX_SIMPLE
    contornos, hierarquia = cv2.findContours(s, modo, metodo)

    maiorArea = 0
    circularidade = 0
    area = 0
    pupila = None

    for c in contornos:
        if (int(len(c) > 5)):

            area = cv2.contourArea(c)
            perimetro = cv2.arcLength(c, True)
            circularidade = (4 * np.pi * area) / (perimetro * perimetro)

            if ((area > maiorArea) and (circularidade > 0.50) and (area > 3000) and (area < 7000)):
                maiorArea = area
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
        y = np.size(frame, 0)
        x = np.size(frame, 1)
    frame = cv2.resize(frame, (int(x), int(y)))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
    return frame

def setPaciente(paciente):
    diretorio = os.getcwd() + "/pacientes/" + paciente["nome"]
    with open(diretorio + '/paciente.json', 'w') as outfile:
        json.dump(paciente, outfile)

def getPaciente(nomePaciente):
    global paciente
    diretorio = os.getcwd() + "/pacientes/" + nomePaciente + '/paciente.json'
    with open(diretorio) as json_file:
        paciente = json.load(json_file)
    return paciente

def setExame(exame, dir):
    with open(dir + '/anamnese.json', 'w') as outfile:
        json.dump(exame, outfile)

def getExame(dir):
    global exame
    dir = dir + '/anamnese.json'
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
    with open(location+'/dados.json') as json_file:
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
