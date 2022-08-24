/* 
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/JSP_Servlet/JavaScript.js to edit this template
 */
jQuery(document).ready(function () {
    var $ = jQuery;
    const  $duracion = document.querySelector("#duracion");
    const  $btnComenzarGrabacion = document.querySelector("#btnComenzarGrabacion"),
            $btnDetenerGrabacion = document.querySelector("#btnDetenerGrabacion");
    const segundosATiempo = numeroDeSegundos => {
        let horas = Math.floor(numeroDeSegundos / 60 / 60);
        numeroDeSegundos -= horas * 60 * 60;
        let minutos = Math.floor(numeroDeSegundos / 60);
        numeroDeSegundos -= minutos * 60;
        numeroDeSegundos = parseInt(numeroDeSegundos);
        if (horas < 10)
            horas = "0" + horas;
        if (minutos < 10)
            minutos = "0" + minutos;
        if (numeroDeSegundos < 10)
            numeroDeSegundos = "0" + numeroDeSegundos;

        return `${horas}:${minutos}:${numeroDeSegundos}`;
    };
    // Variables "globales"
    let tiempoInicio, mediaRecorder, idIntervalo;
    const refrescar = () => {
        $duracion.textContent = segundosATiempo((Date.now() - tiempoInicio) / 1000);
    };
    const comenzarAContar = () => {
        tiempoInicio = Date.now();
        idIntervalo = setInterval(refrescar, 500);
        console.log(idIntervalo);
    };

    const detenerConteo = () => {

        clearInterval(idIntervalo);
        tiempoInicio = null;
        $duracion.textContent = "";

    };

    var myRecorder = {
        objects: {
            context: null,
            stream: null,
            recorder: null
        },
        init: function () {
            if (null === myRecorder.objects.context) {
                myRecorder.objects.context = new (
                        window.AudioContext || window.webkitAudioContext
                        );
            }
        },
        start: function () {
            var options = {
                audio: true,
                video: false
            };
            navigator.mediaDevices.getUserMedia(options).then(function (stream) {
                myRecorder.objects.stream = stream;
                comenzarAContar();
                myRecorder.objects.recorder = new Recorder(
                        myRecorder.objects.context.createMediaStreamSource(stream), {
                    numChannels: 1
                }
                );
                myRecorder.objects.recorder.record();
            }).catch(function (err) {});
        },
        stop: function (listObject) {
            if (null !== myRecorder.objects.stream) {
                myRecorder.objects.stream.getAudioTracks()[0].stop();
            }
            if (null !== myRecorder.objects.recorder) {
                myRecorder.objects.recorder.stop();
                detenerConteo();
                // Validate object
                if (null !== listObject &&
                        'object' === typeof listObject &&
                        listObject.length > 0) {
                    // Export the WAV file
                    myRecorder.objects.recorder.exportWAV(function (blob) {
                        var url = (window.URL || window.webkitURL)
                                .createObjectURL(blob);
                        // Prepare the playback
                        var audioObject = $('<audio controls></audio>')
                                .attr('src', url);
                        // Prepare the download link
                        var downloadObject = $('<a>&#9660;</a>')
                                .attr('href', url)
                                .attr('download', new Date().toUTCString() + '.wav');
                        // Wrap everything in a row
                        var holderObject = $('<div class="row"></div>')
                                .append(audioObject)
                                .append(downloadObject);
                        // Append to the list
                        listObject.append(holderObject);
                        var frmData = new FormData();
                        frmData.append('audio', blob);
                        frmData.append('host', window.location.protocol + '//' + window.location.host);
                        $.ajax({
                            method: "POST",
                            url: "AudioSrv",
                            data: frmData,
                            processData: false,
                            contentType: false,
                            success: function (data) {
                               
                              console.log(frmData);
                                console.log("Archivo guardado con exito");
                            },
                            error: function (error) {
                                console.log("Algo salio mal al guardar el archivo");
                            }
                        });
                    });
                }
            }
        }
    };
    // Prepare the recordings list
    var listObject = $('[data-role="recordings"]');
    // Prepare the record button
//        $('[data-role="controls"] > button').click(function () {
//            
//    console.log('estoy');
// Initialize the recorder
//myRecorder.init();
// // Get the button state 
//        var buttonState = !!$(this).attr('data-recording');
//
//        // Toggle
//        if (!buttonState) {
//            $(this).attr('data-recording', 'true');
//            myRecorder.start();
//        } else {
//            $(this).attr('data-recording', '');
//            myRecorder.stop(listObject);
//        }
//    });

    const comenzarAGrabar = () => {
        myRecorder.init();
        myRecorder.start();

        console.log('inicio y empiezo');
    };
    const detenerGrabacion = () => {
        myRecorder.stop(listObject);

        console.log('detener');
    };
    $btnComenzarGrabacion.addEventListener("click", comenzarAGrabar);
    $btnDetenerGrabacion.addEventListener("click", detenerGrabacion);
//        
//});
});