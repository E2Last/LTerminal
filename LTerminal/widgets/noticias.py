from textual.widgets import Static
from textual.scroll_view import ScrollView
from textual.containers import Container
from ..utils.apis import obtener_noticias_region
from ..utils.helper import truncar

class NoticiasPanel(Container):

    def __init__(self):
        super().__init__()
        self.scroll = ScrollView(id="noticias-scroll")
        self.scroll_static = Static("Cargando noticias...")

    def compose(self):
        yield self.scroll  # ✅ scroll se monta primero

    def on_mount(self):
        self.scroll.mount(self.scroll_static)
        self.actualizar_noticias()

    def actualizar_noticias(self):
        noticias = obtener_noticias_region()

        agrupadas = {}
        for noticia in noticias:
            region = noticia.get("region", "🌍 Otros")
            agrupadas.setdefault(region, []).append(noticia)

        contenido = ""
        for region, lista in agrupadas.items():
            contenido += f"[bold yellow]━━━━━━━━━━━━ {region} ━━━━━━━━━━━━[/bold yellow]\n"
            for n in lista:
                titulo = truncar(n.get("title", "Sin título"), 90)
                descripcion = truncar(n.get("description", ""), 120)
                fuente = n.get("source", {}).get("name", "")
                contenido += f"📌 {titulo}\n🔹 [green]{fuente}[/green]: [italic]{descripcion}[/italic]\n\n"

        self.scroll_static.update(contenido)
