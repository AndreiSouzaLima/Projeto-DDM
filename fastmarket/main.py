import flet as ft
import time
from Telas.login import loginScreen


def splash_screen(page: ft.Page):
    page.title = "Splash Screen"
    page.bgcolor = "#309900"
    
    logo = ft.Image(src="fastmarket/img/logos/logo.png", width=50, height=50)
    msg = ft.Text("FastMarket", style=ft.TextThemeStyle.BODY_LARGE, color="BLACK", size=25)

    content = ft.Row(
        controls=[
            logo,
            msg
        ],
        alignment=ft.MainAxisAlignment.CENTER  
    )
    
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[content],
                alignment=ft.MainAxisAlignment.CENTER,  
                horizontal_alignment=ft.CrossAxisAlignment.CENTER  
            ),
            alignment=ft.alignment.center,  
            expand=True 
        )
    )

    time.sleep(3)  

    page.clean()
    page.update()  
    pag_login = loginScreen(page)
    pag_login.show()


def main(page: ft.Page):
    splash_screen(page)

ft.app(target=main)
