import flet as ft
import random
import math

def main(page: ft.Page):
    page.title = "Creador de Equipos Pro"    
    page.theme_mode = ft.ThemeMode.SYSTEM
    
    lista_input = ft.TextField(label="Lista de Personas", multiline=True, min_lines=3)
    valor_input = ft.TextField(label="Cantidad", value="3", width=100)
    modo_radio = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="por_persona", label="Personas/Grupo"),
        ft.Radio(value="por_grupo", label="Num. Grupos")
    ]))
    modo_radio.value = "por_persona"
    resultado_col = ft.Column(scroll=ft.ScrollMode.ADAPTIVE)

    def generar(e):
        items = [i.strip() for i in lista_input.value.split(",") if i.strip()]
        if not items: return
        valor = int(valor_input.value)
        parejas = [i for i in items if "-" in i]
        indivs = [i for i in items if "-" not in i]
        random.shuffle(parejas); random.shuffle(indivs)
        num_g = valor if modo_radio.value == "por_grupo" else math.ceil(len(items)/valor)
        grupos = [[] for _ in range(max(1, num_g))]
        for i, p in enumerate(parejas): grupos[i % len(grupos)].append(p)
        for p in indivs: grupos.sort(key=len); grupos[0].append(p)
        resultado_col.controls.clear()
        for i, g in enumerate(grupos):
            if g: resultado_col.controls.append(ft.Text(f"Grupo {i+1}: {', '.join(g)}", size=16))
        page.update()

    page.add(ft.Text("Creador de Equipos", size=30, weight="bold"), lista_input, modo_radio, valor_input,
             ft.ElevatedButton("Generar", on_click=generar), ft.Divider(), resultado_col)

if __name__ == "__main__":
    ft.app(target=main)

