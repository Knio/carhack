var U = pyy.utils;

WIDTH = 512;
HEIGHT = 32

function graph() {
  
  this.canvas = pyy.tags.canvas({width:WIDTH, height:HEIGHT});
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


  var scroll = function() {
    tempctx.drawImage(this.canvas, 1, 0, WIDTH-1, HEIGHT, 0, 0)
    ctx.drawImage(tempimage, WIDTH-1, HEIGHT);
  };

  var draw = function() {
    var i;
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
    for (i=0;i<WIDTH;i++) {
        var ii = i + Math.max(0, data.length - WIDTH);
        ctx.fillRect(i, 0, 1, scale(data[ii]));
    }
  }

  this.add = function(x) {
    data.push(x);
    while (data.length > 2*WIDTH) {
        data.splice(0, WIDTH);
    }
    // draw();
    scroll();
    ctx.clearRect(i, 0, 1, HEIGHT);
    ctx.fillRect(i, 0, 1, scale(data[data.length-1]));
  };

};
