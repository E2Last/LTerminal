import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga import Label, Box, ScrollContainer
from apis.noticias import obtener_noticias
from resources.styles import contenedor_seccion, titulo_label, boton_base
from apis.noticias_actuales import obtener_noticias_newsdataio  # Nueva fuente
from apis.noticias_gnews import obtener_noticias_gnews

class NoticiasPanel(toga.Box):
    def __init__(self):
        super().__init__(style=contenedor_seccion)

        self.label = toga.Label("📰 Noticias Económicas", style=titulo_label)
        self.add(self.label)

        # Labels por columna con color
        self.region_label = Label("", style=Pack(color="red", width=150))
        self.fuente_label = Label("", style=Pack(color="cyan", width=200))
        self.titulo_label = Label("", style=Pack(color="yellow", flex=1))
        
        # Contenedor interior con fondo negro real
        contenedor_scroll = Box(
            children=[
                Box(children=[self.region_label, self.fuente_label, self.titulo_label],
                    style=Pack(direction="row", background_color="black", margin=5))
            ],
            style=Pack(direction="column", background_color="black")
        )

        self.scroll_area = ScrollContainer(
            content=contenedor_scroll,
            style=Pack(height=250, margin=5)
        )

        self.add(self.scroll_area)

        # Botón de actualización
        self.boton = toga.Button("🔄 Actualizar noticias", on_press=self.actualizar, style=boton_base)
        self.add(self.boton)

        # Cargar al iniciar
        self.actualizar(None)

    def actualizar(self, widget):
        noticias = self.obtener_noticias_combinadas()

        regiones = []
        fuentes = []
        titulos = []

        for n in noticias:
            regiones.append(n.get("region", "AR"))
            fuentes.append(n.get("fuente", "News"))
            titulos.append(n.get("titulo", "Sin título"))

        self.region_label.text = "\n".join(regiones)
        self.fuente_label.text = "\n".join(fuentes)
        self.titulo_label.text = "\n".join(titulos)

    def obtener_noticias_combinadas(self):
        noticias_1 = obtener_noticias()
        noticias_2 = obtener_noticias_newsdataio()
        noticias_3 = obtener_noticias_gnews()

        # Etiquetas necesarias
        for n in noticias_2:
            n["region"] = "AR"
            n["fuente"] = "NewsData.io"

        todas = noticias_1 + noticias_2 + noticias_3
        todas.sort(key=lambda x: x.get("fecha", ""), reverse=True)
        return todas

