import requests
import logging
import os
import json
from apis.data_cache import obtener_o_cachear

def leer_clave_twelve():
    ruta = os.path.join(os.path.dirname(__file__), "..", "resources", "config.json")
    with open(ruta, encoding="utf-8") as f:
        return json.load(f).get("twelve_api_key")

def obtener_cotizaciones_twelve():
    return obtener_o_cachear("cotizaciones_twelve", 10, _descargar_cotizaciones)

def _descargar_cotizaciones():
    try:
        api_key = leer_clave_twelve()
        if not api_key:
            raise Exception("API key de Twelve Data no encontrada en config.json")

        symbols = {
            "Apple (AAPL)": "AAPL",
            "Google (GOOGL)": "GOOGL",
            "Tesla (TSLA)": "TSLA",
            "S&P 500 (SPX)": "SPX",
            "Crudo WTI": "CL=F",
            "Oro (oz)": "XAU/USD"
        }

        url = "https://api.twelvedata.com/price"
        resultados = {}

        for nombre, simbolo in symbols.items():
            res = requests.get(url, params={"symbol": simbolo, "apikey": api_key}, timeout=10)
            data = res.json()
            precio = float(data.get("price", 0))
            resultados[nombre] = {
                "valor": precio,
                "variacion": 0.0  # No incluye % en endpoint básico
            }

        return resultados

    except Exception as e:
        logging.error(f"❌ Error obteniendo cotizaciones de Twelve Data: {e}")
        return {}
