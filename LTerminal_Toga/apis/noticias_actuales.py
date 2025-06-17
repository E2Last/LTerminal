import requests
import logging
import os
import json
from apis.data_cache import obtener_o_cachear

def leer_clave_newsdataio():
    ruta = os.path.join(os.path.dirname(__file__), "..", "resources", "config.json")
    with open(ruta, encoding="utf-8") as f:
        return json.load(f).get("newsdataio")

def obtener_noticias_newsdataio(pais="ar", categoria="business", idioma="es"):
    return obtener_o_cachear("noticias_newsdataio", 15, lambda: _descargar_newsdataio(pais, categoria, idioma))

def _descargar_newsdataio(pais, categoria, idioma):
    try:
        api_key = leer_clave_newsdataio()
        if not api_key:
            raise Exception("Clave 'newsdataio' no encontrada en config.json")

        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": api_key,
            "country": pais,
            "language": idioma,
            "category": categoria,
            "q": "argentina OR dólar OR inflación OR petróleo OR FMI"
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        noticias = []
        for item in data.get("results", []):
            noticias.append({
                "titulo": item.get("title", ""),
                "descripcion": item.get("description", ""),
                "url": item.get("link", ""),
                "fecha": item.get("pubDate", "")
            })

        return noticias

    except Exception as e:
        logging.error(f"❌ Error en NewsData.io: {e}")
        return []
