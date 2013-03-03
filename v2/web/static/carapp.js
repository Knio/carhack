

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
  return date.toISOString() + " " + date.toLocaleTimeString();
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
  this.view = new plok.view(trip.date_start, trip.date_end);
  this.view.scale = 250.0;
  this.view.set(trip.date_end);

  this.dom = this.build_dom();
};
U.mix(TripUI.prototype, {
  build_dom: function() {
    var t = this.trip;
    var dom = div(
      {class:'trip'},
      h2(t.title),
      div(nice_date_and_duration(t.date_start, t.date_end)),
      this.charts = div({class:'charts'})
    );

    var axis_container
    this.charts.appendChild(div(
      div(h3('Time'), div()),
      div(axis_container = div())
    ));
    new plok.topaxis(axis_container, this.view);

    U.foreach(t.series, function(name) {
      var row = new RawRow(t, this.view, name);
      this.charts.appendChild(row.dom);
    }, this);

    return dom;
  },

  destroy: function() {
    this.view.destroy();
  }
});


function RawRow(trip, view, name) {

  var chart_container;
  var data = null;
  var legend;
  var legend_events;
  this.chart = null;



  this.show = function() {
    this.chart = new plok.chart(chart_container, view);
    this.get_data();
    this.dom.className = 'row show';
  };

  this.hide = function() {
    view.unsubscribe(legend_events);
    this.chart.destroy();
    this.dom.className = 'row hide';
    this.chart = null;
    pyy(legend).clear();
    pyy(chart_container).clear();
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
    if (this.data) {
      this.show_data();
      return;
    }
    var url = '/api/trip/%(tid)s/%s/range/%(ts_start)s/%(ts_end)s';
    pyy(legend)('LOADING...');
    pyy.io.get(U.format(url, name, trip), function(text) {
      this.data = this.parse_data(U.json(text));
      this.show_data();
    }, this);
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

    if (/^test\./.test(name)) {
      for (var j = 0; j < json.length; j++) { json[j][0] *= 1000; }
      data['A'] = new plok.data(json);
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
