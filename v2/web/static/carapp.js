var carapp = {

  trips: null,

  load: function() {
    carapp.get_trips();
  },

  get_trips: function() {
    pyy.io.get('/api/trips', function(data, r, e) {
      console.log([data, r, e]);
      carapp.trips = pyy.utils.json(data);
    });
  },

  trip: function(tid) {
    this.tid = tid
  },

  get_trip: function(tid) {

  },

  __end: null
};


