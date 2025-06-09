from textual.widgets import Static

class PrecioPanel(Static):
    def update_content(self, precios: dict):
        contenido = "\n".join(
            f"💰 [bold cyan]{moneda:<20}[/bold cyan]: [green]{valor:>10}[/green]"
            for moneda, valor in precios.items()
        )
        self.update(contenido)

