import flet as ft
from datetime import datetime
from Telas.iniciar_lista import IniciarLista
from database_listacompras import Database_lista

class BaseScreen:
    def __init__(self, page: ft.Page):
        self.page = page

class ListaCompras(BaseScreen):
    def __init__(self, page: ft.Page, user_id: int):
        super().__init__(page)
        self.user_id = user_id
        self.db = Database_lista()
        self.listas_compras = self.carregar_listas_compras()

        self.total_compras = self.db.carregar_total_compras(self.user_id)
        self.menu_visible = False
        self.nome_nova_lista = ft.TextField(label="Nome da Lista", width=150)

    def carregar_listas_compras(self):
        """Carrega as listas de compras do banco de dados com base no user_id."""
        listas_db = self.db.get_listas_by_user(self.user_id)
        listas = [
            {
                "id_lista": lista[0],
                "user_id": lista[1],
                "nome": lista[2],
                "data_criacao": lista[3],
                "ultima_compra": lista[4]
            }
            for lista in listas_db
        ]
        return listas

    def toggle_menu(self, e):
        self.menu_visible = not self.menu_visible
        self.show()

    def show(self):
        self.page.controls.clear() 
        self.page.bgcolor = "white"
        self.page.title = "Tela Inicial"
        self.page.scroll = ft.ScrollMode.AUTO

        desvincular_button = ft.TextButton(
            "Desvincular Conta",
            on_click=self.desvincular_conta,
            style=ft.ButtonStyle(
                color=ft.colors.RED,
                shape={"side": None}
            )
        )

        self.page.add(ft.Container(content=desvincular_button, alignment=ft.alignment.top_right))

        stats_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Listas Criadas", size=16, color="#309900"),
                            ft.Text(str(len(self.listas_compras)), size=16, weight="bold", color="#309900")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Total de Compras", size=16, color="#309900"),
                            ft.Text(str(self.total_compras), size=16, weight="bold", color="#309900")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=10,
            alignment=ft.alignment.center
        )

        lista_controls = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("|Nome da Lista|", weight="bold", size=12, color="#309900"),
                        ft.Text("|Data de Criação|", weight="bold", size=12, color="#309900"),
                        ft.Container(width=100)  #
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=10
            )
        ]

        for lista in self.listas_compras:
            lista_controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(lista["nome"], size=12, color="#309900"),
                            ft.Text(lista["data_criacao"], size=12, color="#309900"),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.ElevatedButton(
                                            "Remover", 
                                            on_click=lambda e, l=lista: self.remover_lista(l), 
                                            color="RED"
                                        ),
                                        margin=ft.Margin(0, 5, 0, 0)  
                                    ),
                                    ft.Container(
                                        content=ft.ElevatedButton(
                                            "Iniciar", 
                                            on_click=lambda e, l=lista: self.iniciar_compra(l), 
                                            color="GREEN"
                                        ),
                                        margin=ft.Margin(0, 10, 0, 0)  
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                )
            )
    
        entrada_e_botao = ft.Row(
            controls=[
                self.nome_nova_lista,
                ft.TextButton(
                    "Adicionar Lista",
                    on_click=self.criar_lista,
                    style=ft.ButtonStyle(
                        color=ft.colors.GREEN,
                        shape={"side": None}
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=5
        )

        self.page.add(stats_container)
        self.page.add(ft.Divider())
        self.page.add(entrada_e_botao)
        self.page.add(ft.Column(controls=lista_controls))
        self.page.update()

    def criar_lista(self, e):
        nome_lista = self.nome_nova_lista.value
        if nome_lista:
            data_criacao = datetime.now().strftime("%Y-%m-%d")
            self.db.criar_lista(self.user_id, nome_lista, data_criacao)
            self.page.snack_bar = ft.SnackBar(ft.Text(f"A lista '{nome_lista}' foi criada com sucesso!"), bgcolor="#309900")
            self.page.snack_bar.open = True
            self.page.update()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("ERRO: Preencha o nome da lista!"), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()

        self.listas_compras = self.carregar_listas_compras()
        self.show()

    def remover_lista(self, lista):
        self.db.deletar_lista(lista["id_lista"])
        self.page.snack_bar = ft.SnackBar(ft.Text(f"A lista '{lista['nome']}' foi removida com sucesso!"), bgcolor="red")
        self.page.snack_bar.open = True
        self.listas_compras = self.carregar_listas_compras()
        self.show()

    def iniciar_compra(self, lista):
        self.total_compras += 1

        self.db.atualizar_total_compras(self.user_id, self.total_compras)

        self.page.snack_bar = ft.SnackBar(ft.Text(f"Iniciando a compra para a lista '{lista['nome']}'"), bgcolor="green")
        self.page.snack_bar.open = True
        self.show()

        iniciar_lista_screen = IniciarLista(self.page, lista["id_lista"], self.user_id)
        iniciar_lista_screen.build()
    
    def desvincular_conta(self, e):
        from Telas.login import loginScreen
        login_screen = loginScreen(self.page)
        login_screen.show()

        self.page.controls.clear()
        loginScreen(self.page).show()
        self.page.snack_bar = ft.SnackBar(ft.Text("Conta desvinculada com sucesso!"), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()
