package utils;

public final class Log {
  public static final String INFO = "INFO";
  public static final String ERROR = "ERROR";

  public static void log(String level, String msgf, Object... msga) {
    String formatted = msgf == null ? "null" : String.format(msgf, msga);
    System.out.printf("%d %s - %s\n", System.currentTimeMillis(), level, formatted);
  }

}
