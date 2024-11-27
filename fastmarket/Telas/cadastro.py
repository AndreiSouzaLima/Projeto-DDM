import flet as ft
from database import Database

class BaseScreen:
    def __init__(self, page: ft.Page):
        self.page = page


class CadastroScreen(BaseScreen):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.db = Database()

    def on_register_click(self, e):
        username = self.username_field.value
        email = self.email_field.value
        password = self.password_field.value

        if username and email and password:
            self.db.add_user(username, email, password)
            self.page.snack_bar = ft.SnackBar(ft.Text("Cadastro bem sucedido"), bgcolor="#00ff00", open=True)
            self.page.controls.clear()
            from Telas.login import loginScreen  
            loginScreen(self.page).show()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("ERRO: Preencha todos os campos"), bgcolor="#ff0000", open=True)

        self.page.update()

    def show(self):
        self.page.title = "Tela de cadastro"
        self.username_field = ft.TextField(label="Usuário", hint_text="Digite usuário", width=200)
        self.email_field = ft.TextField(label="E-Mail", hint_text="Digite E-mail", width=200)
        self.password_field = ft.TextField(label="Senha", hint_text="Digite sua senha", password=True, width=200)
        self.page.bgcolor = "#309900"

        logo = ft.Row(
            [
                ft.Image(src="fastmarket/img/logos/logo.png", width=100, height=100),
                ft.Text("FastMarket", style=ft.TextThemeStyle.BODY_LARGE, color="BLACK", size=38)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        cadastro_container = ft.Column(
            controls=[
                self.username_field,
                self.email_field,
                self.password_field,
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Registrar", on_click=self.on_register_click)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )

        self.page.add(logo)
        self.page.add(ft.Container(height=100))  
        self.page.add(cadastro_container)
        self.page.update()
