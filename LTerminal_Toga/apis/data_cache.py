import os
import json
from datetime import datetime, timedelta

CACHE_PATH = os.path.join(os.path.dirname(__file__), "data_cache.json")

def leer_cache_completa():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_cache(nombre, datos):
    cache = leer_cache_completa()
    cache[nombre] = {
        "timestamp": datetime.now().isoformat(),
        "data": datos
    }
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def obtener_cache(nombre):
    cache = leer_cache_completa()
    if nombre in cache:
        return cache[nombre]["data"]
    return None

def cache_expirada(nombre, minutos=10):
    cache = leer_cache_completa()
    if nombre not in cache:
        return True
    ts = datetime.fromisoformat(cache[nombre]["timestamp"])
    return datetime.now() - ts > timedelta(minutes=minutos)

def obtener_o_cachear(nombre, minutos, funcion_callback):
    if not cache_expirada(nombre, minutos):
        return obtener_cache(nombre)
    else:
        datos = funcion_callback()
        guardar_cache(nombre, datos)
        return datos
