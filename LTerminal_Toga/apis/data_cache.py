import os
import json
from datetime import datetime, timedelta

CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", "data_cache.json")

def leer_cache_completa():
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def guardar_cache(nombre: str, datos: dict):
    cache = leer_cache_completa()
    cache[nombre] = {
        "timestamp": datetime.now().isoformat(),
        "data": datos
    }
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

def obtener_o_cachear(nombre: str, minutos: int, funcion_callback):
    cache = leer_cache_completa()
    info = cache.get(nombre)

    if info:
        try:
            timestamp = datetime.fromisoformat(info["timestamp"])
            if datetime.now() - timestamp < timedelta(minutes=minutos):
                return info["data"]
        except Exception:
            pass

    # Si no hay caché válido, se ejecuta y se guarda
    datos = funcion_callback()
    guardar_cache(nombre, datos)
    return datos
