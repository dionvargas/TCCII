import glob

import util
import os

from emptyContainer import EmptyContainer
from tkinter import *
from tkinter import ttk

class ListarPacientesContainer(EmptyContainer):

    def __init__(self, father):
        super().__init__()

        self.father = father
        exam = util.getExam()

        # ____ FRAME PRINCIPAL
        self.root = Frame(self)
        self.root.pack(fill="both", expand="True")

        # ____ FRAME DA ESQUERDA
        self.frameLeft = Frame(self.root)
        self.frameLeft.grid(column=0, row=0, sticky=N + S + E + W)

        listboxPacientes = Listbox(self.frameLeft, width=30, height=33)
        scrollbarPacientes = Scrollbar(self.frameLeft, orient="vertical")
        scrollbarPacientes.config(command=listboxPacientes.yview)
        scrollbarPacientes.pack(side="right", fill="y")
        listboxPacientes.config(yscrollcommand=scrollbarPacientes.set)
        def _selectPaciente(evt):
            eventPaciente = evt.widget
            if eventPaciente.curselection():
                indexPaciente = int(eventPaciente.curselection()[0])
                valuePaciente = eventPaciente.get(indexPaciente)
                self.atualizaDados(valuePaciente)

        listboxPacientes.bind('<<ListboxSelect>>', _selectPaciente)
        listboxPacientes.pack()
        pacientes = os.getcwd() + '\pacientes'
        self.listPacientes = []
        for diretorio in glob.glob(pacientes + "\*"):
            nome = diretorio.split("\\")
            nome = nome[len(nome) - 1]
            self.listPacientes.append(nome)

        self.listPacientes = sorted(self.listPacientes)

        for nome in self.listPacientes:
            listboxPacientes.insert(END, nome)

        # ____ FRAME DA DIREITA
        self.frameRight = Frame(self.root)
        self.frameRight.grid(column=1, row=0, sticky=N + S + E + W)

        # LINHA 0
        # NOME
        self.frameNome = Frame(self.frameRight)
        self.frameNome.grid(column=0, row=0, sticky=N + S + E + W)
        Label(self.frameNome, font='bold', text="Nome").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.eNome = Entry(self.frameNome, width=63, font='bold', state=DISABLED)
        self.eNome.grid(row=0, column=1, sticky=W + E, padx=5, pady=5)
        self.editarContato = Button(self.frameRight, text="Editar contato", state=DISABLED, command=lambda: self._editarContato())
        self.editarContato.grid(row=0, column=1, sticky=W + E)

        # DADOS PESSOAIS
        self.framePessoais = Frame(self.frameRight, border=1, relief="groove")
        self.framePessoais.grid(column=0, row=1, sticky=N + S + E + W)
        Label(self.framePessoais, text="Dados pessoais", font='bold').grid(row=0, column=0, columnspan=2, sticky=W+E, padx=3, pady=3)

        # DP LINHA 1
        # DATA DE NASCIMENTO
        Label(self.framePessoais, text="Data de nascimento").grid(row=1, column=0, sticky=W, padx=3, pady=3)
        self.eDataNascimento = Entry(self.framePessoais, width=10, state=DISABLED)
        self.eDataNascimento.grid(row=1, column=1, sticky=W + E, padx=3, pady=3)

        # RG
        Label(self.framePessoais, text="RG").grid(row=1, column=2, sticky=W, padx=3, pady=3)
        self.eRG = Entry(self.framePessoais, width=11, state=DISABLED)
        self.eRG.grid(row=1, column=3, sticky=W + E, padx=3, pady=3)

        # CPF
        Label(self.framePessoais, text="CPF").grid(row=1, column=4, sticky="W", padx=3, pady=3)
        self.eCPF = Entry(self.framePessoais, width=14, state=DISABLED)
        self.eCPF.grid(row=1, column=5, sticky=W + E, padx=3, pady=3)

        # DP LINHA 2
        # ORIENTAÇÃO SEXUAL
        Label(self.framePessoais, text="Orientação sexual").grid(row=2, column=0, sticky=W, padx=3, pady=3)
        self.comboOSexual = ttk.Combobox(self.framePessoais, state=DISABLED, width=10)
        self.comboOSexual.grid(row=2, column=1, sticky=W + E, padx=3, pady=3)
        self.comboOSexual['values'] = [ \
            'Masculimo',
            'Feminino',
        ]

        # ESTADO CIVIL
        Label(self.framePessoais, text="Estado civil").grid(row=2, column=2, sticky=W, padx=3, pady=3)
        self.comboECivil = ttk.Combobox(self.framePessoais, state=DISABLED, width=10)
        self.comboECivil.grid(row=2, column=3, sticky=W + E, padx=3, pady=3)
        self.comboECivil['values'] = [ \
            'Solteiro',
            'Casado',
            'Divorciado',
            'Separado',
            'Viúvo',
        ]

        # DADOS DE CONTATO
        self.frameContatos = Frame(self.frameRight,border=1, relief="groove")
        self.frameContatos.grid(column=0, row=2, sticky=N + S + E + W)
        Label(self.frameContatos, text="Dados de contato", font='bold').grid(row=0, column=0, columnspan=2, sticky=W + E, padx=3, pady=3)

        # DC LINHA 1
        # TELEFONE
        Label(self.frameContatos, text="Telefone").grid(row=1, column=0, sticky=W, padx=3, pady=3)
        self.eTelefone = Entry(self.frameContatos, width=15, state=DISABLED)
        self.eTelefone.grid(row=1, column=1, sticky=W + E, padx=3, pady=3)

        # CELULAR
        Label(self.frameContatos, text="Celular").grid(row=1, column=2, sticky=W, padx=3, pady=3)
        self.eCelular = Entry(self.frameContatos, width=15, state=DISABLED)
        self.eCelular.grid(row=1, column=3, sticky=W + E, padx=3, pady=3)

        # RECADO
        Label(self.frameContatos, text="Recado").grid(row=1, column=4, sticky=W, padx=3, pady=3)
        self.eRecado = Entry(self.frameContatos, width=15, state=DISABLED)
        self.eRecado.grid(row=1, column=5, sticky=W + E, padx=3, pady=3)

        # DC LINHA 2
        # ENDEREÇO
        Label(self.frameContatos, text="Endereço").grid(row=2, column=0, sticky=W, padx=3, pady=3)
        self.eEndereco = Entry(self.frameContatos, width=15, state=DISABLED)
        self.eEndereco.grid(row=2, column=1, columnspan=5, sticky=W + E, padx=3, pady=3)

        # DC LINHA 3
        # ESTADO
        Label(self.frameContatos, text="Estado").grid(row=3, column=0, sticky=W, padx=3, pady=3)
        self.comboEstado = ttk.Combobox(self.frameContatos, state=DISABLED, width=20)
        self.comboEstado.grid(row=3, column=1, sticky=W + E, padx=3, pady=5)
        self.comboEstado['values'] = [ \
            'Acre (AC)',
            'Alagoas (AL)',
            'Amapá (AP)',
            'Amazonas (AM)',
            'Bahia (BA)',
            'Ceará (CE)',
            'Distrito Federal (DF)',
            'Espírito Santo (ES)',
            'Goiás (GO)',
            'Maranhão (MA)',
            'Mato Grosso (MT)',
            'Mato Grosso do Sul (MS)',
            'Minas Gerais (MG)',
            'Pará (PA)',
            'Paraíba (PB)',
            'Paraná (PR)',
            'Pernambuco (PE)',
            'Piauí (PI)',
            'Rio de Janeiro (RJ)',
            'Rio Grande do Norte (RN)',
            'Rio Grande do Sul (RS)',
            'Rondônia (RO)',
            'Roraima (RR)',
            'Santa Catarina (SC)',
            'São Paulo (SP)',
            'Sergipe (SE)',
            'Tocantins (TO)',
        ]

        # CIDADE
        Label(self.frameContatos, text="Cidade").grid(row=3, column=2, sticky=W, padx=3, pady=3)
        self.eCidade = Entry(self.frameContatos, width=15, state=DISABLED)
        self.eCidade.grid(row=3, column=3, sticky=W + E, padx=3, pady=3)

        # CEP
        Label(self.frameContatos, text="CEP").grid(row=3, column=4, sticky=W, padx=3, pady=3)
        self.eCEP = Entry(self.frameContatos, width=15, state=DISABLED)
        self.eCEP.grid(row=3, column=5, sticky=W + E, padx=3, pady=3)

        # DADOS PROFICIONAIS
        self.frameProficionais = Frame(self.frameRight, border=1, relief="groove")
        self.frameProficionais.grid(column=0, row=3, sticky=N + S + E + W)
        Label(self.frameProficionais, text="Dados proficionais", font='bold').grid(row=0, column=0, columnspan=2, sticky=W + E, padx=3, pady=3)

        # DP LINHA 1
        # PROFISÃO
        Label(self.frameProficionais, text="Profisão").grid(row=1, column=0, sticky=W, padx=3, pady=3)
        self.eProfisao = Entry(self.frameProficionais, width=15, state=DISABLED)
        self.eProfisao.grid(row=1, column=1, sticky=W + E, padx=3, pady=3)

        # EMPRESA
        Label(self.frameProficionais, text="Empresa").grid(row=1, column=2, sticky=W, padx=3, pady=3)
        self.eEmpresa = Entry(self.frameProficionais, width=20, state=DISABLED)
        self.eEmpresa.grid(row=1, column=3, sticky=W + E, padx=3, pady=3)

        # EMPRESA
        Label(self.frameProficionais, text="Telefone").grid(row=1, column=4, sticky=W, padx=3, pady=3)
        self.eETelefone = Entry(self.frameProficionais, width=15, state=DISABLED)
        self.eETelefone.grid(row=1, column=5, sticky=W + E, padx=3, pady=3)

        # OBSERVAÇÕES
        self.frameObservacoes = Frame(self.frameRight, border=1, relief="groove")
        self.frameObservacoes.grid(column=0, row=4, columnspan=2, sticky=N + S + E + W)
        Label(self.frameObservacoes, text="Observações", font='bold').grid(row=0, column=0, columnspan=2, sticky=W + E, padx=3, pady=3)

        self.tObservacao = Text(self.frameObservacoes, height=10, width=130)
        self.tObservacao.grid(row=1, column=0, sticky=N + S + W + E, padx=3, pady=3)

        # ____ FRAME DE EXAME
        self.frameExame = Frame(self.frameRight, border=1, relief="groove")
        self.frameExame.grid(column=1, row=1, rowspan=3, sticky=N + S + E + W)
        Label(self.frameExame, text="Exames", font='bold').grid(column=0, row=0, columnspan=2)

        self.frameExameInterno = Frame(self.frameExame)
        self.frameExameInterno.grid(column=0, row=1, columnspan=2, sticky=N + S + E + W)
        self.listboxExames = Listbox(self.frameExameInterno, width=25, height=15)
        scrollbarExames = Scrollbar(self.frameExameInterno, orient="vertical")
        scrollbarExames.config(command=self.listboxExames.yview)
        def _selectExame(evt):
            eventExame = evt.widget
            if eventExame.curselection():
                indexExame = int(eventExame.curselection()[0])
                valueExame = eventExame.get(indexExame)
                self.selecionaExame(valueExame)

        self.listboxExames.bind('<<ListboxSelect>>', _selectExame)
        self.listboxExames.pack()
        scrollbarExames.pack(side="right", fill="y")
        self.listboxExames.config(yscrollcommand=scrollbarExames.set)
        self.listboxExames.pack()

        # Botão de abrir exame e novo exame
        self.abrirExame = Button(self.frameExame, text="Abrir exame", state=DISABLED, command=lambda: self._abrirExame())
        self.abrirExame.grid(column=0, row=2)
        self.novoExame = Button(self.frameExame, text="Novo exame", state=DISABLED, command=lambda: self._novoExame())
        self.novoExame.grid(column=1, row=2)

    def atualizaDados(self, nomePaciente):

        self.abrirExame['state'] = DISABLED
        self.novoExame['state'] = NORMAL
        self.editarContato['state'] = NORMAL

        # Puchar dados do JSON
        self.paciente = util.getPaciente(nomePaciente)

        # Atualizar dados de exames
        # Atualiza dados do self.paciente

        # NOME
        self.eNome["state"] = NORMAL
        self.eNome.delete(0, END)
        self.eNome.insert(0, self.paciente['nome'])
        self.eNome["state"] = DISABLED

        # DATA DE NASCIMENTO
        self.eDataNascimento["state"] = NORMAL
        self.eDataNascimento.delete(0, END)
        self.eDataNascimento.insert(0, self.paciente['dataNascimento'])
        self.eDataNascimento["state"] = DISABLED

        # RG
        self.eRG["state"] = NORMAL
        self.eRG.delete(0, END)
        self.eRG.insert(0, self.paciente['rg'])
        self.eRG["state"] = DISABLED

        # CPF
        self.eCPF["state"] = NORMAL
        self.eCPF.delete(0, END)
        self.eCPF.insert(0, self.paciente['cpf'])
        self.eCPF["state"] = DISABLED

        # ORIENTAÇÃO SEXUAL
        self.comboOSexual["state"] = NORMAL
        self.comboOSexual.delete(0, END)
        self.comboOSexual.insert(0, self.paciente['orientacaoSexual'])
        self.comboOSexual["state"] = DISABLED

        # ESTADO CIVIL
        self.comboECivil["state"] = NORMAL
        self.comboECivil.delete(0, END)
        self.comboECivil.insert(0, self.paciente['estadoCivil'])
        self.comboECivil["state"] = DISABLED

        # TELEFONE
        self.eTelefone["state"] = NORMAL
        self.eTelefone.delete(0, END)
        self.eTelefone.insert(0, self.paciente['telefone'])
        self.eTelefone["state"] = DISABLED

        # CELULAR
        self.eCelular["state"] = NORMAL
        self.eCelular.delete(0, END)
        self.eCelular.insert(0, self.paciente['celular'])
        self.eCelular["state"] = DISABLED

        # RECADO
        self.eRecado["state"] = NORMAL
        self.eRecado.delete(0, END)
        self.eRecado.insert(0, self.paciente['recado'])
        self.eRecado["state"] = DISABLED

        # ENDEREÇO
        self.eEndereco["state"] = NORMAL
        self.eEndereco.delete(0, END)
        self.eEndereco.insert(0, self.paciente['endereco'])
        self.eEndereco["state"] = DISABLED

        # ESTADO
        self.comboEstado["state"] = NORMAL
        self.comboEstado.delete(0, END)
        self.comboEstado.insert(0, self.paciente['estado'])
        self.comboEstado["state"] = DISABLED

        # CIDADE
        self.eCidade["state"] = NORMAL
        self.eCidade.delete(0, END)
        self.eCidade.insert(0, self.paciente['cidade'])
        self.eCidade["state"] = DISABLED

        # CEP
        self.eCEP["state"] = NORMAL
        self.eCEP.delete(0, END)
        self.eCEP.insert(0, self.paciente['cep'])
        self.eCEP["state"] = DISABLED

        # PROFISÃO
        self.eProfisao["state"] = NORMAL
        self.eProfisao.delete(0, END)
        self.eProfisao.insert(0, self.paciente['profisao'])
        self.eProfisao["state"] = DISABLED

        # EMPRESA
        self.eEmpresa["state"] = NORMAL
        self.eEmpresa.delete(0, END)
        self.eEmpresa.insert(0, self.paciente['empresa'])
        self.eEmpresa["state"] = DISABLED

        # TELEFONE DA EMPRESA
        self.eETelefone["state"] = NORMAL
        self.eETelefone.delete(0, END)
        self.eETelefone.insert(0, self.paciente['eTelefone'])
        self.eETelefone["state"] = DISABLED

        # OBSERVAÇÕES
        self.tObservacao["state"] = NORMAL
        self.tObservacao.delete('1.0', END)
        self.tObservacao.insert(END, self.paciente['observacoes'])
        self.tObservacao["state"] = DISABLED

        # EXAMES
        self.listboxExames.delete(0,END)

        exames = os.getcwd() + '\pacientes\\' + self.paciente['nome']
        self.listExames = []

        for diretorio in glob.glob(exames + "\[0-9]*"):
            sData = diretorio.split("\\")
            sData = sData[len(sData) - 1]
            self.listExames.append(sData)

        self.listExames = sorted(self.listExames)

        for exame in self.listExames:
            dataSplit = exame.split("-")
            dataStr = '{}\{}\{} {}:{}'.format(dataSplit[2], dataSplit[1], dataSplit[0], dataSplit[3], dataSplit[4])
            self.listboxExames.insert(END, dataStr)

    def selecionaExame(self, exame):
        #Deixa o botão abrir exame ativo
        self.abrirExame['state'] = NORMAL

        #Monta o diretório novamente
        data = exame.split(" ")
        dias = data[0].split("\\")
        horas = data[1].split(":")
        self.exameDir = '{}-{}-{}-{}-{}'.format(dias[2], dias[1], dias[0], horas[0], horas[1])

    def _novoExame(self):
        self.father._anamnese(self.paciente['nome'])

    def _abrirExame(self):
        self.father._anamnese(self.paciente['nome'], os.getcwd() + "\pacientes\\" + self.paciente['nome'] + "\\" + self.exameDir)

    def _editarContato(self):
        self.father._adicionarPaciente(self.paciente['nome'])