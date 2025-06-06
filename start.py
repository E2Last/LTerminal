import logging
import traceback
import time

# Configurar logging global desde el primer momento
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    from LTerminal import TerminalEconomicaApp
    TerminalEconomicaApp().run()

except Exception as e:
    logging.error("Error fatal al iniciar la aplicación:")
    logging.error(traceback.format_exc())

    print("❌ Error al iniciar la aplicación. Ver error.log para más detalles.")
    input("\nPresioná Enter para cerrar...")
