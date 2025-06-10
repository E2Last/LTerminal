from textual.widgets import Static
from textual.scroll_view import ScrollView
from textual.containers import Container
from ..utils.apis import obtener_noticias_region
from ..utils.helper import truncar

class NoticiasPanel(Container):

    def __init__(self):
        super().__init__()
        self.scroll_static = Static("Cargando noticias...", id="noticias-static")
        self.scroll = ScrollView(self.scroll_static, id="noticias-scroll")

    def compose(self):
        yield self.scroll

    def on_mount(self):
        self.actualizar_noticias()
        

    def actualizar_noticias(self):
        noticias = obtener_noticias_region()
        print("🔔 Cantidad de noticias:", len(noticias))

        if not noticias:
            self.scroll_static.update("[red]⚠️ No se pudieron obtener noticias.[/red]")
            return

        agrupadas = {}
        for noticia in noticias:
            region = noticia.get("region", "🌍 Otros")
            agrupadas.setdefault(region, []).append(noticia)

        contenido = ""
        for region, lista in agrupadas.items():
            contenido += f"\n[bold yellow]━━━━━━━━━━━━ {region} ━━━━━━━━━━━━[/bold yellow]\n"
            for n in lista:
                titulo = truncar(n.get("title", "Sin título"), 90)
                descripcion = truncar(n.get("description", ""), 120)
                fuente = n.get("source", {}).get("name", "Fuente desconocida")
                contenido += f"📌 [b]{titulo}[/b]\n🔹 [green]{fuente}[/green]: [italic]{descripcion}[/italic]\n\n"

        self.scroll_static.update(contenido)
