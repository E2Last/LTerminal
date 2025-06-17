import toga
from toga.style import Pack
from toga import ScrollContainer, Box, Label

class PrecioPanel(toga.Box):
    def __init__(self, precios: dict):
        super().__init__(style=Pack(direction="column", padding=5, background_color="black"))

        categorias = {
            "🪙 Criptomonedas": [],
            "💵 Dólar": [],
            "📈 Acciones": [],
            "🛢 Commodities": [],
            "🌐 Índices": [],
            "Otros": []
        }

        for nombre, datos in precios.items():
            nombre_lower = nombre.lower()
            if "btc" in nombre_lower or "eth" in nombre_lower or "cripto" in nombre_lower:
                categorias["🪙 Criptomonedas"].append((nombre, datos))
            elif "dolar" in nombre_lower:
                categorias["💵 Dólar"].append((nombre, datos))
            elif any(t in nombre_lower for t in ["aapl", "tesla", "googl", "ypf"]):
                categorias["📈 Acciones"].append((nombre, datos))
            elif "oro" in nombre_lower or "wti" in nombre_lower:
                categorias["🛢 Commodities"].append((nombre, datos))
            elif "s&p" in nombre_lower or "spx" in nombre_lower:
                categorias["🌐 Índices"].append((nombre, datos))
            else:
                categorias["Otros"].append((nombre, datos))

        # Contenedor para las filas de precios
        contenido = Box(style=Pack(direction="column", background_color="black"))


        for titulo, items in categorias.items():
            if not items:
                continue

            contenido.add(Label(titulo, style=Pack(padding_top=10, font_weight="bold", color="cyan")))

            for nombre, datos in items:
                variacion = datos.get("variacion", 0.0)
                if variacion > 0:
                    variacion_str = f"🔺 {variacion:.2f}%"
                elif variacion < 0:
                    variacion_str = f"🔻 {abs(variacion):.2f}%"
                else:
                    variacion_str = "→ 0.00%"

                fila = Box(style=Pack(direction="row", padding=2))
                fila.add(Label(nombre, style=Pack(width=200, color="green")))
                fila.add(Label(f"${datos['valor']:.2f}", style=Pack(width=100, color="white")))
                fila.add(Label(variacion_str, style=Pack(width=100, color="yellow")))

                contenido.add(fila)

        # Scroll con altura visible
        scroll = ScrollContainer(content=contenido, style=Pack(height=300, background_color="black"))

        self.add(scroll)
