
var U = pyy.utils;
var H = pyy.html.tags;

ws = new WebSocket(wsurl + 'echo');

var main = pyy('#main')

function Frame(data) {
    if (typeof data === 'string') {
        data = U.json(data);
    }
    this.timestamp  = data.timestamp;
    this.id         = data.id;
    this.flags      = data.flags;
    this.len        = data.len;
    this.data       = data.data;
};


function debug_box(id) {

    var active = false;
    this.toggle = function() {
        if (!active) {
            this.enable();
        } else {
            this.disable();
        }
    };
    this.enable = function() {
        active = true;
        this.dom.className = '';
        can.subscribe(id, this.read, this);
    };
    this.disable = function() {
        active = false;
        this.dom.className = 'disabled';
        can.unsubscribe(id, this.read, this);
    };

    var graph = new Graph();
    var bytes = [];
    var _b;
    var that = this;
    this.dom = div(
        table(tr(
            td(h2(a('ID'+id.toString(16), {
                href:'#',
                onclick:function(e) {that.toggle(); e.preventDefault(); return false; },
                context:this
            }))),
            _b = td(),
            td(graph.canvas)
        ))
    );
    this.dom.className = 'disabled';

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
        if (active) {
            graph.draw();
        }
    };



    // this.enable();
}

var NISSAN_IDS = [
    0x002, 0x160, 0x180, 0x182, 0x1F9, 0x215, 0x216, 0x245, 0x280, 0x284,
    0x285, 0x292, 0x2DE, 0x342, 0x351, 0x354, 0x355, 0x358, 0x35D, 0x385,
    0x421, 0x512, 0x54C, 0x551, 0x580, 0x5C5, 0x60D, 0x625, 0x6E2];


function keys(obj) {
    var keys = [];
    U.foreach(obj, function(v, k) {
        keys.push(k);
    });
    return keys;
};

function values(obj) {
    var values = [];
    U.foreach(obj, function(v, k) {
        values.push(v);
    });
    return values;
};

function event() {
    var listeners = []

    var fire = function() {
        var args = U.args(arguments);
        U.foreach(listeners, function(sub) {
            var a = sub.args.concat(args);
            sub.callback.apply(sub.context, a);
        });
    };

    fire.subscribe = function(callback, context) {
        listeners.push({
            callback: callback,
            context: context,
            args: U.args(arguments, 2)
        });
    };

    fire.unsubscribe = function(callback, context) {
        listeners = U.remove(listeners, function(sub) {
            return (sub.callback == callback) &&
                (sub.context == context);
        });
    };

    fire.len = function() {
        return listeners.length;
    }

    return fire;
}

function CAN() {
    var dom = pyy('#frames');
    var ws = new WebSocket(wsurl + 'can');
    var divs = {};
    var events = {};
    var ids = [];
    var data = pyy('#data')[0];



    this.subscribe = function(id, callback, context) {
        if (!events[id]) {
            events[id] = event();
            ws.send(U.json({ids: U.map(keys(events), function(i) { return i-0; })}));
        }
        events[id].subscribe(callback, context);
    };

    this.unsubscribe = function(id, callback, context) {
        var e = events[id];
        e.unsubscribe(callback, context);
        if (e.len() == 0) {
            delete events[id];
            ws.send(U.json({ids: U.map(keys(events), function(i) { return i-0; })}));
        }
    };

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

    var process = function(frame) {
        var e = events[frame.id];
        if (e === undefined) { return; }
        e(frame);
    }

    ws.onopen = function(e) {
        dom.h3('Open');

        U.foreach(NISSAN_IDS, function(id) {
            divs[id] = new debug_box(id);
            data.appendChild(divs[id].dom);
        }, this);

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

window.can = new CAN()

setInterval(function() {
    // pyy('#cam').clear().img({src:'/cam.jpg', width:'640', height:'480'});
}, 100);
