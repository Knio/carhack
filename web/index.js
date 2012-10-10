ws = new WebSocket(wsurl);

var main = pyy('#main')


function frame() {

};


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



setInterval(function() {
    pyy('#cam').clear().img({src:'/cam.jpg', width:'640', height:'480'});
}, 100);
