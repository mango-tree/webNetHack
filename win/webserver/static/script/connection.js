var host = "ws://mango-tree.xyz:8000";
//var vt100 = require('./contrib/vt100/vt100')
//var helpers = require('./helpers/all')

//var display = document.getElementById('display');//$("#display");
//var vt100 = new VT100({canvas:document.getElementById('display')})

//var v = new VT100({
//    size: {x: 20, y: 20},
    //display: (new helpers.Display)
//})
var controller=display.getContext("2d");
connect();


function connect(){
    var socket;
    try {
        var socket = new WebSocket(host);
        socket.onopen = function(){  
           alert("Socket has been opened!"); 
        }  
        socket.onmessage = function(msg){  
            parseMsg(msg);
           //alert(msg.data); //Awesome!  
           html = AnsiUp.prototype.ansi_to_html(msg.data);
           controller.fillText(html,10,10);

           $("#palatte").append(msg.data);
           //v.write(msg.data);
            
        }  
    } catch(exception) {
        message(exception);
    }

    function send_data(text) {
        try {
            socket.send(text);
        } catch(exception) {
            message(exception);
        }
    }

    $(document).keypress(function(event) {  
        var charcode = getChar(event);
        send_data(charcode);
    });
}
function getChar(event) {
    event = event || window.event;
    var keyCode = event.which || event.keyCode;
    var typedChar = String.fromCharCode(keyCode);
    console.log('press: '+typedChar);
    return typedChar;
}
function parseMsg(msg)
{
    
    console.log(msg);
}



