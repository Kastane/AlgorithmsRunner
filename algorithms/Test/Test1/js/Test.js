function Test() {
    this.NUM = 5;
  }
  
  StringConcat.prototype.run = function() {
    var consumer = new Consumer();
    consumer.consumeObjs(this.NUM);
  }
  