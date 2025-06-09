from textual.widgets import Static

class PrecioPanel(Static):
    def update_content(self, precios: dict):
        categorias = {
            "Criptomonedas": ["Bitcoin (BTC)", "Ethereum (ETH)", "Solana (SOL)", "Cardano (ADA)", "Ripple (XRP)"],
            "Monedas y Commodities": ["Dólar Blue", "Dólar Oficial", "Dólar MEP", "Euro Oficial", "Oro (oz)", "Petróleo WTI"]
        }

        contenido = ""
        for titulo, claves in categorias.items():
            contenido += f"\n[bold reverse]{titulo}[/bold reverse]\n"
            for clave in claves:
                valor = precios.get(clave, "N/A")
                contenido += f"[bold cyan]{clave:<22}[/bold cyan]: [green]{valor}[/green]\n"

        self.update(contenido)
