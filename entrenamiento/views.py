from utils.argutils import print_args
from utils.modelutils import check_model_paths
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa
import argparse
import torch
import os
from audioread.exceptions import NoBackendError

## Preparar las configuraciones del clonador de voz
if __name__ == "__main__":
    ## Info & args
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-e",
        "--enc_model_fpath",
        type=Path,
        default="encoder/saved_models/pretrained.pt",
        help="Path to a saved encoder",
    )
    parser.add_argument(
        "-s",
        "--syn_model_fpath",
        type=Path,
        default="synthesizer/saved_models/cvcorpus/cvcorpus_200k.pt",
        help="Path to a saved synthesizer",
    )
    parser.add_argument(
        "-v",
        "--voc_model_fpath",
        type=Path,
        default="vocoder/saved_models/pretrained/pretrained.pt",
        help="Path to a saved vocoder",
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="If True, processing is done on CPU, even when a GPU is available.",
    )
    parser.add_argument(
        "--no_sound", action="store_true", help="If True, audio won't be played."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random number seed value to make toolbox deterministic.",
    )
    parser.add_argument(
        "--no_mp3_support",
        action="store_true",
        help="If True, disallows loading mp3 files to prevent audioread errors when ffmpeg is not installed.",
    )
    args = parser.parse_args()
    print_args(args, parser)
    if not args.no_sound:
        import sounddevice as sd

    if args.cpu:
        # Oculte las GPU de Pytorch para forzar el procesamiento de la CPU
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    # Revisa si el servidor se encuentra instalado el convertidor de mp3 esta instalado
    if not args.no_mp3_support:
        try:
            librosa.load("../media/sound/audio_test.mp3")
        except NoBackendError:
            print(
                "Librosa will be unable to open mp3 files if additional software is not installed.\n"
                "Please install ffmpeg or add the '--no_mp3_support' option to proceed without support for mp3 files."
            )
            exit(-1)

    print("Running a test of your configuration...\n")

    if torch.cuda.is_available():
        device_id = torch.cuda.current_device()
        gpu_properties = torch.cuda.get_device_properties(device_id)
        ## Imprime alguna información del entorno (para fines de depuración)
        print(
            "Found %d GPUs available. Using GPU %d (%s) of compute capability %d.%d with "
            "%.1fGb total memory.\n"
            % (
                torch.cuda.device_count(),
                device_id,
                gpu_properties.name,
                gpu_properties.major,
                gpu_properties.minor,
                gpu_properties.total_memory / 1e9,
            )
        )
    else:
        print("Using CPU for inference.\n")


# Create your views here.
def clonacion(request):
    ## Cheequea si los modelos están descargados
    check_model = check_model_paths(
        encoder_path=args.enc_model_fpath,
        synthesizer_path=args.syn_model_fpath,
        vocoder_path=args.voc_model_fpath,
    )

    ## Si no están completos los modelos la web indicará al usuario el error -14
    if not check_model:
        return "Lo sentimos el servidor de clonación de voz se encuentra fuera de servicio, contacte algunos de los desarrolladores e indique error -14"

    ## Cargue los modelos uno por uno.
    print("Preparing the encoder, the synthesizer and the vocoder...")
    encoder.load_model(args.enc_model_fpath)
    synthesizer = Synthesizer(args.syn_model_fpath)
    vocoder.load_model(args.voc_model_fpath)
    try:
        # Guardar el audio que es enviado por ajax
        ## Código

        # Obtener la ruta de audio
        ## Código

        # Conseguir la ruta de audio
        audio_path = "../media/sound/audio_test.mp3"

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

        ## Genera el espectograma del texto (Aquí va el texto traido del frontend)
        text = "Esto es una prueba de clonación de voz"

        # Si se especifica la semilla, reinicie la semilla de la antorcha y fuerce la recarga del sintetizador
        if args.seed is not None:
            torch.manual_seed(args.seed)
            synthesizer = Synthesizer(args.syn_model_fpath)

        # El sintetizador funciona por lotes, por lo que debe colocar sus datos en una lista o matriz numérica
        texts = [text]
        embeds = [embed]

        # Si sabe cuáles son las alineaciones de la capa de atención, puede recuperarlas aquí
        # pasando return_alignments=Verdadero
        specs = synthesizer.synthesize_spectrograms(texts, embeds)
        spec = specs[0]
        print("Created the mel spectrogram")

        # Si se especifica la semilla, reinicie la semilla de la antorcha y vuelva a cargar el vocoder
        if args.seed is not None:
            torch.manual_seed(args.seed)
            vocoder.load_model(args.voc_model_fpath)

        # Sintetizar la forma de onda es bastante sencillo. Recuerda que cuanto más tiempo
        # espectrograma, más eficiente en el tiempo es el vocoder.
        generated_wav = vocoder.infer_waveform(spec)

        ## Post-generación
        # Hay un error con el dispositivo de sonido que hace que el audio se corte un segundo antes, así que
        # rellenarlo.
        generated_wav = np.pad(
            generated_wav, (0, synthesizer.sample_rate), mode="constant"
        )

        # Recorte el exceso de silencios para compensar las lagunas en los espectrogramas (problema #53)
        generated_wav = encoder.preprocess_wav(generated_wav)

        # Guardar audio
        route_save = "../media/audio/"
        filename = "%sdemo_output.wav" % route_save
        print(generated_wav.dtype)
        sf.write(filename, generated_wav.astype(np.float32), synthesizer.sample_rate)

        return "Clonación terminada"
    except:
        # Aquí sucede un error
        pass
