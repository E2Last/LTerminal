import json
import requests
import logging
from .helper import ruta_absoluta_recurso
from LTerminal.utils.data_cache import obtener_o_cachear
import os
from typing import List, Dict, Any

# ... (tu función obtener_precios() sigue igual, no la modifico) ...

def obtener_noticias_region() -> List[Dict[str, Any]]:
    def fetch_noticias():
        # Cargar config.json
        with open(ruta_absoluta_recurso("LTerminal/config.json"), encoding="utf-8") as f:
            config = json.load(f)
        news_api_key = config.get("news_api_key")
        apitube_api_key = config.get("apitube_api_key")

        regiones = {
            "🇦🇷 Argentina": "economia argentina",
            "🇧🇷 Brasil": "economia brasil",
            "🇨🇱 Chile": "economia chile",
            "🇨🇳 China": "economia china",
            "🇷🇺 Rusia": "economia rusia",
            "🇺🇦 Ucrania": "economia ucrania",
            "🇪🇺 Europa": "economia europa"
        }

        noticias_total = []

        # ░░░ NewsAPI.org ░░░
        if news_api_key:
            for region, query in regiones.items():
                url = (
                    f"https://newsapi.org/v2/everything?"
                    f"q={query}&language=es&sortBy=publishedAt&pageSize=4&apiKey={news_api_key}"
                )
                try:
                    res = requests.get(url)
                    res.raise_for_status()
                    datos = res.json().get("articles", [])
                    for n in datos:
                        noticias_total.append({
                            "region": region,
                            "title": n.get("title", "Sin título"),
                            "description": n.get("description", "") or n.get("content", "")[:120],
                            "source": {"name": n.get("source", {}).get("name", "Fuente desconocida")}
                        })
                except Exception as e:
                    logging.error(f"Error obteniendo noticias de NewsAPI para {region}: {e}")

        # ░░░ APITube.io ░░░
        if apitube_api_key:
            for region, query in regiones.items():
                url = "https://api.apitube.io/v1/news"
                params = {
                    "q": query,  # Usar la misma consulta que en NewsAPI
                    "limit": 4,  # Igualar el número de artículos por región
                    "language": "es,en",
                    "country": "ar,cl,br,cn,ru,ua,es,us,de,fr",  # Países relevantes para las regiones
                }
                headers = {"x-api-key": apitube_api_key}
                try:
                    res = requests.get(url, params=params, headers=headers)
                    res.raise_for_status()
                    datos = res.json().get("data", [])
                    for n in datos:
                        noticias_total.append({
                            "region": region,
                            "title": n.get("title", "Sin título"),
                            "description": n.get("description", "") or n.get("summary", "")[:120],
                            "source": {"name": n.get("source", "Fuente desconocida")}
                        })
                except Exception as e:
                    logging.error(f"Error obteniendo noticias de APITube para {region}: {e}")

        # Eliminar duplicados por título
        noticias_unicas = {n["title"]: n for n in noticias_total}.values()
        logging.info(f"🔔 Noticias totales obtenidas: {len(noticias_unicas)}")
        return list(noticias_unicas)

    return obtener_o_cachear("noticias", minutos=60, funcion_callback=fetch_noticias)