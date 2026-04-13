import flet as ft
import json
import time

def main(page: ft.Page):
    # 1. CONFIGURACIÓN INICIAL INMEDIATA
    page.title = "App Grupos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Mostramos un mensaje de carga rápido para evitar el timeout de Android
    splash_text = ft.Text("Cargando módulos de sistema...", size=16, color="blue")
    page.add(
        ft.Container(
            content=ft.Column([
                ft.ProgressRing(),
                splash_text,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center
        )
    )
    page.update()

    # 2. CARGA DE DATOS Y LÓGICA (Aquí el S23 audita las librerías)
    try:
        # Simulamos una espera mínima para que el kernel termine de validar
        time.sleep(0.5) 
        
        # Intentamos recuperar datos guardados
        res = page.client_storage.get("datos_grupos")
        lista_nombres = json.loads(res) if res else []
        
        # Funciones de la aplicación
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
                        leading=ft.Icon(ft.icons.GROUP),
                        title=ft.Text(n)
                    )
                )
            page.update()

        # Componentes de la UI
        input_nombre = ft.TextField(
            label="Nombre del Grupo", 
            expand=True,
            on_submit=agregar
        )
        lista_visual = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        # 3. CONSTRUCCIÓN DE LA INTERFAZ FINAL
        page.clean() # Borramos el círculo de carga
        page.add(
            ft.AppBar(
                title=ft.Text("GESTIÓN DE GRUPOS"), 
                bgcolor=ft.colors.SURFACE_VARIANT
            ),
            ft.Row([
                input_nombre, 
                ft.IconButton(icon=ft.icons.ADD, on_click=agregar, icon_color="blue")
            ]),
            lista_visual
        )
        
        # Llenamos la lista con lo que había guardado
        refrescar()
        
        # FORZAMOS LA VISIBILIDAD (Importante para el modo HIDDEN)
        page.window_visible = True
        page.update()

    except Exception as e:
        page.clean()
        page.add(ft.Text(f"Error crítico en el S23: {str(e)}", color="red"))
        page.update()

if __name__ == "__main__":
    # Forzamos puerto 8080 y vista HIDDEN para que Android no sospeche del arranque
    ft.app(
        target=main, 
        view=ft.AppView.FLET_APP_HIDDEN, 
        port=8080
    )
