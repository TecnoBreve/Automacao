# Importação de config.
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox as Qmsg
from os import system
from sys import exit
from qdarktheme import setup_theme as st

# Importação de modulos próprios
from metas import Metas
from hxh import mainHxh
from pa import PA
from vj import VJ
from estore import es
from atualizarEstore import init
from login import Login


class App():
    def __init__(self):
        # Variavel de Metas
        self.m = Metas
        self.m.fl = 'L062'
        self.m()
        self.metaLbl = self.m().soma

        # Settings
        self.app = QApplication([])
        self.winLogin = uic.loadUi('uic\\login.ui') # Exporta o design da Login windown 
        self.mainWin = uic.loadUi('uic\\main.ui') # Exporta o design da Main windown
        st() # Setar tema escuro


        # Callback dos Buttons
        self.mainWin.btnhxh.clicked.connect(self.hxh)
        self.mainWin.btnestore.clicked.connect(self.estore)
        self.mainWin.paBtn.clicked.connect(self.pa)
        self.mainWin.btnvj.clicked.connect(self.vj)
        self.mainWin.logout.clicked.connect(self.logout)
        self.mainWin.metaBtn.clicked.connect(self.localMetas)
        self.mainWin.atualizarEstore.clicked.connect(self.atuEs)
        self.winLogin.btnLogin.clicked.connect(self.entrar)
        self.slvBtn = self.winLogin.salvarUser
        self.mainWin.metaLbl.setText(f'Meta: R${self.metaLbl:.2f}') # Setar o texto com a meta dia

        #  Executando a Tela de Login
        self.winLogin.show()
        self.app.exec()

    # MessageBox 
    def msg(self, win, msg):
        self.tt = 'LOGIN'
        Qmsg.about(win, self.tt, msg)

    # E-Store
    def estore(self):
        system('cd pln && estore.xlsx')
        es().iniciar()

    # Hora X Hora
    def hxh(self):
        with open('txt\\texto.txt', 'w') as doc:
            text = self.mainWin.entex.toPlainText()
            doc.write(text)
        mainHxh()

    # Participação
    def pa(self):
        with open('txt\\clb.txt', 'w') as doc:
            text = self.mainWin.entex.toPlainText()
            doc.write(text)
        PA().cons()

    # Vendas com Juros
    def vj(self):
        with open('txt\\vj.txt', 'w') as doc:
            text = self.mainWin.entex.toPlainText()
            doc.write(text)
        VJ().code()
    
    # Puxa 1% das metas do .XLSX 
    def atuEs(self):
        self.msg(self.winLogin, 'Atualizando...')
        init()
        self.msg(self.winLogin, 'Metas de Estore Atualizada!!!')

    # Local das metas .XLSX
    def localMetas(self):
        system('explorer metas')

    # Logout !
    def logout(self):
        if self.slvBtn.isChecked():
            self.winLogin.mat.setText(self.user)
        else:
            self.winLogin.mat.setText('')
        self.winLogin.pas.setText('')
        self.mainWin.close()
        self.winLogin.show()

    # Realiza o Login
    def entrar(self):
        # Pega valores do campo de texto
        self.user = self.winLogin.mat.text() 
        self.pasw = self.winLogin.pas.text()

        # Config. do módulo de Login
        l = Login()
        l.matriculaLogin = str(self.user)
        l.senhaLogin = str(self.pasw)

        # Teste de Rede
        r = l.resposta
        if r == 'net':
            self.msg(self.winLogin, 'Sem conexão com a Internet')
            exit()

        # Tentativa de Login
        l.tryLogin()
        r = l.resposta   
        if r == 'sim':
            self.nome = l.nome
            self.msg(self.winLogin, f'Seja bem vindo {self.nome}')
            self.mainWin.lblUser.setText(f'{self.nome}')
            self.winLogin.close()
            self.mainWin.show()
        elif r == 'senha':
            self.msg(self.winLogin, 'Senha Incorreta !!')
        elif r == 'user':
            self.msg(self.winLogin, 'Usuário não encontrado !!')
        else:     
            self.msg(self.winLogin, 'Erro desconhecido !')
App()