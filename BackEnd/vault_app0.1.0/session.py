class Sessao:
    def __init__(self):
        self.utilizador = None
        self.password = None

    def login(self, username: str, password: str):
        self.utilizador = username
        self.password = password

    def logout(self):
        self.utilizador = None
        self.password = None

    def esta_autenticado(self):
        return self.utilizador is not None
