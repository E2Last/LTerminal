import json
import requests
import logging
from .helper import ruta_absoluta_recurso

def obtener_precios():
    precios = {}
    try:
        cripto_res = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "bitcoin,ethereum", "vs_currencies": "usd"}
        )
        cripto_data = cripto_res.json()
        precios["Bitcoin (BTC)"] = f"${cripto_data['bitcoin']['usd']}"
        precios["Ethereum (ETH)"] = f"${cripto_data['ethereum']['usd']}"
    except:
        precios["Bitcoin (BTC)"] = "Error"
        precios["Ethereum (ETH)"] = "Error"

    try:
        dolar_res = requests.get("https://api.bluelytics.com.ar/v2/latest")
        dolar_data = dolar_res.json()
        precios["Dólar Blue"] = f"${dolar_data['blue']['value_sell']}"
        precios["Dólar Oficial"] = f"${dolar_data['oficial']['value_sell']}"
        precios["Dólar MEP"] = f"${dolar_data['oficial_euro']['value_sell']}"
    except:
        precios["Dólar Blue"] = "Error"
        precios["Dólar Oficial"] = "Error"
        precios["Dólar MEP"] = "Error"

    return precios


def obtener_noticias_region():
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
