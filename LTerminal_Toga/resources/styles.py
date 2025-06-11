from toga.style import Pack
from toga.style.pack import COLUMN, CENTER

contenedor_seccion = Pack(
    direction=COLUMN,
    background_color="black",
    margin=10
)

# Fondo general negro
app_fondo = Pack(direction=COLUMN, background_color="black", margin=10)

# Título general
titulo_label = Pack(font_size=20, color="white", text_align=CENTER, margin_bottom=10)

# Tabla de cotizaciones
tabla_precios = Pack(
    flex=1,
    margin=5,
    background_color="black",
    color="lime",  # texto verde
)

# Tabla de noticias
tabla_noticias = Pack(
    flex=2,
    margin=5,
    background_color="black",
    color="yellow",
)

# Botones
boton_base = Pack(margin=5, background_color="#222", color="white")
