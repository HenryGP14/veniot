var opciones = 0;
var mensaje = "con tu propia voz"
const $duracion = document.querySelector("#duracion");
var user_name, data_text;

function talk() {
    switch (opciones) {
        case 0:
            talk_user("Hola");
            talk_robot("¿Cómo te llamas?");
            $("#userBox").show();
            $("#btnEnviar span").html("Enviar");
            opciones += 1;
            break;
        case 1:
            if ($("#userBox").val().length > 0) {
                user_name = $("#userBox").val();
                talk_user($("#userBox").val());
                $("#userBox").hide();
                talk_robot(`Hola ${$("#userBox").val()}, un gusto en conocerte`);
                $("#btnEnviar span").html("¿Qué sabes hacer veniot?");
                opciones += 1;
            } else {
                talk_robot("Por favor escribe tu nombre");
            }
            break;
        case 2:
            talk_user("¿Qué sabes hacer veniot?");
            talk_robot("Por el momento solo se clonar voces, ¿Quieres probar?");
            $("#btnEnviar span").html("Si");
            opciones += 1;
            break;
        case 3:
            talk_user("Si");
            talk_robot("Da click en el icono de grabar y lee el siguiente texto. Trabaja mientras otros duermen, Estudia mientras otros se divierten, Persiste mientras otros descansan y luego vivirás lo que otros solo sueñan.");
            $("#btnEnviar").hide();
            $("#btnComenzarGrabacion").show();
            $("#btnDetenerGrabacion").show();
            $("#btnComenzarGrabacion").click(comenzarAGrabar);
            $("#btnDetenerGrabacion").click(detenerGrabacion);
            $("#userBox").val("");
            break;
        case 4:
            $("#btnEnviar").show();
            $("#btnComenzarGrabacion").hide();
            $("#btnDetenerGrabacion").hide();
            talk_robot(`¡Perfecto!, ahora escribe lo que te gustaría escuchar ${ mensaje }`);
            $("#userBox").show();
            $("#btnEnviar span").html("Enviar a clonar");
            $("#btnEnviar").css('width', '200px ');
            $("#btnEnviar").click(EnviarAjax);
            opciones += 1;
            break;
        case 5:
            data_text = $("#userBox").val();
            if ($("#userBox").val().length > 0) {
                talk_user($("#userBox").val());
                $("#userBox").val("");
                talk_robot("Listo dame un tiempo para poder clonar tu voz");
                $("#btnEnviar").prop("disabled", true);
            } else {
                talk_robot("Por favor escribe el texto que quieres escuchar");
            }
            break;
    }
}

function talk_robot(mensaje) {
    var html_content = `
    <div class="portal derecha">
        <div class="profile">
            <img src="/static/svg/veniot.svg">
        </div>
        <div class="content-msj">
            <p class="msj">
                ${ mensaje }
            </p>
            <div class="direccion"></div>
        </div>
    </div>
    `;
    $("#chat").append(html_content);
    $('#chat').scrollTop($('#chat').prop('scrollHeight'));
    $('html').scrollTop($('html').prop('scrollHeight'));
}

function talk_user(mensaje) {
    var html_content = `
    <div class="portal izquierda">
        <div class="profile">
            <img src="/static/img/user.png">
        </div>
        <div class="content-msj">
            <p class="msj">
                ${ mensaje } 
            </p>
            <div class="direccion"></div>
        </div>
    </div>
    `;
    $("#chat").append(html_content);
    $('#chat').scrollTop($('#chat').prop('scrollHeight'));
    $('html').scrollTop($('html').prop('scrollHeight'));
}

// Función para establecer una cookie, que será necesario para las solicitudes Ajax con Django
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Grabar audio
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
let tiempoInicio, idIntervalo;
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
            myRecorder.objects.context = new(
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
        }).catch(function (err) {
            swal("Información!!", "Lo sentimos no pudimos tener acceso a tu micrófono puedes concederlo manualmente si quieres interactuar con Veniot o puedes interactuar con mi voz predeterminada.", "warning").then((value) => {
                talk_robot("Esta es mi voz predeterminada");
                $("#chat").append($('<div class="audio-controler"></div>').append($('<audio controls></audio>').attr('src', '/media/sounds/audio_test2.wav')));
                mensaje = "con mi voz predeterminada";
                opciones += 1;
                talk();
            });;
        });
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
                myRecorder.objects.recorder.exportWAV(function (data) {
                    var url = (window.URL || window.webkitURL)
                        .createObjectURL(data);
                    blob = data;
                    // Prepare the playback
                    var audioObject = $('<audio controls></audio>')
                        .attr('src', url);
                    // Prepare the download link
                    var downloadObject = $('<a>&#9660;</a>')
                        .attr('href', url)
                        .attr('download', new Date().toUTCString() + '.wav');
                    // Wrap everything in a row
                    var holderObject = $('<div class="audio-controler"></div>')
                        .append(audioObject)
                    // Append to the list
                    $("#chat").append(holderObject);
                    opciones += 1;
                    talk();
                });
            }
        }
    }
};
// Prepare the recordings list
var listObject = $('[data-role="recordings"]');

const comenzarAGrabar = () => {
    $("#btnComenzarGrabacion").prop("disabled", true);
    $("#btnDetenerGrabacion").prop("disabled", false);
    myRecorder.init();
    myRecorder.start();
};
const detenerGrabacion = () => {
    myRecorder.stop(listObject);
};

const EnviarAjax = () => {
    if (data_text.length > 0) {
        var spinner = `
        <div id="load" class="spinner-border text-danger position-absolute" role="status" style="right: 10px; bottom:20px;">
            <span class="visually-hidden">Loading...</span>
        </div>
        `;
        $(".portal").css('position', 'relative').last().append(spinner);
        var frmData = new FormData();
        var csrftoken = getCookie('csrftoken');
        var user_send = user_name.normalize('NFD')
            .replace(/([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+/gi, "$1").replace(' ', '_')
            .normalize();
        try {
            audio_file = new File([blob], user_send + ".wav");
            frmData.append('audio', audio_file);
        } catch (error) {
            frmData.append('audio', null);
        }

        frmData.append('user', user_name);
        frmData.append('texto', data_text);
        frmData.append('csrfmiddlewaretoken', csrftoken);
        $.ajax({
            method: "POST",
            url: "/clonar/",
            data: frmData,
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function (data) {
                $("#btnEnviar").prop("disabled", false);
                if (data['code']) {
                    localStorage.setItem("user_session", user_name);
                    $("#load").remove();
                    alert_success(data['message']);
                    talk_robot("¡Perfecto!, pude clonar tu voz aún que fue un poco difícil.");
                    talk_robot("Aún estoy aprendiendo, así que mejorare en clonar cualquier voz al 100%");
                    $("#chat").append($('<div class="audio-controler"></div>').append($('<audio controls></audio>').attr('src', data['url'])));
                    $('#chat').scrollTop($('#chat').prop('scrollHeight'));
                } else {
                    $("#load").remove();
                    alert_error(data['message']);
                }
            },
            error: function (error) {
                $("#load").remove();
                alert_error("El servidor se encuentra fuera de servicio, intentalo más tarde");
            }
        });
    }
};

function alert_success(text) {
    toastr.success(text, 'Información', {
        closeButton: true,
        progressBar: true,
        positionClass: "toast-top-right",
        preventDuplicates: true,
        onclick: null,
        showDuration: "50",
        hideDuration: "0",
        timeOut: "6000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut"
    });
}

function alert_error(text) {
    toastr.error(text, 'Error', {
        closeButton: true,
        progressBar: true,
        positionClass: "toast-top-right",
        preventDuplicates: true,
        onclick: null,
        showDuration: "50",
        hideDuration: "0",
        timeOut: "6000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut"
    });
}