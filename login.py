import requests as rq, json

userDB = "https://dados-9be06-default-rtdb.firebaseio.com/users/.json"
get = rq.get(userDB)
dados = get.json()

class Login():
    def __init__(self):
        self.matriculaL = ''
        self.senhaL = ''
        self.resposta = ''
        self.nome = None

    def tryLogin(self):
        try:
            sn = dados[self.matriculaL]['senha']
            if sn == self.senhaL:
                self.resposta = 'sim'
                self.nome = dados[self.matriculaL]['nome']
            else:
                self.resposta = 'senha'
        except:
            self.resposta = 'user'