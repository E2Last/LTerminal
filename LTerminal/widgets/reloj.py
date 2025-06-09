from datetime import datetime
from pytz import timezone

def generar_hora_multizona():
    zonas = {
        "🇦🇷 AR": "America/Argentina/Buenos_Aires",
        "🇺🇸 NY": "America/New_York",
        "🇪🇺 EU": "Europe/Berlin",
        "🇯🇵 JP": "Asia/Tokyo"
    }

    ahora = []
    for etiqueta, zona in zonas.items():
        tz = timezone(zona)
        hora = datetime.now(tz).strftime("%H:%M:%S")
        ahora.append(f"{etiqueta}: {hora}")

    return " | ".join(ahora)
