var wsUri = "ws://tribot.shack:1337/";
var output;
var query;
function wsInit()
{
    initQuery();
    output = document.getElementById("output");
    testWebSocket();
}

function initQuery()
{
    query = {"direction":0, "speed": 0, "rotation" : 0, "enable": false}
}

function testWebSocket()
{
    websocket = new WebSocket(wsUri);
    websocket.onopen = function(evt) { onOpen(evt) };
    websocket.onclose = function(evt) { onClose(evt) };
    websocket.onmessage = function(evt) { onMessage(evt) };
    websocket.onerror = function(evt) { onError(evt) };
}

function onOpen(evt)
{
    writeToScreen("CONNECTED");
    
}

function onClose(evt)
{
    writeToScreen("DISCONNECTED");
}

function onMessage(evt)
{
    var receivedData = JSON.parse(evt.data);
    if(receivedData["response"]==true)
        writeToScreen('<span style="color: blue;">Command was accepted</span>');
}

function onError(evt)
{
    writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data);
}

function doSend(message)
{
    websocket.send(message);
}

function writeToScreen(message)
{
    var pre = document.createElement("p");
    pre.style.wordWrap = "break-word";
    pre.innerHTML = message;
    $("#output").html(pre);
}
