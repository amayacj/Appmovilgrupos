import flet as ft

# NO IMPORTES NADA MÁS AQUÍ ARRIBA (ni json, ni os, ni time)
# Queremos que Flet arranque en milisegundos.

def main(page: ft.Page):
    # Configuración básica inmediata
    page.title = "App Grupos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Mostramos un mensaje de "Cargando" de inmediato
    # Esto le dice a Android: "Estoy vivo, no me cierres"
    page.add(
        ft.Container(
            content=ft.Column([
                ft.ProgressRing(),
                ft.Text("Iniciando motor de datos...", size=16, color="blue")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center
        )
    )
    page.update()

    # CARGA PESADA DESPUÉS DEL UPDATE
    # Aquí es donde Android revisará las librerías que vimos en el log
    try:
        import json
        import time
        
        # Simulamos una pausa técnica para que el S23 termine de validar
        time.sleep(1) 
        
        # Lógica de datos
        res = page.client_storage.get("datos_grupos")
        lista_nombres = json.loads(res) if res else []
        
        # UI Final
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

        input_nombre = ft.TextField(label="Nuevo Grupo", expand=True)
        lista_visual = ft.Column(scroll=ft.ScrollMode.AUTO)

        # Limpiamos el mensaje de carga y mostramos la App real
        page.clean()
        page.add(
            ft.AppBar(title=ft.Text("GESTIÓN DE GRUPOS"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Row([input_nombre, ft.IconButton(icon=ft.icons.ADD, on_click=agregar)]),
            lista_visual
        )
        refrescar()
        
    except Exception as e:
        page.clean()
        page.add(ft.Text(f"Error crítico: {str(e)}", color="red"))
        page.update()

if __name__ == "__main__":
    # Forzamos puerto y vista para evitar bloqueos de red interna
    ft.app(target=main, view=ft.AppView.FLET_APP, port=8080)
