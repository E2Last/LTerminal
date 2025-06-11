import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from apis.precios import obtener_precios


class LTerminalTogaApp(toga.App):
    def startup(self):
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Título
        self.title_label = toga.Label(
            "📊 Panel de Cotizaciones", style=Pack(font_size=18, padding=(0, 0, 10, 0))
        )
        self.main_box.add(self.title_label)

        # Tabla
        self.tabla = toga.Table(
            headings=["Activo", "Precio", "Variación"],
            style=Pack(flex=1, padding=5),
        )
        self.main_box.add(self.tabla)

        # Botón para refrescar
        self.refresh_button = toga.Button(
            "🔄 Refrescar precios",
            on_press=self.actualizar_precios,
            style=Pack(padding=5),
        )
        self.main_box.add(self.refresh_button)

        # Ventana principal
        self.main_window = toga.MainWindow(title=self.name)
        self.main_window.content = self.main_box
        self.main_window.show()

        # Cargar precios iniciales
        self.actualizar_precios(None)

    def actualizar_precios(self, widget):
        self.tabla.data.clear()
        precios = obtener_precios()
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


def main():
    return LTerminalTogaApp("LTerminal TOGA", "org.lterminal.toga")
