import flet as ft
import json

def main(page: ft.Page):
    # Configuración de página ultra-compatible
    page.title = "CREADOR DE GRUPOS"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "white"
    
    # Manejo de memoria seguro
    def inicializar_datos():
        try:
            res = page.client_storage.get("datos_grupos")
            return json.loads(res) if res else []
        except:
            return []

    lista_nombres = inicializar_datos()

    def refrescar_interfaz():
        lista_visual.controls.clear()
        for n in lista_nombres:
            lista_visual.controls.append(
                ft.ListTile(
                    leading=ft.Icon("person", color="blue"),
                    title=ft.Text(n, color="black"),
                    trailing=ft.IconButton("delete", icon_color="red", data=n, on_click=borrar)
                )
            )
        page.update()

    def agregar(e):
        if input_nombre.value.strip():
            lista_nombres.append(input_nombre.value.strip())
            input_nombre.value = ""
            refrescar_interfaz()

    def borrar(e):
        lista_nombres.remove(e.control.data)
        refrescar_interfaz()

    def guardar(e):
        page.client_storage.set("datos_grupos", json.dumps(lista_nombres))
        page.snack_bar = ft.SnackBar(ft.Text("Guardado"))
        page.snack_bar.open = True
        page.update()

    # UI simple
    input_nombre = ft.TextField(label="Nombre", on_submit=agregar, expand=True)
    lista_visual = ft.Column(scroll=ft.ScrollMode.AUTO)

    page.add(
        ft.Text("GESTIÓN DE GRUPOS", size=25, weight="bold", color="blue"),
        ft.Row([input_nombre, ft.IconButton("add", on_click=agregar)]),
        ft.Divider(),
        lista_visual
    )

    page.floating_action_button = ft.FloatingActionButton(icon="save", on_click=guardar)
    refrescar_interfaz()

if __name__ == "__main__":
    # Para el celular, Flet necesita la ejecución estándar
    ft.app(target=main)
