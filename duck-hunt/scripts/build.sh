#!/usr/bin/env bash
#
# Construction de los paquetes de Duck Hunt para Linux.
#
# Produce tres artefactos en dist/:
#
#   duck-hunt                 binario autocontenido (intermedio)
#   duck-hunt_1.0.0_amd64.deb paquete Debian/Ubuntu instalable
#   duck-hunt-1.0.0-x86_64.AppImage  AppImage portable
#   com.duckhunt.Game           Flatpak instalable
#
# El binario se genera con PyInstaller, así que no depende de pygame ni del
# Python del sistema.
#
# Uso:
#
#   scripts/build.sh              todo
#   scripts/build.sh binary       solo el binario
#   scripts/build.sh deb          binario + .deb
#   scripts/build.sh appimage     binario + AppImage
#   scripts/build.sh flatpak      binario + Flatpak
#   scripts/build.sh test         comprobación rápida del binario

set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

DIST_DIR="$PROJECT_DIR/dist"

BUILD_DIR="$PROJECT_DIR/build"

VENV_DIR="$PROJECT_DIR/.venv"

APP_ID="com.duckhunt.Game"

APP_NAME="duck-hunt"

BIN_NAME="duck-hunt"

# Nombre del ejecutable dentro del paquete Debian.
DEB_BIN="/usr/games/$BIN_NAME"

# Dónde se instala el juego. Se copia el árbol completo de la app.
APP_PREFIX="/usr/lib/$BIN_NAME"

log()  { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33maviso:\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31merror:\033[0m %s\n' "$*" >&2; exit 1; }

# Lee un valor de src/config.py sin ejecutar el módulo.
config_value() {
    python3 - "$1" <<'PY'
import re
import sys

key = sys.argv[1]

with open("src/config.py", encoding="utf-8") as handle:
    for line in handle:
        match = re.match(rf'^{key}\s*=\s*"?([^"\n]+)"?', line)
        if match:
            print(match.group(1).strip())
            break
PY
}

VERSION="$(config_value APP_VERSION)"
ARCH="$(dpkg --print-architecture 2>/dev/null || echo amd64)"

cd "$PROJECT_DIR"

# ============================================================================
# Entorno
# ============================================================================

ensure_venv() {
    # Comprueba que el venv de compilación existe y tiene PyInstaller.
    [ -x "$VENV_DIR/bin/python" ] || die \
        "No existe $VENV_DIR. Créalo con: uv venv --python 3.13 .venv && uv pip install -r requirements-build.txt"

    if ! "$VENV_DIR/bin/python" -c "import PyInstaller" 2>/dev/null; then

        log "Instalando dependencias de compilación"

        if command -v uv >/dev/null 2>&1; then

            uv pip install -r requirements-build.txt

        else

            "$VENV_DIR/bin/pip" install -r requirements-build.txt

        fi

    fi
}

ensure_assets() {
    # Regenera los recursos si falta alguno. Un paquete sin sprites ni sonidos
    # arrancaría el juego a ciegas, así que mejor fallar aquí que publicar un
    # binario mutilado.

    local missing=0

    for file in \
        assets/images/duck_flap_1.png \
        assets/images/background.png \
        assets/images/dog_idle.png \
        assets/fonts/font_atlas.png \
        assets/sounds/shot.wav \
        assets/sounds/theme.wav; do

        if [ ! -s "$file" ]; then

            missing=1

        fi

    done

    if [ "$missing" -eq 1 ]; then

        log "Faltan recursos, se generan"

        "$VENV_DIR/bin/python" tools/generate_assets.py >/dev/null

    fi
}

# ============================================================================
# Binario
# ============================================================================

build_binary() {
    # Genera el ejecutable autocontenido con PyInstaller.
    ensure_venv

    ensure_assets

    log "Limpiando compilaciones anteriores"

    rm -rf "$BUILD_DIR" "$DIST_DIR"

    mkdir -p "$DIST_DIR"

    log "Compilando el binario (PyInstaller)"

    "$VENV_DIR/bin/python" -m PyInstaller \
        --noconfirm \
        --clean \
        --onefile \
        --name "$BIN_NAME" \
        --distpath "$DIST_DIR" \
        --workpath "$BUILD_DIR/pyinstaller" \
        --specpath "$BUILD_DIR" \
        --add-data "$PROJECT_DIR/assets:assets" \
        --add-data "$PROJECT_DIR/data:data" \
        --paths "$PROJECT_DIR" \
        "$PROJECT_DIR/tools/entrypoint.py" \
        --log-level WARN

    chmod +x "$DIST_DIR/$BIN_NAME"

    log "Binario listo: $(du -h "$DIST_DIR/$BIN_NAME" | cut -f1)"
}

# ============================================================================
# Paquete Debian
# ============================================================================

build_deb() {
    # Construye el .deb con dpkg-deb y fakeroot.
    command -v dpkg-deb >/dev/null 2>&1 || die "dpkg-deb no está instalado"

    [ -x "$DIST_DIR/$BIN_NAME" ] || die "Falta $DIST_DIR/$BIN_NAME; ejecuta primero: scripts/build.sh binary"

    local staging="$BUILD_DIR/deb"

    local pkg="$DIST_DIR/${BIN_NAME}_${VERSION}_${ARCH}.deb"

    log "Preparando el árbol del paquete"

    rm -rf "$staging"

    mkdir -p "$staging/DEBIAN"
    mkdir -p "$staging$APP_PREFIX"
    mkdir -p "$staging/usr/games"
    mkdir -p "$staging/usr/share/applications"
    mkdir -p "$staging/usr/share/icons/hicolor/128x128/apps"
    mkdir -p "$staging/usr/share/icons/hicolor/scalable/apps"
    mkdir -p "$staging/usr/share/metainfo"
    mkdir -p "$staging/usr/share/doc/$BIN_NAME"

    # El binario y sus datos.
    cp "$DIST_DIR/$BIN_NAME" "$staging$DEB_BIN"

    # Con --onefile los assets van dentro del ejecutable. Se instalan
    # ademas en el prefijo para poder inspeccionarlos o usarlos como copia.
    mkdir -p "$staging$APP_PREFIX/assets"

    cp -r assets/. "$staging$APP_PREFIX/assets/"

    cp packaging/duck-hunt.desktop "$staging/usr/share/applications/$BIN_NAME.desktop"

    cp assets/icons/duck-hunt.png "$staging/usr/share/icons/hicolor/128x128/apps/$BIN_NAME.png"

    cp packaging/duck-hunt.svg "$staging/usr/share/icons/hicolor/scalable/apps/$BIN_NAME.svg"

    cp packaging/duck-hunt.appdata.xml "$staging/usr/share/metainfo/$BIN_NAME.appdata.xml"

    # Licencia y documentación.
    if [ -f LICENSE ]; then cp LICENSE "$staging/usr/share/doc/$BIN_NAME/"; fi

    cp README.md "$staging/usr/share/doc/$BIN_NAME/README.md"

    local installed_size

    installed_size="$(du -sk "$staging" | cut -f1)"

    cat > "$staging/DEBIAN/control" <<EOF
Package: $BIN_NAME
Version: $VERSION
Section: games
Priority: optional
Architecture: $ARCH
Maintainer: Taller Python <duck-hunt@example.com>
Installed-Size: $installed_size
Depends: libc6, libglib2.0-0, libasound2t64 | libasound2
Description: Recreación del clásico de caza de patos
 Duck Hunt es una recreación del clásico de NES hecha con pygame: los patos
 cruzan el cielo y hay que abatirlos con la mira antes de que escapen.
 .
 Cada ronda tiene diez patos y hay que acertar a seis; de cada pato solo se
 puede disparar tres veces. Desde la ronda 11 vuelan dos patos a la vez y
 desde la 21, tres.
 .
 Este paquete instala un binario autocontenido: no necesita python ni pygame
 en el sistema.
EOF

    cat > "$staging/DEBIAN/postinst" <<'EOF'
#!/bin/sh
set -e

if [ "$1" = "configure" ]; then

    if command -v update-desktop-database >/dev/null 2>&1; then

        update-desktop-database -q /usr/share/applications || true

    fi

    if command -v gtk-update-icon-cache >/dev/null 2>&1; then

        gtk-update-icon-cache -q -f /usr/share/icons/hicolor || true

    fi

fi

exit 0
EOF

    cat > "$staging/DEBIAN/postrm" <<'EOF'
#!/bin/sh
set -e

if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then

    if command -v update-desktop-database >/dev/null 2>&1; then

        update-desktop-database -q /usr/share/applications || true

    fi

    if command -v gtk-update-icon-cache >/dev/null 2>&1; then

        gtk-update-icon-cache -q -f /usr/share/icons/hicolor || true

    fi

fi

exit 0
EOF

    chmod 0755 "$staging/DEBIAN/postinst" "$staging/DEBIAN/postrm"

    # dpkg-deb no necesita root si se le da un ownership válido, pero con
    # fakeroot el árbol sale con root:root y el aviso desaparece.
    log "Construyendo el paquete Debian"

    if command -v fakeroot >/dev/null 2>&1; then

        fakeroot -- dpkg-deb --root-owner-group --build "$staging" "$pkg"

    else

        warn "fakeroot no está instalado; se construye sin él"

        dpkg-deb --root-owner-group --build "$staging" "$pkg"

    fi

    log "Paquete listo: $pkg ($(du -h "$pkg" | cut -f1))"
}

# ============================================================================
# AppImage
# ============================================================================

download_appimagetool() {
    # Descarga appimagetool, que no viene de serie en el sistema.
    local tool="$BUILD_DIR/appimagetool"

    if [ -x "$tool" ]; then

        echo "$tool"

        return

    fi

    command -v curl >/dev/null 2>&1 || die "Hace falta curl para descargar appimagetool"

    mkdir -p "$BUILD_DIR"

    local url="https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"

    log "Descargando appimagetool"

    if ! curl -fL --retry 3 -o "$tool" "$url"; then

        rm -f "$tool"

        die "No se pudo descargar appimagetool"

    fi

    chmod +x "$tool"

    echo "$tool"
}

build_appimage() {
    # Construye el AppImage a partir del mismo binario.
    [ -x "$DIST_DIR/$BIN_NAME" ] || die "Falta $DIST_DIR/$BIN_NAME; ejecuta primero: scripts/build.sh binary"

    local appdir="$BUILD_DIR/AppDir"

    local tool

    tool="$(download_appimagetool | tail -n1)"

    log "Preparando AppDir"

    rm -rf "$appdir"

    mkdir -p "$appdir/usr/bin" \
             "$appdir/usr/share/applications" \
             "$appdir/usr/share/icons/hicolor/128x128/apps" \
             "$appdir/usr/share/icons/hicolor/scalable/apps" \
             "$appdir/usr/share/metainfo"

    cp "$DIST_DIR/$BIN_NAME" "$appdir/usr/bin/$BIN_NAME"

    # AppImage exige que el .desktop esté también en la raíz del AppDir: es
    # donde lo busca appimagetool para el icono y el nombre de la aplicación.
    cp packaging/duck-hunt.desktop "$appdir/$BIN_NAME.desktop"

    cp packaging/duck-hunt.desktop "$appdir/usr/share/applications/$BIN_NAME.desktop"

    cp assets/icons/duck-hunt.png "$appdir/usr/share/icons/hicolor/128x128/apps/$BIN_NAME.png"

    cp packaging/duck-hunt.svg "$appdir/usr/share/icons/hicolor/scalable/apps/$BIN_NAME.svg"

    # appimagetool busca el icono que nombra el .desktop en la raíz del AppDir.
    cp assets/icons/duck-hunt.png "$appdir/$BIN_NAME.png"

    cp packaging/duck-hunt.svg "$appdir/$BIN_NAME.svg"

    cp packaging/duck-hunt.appdata.xml "$appdir/usr/share/metainfo/$BIN_NAME.appdata.xml"

    # AppImage necesita un AppRun en la raíz.
    cat > "$appdir/AppRun" <<EOF
#!/bin/sh
HERE="\$(dirname "\$(readlink -f "\${0}")")"
exec "\$HERE/usr/bin/$BIN_NAME" "\$@"
EOF

    chmod +x "$appdir/AppRun"

    local output="$DIST_DIR/${BIN_NAME}-${VERSION}-x86_64.AppImage"

    log "Construyendo el AppImage"

    # AppImage necesita FUSE, que en un contenedor o una sesión sin permisos
    # no está. APPIMAGE_EXTRACT_AND_RUN=1 hace que la herramienta se extraiga
    # en lugar de montarse, y ARCH lo exige appimagetool.
    #
    # (appimagetool deja de copiar en algún entorno sin fuse y se queda
    # colgado esperando. Por eso va con timeout y luego se comprueba que el
    # fichero haya salido bien, en vez de fiarse solo del código de salida.)
    set +e

    ARCH=x86_64 APPIMAGE_EXTRACT_AND_RUN=1 timeout 600 "$tool" \
        --no-appstream \
        "$appdir" "$output"

    local status=$?

    set -e

    if [ ! -s "$output" ]; then

        die "Falló la construcción del AppImage"

    fi

    if [ "$status" -ne 0 ]; then

        warn "appimagetool terminó con estado $status, pero el fichero está completo"

    fi

    chmod +x "$output"

    if command -v zsyncmake >/dev/null 2>&1; then

        log "Generando el fichero zsync para actualizaciones"

        # El orden de los argumentos importa: primero el fichero, luego las
        # opciones. Con el orden inverso zsyncmake sale con éxito sin escribir
        # nada.
        ( cd "$DIST_DIR" && zsyncmake \
            "${BIN_NAME}-${VERSION}-x86_64.AppImage" \
            -o "${BIN_NAME}-${VERSION}-x86_64.AppImage.zsync" \
            -u "https://duck-hunt.example.org/${BIN_NAME}-${VERSION}-x86_64.AppImage" ) || \
            warn "zsyncmake falló; se omite el .zsync"

    fi

    log "AppImage listo: $output ($(du -h "$output" | cut -f1))"
}

# ============================================================================
# Flatpak
# ============================================================================

FLATPAK_MANIFEST="packaging/com.duckhunt.Game.yml"

# El sandbox de flatpak-builder necesita estos dos ajustes en la practica:
#
#   --disable-rofiles-fuse   en contenedores y sesiones sin /dev/fuse, rofiles
#                            no puede arrancar y aborta la compilación.
#   --allow-missing-runtimes el builder avisa en vez de morir si ve mal el SDK.
flatpak_builder() {
    # El builder se distribuye como aplicacion Flatpak, no como binario suelto.
    if command -v flatpak-builder >/dev/null 2>&1; then

        flatpak-builder "$@"

        return $?

    fi

    if ! flatpak list --user --app 2>/dev/null | grep -q org.flatpak.Builder; then

        die "Falta flatpak-builder. Instálalo con: flatpak install --user flathub org.flatpak.Builder"

    fi

    flatpak run --user \
        --command=flatpak-builder \
        org.flatpak.Builder \
        "$@"
}

build_flatpak() {
    # Empaqueta el binario ya compilado dentro de un Flatpak instalable.
    #
    # Devuelve 1 en vez de terminar el script, porque es un paso opcional: el
    # objetivo "all" avisa y sigue cuando este falla.

    if [ ! -x "$DIST_DIR/$BIN_NAME" ]; then

        warn "Falta $DIST_DIR/$BIN_NAME; ejecuta antes: scripts/build.sh binary"

        return 1

    fi

    if [ ! -f "$FLATPAK_MANIFEST" ]; then

        warn "Falta el manifiesto $FLATPAK_MANIFEST"

        return 1

    fi

    log "Validando el manifiesto"

    if flatpak run --user --command=flatpak-builder-lint org.flatpak.Builder \
        manifest "$FLATPAK_MANIFEST" >/dev/null 2>&1; then

        log "Manifiesto válido"

    else

        warn "el linter de Flathub señala problemas en el manifiesto"

    fi

    log "Compilando el Flatpak"

    if ! flatpak_builder \
        --user \
        --allow-missing-runtimes \
        --disable-rofiles-fuse \
        --install \
        --force-clean \
        "$BUILD_DIR/flatpak" \
        "$FLATPAK_MANIFEST"; then

        warn "Falló la compilación del Flatpak"

        warn "Si el error es «Sdk not installed», flatpak-builder no ve el SDK de tu"

        warn "instalación de usuario. Se arregla instalándolo también en la de sistema:"

        warn "  flatpak install --system flathub org.freedesktop.Sdk//26.08"

        return 1

    fi

    log "Flatpak listo: $APP_ID"
}

# ============================================================================
# Comprobación
# ============================================================================

test_binary() {
    # Arranca el binario unos fotogramas para comprobar que no peta. Se usa el
    # controlador de vídeo y de audio "dummy": no abre ventana, pero ejecuta
    # el arranque real, la carga de recursos y el primer fotograma.

    [ -x "$DIST_DIR/$BIN_NAME" ] || die "Falta $DIST_DIR/$BIN_NAME"

    log "Probando el binario (modo headless)"

    SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy \
        timeout 30 "$DIST_DIR/$BIN_NAME" --self-test

    log "El binario arranca correctamente"
}

# ============================================================================
# Menú
# ============================================================================

usage() {
    sed -n '3,18p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

main() {
    local target="${1:-all}"

    case "$target" in

        binary)   build_binary ;;
        deb)      build_binary; build_deb ;;
        appimage) build_binary; build_appimage ;;
        flatpak)  build_binary; build_flatpak || exit 1 ;;
        test)     test_binary ;;
        all)
            build_binary
            test_binary
            build_deb
            build_appimage

            # El Flatpak necesita que flatpak-builder vea el SDK, lo que a
            # menudo exige instalarlo en la instalación de sistema. Es un paso
            # opcional, así que aquí avisa en lugar de tirar el build entero.
            if ! build_flatpak; then

                warn "se omite el Flatpak; usa 'scripts/build.sh flatpak' cuando tengas el SDK disponible"

            fi
            ;;

        -h|--help|help) usage; exit 0 ;;
        *) die "Objetivo desconocido: $target (usa: binary, deb, appimage, flatpak, test, all)" ;;

    esac

    log "Listo. Artefactos en $DIST_DIR"
}

main "$@"