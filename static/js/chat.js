function talk() {
    var know = {
        "Hola": "Por el momento solo se clonar voces, ¿Quieres probar?",
        "Si": "Perfecto,  da click en el icono de grabar y lee el siguiente texto. Trabaja mientras otros duermen, Estudia mientras otros se divierten, Persiste mientras otros descansan y luego vivirás lo que otros solo sueñan. "
    };
    var user = document.getElementById('userBox').value;
    talkUser(user);

    if (user in know) {
        var insertar = '<div id="portal" class="portal derecha">' +
            '<div class="profile">' +
            '<img src="{% static "svg/veniot.svg" %}">' +
            '</div>' +
            '<div class="content-msj">' +
            '<p class="msj">' +
            know[user] +
            '</p>' +
            '<div class="direccion"></div>' +
            '</div>' +
            '</div>';

        var btn = document.createElement("div");
        btn.innerHTML = insertar;
        document.getElementById("chat").appendChild(btn);
    } else {
        document.getElementById('chatLog').innerHTML = "No entiendo lo que quieres decir";
    }
}

function talkUser(mensaje) {
    var insertar = '<div id="portal" class="portal izquierda">' +
        '<div class="profile">' +
        '<img src="{% static "img/user.png" %}">' +
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