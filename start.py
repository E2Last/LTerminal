import logging
import traceback
import ctypes

logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    from LTerminal.app_main import TerminalEconomicaApp
    TerminalEconomicaApp().run()

except Exception as e:
    logging.error("❌ Error al iniciar la app:")
    logging.error(traceback.format_exc())

    # Mostrar una ventana emergente si falla
    ctypes.windll.user32.MessageBoxW(
        0,
        "Ocurrió un error al iniciar la aplicación.\nRevisá el archivo 'error.log'.",
        "LTerminal - Error crítico",
        0x10  # MB_ICONERROR
    )
