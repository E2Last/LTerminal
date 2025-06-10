import json
import requests
import logging
from .helper import ruta_absoluta_recurso
from LTerminal.utils.data_cache import obtener_o_cachear
import os


def obtener_precios():
    def fetch_precios():
        precios = {}

        # ░░░ CRIPTOMONEDAS ░░░
        try:
            ids = "bitcoin,ethereum,solana,cardano,ripple"
            cripto_res = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": ids, "vs_currencies": "usd"}
            )
            cripto_data = cripto_res.json()
            precios["Bitcoin (BTC)"] = f"${cripto_data['bitcoin']['usd']}"
            precios["Ethereum (ETH)"] = f"${cripto_data['ethereum']['usd']}"
            precios["Solana (SOL)"] = f"${cripto_data['solana']['usd']}"
            precios["Cardano (ADA)"] = f"${cripto_data['cardano']['usd']}"
            precios["Ripple (XRP)"] = f"${cripto_data['ripple']['usd']}"
        except Exception as e:
            logging.error(f"❌ Error cripto: {e}")

        # ░░░ DÓLARES ░░░
        try:
            dolar_res = requests.get("https://api.bluelytics.com.ar/v2/latest")
            dolar_data = dolar_res.json()
            precios["Dólar Blue"] = f"${dolar_data['blue']['value_sell']}"
            precios["Dólar Oficial"] = f"${dolar_data['oficial']['value_sell']}"
            precios["Dólar MEP"] = f"${dolar_data['oficial_euro']['value_sell']}"
        except Exception as e:
            logging.error(f"❌ Error dólar: {e}")

        # ░░░ EURO ░░░
        try:
            res = requests.get("https://v6.exchangerate-api.com/v6/ce19013a4066ac30580c1730/latest/USD")
            data = res.json()
            euro_rate = data["conversion_rates"]["EUR"]
            precios["Euro Oficial"] = f"${round(1 / euro_rate, 2)}"
        except Exception as e:
            logging.error(f"❌ Error euro: {e}")

        # ░░░ ORO ░░░
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            oro_res = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/GC=F", headers=headers)
            oro_data = oro_res.json()
            precios["Oro (oz)"] = f"${oro_data['chart']['result'][0]['meta']['regularMarketPrice']}"
        except Exception as e:
            logging.error(f"❌ Error oro Yahoo: {e}")

        # ░░░ PETRÓLEO WTI ░░░
        try:
            petroleo_res = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/CL=F", headers=headers)
            petroleo_data = petroleo_res.json()
            precios["Petróleo WTI"] = f"${petroleo_data['chart']['result'][0]['meta']['regularMarketPrice']}"
        except Exception as e:
            logging.error(f"❌ Error petróleo Yahoo: {e}")

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
