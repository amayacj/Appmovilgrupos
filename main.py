import flet as ft
import json

def main(page: ft.Page):
    page.title = "CREADOR DE GRUPOS PRO"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "white"
    page.padding = 20

    # --- Persistencia de Datos ---
    def obtener_datos():
        datos = page.client_storage.get("lista_trabajo")
        return json.loads(datos) if datos else []

    lista_integrantes = obtener_datos()

    # --- Funciones de Lógica ---
    def actualizar_lista():
        columna_lista.controls.clear()
        for nombre in lista_integrantes:
            columna_lista.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon("person", color="cyan700"),
                        ft.Text(nombre, size=16, weight="medium", expand=True),
                        ft.IconButton("delete", icon_color="red400", data=nombre, on_click=borrar_nombre)
                    ]),
                    bgcolor="#f0f4f8",
                    padding=10,
                    border_radius=10
                )
            )
        page.update()

    def agregar_nombre(e):
        if campo_input.value.strip():
            lista_integrantes.append(campo_input.value.strip())
            campo_input.value = ""
            actualizar_lista()
        else:
            campo_input.error_text = "Escribe un nombre"
            page.update()

    def borrar_nombre(e):
        lista_integrantes.remove(e.control.data)
        actualizar_lista()

    def grabar_lista(e):
        page.client_storage.set("lista_trabajo", json.dumps(lista_integrantes))
        page.snack_bar = ft.SnackBar(ft.Text("¡Lista guardada en memoria!"))
        page.snack_bar.open = True
        page.update()

    # --- Componentes UI ---
    cabecera = ft.Column([
        ft.Text("CREADOR DE GRUPOS", size=28, weight="bold", color="cyan800"),
        ft.Text("Herramienta de Trabajo", size=16, color="grey600"),
        ft.Divider(height=20)
    ])

    campo_input = ft.TextField(label="Nombre del Integrante", expand=True, on_submit=agregar_nombre)
    btn_add = ft.FloatingActionButton(icon="add", on_click=agregar_nombre, bgcolor="cyan700")
    
    columna_lista = ft.Column(scroll="auto", expand=True)

    # --- Estructura ---
    page.add(
        cabecera,
        ft.Row([campo_input, btn_add]),
        ft.Text("Integrantes Actuales:", weight="bold", size=18),
        columna_lista
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon="save", bgcolor="cyan_accent", on_click=grabar_lista, tooltip="Grabar Lista"
    )

    actualizar_lista()

if __name__ == "__main__":
    import os
    # Si detecta que estás en el entorno de la Chromebook (Linux/Crostini), abre el navegador
    # En el celular, esto se ignorará y abrirá la App normal
    if os.environ.get("TERM"): 
        ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    else:
        ft.app(target=main)
