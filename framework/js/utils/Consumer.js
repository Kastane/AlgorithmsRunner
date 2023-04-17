function Consumer() {
  this.x1 = 0x41c64e6d;
  this.x2 = 0xd431;
  this.x3 = 1;

  this.boola = false;
  this.boolb = true;
  this.chara = 'X';
  this.charb = 'Y';
  this.inta = 24;
  this.intb = 53;
  this.floata = 24.0;
  this.floatb = 53.0;

  this.localObj = new Object();
  this.localObjs = [new Object()];
  this.pseudorand = Date.now();
}

Consumer.prototype.consumeBool = function(boolc) {
  if (boolc === this.boola && boolc === this.boolb) {
    throw new Error();
  }
};

Consumer.prototype.consumeChar = function(charc) {
  if (charc === this.chara && charc === this.charb) {
    throw new Error();
  }
};

Consumer.prototype.consumeInt = function(intc) {
  if (intc === this.inta && intc === this.intb) {
    throw new Error();
  }
};

Consumer.prototype.consumeFloat = function(floatc) {
  if (floatc === this.floata && floatc === this.floatb) {
    throw new Error();
  }
};

Consumer.prototype.consumeObj = function(obj) {
  this.pseudorand = (this.pseudorand * this.x1 + this.x2);
  if ((this.pseudorand & this.x3) === 0) {
    this.x3 = (this.x3 << 1) + 0xad;
    this.localObj = obj;
  }
};

Consumer.prototype.consumeObjs = function(objs) {
  this.pseudorand = (this.pseudorand * this.x1 + this.x2);
  if ((this.pseudorand & this.x3) === 0) {
    this.x3 = (this.x3 << 1) + 0xad;
    this.localObjs = objs;
  }
};
