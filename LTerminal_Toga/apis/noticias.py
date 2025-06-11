import requests
import json
import logging
from pathlib import Path

def obtener_noticias():
    noticias_total = []

    try:
        # Leer config.json desde resources
        base_path = Path(__file__).parent.parent
        config_path = base_path / "resources" / "config.json"
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
        api_key = config.get("news_api_key")

        regiones = {
            "Argentina": "economia argentina",
            "Brasil": "economia brasil",
            "Chile": "economia chile",
            "China": "economia china",
            "Rusia": "economia rusia",
            "Ucrania": "economia ucrania",
            "Europa": "economia europa"
        }

        for region, query in regiones.items():
            url = (
                f"https://newsapi.org/v2/everything?"
                f"q={query}&language=es&sortBy=publishedAt&pageSize=4&apiKey={api_key}"
            )
            res = requests.get(url, timeout=10)
            datos = res.json().get("articles", [])
            for n in datos:
                noticias_total.append({
                    "region": region,
                    "titulo": n["title"],
                    "fuente": n["source"]["name"],
                    "url": n["url"]
                })
    except Exception as e:
        logging.error(f"❌ Error obteniendo noticias: {e}")

    return noticias_total
