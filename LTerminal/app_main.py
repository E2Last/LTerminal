import logging
import traceback
import os

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Horizontal
from textual.scroll_view import ScrollView
from .utils.helper import ruta_absoluta_recurso, truncar
from .utils.apis import obtener_precios, obtener_noticias_region
from .widgets.precios import PrecioPanel
from .widgets.reloj import generar_hora_multizona

# Ruta segura para log de errores
log_path = os.path.join(os.path.expanduser("~"), "Desktop", "LTerminal_error.log")

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    print("🟢 Iniciando LTerminal")

    class TerminalEconomicaApp(App):
        CSS_PATH = ruta_absoluta_recurso("LTerminal/resources/styles.css")

        def compose(self) -> ComposeResult:
            print("!!! Ejecutando compose()")
            self.clock_widget = Static("Cargando hora...", id="clock")
            self.noticias_widget = ScrollView(id="noticias-scroll")
            self.scroll_static = Static("Cargando noticias...")
            
            yield self.clock_widget
            yield Header()

            with Horizontal():
                yield self.noticias_widget
                self.precios_widget = PrecioPanel("Cargando precios...")
                yield self.precios_widget

            yield Button("Refrescar", id="refrescar")
            yield Footer()

        def on_mount(self):
            print("!!! Ejecutando on_mount()")
            self.noticias_widget.mount(self.scroll_static)
            self.actualizar_datos()
            self.set_interval(1, self.actualizar_reloj)

        def on_button_pressed(self, event):
            if event.button.id == "refrescar":
                self.actualizar_datos()

        def actualizar_datos(self):
            precios = obtener_precios()
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
            self.precios_widget.update_content(precios)

        def actualizar_reloj(self):
            hora_final = generar_hora_multizona()
            print("🕓", hora_final)
            self.clock_widget.update(hora_final)


    if __name__ == "__main__":
        TerminalEconomicaApp().run()

except Exception:
    logging.error("❌ Error crítico al iniciar LTerminal")
    logging.error(traceback.format_exc())
    print("❌ Error fatal. Revisá 'error.log' para más información.")
    input("Presioná Enter para cerrar...")
