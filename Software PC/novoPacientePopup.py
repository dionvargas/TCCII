import util
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class NovoPacientePopup:

    def __init__(self, father, nomePaciente):

        self.father = father

        exam = util.getExam()

        widthWindowControl = 720
        heightWindowControl = 510
        yControl = 30
        xControl = int(exam['monitorWidth']/2)

        self.window = Toplevel()
        self.window.title("Novo Paciente")
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

        # ____ FRAME DE DADOS
        self.frameDados = Frame(root)
        self.frameDados.grid(column=0, row=0, sticky=N + S + E + W)

        # LINHA 0
        # NOME
        self.frameNome = Frame(self.frameDados)
        self.frameNome.grid(column=0, row=0, sticky=N + S + E + W)
        Label(self.frameNome, font='bold', text="Nome").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.eNome = Entry(self.frameNome, width=63, font='bold')
        self.eNome.grid(row=0, column=1, sticky=W + E, padx=5, pady=5)

        # DADOS PESSOAIS
        self.framePessoais = Frame(self.frameDados, border=1, relief="groove")
        self.framePessoais.grid(column=0, row=1, sticky=N + S + E + W)
        Label(self.framePessoais, text="Dados pessoais", font='bold').grid(row=0, column=0, columnspan=2, sticky=W + E,
                                                                           padx=3, pady=3)

        # DP LINHA 1
        # DATA DE NASCIMENTO
        Label(self.framePessoais, text="Data de nascimento").grid(row=1, column=0, sticky=W, padx=3, pady=3)
        self.eDataNascimento = Entry(self.framePessoais, width=10)
        self.eDataNascimento.grid(row=1, column=1, sticky=W + E, padx=3, pady=3)

        # RG
        Label(self.framePessoais, text="RG").grid(row=1, column=2, sticky=W, padx=3, pady=3)
        self.eRG = Entry(self.framePessoais, width=11)
        self.eRG.grid(row=1, column=3, sticky=W + E, padx=3, pady=3)

        # CPF
        Label(self.framePessoais, text="CPF").grid(row=1, column=4, sticky="W", padx=3, pady=3)
        self.eCPF = Entry(self.framePessoais, width=14)
        self.eCPF.grid(row=1, column=5, sticky=W + E, padx=3, pady=3)

        # DP LINHA 2
        # ORIENTAÇÃO SEXUAL
        Label(self.framePessoais, text="Orientação sexual").grid(row=2, column=0, sticky=W, padx=3, pady=3)
        self.comboOSexual = ttk.Combobox(self.framePessoais, width=10, state="readonly")
        self.comboOSexual.grid(row=2, column=1, sticky=W + E, padx=3, pady=3)
        self.comboOSexual['values'] = [ \
            'Masculimo',
            'Feminino',
        ]

        # ESTADO CIVIL
        Label(self.framePessoais, text="Estado civil").grid(row=2, column=2, sticky=W, padx=3, pady=3)
        self.comboECivil = ttk.Combobox(self.framePessoais, width=10, state="readonly")
        self.comboECivil.grid(row=2, column=3, sticky=W + E, padx=3, pady=3)
        self.comboECivil['values'] = [ \
            'Solteiro',
            'Casado',
            'Divorciado',
            'Separado',
            'Viúvo',
        ]

        # DADOS DE CONTATO
        self.frameContatos = Frame(self.frameDados, border=1, relief="groove")
        self.frameContatos.grid(column=0, row=2, sticky=N + S + E + W)
        Label(self.frameContatos, text="Dados de contato", font='bold').grid(row=0, column=0, columnspan=2,
                                                                             sticky=W + E, padx=3, pady=3)

        # DC LINHA 1
        # TELEFONE
        Label(self.frameContatos, text="Telefone").grid(row=1, column=0, sticky=W, padx=3, pady=3)
        self.eTelefone = Entry(self.frameContatos, width=15)
        self.eTelefone.grid(row=1, column=1, sticky=W + E, padx=3, pady=3)

        # CELULAR
        Label(self.frameContatos, text="Celular").grid(row=1, column=2, sticky=W, padx=3, pady=3)
        self.eCelular = Entry(self.frameContatos, width=15)
        self.eCelular.grid(row=1, column=3, sticky=W + E, padx=3, pady=3)

        # RECADO
        Label(self.frameContatos, text="Recado").grid(row=1, column=4, sticky=W, padx=3, pady=3)
        self.eRecado = Entry(self.frameContatos, width=15)
        self.eRecado.grid(row=1, column=5, sticky=W + E, padx=3, pady=3)

        # DC LINHA 2
        # ENDEREÇO
        Label(self.frameContatos, text="Endereço").grid(row=2, column=0, sticky=W, padx=3, pady=3)
        self.eEndereco = Entry(self.frameContatos, width=15)
        self.eEndereco.grid(row=2, column=1, columnspan=5, sticky=W + E, padx=3, pady=3)

        # DC LINHA 3
        # ESTADO
        Label(self.frameContatos, text="Estado").grid(row=3, column=0, sticky=W, padx=3, pady=3)
        self.comboEstado = ttk.Combobox(self.frameContatos, width=20, state="readonly")
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
        self.eCidade = Entry(self.frameContatos, width=15)
        self.eCidade.grid(row=3, column=3, sticky=W + E, padx=3, pady=3)

        # CEP
        Label(self.frameContatos, text="CEP").grid(row=3, column=4, sticky=W, padx=3, pady=3)
        self.eCEP = Entry(self.frameContatos, width=15)
        self.eCEP.grid(row=3, column=5, sticky=W + E, padx=3, pady=3)

        # DADOS PROFICIONAIS
        self.frameProficionais = Frame(self.frameDados, border=1, relief="groove")
        self.frameProficionais.grid(column=0, row=3, sticky=N + S + E + W)
        Label(self.frameProficionais, text="Dados proficionais", font='bold').grid(row=0, column=0, columnspan=2,
                                                                                   sticky=W + E, padx=3, pady=3)

        # DP LINHA 1
        # PROFISÃO
        Label(self.frameProficionais, text="Profisão").grid(row=1, column=0, sticky=W, padx=3, pady=3)
        self.eProfisao = Entry(self.frameProficionais, width=15)
        self.eProfisao.grid(row=1, column=1, sticky=W + E, padx=3, pady=3)

        # EMPRESA
        Label(self.frameProficionais, text="Empresa").grid(row=1, column=2, sticky=W, padx=3, pady=3)
        self.eEmpresa = Entry(self.frameProficionais, width=20)
        self.eEmpresa.grid(row=1, column=3, sticky=W + E, padx=3, pady=3)

        # TELEFONE DA EMPRESA
        Label(self.frameProficionais, text="Telefone").grid(row=1, column=4, sticky=W, padx=3, pady=3)
        self.eETelefone = Entry(self.frameProficionais, width=15)
        self.eETelefone.grid(row=1, column=5, sticky=W + E, padx=3, pady=3)

        # OBSERVAÇÕES
        self.frameObservacoes = Frame(self.frameDados, border=1, relief="groove")
        self.frameObservacoes.grid(column=0, row=4, sticky=N + S + E + W)
        Label(self.frameObservacoes, text="Observações", font='bold').grid(row=0, column=0, columnspan=2, sticky=W + E,
                                                                           padx=3, pady=3)
        self.tObservacao = Text(self.frameObservacoes, height=10, width=85)
        self.tObservacao.grid(row=1, column=0, sticky=N + S + W + E, padx=3, pady=3)

        # ____ FRAME DE BOTÕES
        self.frameBotoes = Frame(root)
        self.frameBotoes.grid(column=0, row=1, sticky=N + S + E + W)

        # Botão de abrir exame e novo exame
        self.salvar = Button(self.frameBotoes, text="Salvar", command=lambda: self._gravar(nomePaciente))
        self.salvar.pack(side=RIGHT, pady=5)
        self.cancelar = Button(self.frameBotoes, text="Cancelar", command=lambda: self._close())
        self.cancelar.pack(side=RIGHT, padx=5, pady=5)

        # CASO FOR EDIÇÃO INSERE OS DADOS NOS CAMPOS
        if(not nomePaciente == None):
            self.window.title("Editar Paciente")

            self.paciente = util.getPaciente(nomePaciente)

            self.eNome.insert(0, self.paciente['nome'])
            self.eNome["state"] = DISABLED
            self.eDataNascimento.insert(0, self.paciente['dataNascimento'])
            self.eRG.insert(0, self.paciente['rg'])
            self.eCPF.insert(0, self.paciente['cpf'])
            self.comboOSexual["state"] = NORMAL
            self.comboOSexual.insert(0, self.paciente['orientacaoSexual'])
            self.comboOSexual["state"] = "readonly"
            self.comboECivil["state"] = NORMAL
            self.comboECivil.insert(0, self.paciente['estadoCivil'])
            self.comboECivil["state"] = "readonly"
            self.eTelefone.insert(0, self.paciente['telefone'])
            self.eCelular.insert(0, self.paciente['celular'])
            self.eRecado.insert(0, self.paciente['recado'])
            self.eEndereco.insert(0, self.paciente['endereco'])
            self.comboEstado["state"] = NORMAL
            self.comboEstado.insert(0, self.paciente['estado'])
            self.comboEstado["state"] = "readonly"
            self.eCidade.insert(0, self.paciente['cidade'])
            self.eCEP.insert(0, self.paciente['cep'])
            self.eProfisao.insert(0, self.paciente['profisao'])
            self.eEmpresa.insert(0, self.paciente['empresa'])
            self.eETelefone.insert(0, self.paciente['eTelefone'])
            self.tObservacao.insert(END, self.paciente['observacoes'])

        self.window.protocol("WM_DELETE_WINDOW", self._close)
        self.window.mainloop()

    def _gravar(self, nomePaciente = None):
        if (self._validate(nomePaciente)):

            if(nomePaciente == None):
                dir = os.getcwd() + "/pacientes/" + self.eNome.get()
                os.mkdir(dir)

            paciente = {
                "nome": self.eNome.get(),
                "dataNascimento": self.eDataNascimento.get(),
                "rg": self.eRG.get(),
                "cpf": self.eCPF.get(),
                "orientacaoSexual": self.comboOSexual.get(),
                "estadoCivil": self.comboECivil.get(),
                "telefone": self.eTelefone.get(),
                "celular": self.eCelular.get(),
                "recado": self.eRecado.get(),
                "endereco": self.eEndereco.get(),
                "estado": self.comboEstado.get(),
                "cidade": self.eCidade.get(),
                "cep": self.eCEP.get(),
                "profisao": self.eProfisao.get(),
                "empresa": self.eEmpresa.get(),
                "eTelefone": self.eETelefone.get(),
                "observacoes": self.tObservacao.get("1.0", END)
            }
            util.setPaciente(paciente)

            self.father._listarPacientes()
            self._close()

    def _validate(self, nomePaciente):
        if (self.eNome.get() == ""):
            messagebox.showerror("Erro", "Nome é um campo obrigatório!")
            self.eNome.focus_set()
            return False
        if (nomePaciente == None):
            if os.path.exists(os.getcwd() + "/pacientes/" + self.eNome.get()):
                messagebox.showerror("Erro", "Paciente já cadastrado!")
                self.eNome.focus_set()
                return False
        return True

    def _close(self):

        self.father.flagPopup = False

        # Fecha a janela
        self.window.destroy()