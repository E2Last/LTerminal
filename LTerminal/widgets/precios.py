from textual.widgets import Static

class PrecioPanel(Static):
    def update_content(self, precios: dict):
        # Secciones dinámicas por palabras clave
        categorias = {
            "Criptomonedas": [],
            "Monedas y Commodities": [],
            "Otros": []
        }

        for nombre, valor in precios.items():
            nombre_lower = nombre.lower()
            if any(palabra in nombre_lower for palabra in ["bitcoin", "ethereum", "solana", "cardano", "ripple", "crypto"]):
                categorias["Criptomonedas"].append((nombre, valor))
            elif any(palabra in nombre_lower for palabra in ["dólar", "euro", "oro", "petróleo", "real", "yen", "libra"]):
                categorias["Monedas y Commodities"].append((nombre, valor))
            else:
                categorias["Otros"].append((nombre, valor))

        contenido = ""
        for titulo, elementos in categorias.items():
            if elementos:
                contenido += f"\n[bold reverse]{titulo}[/bold reverse]\n"
                for nombre, valor in elementos:
                    contenido += f"[bold cyan]{nombre:<22}[/bold cyan]: [green]{valor}[/green]\n"

        self.update(contenido)
