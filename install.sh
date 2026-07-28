#!/usr/bin/env bash
# doomfetch installer: locate a WAD, render the sprites, install the CLI.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREFIX="${PREFIX:-$HOME/.local}"
DATA_DIR="${DOOMFETCH_DIR:-$HOME/.local/share/doomfetch}"
BIN_DIR="$PREFIX/bin"

FREEDOOM_VERSION="0.13.0"
FREEDOOM_URL="https://github.com/freedoom/freedoom/releases/download/v${FREEDOOM_VERSION}/freedoom-${FREEDOOM_VERSION}.zip"
SHAREWARE_URL="https://github.com/Akbar30Bill/DOOM_wads/raw/master/doom1.wad"

WAD=""
MODE="auto"
BUILD_ARGS=()

info() { printf '\033[1;32m::\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m::\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31m::\033[0m %s\n' "$*" >&2; exit 1; }

usage() {
    cat <<'EOF'
Install doomfetch

  ./install.sh                     look for an IWAD automatically
  ./install.sh --wad PATH          use a specific IWAD
  ./install.sh --freedoom          download Freedoom (freely licensed)
  ./install.sh --shareware         download the Doom 1 shareware WAD
  ./install.sh --uninstall         remove everything again

Options:
  --max-rows N     maximum sprite height in terminal rows (default 24)
  --max-cols N     maximum width in columns (default 44)
  --max-scale N    maximum upscale factor for small sprites (default 3.0)
  --prefix PATH    install prefix for the CLI (default ~/.local)

doomfetch ships no artwork. Sprites are extracted locally from an IWAD that
you already own or that this script downloads for you.
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --wad)       WAD="${2:?--wad needs a path}"; MODE="explicit"; shift 2 ;;
        --freedoom)  MODE="freedoom"; shift ;;
        --shareware) MODE="shareware"; shift ;;
        --uninstall) MODE="uninstall"; shift ;;
        --prefix)    PREFIX="${2:?--prefix needs a path}"; BIN_DIR="$PREFIX/bin"; shift 2 ;;
        --max-rows)  BUILD_ARGS+=(--max-rows "${2:?}"); shift 2 ;;
        --max-cols)  BUILD_ARGS+=(--max-cols "${2:?}"); shift 2 ;;
        --max-scale) BUILD_ARGS+=(--max-scale "${2:?}"); shift 2 ;;
        -h|--help)   usage; exit 0 ;;
        *)           die "unknown option: $1 (try --help)" ;;
    esac
done

if [[ "$MODE" == "uninstall" ]]; then
    rm -f  "$BIN_DIR/doomfetch"
    rm -rf "$DATA_DIR"
    info "doomfetch removed. Reset your fastfetch config yourself if needed."
    exit 0
fi

# --- prerequisites --------------------------------------------------------
command -v python3 >/dev/null || die "python3 is required but not installed."
python3 -c 'import PIL' 2>/dev/null || die \
"Pillow is missing. Install it with:
    Arch          sudo pacman -S python-pillow
    Debian/Ubuntu sudo apt install python3-pil
    Fedora        sudo dnf install python3-pillow
    macOS/pip     pip install --user Pillow"

# --- obtain a WAD ---------------------------------------------------------
CACHE="$DATA_DIR/wads"

download() {  # url destination
    mkdir -p "$(dirname "$2")"
    if command -v curl >/dev/null; then
        curl -fL --progress-bar -o "$2" "$1"
    elif command -v wget >/dev/null; then
        wget -q --show-progress -O "$2" "$1"
    else
        die "curl or wget is required to download a WAD."
    fi
}

get_freedoom() {
    local zip="$CACHE/freedoom.zip"
    if [[ ! -f "$CACHE/freedoom2.wad" ]]; then
        command -v unzip >/dev/null || die "unzip is required for Freedoom."
        info "Downloading Freedoom $FREEDOOM_VERSION ..."
        download "$FREEDOOM_URL" "$zip"
        unzip -jo "$zip" '*/freedoom1.wad' '*/freedoom2.wad' -d "$CACHE" >/dev/null
        rm -f "$zip"
    fi
    WAD="$CACHE/freedoom2.wad"
}

get_shareware() {
    if [[ ! -f "$CACHE/doom1.wad" ]]; then
        info "Downloading the Doom 1 shareware WAD ..."
        download "$SHAREWARE_URL" "$CACHE/doom1.wad"
    fi
    WAD="$CACHE/doom1.wad"
}

find_wad() {
    local dirs=(
        "${DOOMWADDIR:-}"
        "$HOME/.local/share/games/doom" "$HOME/.doom" "$HOME/doom"
        "/usr/share/games/doom" "/usr/share/doom" "/usr/local/share/games/doom"
        "$HOME/.steam/steam/steamapps/common/Ultimate Doom/base"
        "$HOME/.steam/steam/steamapps/common/Doom 2/base"
        "$HOME/.local/share/Steam/steamapps/common/Ultimate Doom/base"
        "$HOME/.local/share/Steam/steamapps/common/Doom 2/base"
        "$HOME/GOG Games/DOOM  Ultimate/data"
        "$HOME/GOG Games/DOOM II/data"
        "$CACHE"
    )
    # Order matters: richest IWAD first.
    local names=(DOOM2.WAD doom2.wad DOOM.WAD doom.wad
                 freedoom2.wad freedoom1.wad
                 TNT.WAD tnt.wad PLUTONIA.WAD plutonia.wad
                 DOOM1.WAD doom1.wad)
    for name in "${names[@]}"; do
        for dir in "${dirs[@]}"; do
            [[ -n "$dir" && -f "$dir/$name" ]] && { WAD="$dir/$name"; return 0; }
        done
    done
    return 1
}

case "$MODE" in
    explicit)  [[ -f "$WAD" ]] || die "WAD not found: $WAD" ;;
    freedoom)  get_freedoom ;;
    shareware) get_shareware ;;
    auto)
        if find_wad; then
            info "Found IWAD: $WAD"
        else
            warn "No IWAD found."
            echo
            echo "  Pick one of:"
            echo "    ./install.sh --wad /path/to/DOOM2.WAD   use your own copy"
            echo "    ./install.sh --freedoom                 download Freedoom (free)"
            echo "    ./install.sh --shareware                download Doom 1 shareware"
            echo
            die "No WAD, no sprites."
        fi
        ;;
esac

# --- build and install ----------------------------------------------------
info "Rendering sprites from $(basename "$WAD") ..."
python3 "$REPO/build/build.py" --wad "$WAD" --out "$DATA_DIR" "${BUILD_ARGS[@]}"

mkdir -p "$BIN_DIR"
install -m 755 "$REPO/bin/doomfetch" "$BIN_DIR/doomfetch"
info "CLI installed: $BIN_DIR/doomfetch"

case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *) warn "$BIN_DIR is not in your PATH. Add this to your shell config:"
       echo "    export PATH=\"\$PATH:$BIN_DIR\"" ;;
esac

echo
info "Done. Try it:"
echo "    doomfetch -r"
echo "    doomfetch --list"
