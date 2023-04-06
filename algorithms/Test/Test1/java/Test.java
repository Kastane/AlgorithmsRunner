import utils.Consumer;

public class Test {

  public int test() {
    return 5;
  }

  public void run() {
    Consumer.consumeInt(test());
  }
}
