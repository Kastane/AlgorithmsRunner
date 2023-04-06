import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;

public class AlgorithmThreadMode {
  private ArrayList<Algorithm> mAlgorithm = new ArrayList<Algorithm>();

  private ArrayList<Thread> threads = new ArrayList<Thread>();

  //private volatile int total = 0;
  double percentOfDecreasing = 0.9999;

  protected void measure() {
    for (Thread thread: threads) {
      thread.run();
    }
    for (Thread thread: threads) {
      try {
        thread.join();
      } catch (Exception e) {
        System.err.println(e);
        System.exit(0);
      }
    }
  }

  volatile boolean interrupted = false;
  volatile int total = 0;

  public void start(AlgorithmController control) {

    try {
      if (control.methodSetup != null) {
        try {
          control.methodSetup.invoke(control.obj);
        } catch (Throwable e) {
          Throwable t = e instanceof InvocationTargetException ? e.getCause() : e;
          System.err.println("Problems to call setup() method\n" + t);
          t.printStackTrace(System.err);
          System.exit(0);
        }
      }
      int amountThreads = Starter.cfg.threadAmount;

      for (int i = 0; i < amountThreads; ++i) {
        mAlgorithm.add(new Algorithm());
      }

      for (Task task : mAlgorithm) {
        task.mControl = control;
        Thread t = new Thread(task);
        threads.add(t);
      }

      if (Starter.cfg.warmupIters > 0) {
        //warmup
        System.err.println("warmup started");

        control.startMeasuring();
        measure();
        control.stopMeasuring();

        long lastMeasure;
        long currentMeasure = control.getStopTime() - control.getStartTime();

        do {
          control.startMeasuring();
          measure();
          control.stopMeasuring();
          lastMeasure = currentMeasure;
          currentMeasure = control.getStopTime() - control.getStartTime();
        } while (currentMeasure <= lastMeasure * percentOfDecreasing);

        for (int i = 0; i < Starter.cfg.warmupIters; i++) {
          measure();
        }

        System.err.println("warmup finished");
      }

      //TO DO: smart computation of execution time
      Thread threadLauncher = new Thread() {
        public void run() {
          while (!interrupted) {
            total++;
            measure();
          }
        }
      };

      control.startMeasuring();
      threadLauncher.start();
      Thread.sleep(Starter.cfg.measureTime * 1000);
      interrupted = true;
      threadLauncher.join();
      control.stopMeasuring();
      control.total = total;

    } catch (Exception e) {
      System.err.println(e);
      System.exit(0);
    }
  }
}
