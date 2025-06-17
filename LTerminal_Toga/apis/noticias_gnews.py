import requests
import logging
import os
import json
from apis.data_cache import obtener_o_cachear

def leer_clave_gnews():
    ruta = os.path.join(os.path.dirname(__file__), "..", "resources", "config.json")
    with open(ruta, encoding="utf-8") as f:
        return json.load(f).get("gnews_api_key")

def obtener_noticias_gnews():
    return obtener_o_cachear("noticias_gnews", 15, _descargar_noticias_gnews)

def _descargar_noticias_gnews():
    try:
        api_key = leer_clave_gnews()
        if not api_key:
            raise Exception("Clave 'gnews_api_key' no encontrada en config.json")

        url = "https://gnews.io/api/v4/search"

        noticias = []

        # 🟦 1. Argentina - Español
        params_ar = {
            "q": "argentina OR inflación OR dólar OR economia",
            "lang": "es",
            "country": "ar",
            "token": api_key,
            "max": 20
        }

        # 🟩 2. Global - Inglés
        params_global = {
            "q": "inflation OR war OR oil OR markets OR economy",
            "lang": "en",
            "token": api_key,
            "max": 20
        }

        # 🟨 3. Europa - Inglés
        params_europa = {
            "q": "europe OR germany OR france OR spain OR eurozone OR ecb OR brussels",
            "lang": "en",
            "token": api_key,
            "max": 20
        }

        for params, region in [
            (params_ar, "AR"),
            (params_global, "🌍"),
            (params_europa, "EU")
        ]:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            for item in data.get("articles", []):
                noticias.append({
                    "titulo": item.get("title", ""),
                    "descripcion": item.get("description", ""),
                    "url": item.get("url", ""),
                    "fuente": item.get("source", {}).get("name", "GNews"),
                    "region": region,
                    "fecha": item.get("publishedAt", "")
                })

        return noticias

    except Exception as e:
        logging.error(f"❌ Error en GNews: {e}")
        return []
