import requests
import os
from apis.data_cache import obtener_o_cachear  # Asegurate que el path sea correcto


def fetch_desde_api():
    precios = {}
    api_key = os.getenv("TWELVE_API_KEY") or "c3dbde2efe354dd1b9eb9ea7a1b7004d"

    activos = {
        "Bitcoin (BTC)": "BTC/USD",
        "Ethereum (ETH)": "ETH/USD",
        "Oro (oz)": "XAU/USD",
        "YPF": "YPF",
        "Apple (AAPL)": "AAPL"
    }


    for nombre, simbolo in activos.items():
        try:
            url = f"https://api.twelvedata.com/quote?symbol={simbolo}&apikey={api_key}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            print("DEBUG: datos obtenidos", data)

            
            if "close" in data:
                precios[nombre] = {
                    "valor": float(data["close"]),
                    "variacion": float(data.get("percent_change", 0)) * 100
                }
            else:
                print(f"⚠️ No se encontró precio para {nombre}. Respuesta: {data}")
        except Exception as e:
            print(f"❌ Error obteniendo {nombre} ({simbolo}): {e}")

    # Cotizaciones Dólar (DolarAPI)
    try:
        r = requests.get("https://dolarapi.com/v1/dolares", timeout=10)
        if r.ok:
            for item in r.json():
                nombre = f"DOLAR {item['nombre']}"
                compra = item.get("compra") or 0
                venta = item.get("venta") or 0
                promedio = round((compra + venta) / 2, 2)
                precios[nombre] = {
                    "valor": promedio,
                    "variacion": 0
                }
    except Exception as e:
        print(f"❌ Error obteniendo cotizaciones dólar: {e}")

    return precios


def obtener_precios():
    precios = obtener_o_cachear("precios", minutos=360, funcion_callback=fetch_desde_api)


    if not isinstance(precios, dict):
        print("❌ Error: no se obtuvieron precios válidos.")
        return {}

    return precios
