var val = "hola",
    texto = "hola";

function Inicio() {
    const enviar = document.querySelector("#btnEnviar2");
    enviar.disabled = true;

}

function talk() {
    const enviar = document.querySelector("#btnEnviar2");
    console.log(enviar);
    enviar.disabled = false;
    var hola = "hola";
    const enviar2 = document.querySelector("#btnEnviar");
    enviar2.disabled = "true";
    console.log("prueba");
    var insertar = '<div id="portal" class="portal izquierda">' +
        '<div class="profile">' +
        '<img src="{% static "svg/veniot.svg" %}">' +
        '</div>' +
        '<div class="content-msj">' +
        '<p class="msj">' +
        hola +
        '</p>' +
        '<div class="direccion"></div>' +
        '</div>' +
        '</div>';
    console.log(insertar);

    var btn = document.createElement("div");
    btn.innerHTML = insertar;
    document.getElementById("chat").appendChild(btn);
    var user = "Por el momento solo se clonar voces, ¿Quieres probar?";
    talkUser(user);


    //document.getElementById("btnEnviar").style.visibility = "hidden";
    //document.getElementById("btnEnviar2").style.visibility = "visible";

}

function talk2() {
    var hola = "Si";
    const enviar = document.querySelector("#btnEnviar2");
    document.getElementById('userBox').style.visibility = "visible"; // hide
    document.getElementById("btnEnviar").style.visibility = "hidden";
    document.getElementById("btnEnviar2").style.visibility = "hidden";
    document.getElementById("btnEnviar3").style.visibility = "visible";
    //document.getElementById('btnComenzarGrabacion').style.visibility = "visible";
    // document.getElementById('btnDetenerGrabacion').style.visibility = "visible";
    var insertar = '<div id="portal" class="portal izquierda">' +
        '<div class="profile">' +
        '<img src="{% static "svg/veniot.svg" %}">' +
        '</div>' +
        '<div class="content-msj">' +
        '<p class="msj">' +
        hola +
        '</p>' +
        '<div class="direccion"></div>' +
        '</div>' +
        '</div>';
    console.log(insertar);
    var btn = document.createElement("div");
    btn.innerHTML = insertar;
    document.getElementById("chat").appendChild(btn);
    var user = "Perfecto, Primero ingresa tu nombre ";
    talkUser(user);


}

function talk3() {
    console.log("prueba");
    var hola = document.getElementById("userBox").value;

    console.log(hola);
    const enviar = document.querySelector("#btnEnviar3");
    console.log("prueba");
    val = document.getElementById("userBox").value;
    console.log(val);
    console.log(hola);
    var insertar = '<div id="portal" class="portal izquierda">' +
        '<div class="profile">' +
        '<img src="{% static "svg/veniot.svg" %}">' +
        '</div>' +
        '<div class="content-msj">' +
        '<p class="msj">' +
        hola +
        '</p>' +
        '<div class="direccion"></div>' +
        '</div>' +
        '</div>';
    console.log(insertar);
    var btn = document.createElement("div");
    btn.innerHTML = insertar;
    document.getElementById("chat").appendChild(btn);
    var user = "Da click en el icono de grabar y lee el siguiente texto. Trabaja mientras otros duermen, Estudia mientras otros se divierten, Persiste mientras otros descansan y luego vivirás lo que otros solo sueñan.";
    talkUser(user);

    document.getElementById('userBox').style.visibility = "visible"; // hide
    document.getElementById("btnEnviar").style.visibility = "hidden";
    document.getElementById("btnEnviar2").style.visibility = "hidden";
    document.getElementById("btnEnviar3").style.visibility = "hidden";
    document.getElementById('btnComenzarGrabacion').style.visibility = "visible";
    document.getElementById('btnDetenerGrabacion').style.visibility = "visible";

    const detenermensaje = document.querySelector("#btnDetenerGrabacion");
    detenermensaje.disabled = true;

}

function talk4() {
    console.log("prueba");
    var hola = document.getElementById("userBox").value;

    console.log(hola);
    const enviar = document.querySelector("#btnEnviarTexto");
    console.log("prueba");
    texto = document.getElementById("userBox").value;
    console.log(texto);
    console.log(hola);
    var insertar = '<div id="portal" class="portal izquierda">' +
        '<div class="profile">' +
        '<img src="{% static "svg/veniot.svg" %}">' +
        '</div>' +
        '<div class="content-msj">' +
        '<p class="msj">' +
        hola +
        '</p>' +
        '<div class="direccion"></div>' +
        '</div>' +
        '</div>';
    console.log(insertar);
    var btn = document.createElement("div");
    btn.innerHTML = insertar;
    document.getElementById("chat").appendChild(btn);


    document.getElementById('userBox').style.visibility = "visible"; // hide
    document.getElementById("btnEnviar").style.visibility = "hidden";
    document.getElementById("btnEnviar2").style.visibility = "hidden";
    document.getElementById("btnEnviar3").style.visibility = "hidden";
    document.getElementById("btnEnviarTexto").style.visibility = "visible";
    document.getElementById('btnComenzarGrabacion').style.visibility = "hidden";
    document.getElementById('btnDetenerGrabacion').style.visibility = "hidden";

    const detenermensaje = document.querySelector("#btnDetenerGrabacion");
    detenermensaje.disabled = true;

}

function talkUser(mensaje) {


    var insertar = '<div id="portal" class="portal derecha">' +
        '<div class="profile">' +
        '<img src="/static/img/user.png">' +
        '</div>' +
        '<div class="content-msj">' +
        '<p class="msj">' +
        mensaje +
        '</p>' +
        '<div class="direccion"></div>' +
        '</div>' +
        '</div>';

    var btn = document.createElement("div");
    btn.innerHTML = insertar;
    document.getElementById("chat").appendChild(btn);

}