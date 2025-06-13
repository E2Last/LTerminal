import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga import Label, Box, ScrollContainer
from apis.noticias import obtener_noticias
from resources.styles import contenedor_seccion, titulo_label, boton_base

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
        noticias = obtener_noticias()
        regiones = []
        fuentes = []
        titulos = []

        for n in noticias:
            regiones.append(n["region"])
            fuentes.append(n["fuente"])
            titulos.append(n["titulo"])

        self.region_label.text = "\n".join(regiones)
        self.fuente_label.text = "\n".join(fuentes)
        self.titulo_label.text = "\n".join(titulos)
