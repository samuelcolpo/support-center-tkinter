from usuario import Cliente, Tecnico
from ticket import Ticket


class SistemaHelpDesk:

    def __init__(self):

        self.usuarios = {}
        self.tickets = []
        self.usuario_logado = None

    # -------- USUÁRIOS --------

    def cadastrar(self, usuario):

        if usuario.user in self.usuarios:
            return "Usuário já existe"

        self.usuarios[usuario.user] = usuario
        return True

    def login(self, user, senha):

        u = self.usuarios.get(user)

        if not u:
            return "Usuário não encontrado"

        if u.senha != senha:
            return "Senha incorreta"

        self.usuario_logado = u
        return True

    def logoff(self):
        self.usuario_logado = None

    # -------- TICKETS --------

    def gerenciar_abertura(self, descricao):

        if not self.usuario_logado:
            return "Faça login primeiro"

        ticket_id = len(self.tickets) + 1

        ticket = Ticket(
            ticket_id,
            descricao,
            self.usuario_logado.user
        )

        self.tickets.append(ticket)

        # histórico do cliente
        if hasattr(self.usuario_logado, "tickets_abertos"):
            self.usuario_logado.tickets_abertos.append(ticket)

        return True

    def atribuir_ticket(self, id_ticket, tecnico_nome):

        ticket = next((t for t in self.tickets if t.id == id_ticket), None)
        tecnico = self.usuarios.get(tecnico_nome)

        if not ticket or not isinstance(tecnico, Tecnico):
            return "Ticket ou técnico não encontrado"

        ticket.tecnico = tecnico.user
        ticket.atualizar_status("em atendimento")

        return True

    def gerenciar_conclusao(self, id_ticket):

        ticket = next((t for t in self.tickets if t.id == id_ticket), None)

        if not ticket:
            return "Ticket não encontrado"

        if not isinstance(self.usuario_logado, Tecnico):
            return "Apenas técnico pode resolver"

        ticket.atualizar_status("concluído")
        ticket.tecnico = self.usuario_logado.user

        self.usuario_logado.resolvidos += 1

        return True