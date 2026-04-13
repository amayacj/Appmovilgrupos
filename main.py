import flet as ft
# No importamos json ni os aquí arriba para acelerar el boot

def main(page: ft.Page):
    # 1. Configuración ultra-minimalista inicial
    page.title = "GRUPOS"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_visible = True
    
    # 2. Splash screen de carga (evita que Samsung piense que la app se colgó)
    loading_text = ft.Text("Iniciando sistema...", color="blue")
    page.add(loading_text)
    page.update()

    # 3. Importaciones diferidas (Lazy Loading)
    # Esto hace que las librerías que vimos en el log se carguen después de abrir la ventana
    import json
    
    def inicializar_datos():
        try:
            res = page.client_storage.get("datos_grupos")
            return json.loads(res) if res else []
        except:
            return []

    lista_nombres = inicializar_datos()

    # UI principal
    def agregar(e):
        if input_nombre.value.strip():
            lista_nombres.append(input_nombre.value.strip())
            input_nombre.value = ""
            refrescar()

    def refrescar():
        lista_visual.controls.clear()
        for n in lista_nombres:
            lista_visual.controls.append(ft.ListTile(title=ft.Text(n)))
        page.update()

    input_nombre = ft.TextField(label="Nombre", expand=True)
    lista_visual = ft.Column()

    # Limpiamos el texto de carga y ponemos la UI real
    page.controls.clear()
    page.add(
        ft.Text("GESTIÓN DE GRUPOS", size=20, weight="bold"),
        ft.Row([input_nombre, ft.IconButton("add", on_click=agregar)]),
        lista_visual
    )
    refrescar()

if __name__ == "__main__":
    # Agregamos port=8080 para evitar conflictos de red internos en Android
    ft.app(target=main)
