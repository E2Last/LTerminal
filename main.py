import requests
import json
from rich.console import Console
from rich.table import Table
from datetime import datetime

# Cargar API Key desde config.json
with open("config.json", "r") as file:
    config = json.load(file)

API_KEY = config["news_api_key"]
console = Console()

def obtener_noticias():
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=es&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        console.print(f"[red]Error al obtener noticias: {response.status_code}[/red]")
        return []

    noticias = response.json().get("articles", [])
    return noticias

def mostrar_noticias(noticias):
    tabla = Table(title="📰 Noticias Económicas en Tiempo Real", expand=True)

    tabla.add_column("Fuente", style="cyan", no_wrap=True)
    tabla.add_column("Título", style="bold", overflow="fold")
    tabla.add_column("Hora", style="magenta")

    for noticia in noticias[:10]:  # Limita a 10 noticias
        fuente = noticia["source"]["name"]
        titulo = noticia["title"]
        hora = noticia["publishedAt"]
        hora = datetime.fromisoformat(hora.replace("Z", "+00:00")).strftime("%H:%M")
        tabla.add_row(fuente, titulo, hora)

    console.clear()
    console.print(tabla)

if __name__ == "__main__":
    noticias = obtener_noticias()
    if noticias:
        mostrar_noticias(noticias)
    else:
        console.print("[yellow]No hay noticias disponibles por el momento.[/yellow]")
