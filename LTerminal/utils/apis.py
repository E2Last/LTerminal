import json
import requests
import logging
from .helper import ruta_absoluta_recurso
from LTerminal.utils.data_cache import obtener_o_cachear
import os

API_TWELVE = "https://api.twelvedata.com"
API_KEY = "c3dbde2efe354dd1b9eb9ea7a1b7004d"

def obtener_precios():
    def fetch_precios():
        precios = {}

        # ░░░ DOLARAPI ░░░
        try:
            r = requests.get("https://dolarapi.com/v1/dolares", timeout=5)
            for entrada in r.json():
                nombre = entrada["moneda"]
                valor = entrada["venta"]
                precios[nombre] = {"valor": valor, "variacion": 0}
        except Exception as e:
            logging.error(f"❌ Error en DolarAPI: {e}")

        # ░░░ TWELVE DATA: CRIPTOS, ACCIONES, COMMODITIES ░░░
        activos = {
            "Bitcoin (BTC)": "BTC/USD",
            "Ethereum (ETH)": "ETH/USD",
            "Solana (SOL)": "SOL/USD",
            "Cardano (ADA)": "ADA/USD",
            "Ripple (XRP)": "XRP/USD",
            "Oro (oz)": "XAU/USD",
            "Petróleo WTI": "WTI/USD",
            "YPF": "YPF",
            "Galicia (GGAL)": "GGAL",
            "Banco Macro (BMA)": "BMA",
            "Apple (AAPL)": "AAPL",
            "Microsoft (MSFT)": "MSFT",
            "Tesla (TSLA)": "TSLA",
            "Nvidia (NVDA)": "NVDA"
        }

        for nombre, simbolo in activos.items():
            try:
                r = requests.get(
                    f"{API_TWELVE}/quote",
                    params={"symbol": simbolo, "apikey": API_KEY},
                    timeout=5
                )
                data = r.json()
                if "price" in data and "percent_change" in data:
                    precios[nombre] = {
                        "valor": float(data["price"]),
                        "variacion": float(data["percent_change"])
                    }
            except Exception as e:
                logging.error(f"❌ Error en Twelve Data ({nombre}): {e}")

        return precios

    return obtener_o_cachear("precios", minutos=10, funcion_callback=fetch_precios)



def obtener_noticias_region():
    def fetch_noticias():
        with open(ruta_absoluta_recurso("LTerminal/config.json"), encoding="utf-8") as f:
            config = json.load(f)

        api_key = config["news_api_key"]
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
        for region, query in regiones.items():
            url = (
                f"https://newsapi.org/v2/everything?"
                f"q={query}&language=es&sortBy=publishedAt&pageSize=4&apiKey={api_key}"
            )
            try:
                res = requests.get(url)
                datos = res.json().get("articles", [])
                for n in datos:
                    n["region"] = region
                    noticias_total.append(n)
            except Exception as e:
                logging.error(f"Error obteniendo noticias para {region}: {e}")

        return noticias_total

    return obtener_o_cachear("noticias", minutos=60, funcion_callback=fetch_noticias)
