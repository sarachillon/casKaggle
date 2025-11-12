
from rich.console import Console # Podem ignorar aquest warning, funciona be igualment
from rich.theme import Theme
from rich.table import Table

# Definimos colores personalizados
custom_theme = Theme({
    "info": "bold cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "title": "bold magenta underline"
})

# Creamos la consola global
console = Console(theme=custom_theme)
