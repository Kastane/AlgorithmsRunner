import java.lang.reflect.InvocationTargetException;

public class Algorithm extends Task {

  //this case for multi threading
  @Override
  public void run() {
    execute();
  }

  @Override
  public void execute() {
    try {
      mControl.methodRun.invoke(mControl.obj);
    } catch (Throwable e) {
      Throwable t = e instanceof InvocationTargetException ? e.getCause() : e;
      System.err.println("run() is failed\n" + t + "\n");
      t.printStackTrace(System.err);
      System.exit(0);
    }
  }
}
