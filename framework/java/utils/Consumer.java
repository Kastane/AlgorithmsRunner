package utils;

public class Consumer {
  private static final long x1 = 0x41c64e6dL;
  private static final long x2 = 0xd431L;
  private static long x3 = 1L;

  public static volatile boolean boola = false;
  public static boolean boolb = true;
  public static volatile char chara = 'X';
  public static char charb = 'Y';
  public static volatile byte bytea = 24;
  public static byte byteb = 53;
  public static volatile short shorta = 24;
  public static short shortb = 53;
  public static volatile int inta = 24;
  public static int intb = 53;
  public static volatile long longa = 24L;
  public static long longb = 53L;
  public static volatile float floata = 24.0F;
  public static float floatb = 53.0F;
  public static volatile double doublea = 24.0D;
  public static double doubleb = 53.0D;


  public static volatile Object localObj = new Object();
  public static volatile Object[] localObjs = { new Object() };
  public static long pseudorand = System.nanoTime();

  public static void consumeBool(boolean boolc) {
    if (boolc == boola & boolc == boolb) {
      throw new NullPointerException();
    }
  }

  public static void consumeChar(char charc) {
    if (charc == chara & charc == charb) {
      throw new NullPointerException();
    }
  }

  public static void consumeByte(byte bytec) {
    if (bytec == bytea & bytec == byteb) {
      throw new NullPointerException();
    }
  }

  public static void consumeShort(short shortc) {
    if (shortc == shorta & shortc == shortb) {
      throw new NullPointerException();
    }
  }

  public static void consumeInt(int intc) {
    if (intc == inta & intc == intb) {
      throw new NullPointerException();
    }
  }

  public static void consumeLong(long longc) {
    if (longc == longa & longc == longb) {
      throw new NullPointerException();
    }
  }

  public static void consumeFloat(float floatc) {
    if (floatc == floata & floatc == floatb) {
      throw new NullPointerException();
    }
  }

  public static void consumeDouble(double doublec) {
    if (doublec == doublea & doublec == doubleb) {
      throw new NullPointerException();
    }
  }

  // naive "pseudorandom" implementation to trick compiler
  public static void consumeObj(Object obj) {
    pseudorand = (pseudorand * x1 + x2);
    if ((pseudorand & x3) == 0) {
      x3 = (x3 << 1) + 0xadL;
      localObj = obj;
    }
  }

  public static void consumeObjs(Object[] objs) {
    pseudorand = (pseudorand * x1 + x2);
    if ((pseudorand & x3) == 0) {
      x3 = (x3 << 1) + 0xadL;
      localObjs = objs;
    }
  }

  public static void consume(boolean v) {
    consumeBool(v);
  }

  public static void consume(char v) {
    consumeChar(v);
  }

  public static void consume(byte v) {
    consumeByte(v);
  }

  public static void consume(short v) {
    consumeShort(v);
  }

  public static void consume(int v) {
    consumeInt(v);
  }

  public static void consume(long v) {
    consumeLong(v);
  }

  public static void consume(float v) {
    consumeFloat(v);
  }

  public static void consume(double v) {
    consumeDouble(v);
  }

  public static void consume(Object v) {
    consumeObj(v);
  }

}

