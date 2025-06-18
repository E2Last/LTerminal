import toga
from toga.style import Pack
from toga.style.pack import ROW, CENTER
from datetime import datetime

class RelojMundial(toga.Box):
    def __init__(self):
        super().__init__(style=Pack(direction=ROW, alignment=CENTER, padding=5, height=30))

        self.label = toga.Label(
            "Cargando hora...",
            style=Pack(
                font_size=16,
                color="orange",
                background_color="rgb(30, 30, 30)",  # Fondo oscuro
                padding=5
            )
        )

        self.add(self.label)

    def actualizar_horas(self):
        ahora = datetime.now().strftime("%H:%M:%S")
        self.label.text = f"🕒 Hora local: {ahora}"
        print(f"[🕒] Hora actualizada: {ahora}")

