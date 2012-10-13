var U = pyy.utils;

WIDTH = 720;
HEIGHT = 256

HISTORY = 100 * 300;

FILL_COLORS = [
  'hsla(32,  70%, 80%, 0.2)',
  'hsla(167, 70%, 80%, 0.2)',
  'hsla(302, 70%, 80%, 0.2)',
  'hsla(77,  70%, 80%, 0.2)',
  'hsla(122, 70%, 80%, 0.2)',
  'hsla(257, 70%, 80%, 0.2)',
  'hsla(212, 70%, 80%, 0.2)',
  'hsla(347, 70%, 80%, 0.2)'
];


COLORS = [
  'hsla(32,  70%, 70%, 1.0)',
  'hsla(167, 70%, 70%, 1.0)',
  'hsla(302, 70%, 70%, 1.0)',
  'hsla(77,  70%, 70%, 1.0)',
  'hsla(122, 70%, 70%, 1.0)',
  'hsla(257, 70%, 70%, 1.0)',
  'hsla(212, 70%, 70%, 1.0)',
  'hsla(347, 70%, 70%, 1.0)'
];

function Source() {
  this.data = [];
  this.add = function(x) {
    this.data.push(x)
    if (data.length > 2 * HISTORY) {
      data.splice(0, HISTORY);
    }
  };
};

function Graph() {

  var canvas = this.canvas = pyy.tags.canvas({width:WIDTH, height:HEIGHT});
  var tempimage = pyy.tags.canvas({width:WIDTH, height:HEIGHT});
  var ctx = this.canvas.getContext('2d');
  var tempctx = tempimage.getContext('2d');
  ctx.scale(1, -1);
  ctx.translate(0, -HEIGHT);
  ctx.fillStyle = '#0000dd';
  var data = [];

  var scale = d3.scale.linear();
  scale.domain([0, 256]);
  scale.range([0, HEIGHT]);

  // var scroll = function() {
  //   tempctx.drawImage(canvas, 1, 0, WIDTH-1, HEIGHT, 0, 0)
  //   ctx.drawImage(tempimage, WIDTH-1, HEIGHT);
  // };

  this.draw = function() {
    var i, j, ii, v, p, s, h;
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
    for (j=0;j<data.length;j++) {
      d = data[j].data;
      ctx.fillStyle = FILL_COLORS[j];
      for (i=0;i<WIDTH;i++) {
          ii = i + Math.max(0, d.length - WIDTH);
          v = scale(d[ii]);
          // console.log(ii);
          ctx.fillRect(i, 0, 1, v);
      }
      p = null;
      ctx.fillStyle = COLORS[j];
      for (i=0;i<WIDTH;i++) {
          ii = i + Math.max(0, d.length - WIDTH);
          v = scale(d[ii]);
          if (p === null) { p = v; }
          s = Math.min(p, v);
          h = Math.abs(v - p) + 2;
          ctx.fillRect(i, s, 1, h);
          p = v;
      }
    }
  };

  this.add_source = function(s) {
    data.push(s);
  };

};
