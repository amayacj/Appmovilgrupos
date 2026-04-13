import flet as ft
import json
import time

def main(page: ft.Page):
    # 1. Configuración de página inmediata para evitar el timeout de Android
    page.title = "App Grupos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Splash screen de carga inmediata
    page.add(
        ft.Container(
            content=ft.Column([
                ft.ProgressRing(),
                ft.Text("Iniciando componentes nativos...", color="blue")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center
        )
    )
    page.update()

    try:
        # 2. Carga de Datos y Lógica
        # Un pequeño respiro para que el kernel de Samsung termine su auditoría
        time.sleep(0.5) 
        
        # Recuperar datos guardados
        res = page.client_storage.get("datos_grupos")
        lista_nombres = json.loads(res) if res else []

        def agregar(e):
            if input_nombre.value.strip():
                lista_nombres.append(input_nombre.value.strip())
                page.client_storage.set("datos_grupos", json.dumps(lista_nombres))
                input_nombre.value = ""
                refrescar()

        def refrescar():
            lista_visual.controls.clear()
            for n in lista_nombres:
                lista_visual.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.GROUP, color="blue"),
                        title=ft.Text(n)
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

        # 3. Construcción de la UI Final
        page.clean()
        page.add(
            ft.AppBar(
                title=ft.Text("GESTIÓN DE GRUPOS"), 
                bgcolor=ft.colors.SURFACE_VARIANT
            ),
            ft.Row([
                input_nombre, 
                ft.ElevatedButton("AÑADIR", on_click=agregar)
            ]),
            lista_visual
        )
        
        refrescar()
        
        # Despertamos la ventana manualmente (Muy importante para Samsung)
        page.window_visible = True
        page.update()

    except Exception as e:
        page.clean()
        page.add(ft.Text(f"Error técnico: {str(e)}", color="red"))
        page.update()

if __name__ == "__main__":
    # Usamos FLET_APP_HIDDEN y puerto 8080 para máxima compatibilidad
    ft.app(
        target=main, 
        view=ft.AppView.FLET_APP_HIDDEN, 
        port=8080
    )
