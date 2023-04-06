public class Starter {
  // Entrypoint
  public static BaseConfig cfg;

  public static void main(String[] args) {
    System.err.println("we are hear");

    Class<?> cfgClass = null;
    try {
      cfgClass = Class.forName(Global.GEN_ALGORITHM_CONFIG_CLASS_NAME);
    } catch (ClassNotFoundException e) {
      System.err.println("Add config file\n" + e);
      System.exit(0);
    }
    try {
      cfg = (BaseConfig) cfgClass.newInstance();

      start(cfg);
    } catch (Exception e) {
      System.err.println("BaseConfig cfg failed\n" + e);
      System.exit(0);
    }
  }


  public static void start(BaseConfig cfg) {
    try {
      if (cfg != null) {
        System.err.println("Current algorithm: " + cfg.className);
      }

      AlgorithmController ac = new AlgorithmController(new AlgorithmThreadMode());
      ac.start();
    } catch (Exception e) {
      System.err.println(e);
      System.exit(0);
    }
  }
}
