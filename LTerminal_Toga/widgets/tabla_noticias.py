import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from apis.noticias import obtener_noticias
from resources.styles import contenedor_seccion, titulo_label, tabla_noticias, boton_base

class NoticiasPanel(toga.Box):
    def __init__(self):
        super().__init__(style=contenedor_seccion)

        self.label = toga.Label(
            "📰 Noticias Económicas",
            style=titulo_label
        )
        self.add(self.label)

        self.tabla = toga.Table(
            headings=["Región", "Fuente", "Título"],
            style=tabla_noticias
        )


        self.add(self.tabla)

        self.boton = toga.Button(
            "🔄 Actualizar noticias",
            on_press=self.actualizar,
            style=boton_base
        )
        self.add(self.boton)

        # Cargar noticias al iniciar
        self.actualizar(None)

    def actualizar(self, widget):
        self.tabla.data.clear()
        noticias = obtener_noticias()
        for n in noticias:
            self.tabla.data.append((n["region"], n["fuente"], n["titulo"]))
