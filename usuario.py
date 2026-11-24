class Usuario:
    def __init__(self, user, senha, email):
        self.user = user
        self.senha = senha
        self.email = email


class Tecnico(Usuario):
    def __init__(self, user, senha, email, especialidade):
        super().__init__(user, senha, email)
        self.especialidade = especialidade
        self.resolvidos = 0


class Cliente(Usuario):
    def __init__(self, user, senha, email, telefone):
        super().__init__(user, senha, email)
        self.telefone = telefone
        self.tickets_abertos = []