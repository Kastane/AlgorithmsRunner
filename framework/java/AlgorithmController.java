import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class AlgorithmController {
  private long startTime = 0;
  private long stopTime = 0;

  public void startMeasuring() {
    startTime = System.nanoTime();
  }

  public long getStartTime() {
    return startTime;
  }

  public void stopMeasuring() {
    stopTime = System.nanoTime();
  }

  public long getStopTime() {
    return stopTime;
  }

  // AlgorithmThreadMode control stuff.
  private AlgorithmThreadMode mAlgorithmThreadMode;

  public AlgorithmController(AlgorithmThreadMode ts) {
    mAlgorithmThreadMode = ts;
  }

  public Object obj;
  public Method methodSetup = null;
  public Method methodRun = null;
  public int total;

  public void start() {
    Class classAlgorithm;
    try {
      try {
        classAlgorithm = Class.forName(Starter.cfg.className);
        obj = classAlgorithm.newInstance();
      } catch (Exception e) {
        System.err.println("Class.forName(algorithm) doesn't work\n" + e);
        System.exit(0);
      }

      try {
        methodSetup = obj.getClass().getDeclaredMethod("setup");
      } catch (Exception e) {
        System.err.println("Algorithm without setup() method\n" + e);
      }

      try {
        methodRun = obj.getClass().getDeclaredMethod("run");
      } catch (Exception e) {
        System.err.println("Algorithm without run() method\n" + e);
        System.exit(0);
      }

      if (Starter.cfg.threadAmount > 0) {
        System.err.println("threading case");
        System.err.println(Starter.cfg.measureTime);
        mAlgorithmThreadMode.start(this);
        if (total != 0) {
          System.out.println("Algorithm result: " + Starter.cfg.className
              + " " + (stopTime - startTime) / total);
        } else {
          System.err.println("Something is not working");
        }
      } else {
        System.err.println("amount of thread cannot be zero");
      }
    } catch (Throwable e) {
      Throwable t = e instanceof InvocationTargetException ? e.getCause() : e;
      System.err.println(t);
      t.printStackTrace(System.err);
      System.exit(0);
    }
  }
}
