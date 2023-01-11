import requests as rq, json

class Login():
    def __init__(self):
        self.matriculaLogin = None
        self.senhaLogin = None
        self.resposta = None
        self.nome = None
        self.conn()

    def conn(self):
        try:
            self.userDB = "https://dados-9be06-default-rtdb.firebaseio.com/users/.json"
            self.get = rq.get(self.userDB)
            self.dados = self.get.json()
        except rq.exceptions.ConnectionError:
            self.resposta = 'net'

    def tryLogin(self):
        try:
            sn = self.dados[self.matriculaLogin]['senha']
            if sn == self.senhaLogin:
                self.resposta = 'sim'
                self.nome = self.dados[self.matriculaLogin]['nome']
            else:
                self.resposta = 'senha'
        except:
            self.resposta = 'user'