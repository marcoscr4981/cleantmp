#!/usr/bin/env python3
"""CleanTMP

Aplicación que elimina archivos temporales o basura que aparecen en directorios
de usuario (como carpetas con música, fotos, etc.), y que no son archivos de 
sistema o logs formales, sino cosas como caché residual o metadatos inútiles.

Como root se añade a /usr/local/bin con el nombre cleantmp y se añade permiso
de ejecución (chmod +x /usr/local/bin/cleantmp)

Autor: Marcos Cuadrado Rey
Versión: v1.1
Licencia: MIT
"""
import argparse
import fnmatch
import os
import signal
import sys
from types import FrameType
from typing import Optional


colors = {
    'examined': '\033[0;32m',
    'eliminated': '\033[0;36m',
    'error': '\033[0;31m',
    'no_access': '\033[0;35m',
    'ignored': '\033[0;35m',
    'reset': '\033[0;37m',
}


stats = {
    "examined_files": 0,
    "examined_dirs": 0,
    "deleted_files": 0,
    "inaccessible_files": 0,
    "inaccessible_dirs": 0,
    "ignored_dirs": 0
}

TEMP_FILES = [
    ".DS_Store",
    "Thumbs.db",
    "ehthumbs.db",
    "Desktop.ini"
    ]

FILES_PATTERNS = [
    "._*",      # macOS metadata on non-HFS filesystems
    "*~",       # Backups (ej. archivo.txt~)
    ".*.sw?"    # Vim swap files (.file.swp, .file.swo, etc.)
]

DIRS_TO_IGNORE = [
    ".Spotlight-V100",
    ".fseventsd",
    ".Trash",
    ".Trashes",
    "$RECYCLE.BIN",
    "System Volume Information",
]


class CleanTmpException(Exception):
    """Excepción que se lanza cuando se produce un error en la gestión de carpetas o archivos.

    Attributes:
        message (str): Mensaje que se mostrará al usuario.
    """
    def __init__(self, message:Optional[str] = "Se ha producido un error al acceder a una carpeta o archivo") -> None:
        super().__init__(message)


def def_handler(sig:int, frame:Optional[FrameType]) -> None:
    """Función que maneja la señal SIGINT (Ctrl + C), permitiendo una terminación ordenada del programa.

    Args:
        sig (int): Señal recibida (en este caso, SIGINT).
        frame (FrameType): Marco de pila en el momento de la interrupción.
    """
    print(f"\n\n{colors['error']}[!] Saliendo...{colors['reset']}\n")
    sys.exit(1)


def config_argparse() -> argparse.Namespace:
    """Configura el parser de argumentos que define las opciones disponibles para el usuario.
    
    Returns:
        argparse.Namespace: Objeto con los argumentos de línea de comandos parseados:
            - path (str): Ruta a la carpeta a limpiar (por defecto, la actual).
            - recursive (bool): Si se deben eliminar archivos de forma recursiva.
            - version (str): Muestra la versión y termina el programa.
    """
    parser = argparse.ArgumentParser(description = 'CleanTMP - Elimina archivos temporales del sistema')
    parser.add_argument('-r', '--recursive', action='store_true', help='Elimina archivos temporales de forma recursiva en carpetas')
    parser.add_argument('path', nargs='?', default='.', type=str, help='Ruta a la carpeta a limpiar')
    parser.add_argument('-v', '--version', action='version', version=f'CleanTMP v1.1', help=f'Versión de CleanTMP')
    
    return parser.parse_args()


def is_temp_file(filename:str) -> bool:
    """Devuelve True si el archivo es considerado temporal.

    Args:
        filename (str): Nombre del archivo a comprobar.
    
    Returns:
        bool: True si es un archivo a eliminar, False en caso contrario.
    """
    if filename in TEMP_FILES:
        return True
    
    for pattern in FILES_PATTERNS:
        if fnmatch.fnmatch(filename, pattern):
            return True
        
    return False


def is_access(path:str) -> bool:
    """Si se tiene acceso a una carpeta o a un archivo.

    Args:
        path (str): Path con la ruta de la carpeta o archivo a comprobar.
    
    Returns:
        bool: True si se tiene acceso, False en caso contrario.
    """
    if os.path.isdir(path):
        return os.access(path, os.R_OK) and os.access(path, os.X_OK)
    else:
        return os.access(path, os.R_OK) and os.access(path, os.W_OK)


def report(recursive:bool) -> str:
    """Reporte con el resultado de la eliminación.
    
    Args:
        recursive (bool): Si la eliminación de archivos fue de forma recursiva.
        
    Returns:
        str: Reporte final.
    """
    lines = []

    if recursive:
        lines.append(f"\n{colors['examined']}Carpetas examinadas:{colors['reset']} {stats['examined_dirs']}")

        if stats['ignored_dirs'] > 0:
            lines.append(f"  {colors['ignored']}Carpetas ignoradas:{colors['reset']}  {stats['ignored_dirs']}")

        if stats['inaccessible_dirs'] > 0:
            lines.append(f"  {colors['no_access']}Carpetas sin acceso:{colors['reset']} {stats['inaccessible_dirs']}\n")

    lines.append(f"{colors['examined']}Archivos examinados:{colors['reset']} {stats['examined_files']}")
    lines.append(f"  {colors['eliminated']}Archivos eliminados:{colors['reset']} {stats['deleted_files']}")

    if stats['inaccessible_files'] > 0:
        lines.append(f"  {colors['no_access']}Archivos sin acceso:{colors['reset']} {stats['inaccessible_files']}")

    return "\n".join(lines)


def clean_temp_files(path:str, recursive:bool = False) -> None:
    """Función principal para la eliminación de archivos temporales.
    
    Args:
        path (str): Ruta a examinar.
        recursive (bool): Si la eliminación se hará de forma recursiva.

    Raises:
        CleanTmpException: Si se ha producido un error en el escaneo o eliminación de archivos temporales.
    """
    if not os.path.exists(path) or not os.path.isdir(path):
        raise CleanTmpException(f"No se ha podido obtener una ruta válida")
    
    stats['examined_dirs'] += 1

    if not is_access(path):
        if recursive:
            stats['inaccessible_dirs'] += 1
            return
        else:
            raise CleanTmpException(f"No se puede acceder a la carpeta {path}")

    file_list = os.listdir(path)
    
    if len(file_list) == 0 and not recursive:
        raise CleanTmpException(f"La carpeta está vacía: {path}")
    
    for file in file_list:
        filepath = os.path.join(path, file)
        if os.path.isdir(filepath):
            if recursive:
                if file in DIRS_TO_IGNORE:
                    stats['ignored_dirs'] += 1
                    continue

                clean_temp_files(filepath, recursive)

            continue

        stats['examined_files'] += 1
        
        if is_temp_file(file):
            if not is_access(filepath):
                print(f"{colors['error']}[!] No se ha podido eliminar el archivo:{colors['reset']} {filepath}")
                stats['inaccessible_files'] += 1
                continue
            
            try:
                os.remove(filepath)
                stats['deleted_files'] += 1
            except Exception:
                print(f"{colors['error']}[!] No se ha podido eliminar el archivo:{colors['reset']} {filepath}")
                stats['inaccessible_files'] += 1


def main() -> None:
    """Función principal que gestiona la ejecución completa del programa.
    
    Raises:
        CleanTmpException: Si se ha producido un error en el escaneo o eliminación de archivos temporales.
        Excepcion: Excepción genérica.
    """
    parser = config_argparse()

    try:
        clean_temp_files(parser.path, parser.recursive)

        print(report(parser.recursive))
    except CleanTmpException as ex:
        print(f"\n{colors['error']}[!] {str(ex)}{colors['reset']}\n")
    except Exception as ex:
        print(f"\n{colors['error']}[!] Se ha producido un error inesperado:{colors['reset']} {str(ex)}\n")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, def_handler)
    main()