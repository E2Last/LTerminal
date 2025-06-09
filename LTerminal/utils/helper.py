import sys
import os

def ruta_absoluta_recurso(nombre_archivo):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, nombre_archivo)
    return os.path.join(os.path.abspath("."), nombre_archivo)


def truncar(texto, max_len=120):
    texto = str(texto or "")
    return texto if len(texto) <= max_len else texto[:max_len - 3].rstrip() + "..."
