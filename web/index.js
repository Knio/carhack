ws = new WebSocket(wsurl);

var main = pyy('#main')

ws.onopen = function(evt) {
    main.div(h3('open websocket'));
    ws.send('Hello world from a websocket');
};

ws.onclose = function(evt) {
    main.div(h3('close websocket'));
};

ws.onmessage = function(evt) {
    main.div(h3('message'), evt.data);
};

ws.onerror = function(evt) {
    main.div(h3('websocket error'));
};

