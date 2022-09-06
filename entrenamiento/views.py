import unicodedata
import numpy as np
import soundfile as sf
import librosa
import torch

from entrenamiento.utils.modelutils import check_model_paths
from entrenamiento.synthesizer.inference import Synthesizer
from entrenamiento.encoder import inference as encoder
from entrenamiento.vocoder import inference as vocoder
from pathlib import Path
from django.http import JsonResponse
from entrenamiento.models import Media

# Create your views here.
def clonar(request):
    if request.method == "POST":
        enc_model_fpath = Path("entrenamiento/encoder/saved_models/pretrained.pt")
        syn_model_fpath = Path("entrenamiento/synthesizer/saved_models/cvcorpus/cvcorpus_200k.pt")
        voc_model_fpath = Path("entrenamiento/vocoder/saved_models/pretrained/pretrained.pt")
        # Cheequea si los modelos están descargados
        check_model = check_model_paths(
            encoder_path=enc_model_fpath,
            synthesizer_path=syn_model_fpath,
            vocoder_path=voc_model_fpath,
        )

        ## Si no están completos los modelos la web indicará al usuario el error -14
        if not check_model:
            print(
                "Lo sentimos el servidor de clonación de voz se encuentra fuera de servicio, contacte algunos de los desarrolladores e indique error -14"
            )
            return JsonResponse(
                {
                    "code": 0,
                    "message": "Lo sentimos el servidor de clonación de voz se encuentra fuera de servicio, contacte algunos de los desarrolladores e indique error -14",
                }
            )

        ## Cargue los modelos uno por uno.
        print("Preparing the encoder, the synthesizer and the vocoder...")
        encoder.load_model(enc_model_fpath)
        synthesizer = Synthesizer(syn_model_fpath)
        vocoder.load_model(voc_model_fpath)
        try:
            # Guardar el audio que es enviado por ajax
            ## Código
            try:
                if request.FILES["audio"] != None:
                    audio_media = Media.objects.create(
                        nombre=request.POST["user"], ruta=request.FILES["audio"]
                    )
                    audio_path = "." + audio_media.ruta.url
                    text = request.POST["texto"]
                    nombre_usuario = audio_media.ruta.name.replace("sounds/", "").replace(
                        ".wav", ""
                    )
            except:
                audio_media = Media()
                audio_media.nombre = request.POST["user"]
                audio_media.save()
                audio_path = "./media/sounds/audio_test.mp3"
                text = request.POST["texto"]
                nombre_usuario = "Ejemplo" + str(audio_media.id)
            # Obtener la ruta de audio
            ## Código

            # Conseguir la ruta de audio

            ## Calculando la incrustación
            # Primero, cargamos el wav usando la función que proporciona el codificador del altavoz. Esto es
            # importante: hay preprocesamiento que se debe aplicar.

            # Los siguientes dos métodos son equivalentes:
            # - Cargar directamente desde la ruta del archivo:
            preprocessed_wav = encoder.preprocess_wav(audio_path)

            # - Si el wav ya está cargado:
            original_wav, sampling_rate = librosa.load(str(audio_path))
            preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)

            # Luego derivamos la incrustación. Hay muchas funciones y parámetros que el
            # interfaces de codificador de altavoz. Estos son principalmente para la investigación en profundidad. normalmente
            # solo use esta función (con sus parámetros predeterminados):
            embed = encoder.embed_utterance(preprocessed_wav)

            # Si se especifica la semilla, reinicie la semilla de la antorcha y fuerce la recarga del sintetizador
            seed = None
            if seed is not None:
                torch.manual_seed(seed)
                synthesizer = Synthesizer(syn_model_fpath)

            # El sintetizador funciona por lotes, por lo que debe colocar sus datos en una lista o matriz numérica
            texts = [text]
            embeds = [embed]

            # Si sabe cuáles son las alineaciones de la capa de atención, puede recuperarlas aquí
            # pasando return_alignments=Verdadero
            specs = synthesizer.synthesize_spectrograms(texts, embeds)
            spec = specs[0]
            print("Created the mel spectrogram")

            # Si se especifica la semilla, reinicie la semilla de la antorcha y vuelva a cargar el vocoder
            if seed is not None:
                torch.manual_seed(seed)
                vocoder.load_model(voc_model_fpath)

            # Sintetizar la forma de onda es bastante sencillo. Recuerda que cuanto más tiempo
            # espectrograma, más eficiente en el tiempo es el vocoder.
            generated_wav = vocoder.infer_waveform(spec)

            ## Post-generación
            # Hay un error con el dispositivo de sonido que hace que el audio se corte un segundo antes, así que
            # rellenarlo.
            generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")

            # Recorte el exceso de silencios para compensar las lagunas en los espectrogramas (problema #53)
            generated_wav = encoder.preprocess_wav(generated_wav)

            # Guardar audio
            route_save = "media/audios/"
            filename = route_save + nombre_usuario + ".wav"
            try:
                audio_media.ruta_audio_clonado = filename
                audio_media.save()
            except:
                pass
            sf.write(
                "./" + filename,
                generated_wav.astype(np.float32),
                synthesizer.sample_rate,
            )

            return JsonResponse(
                {
                    "code": 1,
                    "message": "Tu voz a sido clonada, revisa y escuala",
                    "url": "/" + audio_media.ruta_audio_clonado,
                }
            )
        except Exception as e:
            # El error -45 aparece cuando algunos de los modelos no esta bien descargados y se encuentran vacios
            print(
                "Lo sentimos el servidor de clonación de voz se encuentra fuera de servicio, contacte algunos de los desarrolladores e indique error -45"
            )
            # Aquí sucede un error
            return JsonResponse(
                {
                    "code": 0,
                    "message": "Lo sentimos el servidor de clonación de voz se encuentra fuera de servicio, contacte algunos de los desarrolladores e indique error -45",
                }
            )
    else:
        return JsonResponse(
            {"code": 0, "message": "Lo sentimos estás tratando de acceder ilegalmente"}
        )
