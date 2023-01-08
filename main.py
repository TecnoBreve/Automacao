from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox as Qmsg
from sqlite3 import connect as con 
import os, qdarktheme

from metas import Metas
from hxh import mainHxh
from pa import PA
from vj import VJ
from estore import es
from atualizarEstore import init
from login import Login


class App():
    def __init__(self):
        # VAR Metas
        self.m = Metas
        self.m.fl = 'L062'
        self.m()
        self.metaLbl = self.m().soma

        # Settings
        self.app = QApplication([])
        self.winLogin = uic.loadUi('uic\\login.ui')
        self.mainWin = uic.loadUi('uic\\main.ui')
        self.mainWin.metaLbl.setText(f'Meta: R${self.metaLbl:.2f}')
        qdarktheme.setup_theme()

        # Callback
        self.mainWin.btnhxh.clicked.connect(self.hxh)
        self.mainWin.btnestore.clicked.connect(self.estore)
        self.mainWin.paBtn.clicked.connect(self.pa)
        self.mainWin.btnvj.clicked.connect(self.vj)
        self.mainWin.logout.clicked.connect(self.logout)
        self.mainWin.metaBtn.clicked.connect(self.localMetas)
        self.mainWin.atualizarEstore.clicked.connect(self.atuEs)
        self.winLogin.btnLogin.clicked.connect(self.entrar)
        self.winLogin.show()
        self.app.exec()

    # Mensagem
    def msg(self, win, msg):
        self.tt = 'LOGIN'
        Qmsg.about(win, self.tt, msg)

    # Hora X Hora
    def hxh(self):
        with open('txt\\texto.txt', 'w') as doc:
            text = self.mainWin.entex.toPlainText()
            doc.write(text)
        mainHxh()
    
    # E-Store
    def estore(self):
        os.system('cd pln && estore.xlsx')
        es().iniciar()

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
    
    # Atualizar Estore
    def atuEs(self):
        self.msg(self.winLogin, 'Atualizando...')
        init()
        self.msg(self.winLogin, 'Metas de Estore Atualizada!!!')

    # Local das metas XLSX
    def localMetas(self):
        os.system('explorer metas')

    # Logout !
    def logout(self):
        self.winLogin.pas.setText('')
        self.winLogin.mat.setText('')
        self.mainWin.close()
        self.winLogin.show()

    # Login !
    def entrar(self):
        user = self.winLogin.mat.text()
        pasw = self.winLogin.pas.text()
        l = Login()
        l.matriculaL = str(user)
        l.senhaL = str(pasw)
        l.tryLogin()
        r = l.resposta   
        if r == 'sim':
            self.msg(self.winLogin, 'Sucesso')
            self.nome = l.nome
            self.mainWin.lblUser.setText(f'{self.nome}')
            self.winLogin.close()
            self.mainWin.show()
        elif r == 'senha':
            self.msg(self.winLogin, 'Senha Incorreta !!')
        elif r == 'user':
            self.msg(self.winLogin, 'Usuário não encontrado !!')
        else:
            self.msg(self.winLogin, 'Erro Inesperado')     
App()