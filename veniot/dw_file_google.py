# https://drive.google.com/file/d/1XjDcYh9qf4js5h0TZPw8SSxwzFqvxctP/view?usp=share_link lang/en/encoder.pt
# https://drive.google.com/file/d/1PL1Nvy2Tnf-xXEhdT-Rm9lbj1RmZSpRo/view?usp=share_link lang/en/synthesizer.pt
# https://drive.google.com/file/d/1DL5bS-qsNq1dfemOmPnLusWu4XHNUhHf/view?usp=share_link lang/en/vocoder.pt

# https://drive.google.com/file/d/1c-1ArKmgT-iu0AJTL_CvcI6IYITqo0f5/view?usp=share_link lang/es/encoder.pt
# https://drive.google.com/file/d/1HpJU6Cs4ikQYi9bdSylwRm7i_Cu37tPi/view?usp=share_link lang/es/synthesizer.pt
# https://drive.google.com/file/d/1Cke_maOHVixZNeGsW8qMDcDWSKV4BLKz/view?usp=share_link lang/es/vocoder.pt
import os

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

directorio_credenciales = "credentials_module.json"

# INICIAR SESION
def login():
    GoogleAuth.DEFAULT_SETTINGS["client_config_file"] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8080])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales


# DESCARGAR UN ARCHIVO DE DRIVE POR ID
def bajar_archivo_por_id(id_drive, ruta_descarga):
    credenciales = login()
    archivo = credenciales.CreateFile({"id": id_drive})
    nombre_archivo = archivo["title"]
    if not os.path.isfile(ruta_descarga + nombre_archivo):
        archivo.GetContentFile(ruta_descarga + nombre_archivo)
    else:
        print("El archivo ya se encuentra descargado = %s_%s", ruta_descarga, nombre_archivo)


# DESCARGAR UN ARCHIVO DE DRIVE POR NOMBRE
def bajar_acrchivo_por_nombre(nombre_archivo, ruta_descarga):
    credenciales = login()
    lista_archivos = credenciales.ListFile({"q": "title = '" + nombre_archivo + "'"}).GetList()
    if not lista_archivos:
        print("No se encontro el archivo: " + nombre_archivo)
    archivo = credenciales.CreateFile({"id": lista_archivos[0]["id"]})
    archivo.GetContentFile(ruta_descarga + nombre_archivo)


def descargar_archivos():
    files = [
        "1XjDcYh9qf4js5h0TZPw8SSxwzFqvxctP",
        "1PL1Nvy2Tnf-xXEhdT-Rm9lbj1RmZSpRo",
        "1DL5bS-qsNq1dfemOmPnLusWu4XHNUhHf",
        "1c-1ArKmgT-iu0AJTL_CvcI6IYITqo0f5",
        "1HpJU6Cs4ikQYi9bdSylwRm7i_Cu37tPi",
        "1Cke_maOHVixZNeGsW8qMDcDWSKV4BLKz",
    ]
    rutas_descargas = [
        "./entrenamiento/lang/en/",
        "./entrenamiento/lang/en/",
        "./entrenamiento/lang/en/",
        "./entrenamiento/lang/es/",
        "./entrenamiento/lang/es/",
        "./entrenamiento/lang/es/",
    ]

    for archivo, ruta in zip(files, rutas_descargas):
        os.makedirs(ruta, exist_ok=True)
        bajar_archivo_por_id(archivo, ruta)
