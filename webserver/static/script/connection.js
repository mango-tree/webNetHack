var host = "ws://mango-tree.xyz:8000";

connect();

function connect() {
    var socket;
    try {
        var socket = new WebSocket(host);
        socket.onopen = function () {
            alert("Socket has been opened!");
        }
        socket.onmessage = function (msg) {
            parseMsg(msg);
            document.querySelector("#palatte").innerHTML += msg.data;
        }
    } catch (exception) {
        message(exception);
    }

    function send_data(text) {
        try {
            socket.send(text);
        } catch (exception) {
            message(exception);
        }
    }

    document.addEventListener("keypress", function (event) {
        var charcode = getChar(event);
        send_data(charcode);
    });
}

function getChar(event) {
    event = event || window.event;
    var keyCode = event.which || event.keyCode;
    var typedChar = String.fromCharCode(keyCode);
    console.log('press: ' + typedChar);
    return typedChar;
}

function parseMsg(msg) {
    console.log(msg);
}

