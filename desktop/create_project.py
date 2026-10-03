from pathlib import Path
import json


PROJECT_NAME = "duck-hunt"

FILES = [
    "run.py",
    "requirements.txt",
    "README.md",

    "src/__init__.py",
    "src/app.py",
    "src/game.py",
    "src/config.py",

    "src/entities/__init__.py",
    "src/entities/duck.py",
    "src/entities/dog.py",
    "src/entities/bullet.py",

    "src/screens/__init__.py",
    "src/screens/menu.py",
    "src/screens/game_screen.py",
    "src/screens/round_complete.py",
    "src/screens/game_over.py",

    "src/ui/__init__.py",
    "src/ui/hud.py",
    "src/ui/crosshair.py",

    "src/audio/__init__.py",
    "src/audio/sound_manager.py",

    "src/system/__init__.py",
    "src/system/app_indicator.py",
    "src/system/desktop_entry.py",

    "assets/images/background.png",
    "assets/images/duck.png",
    "assets/images/duck_flap_1.png",
    "assets/images/duck_flap_2.png",
    "assets/images/duck_dead.png",
    "assets/images/dog.png",
    "assets/images/crosshair.png",
    "assets/images/logo.png",

    "assets/sounds/shot.wav",
    "assets/sounds/duck_hit.wav",
    "assets/sounds/duck_fly.wav",
    "assets/sounds/dog_laugh.wav",
    "assets/sounds/round_complete.wav",

    "assets/fonts/game_font.ttf",

    "data/high_scores.json",

    "packaging/duck-hunt.desktop",
    "packaging/duck-hunt.svg",
    "packaging/duck-hunt.appdata.xml",

    "tests/test_duck.py",
    "tests/test_game.py",
]


def create_project():
    root = Path(PROJECT_NAME)

    # Crear directorio raíz
    root.mkdir(parents=True, exist_ok=True)

    for file_path in FILES:
        path = root / file_path

        # Crear directorios padre
        path.parent.mkdir(parents=True, exist_ok=True)

        # Crear archivo si no existe
        if not path.exists():
            if path.name == "high_scores.json":
                path.write_text(
                    json.dumps({"high_scores": []}, indent=4) + "\n",
                    encoding="utf-8"
                )
            else:
                path.touch()

    print(f"Proyecto creado correctamente en: {root.resolve()}")


if __name__ == "__main__":
    create_project()
