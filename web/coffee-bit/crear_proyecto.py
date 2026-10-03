from pathlib import Path


# Carpeta donde está ubicado este script
BASE_DIR = Path(__file__).resolve().parent

# Directorio raíz del proyecto
PROJECT_DIR = BASE_DIR / "coffee-bit"


# Directorios que se deben crear
DIRECTORIES = [
    PROJECT_DIR,
    PROJECT_DIR / "data",
    PROJECT_DIR / "templates",
    PROJECT_DIR / "static",
    PROJECT_DIR / "static" / "css",
    PROJECT_DIR / "static" / "js",
    PROJECT_DIR / "static" / "images",
    PROJECT_DIR / "static" / "other",
]


# Archivos vacíos que se deben crear
FILES = [
    PROJECT_DIR / "app.py",
    PROJECT_DIR / "config.py",
    PROJECT_DIR / "requirements.txt",
    PROJECT_DIR / "README.md",

    PROJECT_DIR / "data" / "products.py",

    PROJECT_DIR / "templates" / "base.html",
    PROJECT_DIR / "templates" / "index.html",
    PROJECT_DIR / "templates" / "product.html",
    PROJECT_DIR / "templates" / "cart.html",
    PROJECT_DIR / "templates" / "checkout.html",

    PROJECT_DIR / "static" / "css" / "style.css",
    PROJECT_DIR / "static" / "js" / "main.js",

    PROJECT_DIR / "static" / "other" / ".gitkeep",
]


def create_project():
    print("Creando proyecto...")
    print(f"Ubicación: {PROJECT_DIR}")
    print()

    # Crear carpetas
    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"[CARPETA] {directory}")

    # Crear archivos vacíos
    for file in FILES:
        file.touch(exist_ok=True)
        print(f"[ARCHIVO]  {file}")

    print()
    print("===================================")
    print("Proyecto creado correctamente.")
    print("===================================")
    print()
    print(f"Ubicación del proyecto:")
    print(PROJECT_DIR)


if __name__ == "__main__":
    create_project()
