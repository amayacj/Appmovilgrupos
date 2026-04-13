import flet as ft
import json
import os

def main(page: ft.Page):
    # --- Configuración Base ---
    page.title = "CREADOR DE GRUPOS"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "white"
    page.padding = 20
    # Esto ayuda a que el teclado del celular no tape los campos
    page.scroll = ft.ScrollMode.ADAPTIVE 

    # --- Persistencia Segura ---
    def obtener_datos():
        try:
            datos = page.client_storage.get("lista_trabajo_v2")
            return json.loads(datos) if datos else []
        except:
            return []

    lista_integrantes = obtener_datos()

    # --- Lógica de la Interfaz ---
    def actualizar_lista():
        columna_lista.controls.clear()
        for nombre in lista_integrantes:
            columna_lista.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon("person", color="cyan700"),
                        ft.Text(nombre, size=16, weight="medium", expand=True, color="black"),
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
            campo_input.error_text = ""
            actualizar_lista()
        else:
            campo_input.error_text = "Escribe un nombre"
            page.update()

    def borrar_nombre(e):
        lista_integrantes.remove(e.control.data)
        actualizar_lista()

    def grabar_lista(e):
        try:
            page.client_storage.set("lista_trabajo_v2", json.dumps(lista_integrantes))
            page.snack_bar = ft.SnackBar(ft.Text("¡Lista guardada con éxito!"))
            page.snack_bar.open = True
            page.update()
        except:
            pass

    # --- Componentes UI ---
    cabecera = ft.Column([
        ft.Text("CREADOR DE GRUPOS", size=26, weight="bold", color="cyan800"),
        ft.Text("Herramienta de Trabajo", size=14, color="grey600"),
        ft.Divider(height=10, thickness=1)
    ])

    campo_input = ft.TextField(
        label="Nombre del Integrante", 
        expand=True, 
        on_submit=agregar_nombre,
        border_radius=10
    )
    
    btn_add = ft.FloatingActionButton(icon="add", on_click=agregar_nombre, bgcolor="cyan700")
    
    columna_lista = ft.Column(scroll="auto", expand=True, spacing=10)

    # --- Construcción Final ---
    page.add(
        cabecera,
        ft.Row([campo_input, btn_add], alignment="center"),
        ft.Text("Integrantes Actuales:", weight="bold", size=16, color="black"),
        ft.Container(content=columna_lista, expand=True)
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon="save", 
        bgcolor="cyan", 
        on_click=grabar_lista, 
        tooltip="Grabar Lista"
    )

    actualizar_lista()

if __name__ == "__main__":
    # Lógica Universal: 
    # Si detecta entorno de terminal (Laptop), usa Web. 
    # Si no (Celular/GitHub Actions), usa modo estándar.
    if os.environ.get("TERM"):
        ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    else:
        ft.app(target=main)
