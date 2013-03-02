

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
    trips.sort(function(a,b) {
      return a.ts_start < b.ts_start;
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
      h2(t.title),
      div(nice_date_and_duration(t.date_start, t.date_end)),
      this.charts = div()
    );

    new plok.topaxis(this.charts, this.view);

    U.foreach(t.series, function(name) {
      var data = new plok.data();

      var url = '/api/trip/%(tid)s/%s/range/%(ts_start)s/%(ts_end)s';
      pyy.io.get(U.format(url, name, t), function(text) {
        json = U.json(text);
        // map timestamps to js times
        U.foreach(json, function(a) { a[0] *= 1000; });
        data.data = json;
        this.view.update();
      }, this);

      var c1 = div({style: {height: '200px'}});
      this.charts.appendChild(div(h4(name), c1));
      new plok.chart(c1, this.view, data)

    }, this);

    return dom;
  },

  destroy: function() {
    this.view.destroy();
  }
});


