var U = pyy.utils;

WIDTH = 128;
HEIGHT = 128

function graph() {
  
  this.canvas = pyy.tags.canvas({width:WIDTH, height:HEIGHT});
  var ctx = this.canvas.getContext('2d');
  ctx.scale(1, -1);
  ctx.translate(0, -HEIGHT);
  ctx.fillStyle = '#0000dd';
  var data = [];

  var draw = function() {
    var i;
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
    for (i=0;i<WIDTH;i++) {
        ctx.fillRect(i, 0, 1, data[i] * HEIGHT / 256);
    }
  }

  this.add = function(x) {
    data.push(x);
    while (data.length > WIDTH) {
        data.shift();
    }
    draw();
  };

};
