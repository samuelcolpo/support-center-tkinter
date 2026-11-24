class Ticket:

    def __init__(self, id_ticket, descricao, cliente_nome):

        self.id = id_ticket
        self.descricao = descricao
        self.cliente = cliente_nome
        self.status = "aberto"
        self.tecnico = None

    def atualizar_status(self, novo_status):
        self.status = novo_status