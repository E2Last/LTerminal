import logging
import traceback
import os
from datetime import datetime
from pytz import timezone
import pytz
import json
import requests
import sys

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Vertical, Horizontal
from textual.scroll_view import ScrollView

#  Definir ruta segura en el escritorio del usuario
log_path = os.path.join(os.path.expanduser("~"), "Desktop", "LTerminal_error.log")

#  INICIALIZAR LOG INMEDIATO
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,  # ⚠️ TEMPORAL para ver más
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    def ruta_absoluta_recurso(nombre_archivo):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, nombre_archivo)
        return os.path.join(os.path.abspath("."), nombre_archivo)

    def truncar(texto, max_len=120):
        texto = str(texto or "")
        return texto if len(texto) <= max_len else texto[:max_len - 3].rstrip() + "..."


    class PrecioPanel(Static):
        def update_content(self, precios):
            contenido = "\n".join(
                f"[bold cyan]{k}:[/bold cyan] [green]{v}[/green]" for k, v in precios.items()
            )
            self.update(contenido)

    class TerminalEconomicaApp(App):
        CSS_PATH = ruta_absoluta_recurso("styles.css")

        def compose(self) -> ComposeResult:
            self.clock_widget = Static("Cargando hora...", id="clock")  # ✅ Definición
            self.noticias_widget = ScrollView(id="noticias-scroll")
            self.scroll_static = Static("Cargando noticias...")

            yield self.clock_widget
            yield Header()

            with Horizontal():
                yield self.noticias_widget
                self.precios_widget = PrecioPanel("Cargando precios...")
                yield self.precios_widget

            yield Button("Refrescar", id="refrescar")
            yield Footer()
            

        def on_mount(self):
            self.noticias_widget.mount(self.scroll_static)
            self.actualizar_datos()
            self.set_interval(1, self.actualizar_reloj)


        def on_button_pressed(self, event):
            if event.button.id == "refrescar":
                self.actualizar_datos()
        
        
        def actualizar_datos(self):
            precios = self.obtener_precios()
            noticias = self.obtener_noticias_region()

            # Agrupar por región
            agrupadas = {}
            for noticia in noticias:
                region = noticia.get("region", "🌍 Otros")
                if region not in agrupadas:
                    agrupadas[region] = []
                agrupadas[region].append(noticia)

            contenido = ""
            for region, lista in agrupadas.items():
                contenido += f"[bold yellow]━━━━━━━━━━━━ {region} ━━━━━━━━━━━━[/bold yellow]\n"
                for n in lista:
                    titulo = truncar(n.get("title", "Sin título"), 90)
                    descripcion = truncar(n.get("description", ""), 120)
                    fuente = n.get("source", {}).get("name", "")
                    contenido += f"📌 {titulo}\n🔹 [green]{fuente}[/green]: [italic]{descripcion}[/italic]\n\n"

            self.scroll_static.update(contenido)
            self.precios_widget.update_content(precios)

        
        def obtener_noticias(self):
            with open(ruta_absoluta_recurso("config.json"), encoding="utf-8") as f:
                config = json.load(f)
            api_key = config["news_api_key"]
            url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={api_key}"
            res = requests.get(url)
            noticias = res.json().get("articles", [])
            print("Cantidad de noticias:", len(noticias))
            json_data = res.json()
            logging.info("Respuesta NewsAPI: %s", json_data)
            return json_data.get("articles", [])
        
        def obtener_noticias_region(self):
            with open(ruta_absoluta_recurso("config.json"), encoding="utf-8") as f:
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
                        n["region"] = region  # 👈 Etiqueta visible
                        noticias_total.append(n)
                except Exception as e:
                    logging.error(f"Error obteniendo noticias para {region}: {e}")

            return noticias_total


            
        def obtener_precios(self):
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

        def actualizar_reloj(self):
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

            hora_final = " | ".join(ahora)
            print("🕓", hora_final)  # 👈 Te lo muestra por consola
            self.clock_widget.update(hora_final)



    if __name__ == "__main__":
        TerminalEconomicaApp().run()

except Exception:
    logging.error("❌ Error crítico al iniciar LTerminal")
    logging.error(traceback.format_exc())
    print("❌ Error fatal. Revisá 'error.log' para más información.")
    input("Presioná Enter para cerrar...")
