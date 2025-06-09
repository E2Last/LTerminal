import os
import json
import logging
from datetime import datetime, timedelta
import sys

if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

CACHE_PATH = os.path.join(BASE_PATH, "data_cache.json")

def leer_cache_completa():
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"❌ No se pudo leer data_cache.json: {e}")
    return {}


def guardar_cache(nombre: str, datos: dict):
    cache = leer_cache_completa()
    cache[nombre] = {
        "timestamp": datetime.now().isoformat(),
        "data": datos
    }
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"❌ No se pudo guardar data_cache.json: {e}")


def obtener_cache(nombre: str):
    cache = leer_cache_completa()
    if nombre in cache:
        return cache[nombre]["data"]
    return None


def cache_expirada(nombre: str, minutos: int = 60):
    cache = leer_cache_completa()
    if nombre not in cache:
        return True
    try:
        ts = datetime.fromisoformat(cache[nombre]["timestamp"])
        return datetime.now() - ts > timedelta(minutes=minutos)
    except Exception as e:
        logging.warning(f"⚠️ Error verificando expiración de {nombre}: {e}")
        return True


def obtener_o_cachear(nombre: str, minutos: int, funcion_callback):
    """
    Si el cache de 'nombre' no expiró, lo devuelve. Caso contrario, ejecuta 'funcion_callback()', lo guarda y lo devuelve.
    """
    if not cache_expirada(nombre, minutos):
        return obtener_cache(nombre)
    else:
        datos = funcion_callback()
        guardar_cache(nombre, datos)
        return datos
