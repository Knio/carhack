
var U = pyy.utils;

ws = new WebSocket(wsurl + 'echo');

var main = pyy('#main')

function Frame(data) {
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

    var graph = new Graph();
    var bytes = [];
    var _b;
    this.dom = pyy('#data').div(
        table(tr(
            td(h2('ID'+id.toString(16))),
            _b = td(),
            td(graph.canvas)
        ))
    );

    var data = [];

    this.read = function(frame) {
        for (var i=0; i<frame.len; i++) {
            if (i === data.length) {
                var s = new Source();
                data.push(s);
                graph.add_source(s);
            }
            data[i].add(frame.data[i]);


            if (i === bytes.length) {
                var d = div();
                d.setAttribute('class', 'byte'+i);
                bytes.push(d);
                _b.appendChild(d);
            }

            bytes[i].innerHTML = ''+frame.data[i];
        }
    };

    this.draw = function() {
        graph.draw();
    };
}

function can() {
    var dom = pyy('#frames');
    var ws = new WebSocket(wsurl + 'can');
    var divs = {};
    var frame_delay = null;

    // try to render at 50Hz
    var drawing = false;
    var draw = function() {
        U.foreach(divs, function(d) {
            d.draw();
        });
        drawing = false;
    };
    var schedule_draw = function() {
        if (drawing) { return; }
        drawing = true;
        window.setTimeout(draw, 10);
    };
    window.setInterval(schedule_draw, 20);

    window.setInterval(function() {
        if (frame_delay !== null) {
            frame_delay -= 10;
        }
        // console.log(frame_delay);
    }, 100);

    // process incoming log at 100Hz
    var frames = [];
    var frames_i = 0;
    window.setInterval(function() {
        var now = new Date() - 0;
        for (var i=frames_i;i<frames.length;i++) {
            if (frames[i][0] < now) {
                process(frames[i][1]);
                frames_i++;
            } else {
                break;
            }
        }
        if (frames_i > 10240) {
            frames.splice(0, frames_i);
            frames_i = 0;
        }
    }, 10);

    var get_div = function(id) {
        if (divs[id] === undefined) {
            divs[id] = new debug_box(id);
        }
        return divs[id];
    };

    var process = function(frame) {
        var d = get_div(frame.id);
        d.read(frame);
    }

    ws.onopen = function(e) {
        dom.h3('Open');
        // ws.send(pyy.utils.json({ids:[0x421, 0x180, 0x160]}));
        ws.send(pyy.utils.json({ids:[2]}));
    };
    ws.onmessage = function(e) {
        // pyy('#frames').pre(e.data);
        var f = new Frame(e.data);
        var ts = new Date(f.timestamp * 1000);
        if (frame_delay === null) {
            frame_delay = ts - (new Date());
        };
        var delay = (ts - 0 + frame_delay) - (new Date());
        console.log(delay);
        // this frame took a long time to arrive
        if (delay < 0) {
            frame_delay -= delay;
            delay = 0;
        }
        delay = 0;
        var schedule = new Date() - 0 + delay;
        frames.push([schedule, f]);

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
