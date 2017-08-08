var host = "ws://127.0.0.1:8000";
var gameboard = [];
for (var i = 0; i < 25; i++){
    gameboard[i] = [];
} // gameboard is 25 lines, 80 columns
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
            updateBoard(msg.data);
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

var curCol = 0, curLine = 0;
var ansi_esc = String.fromCharCode(27) + "[";
function updateBoard(update) {
    for (var i = 0, len = update.length; i < len; i++) {
        if (update.substr(i, 2) == ansi_esc) {
            if (update[i+2] == "?") { // Xterm declaration. Ignore it.
                i += 7;
            }
            else if (update[i+2] == "H") { // put cursor to home position (0, 0)
                i += 2;
                curLine = 0; curCol = 0;
            }
            else if (update.substr(i+2, 2) == "2J") { // clear screen
                for (var j = 0; j < 25; j++) {
                    for (var k = 0; k < 80; k++) {
                        gameboard[j][k] = "";
                    }
                }
                i += 3;
            }
            else if (update[i+2] == "K") { // erase from cursor to end of line
                for (var j = curCol; j < 80; j++) {
                    gameboard[curLine][j] = "";
                }
                i += 2;
            }
            else if (update[i+2] == "A") { // up
                if (curLine-1 >= 0) {
                    curLine -= 1;
                }
                i += 2;
            }
            else if (update[i+2] == "B") { // down
                if (curLine+1 < 25) {
                    curLine += 1;
                }
                i += 2;
            }
            else if (update[i+2] == "C") { // right
                if (curCol+1 < 80) {
                    curCol += 1;
                }
                i += 2;
            }
            else if (update[i+2] == "D") { // left
                if (curCol-1 >= 0) {
                    curCol -= 1;
                }
                i += 2;
            }
            else { // assume all coordinate is just for moving cursors
                   // [line;colH
                if (!isNaN(update[i+2])) { // number comes right after '['
                    if (!isNaN(update[i+3])) { // line is 2 digits
                        curLine = parseInt(update[i+2] + update[i+3]);
                        // update[i+4] == ';'
                        if (!isNaN(update[i+5])) {
                            if (!isNaN(update[i+6])) { // col is 2 digits
                                curCol = parseInt(update[i+5] + update[i+6]);
                                i += 7; console.log("7");
                            }
                            else { // col is 1 digit
                                curCol = update[i+6];
                                i += 6; console.log("6");
                            }
                        }
                    }
                    else if (update[i+3] == ';') { // line is 1 digit
                        curLine = update[i+2];
                        if (!isNaN(update[i+4])) {
                            if (!isNaN(update[i+5])) { // col is 2 digits
                                curCol = parseInt(update[i+4] + update[i+5]);
                                i += 6; console.log("6");
                            }
                            else { // col is 1 digit
                                curCol = update[i+4];
                                i += 5; console.log("5");
                            }
                        }
                    } // end of parsing coordinate
                }
                else {
                    alert("parse error!");
                }
            }
        }
        else {
            console.log(update[i]);
            gameboard[curLine][curCol] = update[i];
            curCol = parseInt(curCol) + 1;
            curLine = parseInt(curLine);
        }
    }
    printGameboard(gameboard);
    console.log(update);
}

function printGameboard(content) {
    document.querySelector("#palatte").innerHTML = "";
    for (var i = 0; i < 25; i++) {
        for (var j = 0; j < 80; j++) {
            document.querySelector("#palatte").innerHTML += content[i][j];
        }
        document.querySelector("#palatte").innerHTML += "<br>";
    }
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

