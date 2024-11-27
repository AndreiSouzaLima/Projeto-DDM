import flet as ft
from database import Database
from Telas.listacompras import ListaCompras

class BaseScreen:
    def __init__(self, page: ft.Page):
        self.page = page

class loginScreen(BaseScreen):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.db = Database()

    def on_login_click(self, e):
        username = self.username_field.value
        password = self.password_field.value

        if not username or not password:
            self.page.snack_bar = ft.SnackBar(ft.Text("ERRO: Preencha todos os campos"), bgcolor="#ff0000")
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        user = self.db.get_user(username, password)
        if user:
            user_id = user['id']

            self.page.controls.clear()
            ListaCompras(self.page, user_id).show()
            self.page.update()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("ERRO: Login ou senha incorretos"), bgcolor="#ff0000")
            self.page.snack_bar.open = True

        self.page.update()
        
    def on_registrar_click(self, e):
        from Telas.cadastro import CadastroScreen
        self.page.controls.clear()
        CadastroScreen(self.page).show()
        self.page.update()
    
    def show(self):
        self.page.title = "Tela de Login"
        self.username_field = ft.TextField(label="Usuário", hint_text="Digite usuário", width=150)
        self.password_field = ft.TextField(label="Senha", hint_text="Digite sua senha", password=True, width=150)
        self.page.bgcolor = "#309900"

        logo = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Image(src="fastmarket/img/logos/logo.png", width=100, height=100),
                    ft.Text("FastMarket", style=ft.TextThemeStyle.BODY_LARGE, color="BLACK", size=25)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            width=self.page.width
        )

        login_controls = ft.Column(
            controls=[
                self.username_field,
                self.password_field,
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Login", on_click=self.on_login_click),
                        ft.ElevatedButton("Registrar", on_click=self.on_registrar_click)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )

        login_container = ft.Container(
            content=login_controls,
            alignment=ft.alignment.center,
            padding=20,
            width=250
        )

        self.page.add(logo)
        self.page.add(ft.Container(height=100))  
        self.page.add(
            ft.Row(
                controls=[login_container],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.page.update()
