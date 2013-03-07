

var CarApp = function() {
  this.event = new U.event();
  this.data = null;
  this.trips = {}
  this.load();
}
U.mix(CarApp.prototype, {
  load: function() {
    pyy.io.get('/api/trips', function(data, r, e) {
      data = pyy.utils.json(data);
      U.foreach(data, function(trip, tid) {
        this.trips[tid] = new Trip(tid, trip);
      }, this);
      this.event('trips_loaded', this.trips);
    }, this);
  },

  __end: null
});


var Trip = function(tid, data) {
  this.tid = tid;
  U.mix(this, data);
  this.date_start = new Date(this.ts_start * 1000);
  this.date_end   = new Date(this.ts_end * 1000);
  this.duration = this.ts_end - this.ts_start;
}

U.mix(Trip.prototype, {
  load: function() {
    pyy.io.get('/api/trip/')
  }
});

window.app = new CarApp();

var nice_date = function(date) {
  return moment(date).format('LLL');
};

var nice_duration = function(s) {
  r = "";
  while (s > 3600) {
    hours = Math.floor(s / 3600);
    if (r) { r += ", " }
    r += (hours + " hours")
    s = s - (hours * 3600);
  }
  while (s > 60) {
    minutes = Math.floor(s / 60);
    if (r) { r += ", " }
    r += (minutes + " minutes")
    s = s - (minutes * 60);
  }
  if (r) { r += ", " }
  s = Math.floor(s);
  r += (s + " seconds")

  return r;
}

var nice_date_and_duration = function(a, b) {
  sa = nice_date(a);
  sb = nice_date(b);
  var br = 0;
  var i;
  for (i=0; i<sb.length && i<sa.length; i++) {
    if (sa.charAt(i) !== sb.charAt(i)) {
      break;
    }
    if (sa.charAt(i) == ' ') {
      br = i;
    }
  }
  if (i == sb.length) { br = i; }
  sb = sb.substring(br);
  sd = nice_duration((b - a) / 1000);
  return sa + " - " + sb + " (" + sd + ")"
};


function CarAppUi(selector) {
  this.build_dom(selector);
  this.selected_trip = null;
  this.trips_loaded(app.trips);
  U.listen(app.event, this);
};
U.mix(CarAppUi.prototype, {
  build_dom: function(selector) {
    this.dom = div(
      div(this.trip_select = select({onchange: this.select_trip, context:this})),
      this.trip = div()
    );
    pyy(selector)[0].appendChild(this.dom);
  },

  select_trip: function() {
    if (this.selected_trip) {
      this.selected_trip.destroy();
      H.empty(this.trip);
    }
    var ts = this.trip_select;
    var trip = app.trips[ts.options[ts.selectedIndex].value];
    this.trip.appendChild((this.selected_trip = (new TripUI(trip))).dom);
  },

  trips_loaded: function(trips) {
    H.empty(this.trip_select);
    trips = U.values(trips);
    trips.sort(function(a, b) {
      return b.ts_start - a.ts_start;
    });
    U.foreach(trips, function(trip) {
      var name = nice_date(trip.date_start);
      var opt = option(name, {value: trip.tid})
      this.trip_select.appendChild(opt);
    }, this);
    if (!this.selected_trip && trips[0]) {
      this.select_trip(trips[0]);
    }
  }
});


function TripUI(trip) {
  window.tripui = this;
  this.trip = trip;
  this.view = new plok.view(trip.date_start, trip.live ? null : trip.date_end);
  this.view.scale = 100.0;
  this.view.set(trip.live ? +new Date() : trip.date_end);
  this.rows = [];
  this.socket = null;
  if (trip.live) {
    this.socket = new WebSocket(U.format('ws://%s/api/socket', window.location.host));

    var subscriptions = {};
    this.subscribe = function(name, cb, context) {
      if (subscriptions[name] === undefined) {
        subscriptions[name] = U.event();
        var msg = U.json({series: U.keys(subscriptions)});
        this.socket.send(msg);
      }
      subscriptions[name].subscribe(cb, context);
    }
    this.unsubscribe = function(name, cb, context) {
      subscriptions[name].unsubscribe(cb, context);
      if (subscriptions[name].len() === 0) {
        delete subscriptions[name];
        var msg = U.json({series: U.keys(subscriptions)});
        this.socket.send(msg);
      }
    }

    this.socket.onopen = function(e) {
      console.log(e);
    };
    this.socket.onclose = function(e) {
      console.log(e);
    };
    this.socket.onerror = function(e) {
      console.log(e);
    };
    this.socket.onmessage = function(e) {
      var data = U.json(e.data);
      if (subscriptions[data.name] === undefined) {
        return;
      }
      subscriptions[data.name](data.data[0], data.data[1]);
    }

    this.view.animate();
  }

  this.dom = this.build_dom();
};
U.mix(TripUI.prototype, {
  build_dom: function() {
    var t = this.trip;
    var dom = div(
      {class:'trip'},
      h2(t.title),
      t.live ?
        nice_date(t.date_start) + ' - Now' :
        div(nice_date_and_duration(t.date_start, t.date_end)),
      this.map = div(),
      this.charts = div({class:'charts'})
    );

    var gps_track = 'nmea_proc.gps.position'

    if (this.trip.series.indexOf(gps_track) !== -1) {
      this.map.className = 'map';

      var url = '/api/trip/%(tid)s/%s/range/%(ts_start)s/%(ts_end)s';
      pyy.io.get(U.format(url, gps_track, this.trip), function(text) {
        gps_data = U.json(text);
        var bing_map = make_map(this.map, gps_data, this.view);
      }, this)
    }

    var axis_container
    this.charts.appendChild(div({class:'row time'},
      div(h3('Time'), div()),
      div(axis_container = div())
    ));
    new plok.topaxis(axis_container, this.view);

    U.foreach(t.series, function(name) {
      var row = new RawRow(t, this, this.view, name);
      this.rows.push(row);
      this.charts.appendChild(row.dom);
    }, this);

    return dom;
  },

  recalculate: function() {
    I.get(U.format('/api/trip/%s/recalculate', this.trip.tid), function(json) {
      alert(json);
    }, this);
  },

  destroy: function() {
    this.view.destroy();
    U.foreach(this.rows, function(row) {
      row.hide();
    });
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
});


scalar_data = [
  /^nissan_370z\./,
  /^test/,
  /^nmea_proc.gps.speed_over_ground/,
  /^nmea_proc.gps.direction/,
  /^nmea_proc.gps.altitude/,
];

function RawRow(trip, ui, view, name) {

  var chart_container;
  var legend;
  var legend_events;
  this.chart = null;
  this.data = null;

  this.show = function(e) {
    if (e) { e.preventDefault(); }
    this.chart = new plok.chart(chart_container, view);
    this.get_data();
    this.dom.className = 'row show';
  };

  this.hide = function(e) {
    if (e) { e.preventDefault(); }
    view.unsubscribe(legend_events);
    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }
    this.dom.className = 'row hide';
    pyy(legend).clear();
    pyy(chart_container).clear();
    if (trip.live && this.cb) {
      ui.unsubscribe(name, this.cb, this);
      this.cb = null;
    }
  };

  this.dom = div({class:'row hide'},
    div(
      a({href:'#', onclick:this.show, context:this}, '[show]'),
      a({href:'#', onclick:this.hide, context:this}, '[hide]'),
      h3(name),
      legend = div()
    ),
    div(chart_container = div())
  );

  this.get_data = function() {
    if (this.data && !trip.live) {
      this.show_data();
      return;
    }
    var url = '/api/trip/%(tid)s/%s/range/%(ts_start)s/%(ts_end)s';
    pyy(legend)('LOADING...');
    pyy.io.get(U.format(url, name, trip), function(text) {
      this.data = this.parse_data(U.json(text));
      if (!this.chart) { return; } // canceled
      this.show_data();
    }, this);

    if (trip.live) {
      ui.subscribe(name, this.cb=function(ts, value) {
        if (!this.data) { return; }
        if (/^canusb\./.test(name)) {
          for (var i = 0; i < value.len; i++) {
            var ts = ts * 1000;
            this.data['ABCDEFGH'.charAt(i)].append(ts, value.data[i]);
          }
        }
        else if (U.foreach(scalar_data, function(r) {
          if (r.test(name)) return true})) {

          var ts = ts * 1000;
          this.data['A'].append(ts, value);
        }

        else {
          throw "unknown data format";
        }

        if (ts < view.end) {
          view.update();
        }
      }, this);
    }
  }

  this.parse_data = function(json) {
    var data = {};

    if (/^canusb\./.test(name)) {
      var len = json[0][1].len;
      for (var i = 0; i < len; i++) {
        var d = [];
        for (var j = 0; j < json.length; j++) {
          d.push([json[j][0] * 1000, json[j][1].data[i]]);
        }
        data['ABCDEFGH'.charAt(i)] = new plok.data(d);
      }
    }

    else if (U.foreach(scalar_data, function(r) {
      if (r.test(name)) return true})) {

      for (var j = 0; j < json.length; j++) { json[j][0] *= 1000; }
      data['A'] = new plok.data(json);
    }

    else {
      throw "unknown data format";
    }

    return data;
  };

  this.show_data = function() {
    var l = pyy(legend).clear();
    var f = [];
    U.foreach(this.data, function(d, name) {
      this.chart.add_data(d);
      var s = span();
      l.div(name, s);
      f.push([d, s]);
    }, this);

    view.subscribe(legend_events = {
      focus: function(ts) {
        U.foreach(f, function(v) {
          var x = v[0].get_value(ts);
          pyy(v[1]).clear().text(U.format("%03d", x));
        });
      },
      update: function() {}
    });
    window.setTimeout(function() {
      view.update();
    }, 0);
  };
}
