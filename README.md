# CleanTMP

## Tabla de contenidos

- [01 Descripción](#01-descripción)
- [02 Instalación](#02-instalación)
- [03 Uso](#03-uso)
- [04 Archivos eliminados](#04-archivos-eliminados)
- [05 Autor](#05-autor)
- [06 Licencia](#06-licencia)

---

## 01 Descripción

**CleanTMP** es una herramienta de línea de comandos para eliminar archivos temporales o residuales en carpetas de usuario. Elimina elementos como `.DS_Store`, `Thumbs.db`, archivos swap de Vim, metadatos de macOS, entre otros.

Ideal para mantener limpias carpetas de documentos, música, descargas o para compartir directorios sin archivos innecesarios.

- **Versión:** v1.0  
- **Última revisión:** 11/06/2025  

### Características

- Elimina archivos temporales comunes en **Windows**, **macOS** y **Linux**.
- Soporte para limpieza **recursiva**.
- Ignora carpetas protegidas del sistema.
- Genera un **reporte detallado** tras la ejecución.
- Compatible con **Python 3.7+**.

[Subir](#tabla-de-contenidos)

---

## 02 Instalación

### Requisitos

- Python 3.7 o superior

### Clonar el repositorio de GitHub

```bash
git clone https://github.com/marcoscr4981/cleantmp.git
```

### Opción 1: Ejecutar desde el repositorio

1. Sitúate en la raíz del proyecto (donde están `README.md` y la carpeta `cleantmp/`).

2. Ejecuta el script:

```bash
python3 cleantmp -r /ruta/a/limpiar
```

### Opción 2: Instalar en el sistema

#### En macOS o Linux

1. Da permisos de ejecución:

```bash
chmod +x cleantmp/__main__.py
```

2. Mueve el script a una carpeta en el PATH (como `/usr/local/bin`):

```bash
sudo mv cleantmp/__main__.py /usr/local/bin/cleantmp
```

3. Ejecuta desde cualquier lugar:

```bash
cleantmp -r ~/Downloads
```

#### En Windows

1. Asegúrate de tener Python instalado y agregado al PATH.

2. Copia el archivo `__main__.py` a una carpeta que esté en el PATH (ej. Scripts de Python):

```powershell
copy cleantmp\__main__.py C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\Scripts\cleantmp.py
```

3. Ejecuta desde CMD o PowerShell:

```powershell
python cleantmp.py -r C:\Users\%USERNAME%\Downloads
```

> Opcional: puedes crear un archivo .bat para ejecutar el script más fácilmente como un comando.

[Subir](#)

## 03 Uso

```bash
cleantmp [opciones] <ruta>
```

### Opciones

- **-r**, **--recursive**: Limpia carpetas de forma recursiva.
- **-v**, **--version**: Muestra la versión actual del script.

[Subir](#)

## 04 Archivos eliminados

- Archivos comunes de metadatos:
  - `.DS_Store`, `Thumbs.db`, `Desktop.ini`, `ehthumbs.db`
- Archivos de respaldo o caché:
  - `*~`, `._*`
- Archivos swap de editores:
  - `.file.swp`, `.file.swo`, `.*.sw?`

[Subir](#)

## 05 Autor

- **Nombre:** Marcos Cuadrado Rey
- **Email:** [marcoscr4981@gmail.com](mailto:marcoscr4981@gmail.com)
- **Web:** [https://github.com/marcoscr4981](https://github.com/marcoscr4981)

[Subir](#)

## 06 Licencia

- **Licencia:** MIT

[Subir](#)

---

> Última modificación: 11 de Junio de 2025