import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from sistema import SistemaHelpDesk
from usuario import Cliente, Tecnico


class HelpDeskGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Support Center")
        self.root.geometry("1100x650")
        self.root.configure(bg="#202124")

        self.sistema = SistemaHelpDesk()

        # -------- UI --------
        tk.Label(root, text="SUPPORT CENTER",
                 bg="#202124", fg="white",
                 font=("Arial", 24, "bold")).pack(pady=15)

        self.lbl_user = tk.Label(
            root,
            text="Nenhum usuário logado",
            bg="#202124",
            fg="white"
        )
        self.lbl_user.pack()

        # -------- BOTÕES --------
        painel = tk.Frame(root, bg="#202124")
        painel.pack(pady=20)

        botoes = [
            ("Cadastrar Cliente", self.cadastrar_cliente),
            ("Cadastrar Técnico", self.cadastrar_tecnico),
            ("Login", self.login),
            ("Logoff", self.logoff),
            ("Abrir Ticket", self.abrir_ticket),
            ("Atribuir", self.atribuir),
            ("Resolver", self.resolver),
        ]

        for txt, cmd in botoes:
            tk.Button(
                painel,
                text=txt,
                command=cmd,
                bg="#3b82f6",
                fg="white",
                width=15
            ).pack(side="left", padx=5)

        # -------- TABELA --------
        cols = ("ID", "Status", "Cliente", "Tecnico", "Descricao")

        self.tree = ttk.Treeview(root, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c)

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        # 🔥 importante: carregar tabela ao iniciar
        self.atualizar()

    # -------- UPDATE --------

    def atualizar(self):

        self.tree.delete(*self.tree.get_children())

        for t in self.sistema.tickets:

            self.tree.insert("", "end", values=(
                t.id,
                t.status,
                t.cliente,
                t.tecnico if t.tecnico else "Pendente",
                t.descricao
            ))

        if self.sistema.usuario_logado:
            self.lbl_user.config(text=f"Logado: {self.sistema.usuario_logado.user}")
        else:
            self.lbl_user.config(text="Nenhum usuário logado")

    # -------- AÇÕES --------

    def cadastrar_cliente(self):

        u = simpledialog.askstring("User", "Nome", parent=self.root)
        s = simpledialog.askstring("Senha", "Senha", parent=self.root)
        e = simpledialog.askstring("Email", "Email", parent=self.root)
        tel = simpledialog.askstring("Telefone", "Telefone", parent=self.root)

        if not u or not s or not e:
            messagebox.showerror("Erro", "Preencha tudo")
            return

        self.sistema.cadastrar(Cliente(u, s, e, tel))
        messagebox.showinfo("OK", "Cliente criado")

    def cadastrar_tecnico(self):

        u = simpledialog.askstring("User", "Nome", parent=self.root)
        s = simpledialog.askstring("Senha", "Senha", parent=self.root)
        e = simpledialog.askstring("Email", "Email", parent=self.root)
        esp = simpledialog.askstring("Especialidade", "Especialidade", parent=self.root)

        self.sistema.cadastrar(Tecnico(u, s, e, esp))
        messagebox.showinfo("OK", "Técnico criado")

    def login(self):

        u = simpledialog.askstring("Login", "User", parent=self.root)
        s = simpledialog.askstring("Senha", "Senha", parent=self.root)

        r = self.sistema.login(u, s)

        if r is not True:
            messagebox.showerror("Erro", r)

        self.atualizar()

    def logoff(self):

        self.sistema.logoff()
        self.atualizar()

    def abrir_ticket(self):

        d = simpledialog.askstring("Ticket", "Descrição", parent=self.root)

        r = self.sistema.gerenciar_abertura(d)

        if r is not True:
            messagebox.showerror("Erro", r)

        self.atualizar()

    def atribuir(self):

        try:
            idt = int(simpledialog.askstring("ID", "Ticket", parent=self.root))
        except:
            messagebox.showerror("Erro", "ID inválido")
            return

        tec = simpledialog.askstring("Tecnico", "Nome", parent=self.root)

        r = self.sistema.atribuir_ticket(idt, tec)

        if r is not True:
            messagebox.showerror("Erro", r)

        self.atualizar()

    def resolver(self):

        try:
            idt = int(simpledialog.askstring("ID", "Ticket", parent=self.root))
        except:
            messagebox.showerror("Erro", "ID inválido")
            return

        r = self.sistema.gerenciar_conclusao(idt)

        if r is not True:
            messagebox.showerror("Erro", r)

        self.atualizar()


# -------- RUN --------

root = tk.Tk()
HelpDeskGUI(root)
root.mainloop()