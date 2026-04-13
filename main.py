import flet as ft
import time

def main(page: ft.Page):
    # CONFIGURACIÓN INICIAL ULTRA-RÁPIDA
    page.title = "App Grupos"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Mostramos algo DE INMEDIATO para que el sistema no cierre la app
    log_status = ft.Text("Iniciando módulos de sistema...", color="blue")
    page.add(
        ft.Container(
            content=ft.Column([
                ft.ProgressRing(),
                log_status,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True
        )
    )
    page.update()

    # CARGA DIFERIDA (Aquí es donde Android revisa las librerías)
    try:
        import json
        import os
        log_status.value = "Cargando base de datos..."
        page.update()
        
        # Simulamos una pequeña espera para que el SO valide los permisos que vimos en el log
        time.sleep(0.5) 
        
        # Lógica de carga de datos
        res = page.client_storage.get("datos_grupos")
        lista_nombres = json.loads(res) if res else []
        
    except Exception as e:
        log_status.value = f"Error de inicio: {str(e)}"
        page.update()
        return

    # UI PRINCIPAL (Solo se carga cuando lo anterior termina)
    def agregar(e):
        if input_nombre.value.strip():
            lista_nombres.append(input_nombre.value.strip())
            page.client_storage.set("datos_grupos", json.dumps(lista_nombres))
            input_nombre.value = ""
            refrescar()

    def refrescar():
        lista_visual.controls.clear()
        for n in lista_nombres:
            lista_visual.controls.append(ft.ListTile(title=ft.Text(n)))
        page.update()

    input_nombre = ft.TextField(label="Nombre del Grupo", expand=True)
    lista_visual = ft.Column(scroll=ft.ScrollMode.AUTO)

    # Limpiamos el splash screen y mostramos la app
    page.clean()
    page.add(
        ft.AppBar(title=ft.Text("GESTIÓN DE GRUPOS"), bgcolor=ft.colors.SURFACE_VARIANT),
        ft.Row([input_nombre, ft.IconButton(icon=ft.icons.ADD, on_click=agregar, icon_color="blue")]),
        lista_visual
    )
    refrescar()

if __name__ == "__main__":
    # Importante: No uses el modo web, usa el modo nativo para evitar más capas de red
    ft.app(target=main)
