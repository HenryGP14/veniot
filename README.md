# **Veniot**

## **Bot web que permite clonar la voz**

Veniot es un chatrobot con el cual podrás interactuar mediante texto, para luego proporcionarte un texto lo cual debe ir leyendo mientras tu voz será grabada. Esta grabación de voz se realiza para poder entrenar un modelo de inteligencia artificial enfocado en redes neuronales que son aplicados para que Veniot pueda clonar tu voz.

## **Requisitos de instalación**

1. Se admiten tanto Windows como Linux. Se recomienda una GPU para el entrenamiento y la velocidad de inferencia, pero no es obligatoria.
2. Se recomienda **Python 3.7.***, pero probablemente si instala una versión superior tendrá que modificar las versiones de las dependencias. Recomiendo configurar un entorno virtual usando `venv`, pero esto es opcional.
3. Instale [ffmpeg](https://ffmpeg.org/download.html#get-packages). Esto es necesario para leer archivos de audio.
4. Instale [PyTorch](https://pytorch.org/get-started/locally/). Elija la última versión estable, su sistema operativo, su administrador de paquetes (pip por defecto) y finalmente elija cualquiera de las versiones propuestas de CUDA si tiene una GPU; de lo contrario, elija una CPU. Ejecute el comando dado.
5. Instale los requisitos restantes con `pip install -r requirements.txt`

## **Requisitos opcionales**

Los modelos preentrenados ahora se descargan automáticamente. Si esto no funciona para usted, puede descargarlos manualmente y colocarlo en la ruta la carpeta de **./entrenamiento**

1. **Encoder** [encoder/saved_models/pretrained.pt](https://drive.google.com/file/d/1SqKizB5AuPm5e_JUcZUrlEqjfzYjDhMu/view?usp=sharing)
2. **Synthsizer cvcorpus** [synthsizer/saved_models/cvcorpus](https://drive.google.com/drive/folders/1Arxft7xy1WnkCCLGJ5zV4XSsLuYYKNnN?usp=sharing)
3. **Synthsizer pretrained** [synthsizer/saved_models/pretrained](https://drive.google.com/drive/folders/1usXB391J0hHwuQYJkhPapMSwH-Wt-krn?usp=sharing)
4. **Vocoder pretrained** [vocoder/saved_models/pretrained](https://drive.google.com/drive/folders/1pj_l-j4yht9x9txz2arqajuPKHUucGsG?usp=sharing)

La descarga de los modelos se lo realiza mediante a una conexión a **Google Drive Auth2** y por lo general los modelos se descarga automáticamente, pero acceso es por tiempo limitado. Si al intentar ejecutar el proyecto se presenta el error de **token expirado** intente eliminar el archivo **credentials_module.json** y vuelva a ejecutar el programa, donde le redireccionara a un link para volver a crear un nuevo token de acceso.

Si al intentar iniciar sesión le sale acceso denegado, procure crear nuevas credenciales de **Google Cloud Platform** puede dar [**click aquí**](https://youtu.be/ZI4XjwbpEwU) para guiarse con siguiente video y tenga una mejor compresión.

## **Surgimiento**

La idea de la creación de veniot (**V**oic**e** Clo**ni**ng Rob**ot**) surgió en la demanda del mercado de la clonación de voz es cada vez mayor, debido a sus interesantes y variadas aplicaciones que se puede ofrecer, entre las que se encuentran los asistentes conversacionales, los altavoces inteligentes, el doblaje, los personajes digitales, los juegos, los audiolibros, los sistemas de navegación o el branding de voz.

## **Código original**

[**Real-Time Voice Cloning**](https://github.com/CorentinJ/Real-Time-Voice-Cloning) by CorentinJ
