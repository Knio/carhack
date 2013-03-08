


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
  var locations = U.map(track, function(x) {
    return new Microsoft.Maps.Location(x[1][0], x[1][1]);
  });

  var = options = U.mix({}, map_options);
  options.bounds: Microsoft.Maps.LocationRect.fromLocations(locations)

  var map = new Microsoft.Maps.Map(dom, options);
  var polyline = new Microsoft.Maps.Polyline(locations);
  var pushpin= new Microsoft.Maps.Pushpin(locations[0], null);
  map.entities.push(polyline);
  map.entities.push(pushpin);

  for (var j = 0; j < track.length; j++) { track[j][0] *= 1000; }
  var tdata = new plok.data(track);

  view.subscribe({
    update: function() {},
    focus: function(time) {
      var v = tdata.get_value(time, track[0]);
      loc = new Microsoft.Maps.Location(v[0], v[1])
      pushpin.setLocation(loc);
    }
  });


   return map;
};

