import toga
from toga.style import Pack
from datetime import datetime
import pytz

class RelojMundial(toga.Box):
    def __init__(self):
        super().__init__(style=Pack(direction="column", background_color="black", padding=5))

        self.label_titulo = toga.Label("🕒 Reloj Mundial", style=Pack(color="cyan", font_weight="bold", margin_bottom=5))
        self.add(self.label_titulo)

        self.zonas = {
            "AR": ("Argentina", "America/Argentina/Buenos_Aires"),
            "US": ("USA (NY)", "America/New_York"),
            "EU": ("Europa (Berlín)", "Europe/Berlin"),
            "JP": ("Japón", "Asia/Tokyo"),
            "RU": ("Rusia (Moscú)", "Europe/Moscow")
        }

        self.labels = {}
        fila = toga.Box(style=Pack(direction="row", background_color="black", flex=1))

        for codigo, (nombre, zona) in self.zonas.items():
            lbl = toga.Label("", style=Pack(color="#FFA500", margin_right=20, font_family="monospace"))
            self.labels[codigo] = (lbl, zona, nombre)
            fila.add(lbl)

        self.add(fila)
        self.actualizar_horas()

    def actualizar_horas(self):
        for codigo, (label, zona, nombre) in self.labels.items():
            tz = pytz.timezone(zona)
            ahora = datetime.now(tz).strftime("%H:%M:%S")
            label.text = f"{codigo}: {ahora}"
