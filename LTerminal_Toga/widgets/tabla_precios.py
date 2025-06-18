import toga
from toga.style import Pack
from toga import ScrollContainer, Box, Label
from math import ceil

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

            # Agrupar en columnas (máx 3 elementos por columna)
            columnas = []
            chunk_size = ceil(len(items) / 3)
            for i in range(0, len(items), chunk_size):
                chunk = items[i:i + chunk_size]
                col = Box(style=Pack(direction="column", padding_right=10))
                for nombre, datos in chunk:
                    variacion = datos.get("variacion", 0.0)
                    if variacion > 0:
                        variacion_str = f"🔺 {variacion:.2f}%"
                    elif variacion < 0:
                        variacion_str = f"🔻 {abs(variacion):.2f}%"
                    else:
                        variacion_str = "→ 0.00%"

                    fila = Box(style=Pack(direction="row"))
                    fila.add(Label(nombre, style=Pack(width=160, color="#38CF39")))  # verde lima
                    fila.add(Label(f"${datos['valor']:.2f}", style=Pack(width=100, color="#38CF39")))
                    fila.add(Label(variacion_str, style=Pack(width=100, color="yellow")))
                    col.add(fila)
                columnas.append(col)

            # Fila horizontal con 2-3 columnas
            fila_con_columnas = Box(style=Pack(direction="row", background_color="black"))
            for col in columnas:
                fila_con_columnas.add(col)

            contenido.add(fila_con_columnas)

        # Scroll con altura visible
        scroll = ScrollContainer(content=contenido, style=Pack(height=400, background_color="black"))

        self.add(scroll)
