import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from apis.precios import obtener_precios
from widgets.tabla_noticias import NoticiasPanel
import traceback
import sys
from pathlib import Path
from resources.styles import (
    app_fondo, titulo_label, tabla_precios,
    tabla_noticias, boton_base, contenedor_seccion
)
from widgets.tabla_precios import PrecioPanel

log_path = Path(__file__).resolve().parent / "error-log.txt"

class LTerminalTogaApp(toga.App):
    def startup(self):
        try:
            # Contenedor principal
            self.main_box = toga.Box(style=app_fondo)

            # Título
            self.title_label = toga.Label("📊 Panel de Cotizaciones", style=titulo_label)
            self.main_box.add(self.title_label)
            # Cargar precios iniciales primero
            precios_iniciales = obtener_precios()
            self.panel_precios = PrecioPanel(precios_iniciales)
            self.main_box.add(self.panel_precios)

            
            # Tabla de cotizaciones
            # self.tabla = toga.Table(headings=["Activo", "Precio", "Variación"], style=tabla_precios)
            # self.main_box.add(self.tabla)

            
            # Botón refrescar cotizaciones
            self.refresh_button = toga.Button("🔄 Refrescar precios", on_press=self.actualizar_precios, style=boton_base)
            self.main_box.add(self.refresh_button)

            # Panel de noticias
            self.main_box.add(NoticiasPanel())

            # Ventana principal
            self.main_window = toga.MainWindow(title=self.formal_name)
            self.main_window.content = self.main_box
            self.main_window.size = (1600, 900)  # Tamaño inicial sugerido
            self.main_window.show()

        except Exception:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("❌ Error en startup():\n")
                traceback.print_exc(file=f)
            raise

    def actualizar_precios(self, widget):
        try:
            self.main_box.remove(self.panel_precios)
            self.panel_precios = PrecioPanel(obtener_precios())
            self.main_box.add(self.panel_precios, index=2)  # justo después del título
        except Exception:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("❌ Error al actualizar precios:\n")
                traceback.print_exc(file=f)

                
#AFUERA DE LA CLASE PRINCIPAL
def main():
    return LTerminalTogaApp("ETerminal - Data", "org.lterminal.data")

if __name__ == "__main__":
    try:
        with open("start.log", "w", encoding="utf-8") as f:
            f.write("✅ Entró en main()\n")
        app = main()
        with open("start.log", "a", encoding="utf-8") as f:
            f.write("✅ Ejecutando main_loop()\n")
        app.main_loop()
    except Exception as e:
        with open("error-log.txt", "w", encoding="utf-8") as f:
            import traceback
            f.write("❌ Error en main_loop():\n")
            traceback.print_exc(file=f)
