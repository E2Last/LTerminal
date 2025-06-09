from textual.widgets import Static

class PrecioPanel(Static):
    def update_content(self, precios):
        contenido = "\n".join(
            f"[bold cyan]{k}:[/bold cyan] [green]{v}[/green]" for k, v in precios.items()
        )
        self.update(contenido)
