import flet as ft
from database_iniciar import DatabaseIniciar

class IniciarLista(ft.UserControl):
    def __init__(self, page: ft.Page, id_lista: int, user_id: int):
        super().__init__()
        self.page = page
        self.id_lista = id_lista
        self.db = DatabaseIniciar()
        self.user_id = user_id
        self.items_container = ft.Column()
        self.stats_container = ft.Column()
        self.itens_na_lista = 0
        self.itens_comprados = 0
        self.valor_total = 0
        
        self.stats_controls = {
            'itens_na_lista': None,
            'itens_comprados': None,
            'valor_total': None
        }

    def build(self):
        self.page.controls.clear()
        self.page.scroll = ft.ScrollMode.AUTO

        itens = self.db.get_itens_by_lista(self.id_lista)


        self.items_container.controls = []
        for item in itens:
            item_column = ft.Column(
                controls=[
                    ft.TextField(value=item[2], label="Nome do Item", width=150),  
                    ft.TextField(value=item[3], label="Marca", width=150), 
                    ft.TextField(value=str(item[4]), label="Unidade", width=150, on_change=self.atualizar_lista), 
                    ft.TextField(value=str(item[5]), label="Preço Unidade", width=150, on_change=self.atualizar_lista) 
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
            remove_button = ft.ElevatedButton(
                "Remover",
                on_click=lambda e, col=item_column, id_item=item[0]: self.remover_item(col, id_item), 
                color="RED"
            )
            item_column.controls.append(remove_button)
            item_column.controls.append(ft.Divider(height=10, thickness=1, color=ft.colors.GREY))
            self.items_container.controls.append(item_column)

        stats = ft.Column(
            controls=[
                ft.Text("Itens na Lista", size=16, color="#309900"),
                ft.Text(str(len(itens)), size=16, weight="bold", color="#309900"),
                ft.Text("Itens Comprados", size=16, color="#309900"),
                ft.Text(str(self.itens_comprados), size=16, weight="bold", color="#309900"),
                ft.Text("Valor Total", size=16, color="#309900"),
                ft.Text(f"R$ {self.valor_total:.2f}", size=16, weight="bold", color="#309900"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.stats_controls['itens_na_lista'] = stats.controls[1]  
        self.stats_controls['itens_comprados'] = stats.controls[3] 
        self.stats_controls['valor_total'] = stats.controls[5]  

        add_item_row = ft.Row(
            controls=[
                ft.TextButton(
                    "Adicionar Item",
                    on_click=self.adicionar_item,
                    style=ft.ButtonStyle(
                        color=ft.colors.GREEN,
                        shape={"side": None}
                    )
                ),

                ft.TextButton(
                    "Limpar Marca, Unidade e Preço",
                    on_click=self.limpar_campos,
                    style=ft.ButtonStyle(
                        color=ft.colors.RED,
                        shape={"side": None}
                    )
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        lista_de_compras = ft.Column(
            controls=[add_item_row, self.items_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        back_button = ft.TextButton(
            "Voltar Menu",
            on_click=self.voltar_para_lista_compras,
            style=ft.ButtonStyle(
                color="#309900"
            )
        )

        self.page.add(
            ft.Column(
                controls=[back_button, stats, lista_de_compras],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.page.update()

        self.atualizar_lista(None)

    def limpar_campos(self, e):
        for item in self.items_container.controls:
            item.controls[1].value = ""  
            item.controls[2].value = ""  
            item.controls[3].value = ""  


            nome = item.controls[0].value
            if nome:
                item_db = next((i for i in self.db.get_itens_by_lista(self.id_lista) if i[2] == nome), None)

                if item_db:
                    id_item = item_db[0]
                    self.db.update_item(id_item, nome, "", 0, 0) 

        self.page.update()

        self.atualizar_lista(None)

    def adicionar_item(self, e):
        nome = ft.TextField(label="Nome do Item", width=150)
        marca = ft.TextField(label="Marca", width=150)
        unidade = ft.TextField(label="Unidade", width=150, on_change=self.atualizar_lista)
        preco = ft.TextField(label="Preço Unidade", width=150, on_change=self.atualizar_lista)

        new_item_column = ft.Column(
            controls=[nome, marca, unidade, preco],
            alignment=ft.MainAxisAlignment.CENTER
        )

        remove_button = ft.ElevatedButton(
            "Remover",
            on_click=lambda e, col=new_item_column: self.remover_item(col, None),
            color="RED"
        )

        new_item_column.controls.append(remove_button)
        new_item_column.controls.append(ft.Divider(height=10, thickness=1, color=ft.colors.GREY))
        
        self.items_container.controls.append(new_item_column)
        self.page.update()

        try:
            unidade_value = float(unidade.value) if unidade.value else 0
            preco_value = float(preco.value) if preco.value else 0
            if nome.value and preco.value:
                self.db.adicionar_item(self.id_lista, nome.value, marca.value, unidade_value, preco_value)
        except ValueError as ex:
            print(f"Erro ao adicionar item: {ex}")
        
        self.atualizar_lista(None)

    def remover_item(self, item_column, id_item):
        self.items_container.controls.remove(item_column)
        self.page.update()

        if id_item:
            self.db.remover_item(id_item)

        self.atualizar_lista(None)

    def atualizar_lista(self, e):
        self.itens_na_lista = len(self.items_container.controls)
        self.itens_comprados = 0
        self.valor_total = 0

        for item in self.items_container.controls:
            unidade = item.controls[2].value
            preco_unitario = item.controls[3].value

            if unidade and preco_unitario:
                try:
                    unidade = float(unidade)
                    preco_unitario = float(preco_unitario)
                    self.itens_comprados += 1
                    self.valor_total += unidade * preco_unitario
                except ValueError:
                    pass  

        if self.stats_controls['itens_na_lista']:
            self.stats_controls['itens_na_lista'].value = str(self.itens_na_lista)
        if self.stats_controls['itens_comprados']:
            self.stats_controls['itens_comprados'].value = str(self.itens_comprados)
        if self.stats_controls['valor_total']:
            self.stats_controls['valor_total'].value = f"R$ {self.valor_total:.2f}"

        self.page.update()

    def voltar_para_lista_compras(self, e):
        campos_preenchidos = True

        for item in self.items_container.controls:
            nome = item.controls[0].value  
            marca = item.controls[1].value  
            unidade = item.controls[2].value  
            preco_unitario = item.controls[3].value  

            if not nome or not marca or not unidade or not preco_unitario:
                campos_preenchidos = False
                break

        if not campos_preenchidos:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("ERRO: Preencha todos os campos"),
                bgcolor="#ff0000",
                open=True
            )
            self.page.update()
            return

        for item in self.items_container.controls:
            nome = item.controls[0].value  
            marca = item.controls[1].value  
            unidade = item.controls[2].value  
            preco_unitario = item.controls[3].value  

            if nome:
                item_db = next((i for i in self.db.get_itens_by_lista(self.id_lista) if i[2] == nome), None)

                if item_db:
                    id_item = item_db[0]
                    self.db.update_item(id_item, nome, marca, float(unidade), float(preco_unitario))
                else:
                    self.db.adicionar_item(self.id_lista, nome, marca, float(unidade), float(preco_unitario))

        from Telas.listacompras import ListaCompras
        lista_compras_screen = ListaCompras(self.page, self.user_id)
        lista_compras_screen.show()

