import util

from emptyContainer import EmptyContainer
from tkinter import *
from tkinter import messagebox

class AnamneseContainer(EmptyContainer):

    def __init__(self, father, nome, dir):
        super().__init__()

        self.father = father
        self.nome = nome
        self.dir = dir

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
        self.eExame = Entry(self.frameLeft, width=13, font='bold', state=DISABLED)
        self.eExame.grid(row=1, column=1, sticky=W + E, padx=5, pady=5)

        Label(self.frameLeft, font=("Helvetica", 18, "bold"), text="Status").grid(row=2, column=0, columnspan=2,
                                                                                  sticky=W + E + N, padx=5, pady=5)
        self.varExame = BooleanVar()
        self.varExame.set(False)
        self.checkExame = Checkbutton(self.frameLeft, var=self.varExame, state=DISABLED, offvalue=False, onvalue=True)
        self.checkExame.grid(row=3, column=0, sticky=N + S + E, padx=3, pady=3)
        Label(self.frameLeft, font=("Helvetica", 18), justify=LEFT, text="Exame").grid(row=3, column=1, sticky=N + S + W)

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

        Label(self.frameLeft, height=19, text=" ").grid(row=9, column=0, sticky=N + S + W + E)

        self.frameButtons = Frame(self.frameLeft)
        self.frameButtons.grid(column=0, row=10, columnspan=2, sticky=N + S + E + W)

        # Botão de próxima etapa e etapa anterior
        self.btnAnterior = Button(self.frameButtons, text="Atapa anterior", state=DISABLED)
        self.btnAnterior.grid(column=0, row=0, padx=15, pady=5, sticky=N + S + W)
        self.btnProxima = Button(self.frameButtons, text="Próxima etapa", command=lambda: self._proximaEtapa(),
                                 state=DISABLED)
        self.btnProxima.grid(column=1, row=0, padx=15, pady=5, sticky=N + S + W)

        # ____ FRAME DA DIREITA
        self.frameRight = Frame(self.root)
        self.frameRight.grid(column=1, row=0, sticky=N + S + E + W)

        # LINHA 0

        # FRAME DE ANAMNESE 1
        fAnamnese1 = Frame(self.frameRight, border=1, relief="groove")
        fAnamnese1.pack()

        # Anamnese linha 1
        Label(fAnamnese1, text="Possui problema de saúde?").grid(row=1, column=0, sticky=W, padx=3, pady=3)
        self.vPSaude = StringVar()
        self.vPSaude.set("N")
        self.radioSPSaude = Radiobutton(fAnamnese1, text="Sim", state=DISABLED, variable=self.vPSaude, value="S", command=self._changePSaude)
        self.radioSPSaude.grid(row=1, column=1, sticky=W, padx=3, pady=3)
        self.radioNPSaude = Radiobutton(fAnamnese1, text="Não", state=DISABLED, variable=self.vPSaude, value="N", command=self._changePSaude)
        self.radioNPSaude.grid(row=1, column=2, sticky=W, padx=3, pady=3)
        Label(fAnamnese1, text="Qual?").grid(row=1, column=3, sticky=W, padx=3, pady=3)
        self.ePSaude = Entry(fAnamnese1, width=48, state=DISABLED)
        self.ePSaude.config(state='disabled')
        self.ePSaude.grid(row=1, column=4, sticky=W + E, padx=3, pady=3)

        # Anamnese linha 2
        Label(fAnamnese1, text="Usa algum medicamento?").grid(row=2, column=0, sticky=W, padx=3, pady=3)
        self.vMedicamento = StringVar()
        self.vMedicamento.set("N")
        self.radioSMedicamento = Radiobutton(fAnamnese1, text="Sim", state=DISABLED, variable=self.vMedicamento, value="S",
                                             command=self._changeMedicamento)
        self.radioSMedicamento.grid(row=2, column=1, sticky=W, padx=3, pady=3)
        self.radioNMedicamento = Radiobutton(fAnamnese1, text="Não", state=DISABLED, variable=self.vMedicamento, value="N",
                                             command=self._changeMedicamento)
        self.radioNMedicamento.grid(row=2, column=2, sticky=W, padx=3, pady=3)
        Label(fAnamnese1, text="Qual?").grid(row=2, column=3, sticky=W, padx=3, pady=3)
        self.eMedicamento = Entry(fAnamnese1, state=DISABLED)
        self.eMedicamento.config(state='disabled')
        self.eMedicamento.grid(row=2, column=4, sticky=W + E, padx=3, pady=3)

        # Anamnese linha 3
        Label(fAnamnese1, text="Está sob algum tratamento médico?").grid(row=3, column=0, sticky=W, padx=3, pady=3)
        self.vTratamento = StringVar()
        self.vTratamento.set("N")
        self.radioSTratamento = Radiobutton(fAnamnese1, text="Sim", state=DISABLED, variable=self.vTratamento, value="S",
                                            command=self._changeTratamento)
        self.radioSTratamento.grid(row=3, column=1, sticky=W, padx=3, pady=3)
        self.radioNTratamento = Radiobutton(fAnamnese1, text="Não", state=DISABLED, variable=self.vTratamento, value="N",
                                            command=self._changeTratamento)
        self.radioNTratamento.grid(row=3, column=2, sticky=W, padx=3, pady=3)
        Label(fAnamnese1, text="Por que?").grid(row=3, column=3, sticky=W, padx=3, pady=3)
        self.eTratamento = Entry(fAnamnese1, state=DISABLED)
        self.eTratamento.config(state='disabled')
        self.eTratamento.grid(row=3, column=4, sticky=W + E, padx=3, pady=3)

        # Anamnese linha 4
        Label(fAnamnese1, text="Possui alergia a algum medicamento?").grid(row=4, column=0, sticky=W, padx=3, pady=3)
        self.vAlergia = StringVar()
        self.vAlergia.set("N")
        self.radioSAlergia = Radiobutton(fAnamnese1, text="Sim", state=DISABLED, variable=self.vAlergia, value="S",
                                         command=self._changeAlergia)
        self.radioSAlergia.grid(row=4, column=1, sticky=W, padx=3, pady=3)
        self.radioNAlergia = Radiobutton(fAnamnese1, text="Não", state=DISABLED, variable=self.vAlergia, value="N",
                                         command=self._changeAlergia)
        self.radioNAlergia.grid(row=4, column=2, sticky=W, padx=3, pady=3)
        Label(fAnamnese1, text="Qual?").grid(row=4, column=3, sticky=W, padx=3, pady=3)
        self.eAlergia = Entry(fAnamnese1, state=DISABLED)
        self.eAlergia.config(state='disabled')
        self.eAlergia.grid(row=4, column=4, sticky=W + E, padx=3, pady=3)

        # Anamnese linha 5
        Label(fAnamnese1, text="Usa lentes corretivas?").grid(row=5, column=0, sticky="W", padx=3, pady=3)
        self.vLentes = StringVar()
        self.vLentes.set("N")
        self.radioLLentes = Radiobutton(fAnamnese1, text="Lentes", state=DISABLED, variable=self.vLentes, value="L")
        self.radioLLentes.grid(row=5, column=1, sticky=W, padx=3, pady=3)
        self.radioOLentes = Radiobutton(fAnamnese1, text="Óculos", state=DISABLED, variable=self.vLentes, value="O")
        self.radioOLentes.grid(row=5, column=2, sticky=W, padx=3, pady=3)
        self.radioNLentes = Radiobutton(fAnamnese1, text="Não", state=DISABLED, variable=self.vLentes, value="N")
        self.radioNLentes.grid(row=5, column=3, sticky=W, padx=3, pady=3)

        # FRAME DE ANAMNESE 2

        fAnamnese2 = Frame(self.frameRight, border=1, relief="groove")
        fAnamnese2.pack()

        textTam = 830

        self.varAnamnese1 = BooleanVar()
        self.varAnamnese1.set(False)
        self.checkAnamnese1 = Checkbutton(fAnamnese2, var=self.varAnamnese1, state=DISABLED, offvalue=False, onvalue=True)
        self.checkAnamnese1.grid(row=0, column=0, sticky=N + S + W, padx=3, pady=5)
        Label(fAnamnese2, justify=LEFT, wraplength=textTam, text="Nistagmo não fatigável?").grid(row=0, column=1, sticky=N + S + W, padx=5, pady=5)

        self.varAnamnese2 = BooleanVar()
        self.varAnamnese2.set(False)
        self.checkAnamnese2 = Checkbutton(fAnamnese2, var=self.varAnamnese2, state=DISABLED, offvalue=False, onvalue=True)
        self.checkAnamnese2.grid(row=1, column=0, sticky=N + S + W, padx=3, pady=5)
        Label(fAnamnese2, justify=LEFT, wraplength=textTam,  text="Nistagmo  posicional é vertical puro e pode mudar de direção à mudança da posição da cabeça?").grid(row=1, column=1, sticky=N + S + W, padx=5, pady=5)

        self.varAnamnese3 = BooleanVar()
        self.varAnamnese3.set(False)
        self.checkAnamnese3 = Checkbutton(fAnamnese2, var=self.varAnamnese3, state=DISABLED, offvalue=False, onvalue=True)
        self.checkAnamnese3.grid(row=2, column=0, sticky=N + S + W, padx=3, pady=5)
        Label(fAnamnese2, justify=LEFT, wraplength=textTam, text="Nistagmo posicional é contínuo se o posicionamento desencadeante é mantido, com ou sem mudança de direção nas diferentes posições da cabeça?").grid(row=2, column=1, sticky=N + S + W, padx=5, pady=5)

        self.varAnamnese4 = BooleanVar()
        self.varAnamnese4.set(False)
        self.checkAnamnese4 = Checkbutton(fAnamnese2, var=self.varAnamnese4, state=DISABLED, offvalue=False, onvalue=True)
        self.checkAnamnese4.grid(row=3, column=0, sticky=N + S + W, padx=3, pady=5)
        Label(fAnamnese2, justify=LEFT, wraplength=textTam, text="Vertigem acompanhada ou não de desequilíbrio transitório ou duradouro à marcha? (Em episódios agudos, pode acompanhar nistagmo espontâneo, posicional ou de posicionamento, náuseas e vômitos)").grid(row=3, column=1, sticky=N + S + W, padx=5, pady=5)

        self.varAnamnese5 = BooleanVar()
        self.varAnamnese5.set(False)
        self.checkAnamnese5 = Checkbutton(fAnamnese2, var=self.varAnamnese5, state=DISABLED, offvalue=False, onvalue=True)
        self.checkAnamnese5.grid(row=4, column=0, sticky=N + S + W, padx=3, pady=5)
        Label(fAnamnese2, justify=LEFT, wraplength=textTam, text="Acompanha crises de nevralgia do trigêmio, espasmo facial e nevralgia glossofaríngea? A intensa vertigem posicional ou de posicionamento é acompanhada de desequilíbrio e osciloscopia?").grid(row=4, column=1, sticky=N + S + W, padx=5, pady=5)

        self.varAnamnese6 = BooleanVar()
        self.varAnamnese6.set(False)
        self.checkAnamnese6 = Checkbutton(fAnamnese2, var=self.varAnamnese6, state=DISABLED, offvalue=False, onvalue=True)
        self.checkAnamnese6.grid(row=5, column=0, sticky=N + S + W, padx=3, pady=5)
        Label(fAnamnese2, justify=LEFT, wraplength=textTam, text="Vertigens são posicionais intensas, acompanhadas de nistagmo posicional e/ou de posicionamento, sucedendo quadro clínico de vertigem aguda, por trombose da artéria vestibular anterior?").grid(row=5, column=1, sticky=N + S + W, padx=5, pady=5)

        self.btnExame = Button(self.frameRight, text="Realizar exame", font="bold", command=lambda: self._gravar())
        self.btnExame.pack(fill=BOTH, expand=1)

        self.btnProxima["state"] = NORMAL

        # ___ SE FOR UM NOVO EXAME
        if(self.dir is None):
            self.eNome["state"] = NORMAL
            self.eNome.delete(0, END)
            self.eNome.insert(0, self.nome)
            self.eNome["state"] = DISABLED

            self.labelExame.destroy()
            self.eExame.destroy()
            self.frameButtons.destroy()

            Label(self.frameLeft, height=5, text=" ").grid(row=10, column=0, sticky=N + S + W + E)

            self.radioSPSaude["state"] = NORMAL
            self.radioNPSaude["state"] = NORMAL
            self.radioSMedicamento["state"] = NORMAL
            self.radioNMedicamento["state"] = NORMAL
            self.radioSTratamento["state"] = NORMAL
            self.radioNTratamento["state"] = NORMAL
            self.radioSAlergia["state"] = NORMAL
            self.radioNAlergia["state"] = NORMAL
            self.radioLLentes["state"] = NORMAL
            self.radioOLentes["state"] = NORMAL
            self.radioNLentes["state"] = NORMAL

            self.checkAnamnese1["state"] = NORMAL
            self.checkAnamnese2["state"] = NORMAL
            self.checkAnamnese3["state"] = NORMAL
            self.checkAnamnese4["state"] = NORMAL
            self.checkAnamnese5["state"] = NORMAL
            self.checkAnamnese6["state"] = NORMAL

        # ___ SE FOR UM EXAME JÁ FEITO
        else:

            # Pega os dados da anamnese
            dadosExame = util.getExame(self.dir)

            # Nome
            self.eNome["state"] = NORMAL
            self.eNome.delete(0, END)
            self.eNome.insert(0, dadosExame['nome'])
            self.eNome["state"] = DISABLED

            # Número do exame
            self.eExame["state"] = NORMAL
            self.eExame.delete(0, END)
            self.eExame.insert(0, dadosExame['numero'])
            self.eExame["state"] = DISABLED

            # Checks de status
            if (str(dadosExame['exame']) is "S"):
                self.checkExame["state"] = NORMAL
                self.varExame.set(True)
                self.checkExame["state"] = DISABLED

            if (str(dadosExame['processamento']) is "S"):
                self.checkProcessamento["state"] = NORMAL
                self.varProcessamento.set(True)
                self.checkProcessamento["state"] = DISABLED

            if (str(dadosExame['resultados']) is "S"):
                self.checkResultados["state"] = NORMAL
                self.varResultados.set(True)
                self.checkResultados["state"] = DISABLED

            # Checks da anamnese 1
            if (str(dadosExame['problemaSaude']) is "S"):
                self.radioSPSaude["state"] = NORMAL
                self.vPSaude.set("S")
                self.radioSPSaude["state"] = DISABLED
                self.ePSaude["state"] = NORMAL
                self.ePSaude.delete(0, END)
                self.ePSaude.insert(0, str(dadosExame['tProblemaSaude']))
                self.ePSaude["state"] = DISABLED

            if (str(dadosExame['medicamento']) is "S"):
                self.radioSMedicamento["state"] = NORMAL
                self.vMedicamento.set("S")
                self.radioSMedicamento["state"] = DISABLED
                self.eMedicamento["state"] = NORMAL
                self.eMedicamento.delete(0, END)
                self.eMedicamento.insert(0, str(dadosExame['tMedicamento']))
                self.eMedicamento["state"] = DISABLED

            if (str(dadosExame['tratamento']) is "S"):
                self.radioSTratamento["state"] = NORMAL
                self.vTratamento.set("S")
                self.radioSTratamento["state"] = DISABLED
                self.eTratamento["state"] = NORMAL
                self.eTratamento.delete(0, END)
                self.eTratamento.insert(0, str(dadosExame['tTratamento']))
                self.eTratamento["state"] = DISABLED

            if (str(dadosExame['alergia']) is "S"):
                self.radioSAlergia["state"] = NORMAL
                self.vAlergia.set("S")
                self.radioSAlergia["state"] = DISABLED
                self.eAlergia["state"] = NORMAL
                self.eAlergia.delete(0, END)
                self.eAlergia.insert(0, str(dadosExame['tAlergia']))
                self.eAlergia["state"] = DISABLED

            if (str(dadosExame['lentes']) is "L"):
                self.radioLLentes["state"] = NORMAL
                self.vLentes.set("L")
                self.radioLLentes["state"] = DISABLED

            if (str(dadosExame['lentes']) is "O"):
                self.radioOLentes["state"] = NORMAL
                self.vLentes.set("O")
                self.radioOLentes["state"] = DISABLED

            # Checks da anamnese 2
            if (str(dadosExame['fatigavel']) is "S"):
                self.checkAnamnese1["state"] = NORMAL
                self.varAnamnese1.set(True)
                self.checkAnamnese1["state"] = DISABLED

            if (str(dadosExame['mudaPosicao']) is "S"):
                self.checkAnamnese2["state"] = NORMAL
                self.varAnamnese2.set(True)
                self.checkAnamnese2["state"] = DISABLED

            if (str(dadosExame['continuo']) is "S"):
                self.checkAnamnese3["state"] = NORMAL
                self.varAnamnese3.set(True)
                self.checkAnamnese3["state"] = DISABLED

            if (str(dadosExame['vertigem']) is "S"):
                self.checkAnamnese4["state"] = NORMAL
                self.varAnamnese4.set(True)
                self.checkAnamnese4["state"] = DISABLED

            if (str(dadosExame['navralgia']) is "S"):
                self.checkAnamnese5["state"] = NORMAL
                self.varAnamnese5.set(True)
                self.checkAnamnese5["state"] = DISABLED

            if (str(dadosExame['intensas']) is "S"):
                self.checkAnamnese6["state"] = NORMAL
                self.varAnamnese6.set(True)
                self.checkAnamnese6["state"] = DISABLED

            self.btnExame["text"] = "O exame já foi realizado"
            self.btnExame["state"] = DISABLED

    def _changePSaude(self):
        if self.vPSaude.get() is "S":
            self.ePSaude.config(state='normal')
        else:
            self.ePSaude.delete(0, END)
            self.ePSaude.config(state='disabled')

    def _changeMedicamento(self):
        if self.vMedicamento.get() is "S":
            self.eMedicamento.config(state='normal')
        else:
            self.eMedicamento.delete(0, END)
            self.eMedicamento.config(state='disabled')

    def _changeTratamento(self):
        if self.vTratamento.get() is "S":
            self.eTratamento.config(state='normal')
        else:
            self.eTratamento.delete(0, END)
            self.eTratamento.config(state='disabled')

    def _changeAlergia(self):
        if self.vAlergia.get() is "S":
            self.eAlergia.config(state='normal')
        else:
            self.eAlergia.delete(0, END)
            self.eAlergia.config(state='disabled')

    def _validate(self):
        if (self.vPSaude.get() == "S" and self.ePSaude.get() == ""):
            messagebox.showerror("Erro", "Expecificar o problema de saúde")
            self.ePSaude.focus_set()
            return False

        if (self.vMedicamento.get() == "S" and self.eMedicamento.get() == ""):
            messagebox.showerror("Erro", "Expecificar o medicamento")
            self.eMedicamento.focus_set()
            return False

        if (self.vTratamento.get() == "S" and self.eTratamento.get() == ""):
            messagebox.showerror("Erro", "Expecificar o tratamento")
            self.eTratamento.focus_set()
            return False

        if (self.vAlergia.get() == "S" and self.eAlergia.get() == ""):
            messagebox.showerror("Erro", "Expecificar qual medicament possui alergia")
            self.eAlergia.focus_set()
            return False

        return True

    def _gravar(self):
        if (self._validate()):

            # Cria o dicionário com os dados da anamnese
            exame = {
                "nome": self.eNome.get(),

                "exame": "S",
                "processamento": "N",
                "resultados": "N",

                "numero": "",
                "data": "",
                "hora": "",

                "problemaSaude": self.vPSaude.get(),
                "tProblemaSaude": self.ePSaude.get(),
                "medicamento": self.vMedicamento.get(),
                "tMedicamento": self.eMedicamento.get(),
                "tratamento": self.vTratamento.get(),
                "tTratamento": self.eTratamento.get(),
                "alergia": self.vAlergia.get(),
                "tAlergia": self.eAlergia.get(),
                "lentes": self.vLentes.get(),

                "fatigavel": self.varAnamnese1.get(),
                "mudaPosicao": self.varAnamnese2.get(),
                "continuo": self.varAnamnese3.get(),
                "vertigem": self.varAnamnese4.get(),
                "navralgia": self.varAnamnese5.get(),
                "intensas": self.varAnamnese6.get(),

                "t1": "",
                "t2": "",
                "t3": "",
                "t4": "",
                "t5": "",
                "t6": "",
                "t7": "",
                "t8": "",

                "frames": "",
                "fps": "",

                "mediaX": "",
                "desvioX": "",
                "mediaY": "",
                "desvioY": "",
                "mediaArea": "",
                "desvioArea": "",
                "mediaAngulo": "",
                "desvioAngulo": ""
            }

            self.father._gravar(exame, self.dir)

    def _etapaAnterior(self):
        print("Etapa anterior")

    def _proximaEtapa(self):
        self.father._preProcessamento(self.dir)
