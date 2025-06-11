from textual.widgets import Static
from rich.text import Text

class PrecioPanel(Static):
    def update_content(self, precios: dict):
        from rich import print as rprint
        rprint("🧪 Precios recibidos:", precios)
        # Agrupar por categoría
        categorias = {
            "Criptomonedas": [],
            "Monedas y Commodities": [],
            "Acciones": [],
            "Otros": []
        }

        for nombre, data in precios.items():
            nombre_lower = nombre.lower()
            valor = data.get("valor")
            variacion = data.get("variacion", 0)

            # Determinar flecha y color
            if variacion > 0:
                variacion_str = f"[green]🔺 {variacion:.2f}%[/]"
            elif variacion < 0:
                variacion_str = f"[red]🔻 {abs(variacion):.2f}%[/]"
            else:
                variacion_str = "[white]→ 0.00%[/]"

            linea = f"{nombre:<20} : ${valor} {variacion_str}"

            if any(p in nombre_lower for p in ["bitcoin", "eth", "crypto", "solana", "cardano", "xrp"]):
                categorias["Criptomonedas"].append(linea)
            elif any(p in nombre_lower for p in ["dólar", "euro", "oro", "petróleo", "commodity", "real"]):
                categorias["Monedas y Commodities"].append(linea)
            elif any(p in nombre_lower for p in ["ypf", "ggal", "tsla", "apple", "nvda", "merval"]):
                categorias["Acciones"].append(linea)
            else:
                categorias["Otros"].append(linea)

        # Construir contenido Rich Text
        contenido = Text()
        for titulo, items in categorias.items():
            if items:
                contenido.append(f"\n[bold reverse]{titulo}[/bold reverse]\n")
                for item in items:
                    contenido.append(item + "\n")

        self.update(contenido)
