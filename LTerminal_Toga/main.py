import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from apis.precios import obtener_precios
from widgets.tabla_noticias import NoticiasPanel
from widgets.tabla_precios import PrecioPanel
from resources.styles import (
    app_fondo, titulo_label, tabla_precios,
    tabla_noticias, boton_base, contenedor_seccion
)
from pathlib import Path
import traceback
import asyncio
from widgets.reloj_mundial import RelojMundial

log_path = Path(__file__).resolve().parent / "error-log.txt"

class LTerminalTogaApp(toga.App):
    def __init__(self, name, app_id):
        super().__init__(formal_name=name, app_id=app_id)
        
    async def reloj_loop(self):
        while True:
            self.reloj.actualizar_horas()
            await asyncio.sleep(1)


    def startup(self):
        try:
            # Contenedor principal
            self.main_box = toga.Box(style=app_fondo)

            # Reloj mundial
            self.reloj = RelojMundial()
            self.main_box.add(self.reloj)

            # Título
            self.title_label = toga.Label("📊 Panel de Cotizaciones", style=titulo_label)
            self.main_box.add(self.title_label)

            # Cotizaciones
            precios_iniciales = obtener_precios()
            self.panel_precios = PrecioPanel(precios_iniciales)
            self.main_box.add(self.panel_precios)

            # Botón refrescar precios
            self.refresh_button = toga.Button("🔄 Refrescar precios", on_press=self.actualizar_precios, style=boton_base)
            self.main_box.add(self.refresh_button)

            # Noticias
            self.main_box.add(NoticiasPanel())

            # Ventana principal
            self.main_window = toga.MainWindow(title=self.formal_name)
            self.main_window.content = self.main_box
            self.main_window.size = (1600, 900)
            self.main_window.show()
            # Aseguramos que se registre en el loop de eventos
            loop = asyncio.get_event_loop()
            loop.call_later(0.1, lambda: self.add_background_task(self.reloj_loop))

        except Exception:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("❌ Error en startup():\n")
                traceback.print_exc(file=f)
            raise

    def actualizar_precios(self, widget):
        try:
            self.main_box.remove(self.panel_precios)
            self.panel_precios = PrecioPanel(obtener_precios())
            self.main_box.add(self.panel_precios, index=2)
        except Exception:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("❌ Error al actualizar precios:\n")
                traceback.print_exc(file=f)

def main():
    return LTerminalTogaApp("ETerminal - Data", "org.lterminal.data")

if __name__ == "__main__":
    try:
        with open("start.log", "w", encoding="utf-8") as f:
            f.write("✅ Entró en main()\n")
        app = main()
        with open("start.log", "a", encoding="utf-8") as f:
            f.write("✅ Ejecutando main_loop()\n")
        app.main_loop()  # SOLO esto, no startup(), no add_background_task()
    except Exception as e:
        with open("error-log.txt", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
