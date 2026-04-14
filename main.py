import flet as ft
import json
import time

def main(page: ft.Page):
    # 1. Configuración de la página
    page.title = "Gestión de Grupos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # Intentar recuperar datos guardados
    try:
        res = page.client_storage.get("datos_grupos")
        lista_nombres = json.loads(res) if res else []
    except:
        lista_nombres = []

    def agregar(e):
        if input_nombre.value.strip():
            lista_nombres.append(input_nombre.value.strip())
            page.client_storage.set("datos_grupos", json.dumps(lista_nombres))
            input_nombre.value = ""
            refrescar()

    def borrar_todo(e):
        lista_nombres.clear()
        page.client_storage.remove("datos_grupos")
        refrescar()

    def refrescar():
        lista_visual.controls.clear()
        for n in lista_nombres:
            lista_visual.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.GROUP, color="blue"),
                    title=ft.Text(n),
                )
            )
        page.update()

    # Componentes de la interfaz
    input_nombre = ft.TextField(
        label="Nombre del Grupo", 
        expand=True,
        on_submit=agregar
    )
    
    lista_visual = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # 2. Construcción de la interfaz
    page.add(
        ft.AppBar(
            title=ft.Text("GESTIÓN DE GRUPOS"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.DELETE_SWEEP, on_click=borrar_todo)
            ]
        ),
        ft.Container(
            padding=10,
            content=ft.Column([
                ft.Row([
                    input_nombre,
                    ft.ElevatedButton("AÑADIR", on_click=agregar),
                ]),
                ft.Divider(),
                lista_visual,
            ], expand=True)
        )
    )

    # Carga inicial de datos
    refrescar()

if __name__ == "__main__":
    # IMPORTANTE: Usamos WEB_BROWSER para saltar las restricciones de red del S23
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
