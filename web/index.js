ws = new WebSocket(wsurl + 'echo');

var main = pyy('#main')

function frame(data) {
    if (typeof data === 'string') {
        data = pyy.utils.json(data);
    }
    this.timestamp  = data.timestamp;
    this.id         = data.id;
    this.flags      = data.flags;
    this.len        = data.len;
    this.data       = data.data;
};


function debug_box(id) {
    this.dom = pyy('#data').div();
    this.dom.div(h2('ID '+id.toString(16)), this.last=div('None'));
    this.graphs = [];
    for (var i=0; i<8; i++) {
        this.graphs[i] = new graph();
        this.dom[0].appendChild(this.graphs[i].canvas);
    }
}

function can() {
    var dom = pyy('#frames');
    var ws = new WebSocket(wsurl + 'can');
    var divs = {};

    var get_div = function(id) {
        if (divs[id] === undefined) { 
            divs[id] = new debug_box(id);
        }
        return divs[id];
    };

    ws.onopen = function(e) {
        dom.h3('Open');
        ws.send(pyy.utils.json({ids:[0x2]}));
    };
    ws.onmessage = function(e) {
        // pyy('#frames').pre(e.data);
        var f = new frame(e.data);
        var d = get_div(f.id);
        for (var i=0; i<f.len; i++) {
            d.graphs[i].add(f.data[i]);
        }
        pyy(d.last).clear();
        pyy(d.last).span(U.json(f.data));
    };
    ws.onerror = function(e) {
        dom.h3('Error');
    };
    ws.onclose = function(e) {
        dom.h3('Close');
    };
    dom.h3('Init');
};

var c = new can()

setInterval(function() {
    // pyy('#cam').clear().img({src:'/cam.jpg', width:'640', height:'480'});
}, 100);
