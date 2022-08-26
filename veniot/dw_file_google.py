# https://drive.google.com/file/d/1SqKizB5AuPm5e_JUcZUrlEqjfzYjDhMu/view?usp=sharing # encoder/saved_models/pretrained.pt
# https://drive.google.com/file/d/15caUh6KS2bENCp4GOYXH-LKC98rTW98B/view?usp=sharing # synthsizer/saved_models/cvcorpus/cvcorpus_200k.pt
# https://drive.google.com/file/d/1nd_8uraS3vA3oCaD8u5PwdZjQCgTZizP/view?usp=sharing # synthsizer/saved_models/cvcorpus/cvcorpus_225k.pt
# https://drive.google.com/file/d/1nO9R1Lch1N7YJTmVQWYu_x_WcMyKurht/view?usp=sharing # synthsizer/saved_models/pretrained/pretrained.pt
# https://drive.google.com/file/d/1grP-F5SafzgunkNOuPldOcNJg074xbkT/view?usp=sharing # vocoder/saved_models/pretrained/pretrained.pt

# https://drive.google.com/drive/folders/1Arxft7xy1WnkCCLGJ5zV4XSsLuYYKNnN?usp=sharing # synthsizer/saved_models/cvcorpus
# https://drive.google.com/drive/folders/1usXB391J0hHwuQYJkhPapMSwH-Wt-krn?usp=sharing # synthsizer/saved_models/pretrained
# https://drive.google.com/drive/folders/1pj_l-j4yht9x9txz2arqajuPKHUucGsG?usp=sharing # vocoder/saved_models/pretrained
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
    lista_archivos = credenciales.ListFile(
        {"q": "title = '" + nombre_archivo + "'"}
    ).GetList()
    if not lista_archivos:
        print("No se encontro el archivo: " + nombre_archivo)
    archivo = credenciales.CreateFile({"id": lista_archivos[0]["id"]})
    archivo.GetContentFile(ruta_descarga + nombre_archivo)


def descargar_archivos():
    files = [
        "1SqKizB5AuPm5e_JUcZUrlEqjfzYjDhMu",
        "15caUh6KS2bENCp4GOYXH-LKC98rTW98B",
        "1nd_8uraS3vA3oCaD8u5PwdZjQCgTZizP",
        "1nO9R1Lch1N7YJTmVQWYu_x_WcMyKurht",
        "1grP-F5SafzgunkNOuPldOcNJg074xbkT",
    ]
    rutas_descargas = [
        "./entrenamiento/encoder/saved_models/",
        "./entrenamiento/synthesizer/saved_models/cvcorpus/",
        "./entrenamiento/synthesizer/saved_models/cvcorpus/",
        "./entrenamiento/synthesizer/saved_models/pretrained/",
        "./entrenamiento/vocoder/saved_models/pretrained/",
    ]

    for archivo, ruta in zip(files, rutas_descargas):
        os.makedirs(ruta, exist_ok=True)
        bajar_archivo_por_id(archivo, ruta)
