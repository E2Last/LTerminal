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

log_path = Path(__file__).resolve().parent / "error-log.txt"

class LTerminalTogaApp(toga.App):
    def startup(self):
        try:
            # Contenedor principal
            self.main_box = toga.Box(style=app_fondo)

            # Título
            self.title_label = toga.Label("📊 Panel de Cotizaciones", style=titulo_label)
            self.main_box.add(self.title_label)

            # Tabla de cotizaciones
            self.tabla = toga.Table(headings=["Activo", "Precio", "Variación"], style=tabla_precios)
            self.main_box.add(self.tabla)

            # Botón refrescar cotizaciones
            self.refresh_button = toga.Button("🔄 Refrescar precios", on_press=self.actualizar_precios, style=boton_base)
            self.main_box.add(self.refresh_button)

            # Panel de noticias
            self.main_box.add(NoticiasPanel())

            # Ventana principal
            self.main_window = toga.MainWindow(title=self.formal_name)
            self.main_window.content = self.main_box
            self.main_window.show()

            # Cargar precios iniciales
            self.actualizar_precios(None)

        except Exception:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("❌ Error en startup():\n")
                traceback.print_exc(file=f)
            raise

    def actualizar_precios(self, widget):
        try:
            self.tabla.data.clear()
            precios = obtener_precios()
            
            if not isinstance(precios, dict):
                raise ValueError("❌ El resultado de obtener_precios no es un diccionario válido.")

            for nombre, datos in precios.items():
                valor = f"${datos['valor']:.2f}"
                variacion = datos['variacion']
                if variacion > 0:
                    variacion_str = f"🔺 {variacion:.2f}%"
                elif variacion < 0:
                    variacion_str = f"🔻 {abs(variacion):.2f}%"
                else:
                    variacion_str = "→ 0.00%"
                self.tabla.data.append((nombre, valor, variacion_str))
        except Exception:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("❌ Error al actualizar precios:\n")
                traceback.print_exc(file=f)
                
    def main():
        return LTerminalTogaApp("ETerminal - Data", "org.lterminal.data")


    if __name__ == "__main__":
        try:
            app = main()
            app.main_loop()
        except Exception:
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("❌ Error en main_loop():\n")
                traceback.print_exc(file=f)
