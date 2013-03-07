


var map_options = {
  credentials:
    'AvJ6JoHEmfEFWn29QfSTgJfZAGJxICmyh-NlWb18Id34smIfiRLUt7PYnGRwf1DC',
  backgroundColor: '#ffffff',
  disableBirdseye: true,
  enableClickableLogo: false,
  enableSearchLogo: false,
  inertiaIntensity: 0,
  showBreadcrumb: true,
  showDashboard: false,
  showMapTypeSelector: false,
  showScalebar: false,
  tileBuffer: 2
};

make_map = function(dom, track, view) {

  // var lat_max = Math.max.apply(null, U.map(track, function(x) { return x[0]; }));
  // var lat_min = Math.min.apply(null, U.map(track, function(x) { return x[0]; }));
  // var lon_max = Math.max.apply(null, U.map(track, function(x) { return x[1]; }));
  // var lon_min = Math.min.apply(null, U.map(track, function(x) { return x[1]; }));

  console.log(track);
  var locations = U.map(track, function(x) { return new Microsoft.Maps.Location(x[1][0], x[1][1]); });

  options = {
    bounds: Microsoft.Maps.LocationRect.fromLocations(locations)
  };
  U.mix(options, map_options);

  console.log(options);

  var map = new Microsoft.Maps.Map(dom, options);

  var polyline = new Microsoft.Maps.Polyline(locations);
  map.entities.push(polyline);


  var pushpin= new Microsoft.Maps.Pushpin(locations[0], null);
  map.entities.push(pushpin);

  for (var j = 0; j < track.length; j++) { track[j][0] *= 1000; }
  var tdata = new plok.data(track);

  view.subscribe({
    update: function() {},
    focus: function(time) {
      var v = tdata.get_value(time, track[0]);
      console.log(v);
      loc = new Microsoft.Maps.Location(v[0], v[1])
      console.log(loc);
      pushpin.setLocation(loc);
    }
  });


   return map;
};

