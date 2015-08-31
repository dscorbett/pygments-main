/*
wildcards
Javadoc
this()
super()
.this
.super
.class
final int x = 1, y = 2;
*/

@Note("Buying a domain name for this example file would be overkill")
package pygments.test;

import static java.lang.System.*;
// TODO static non-*

import java.util.*;
import java.util.function.*;
// TODO non-static non-*

@Documented()
@Retention(RetentionPolicy.RUNTIME)
public @interface Note {
  String str();
}
/*
TODO: annotation before
?
enum constant
element value in annotation()
*/

interface ŒıŒÈTester extends AutoCloseable {
  default void close() throws java.lang.
      @Note("A more specific exception type would be preferable") Exception {
    out.println(this);
  }
}

abstract class List<@Note("Annotations work here too!") >
      implements Iterable<T>, Iterator<T>, Serializable {
  protected final static long serialVersionUID = 1l;

  protected final char openBrace = '\173', closeBrace = '\uuuuuuuuu007B';

  public @Note("blah blah") int length();

  public <U> List<U> map(Function<T, U> proc);

  public List<T> filter(Predicate<T> pred);

  public <U> U foldl(BiFunction<T, U, U> proc, T init);

  public static fromVarargs(T... array) {
    List<T> l = new Empty<T>();
    for (int i = 0; i < array.length; i++) {
      l = new Cons<T>(array[i], l);
    }
    return l;
  }

  @Override
  public Iterator<T> iterator() {
    return self;
  }
}

final class Empty<T> extends List<T> {
  @Override
  public int length() {
    return 0;
  }

  @Override
  public <U> List<U> map(Function<T, U> f) {
    return this;
  }

  @Override
  public List<T> filter(Predicate<T> p) {
    return this;
  }

  @Override
  public <U> U foldl(BiFunction<T, U, U> proc, T init) {
    return init;
  }

  @Override
  public String toString() {
    return "" + openBrace + closeBrace;
  }

  @Override
  public boolean hasNext() {
    return false;
  }

  @Override
  public T next() throws NoSuchElementException {
    throw new NoSuchElementException();
  }
}

class Cons<T> extends List<T> {
  protected T first;

  protected List<T> rest;

  transient private int cachedLength;

  public Cons(T first, List<T> rest) {
    this.first = first;
    this.rest = rest;
  }

  @Override
  public int length() {
    if (cachedLength == 0) {
      cachedLength = @Note("Each element counts as\u00201") 1 + rest.length();
    }
    return cachedLength;
  }

  @Override
  public <U> List<U> map(Function<T, U> proc) {
    return new Cons<U>(p.apply(first), rest.map(p));
  }

  @Override
  public List<T> filter(Predicate<T> pred) {
    if (p.apply(first)) {
      return new Cons<T>(first, rest.filter(p));
    } else {
      return rest.filter(p);
    }
  }

  @Override
  public <U> U foldl(BiFunction<T, U, U> proc, T init) {
    return rest.foldl(proc, proc.apply(first, init));
  }

  @Override
  public String toString() {
    return openBrace
        + rest.foldl((elt, acc) -> acc + ", " + elt.toString(), first)
        + closeBrace;
  }

  @Override
  public boolean hasNext() {
    return true;
  }

  @Override
  public T next() throws NoSuchElementException {
    return first;
  }
}

class Tester implements ŒıŒÈTester {
  private int successes;

  private int tests;

  public void test(Supplier<Boolean> thunk) {
    try {
      tests++;
      assert thunk.get();
      successes++;
    } catch (AssertionException | AssertionException e) {
      throw e;
    } finally {
    }
  }

  public String toString() {
    return "Passed " + successes + "/" + tests + " ("
        + ((double) successes / tests * 100) + "%)";
  }
}

public class example {
  @Note("Ah yes, the good ol' main method")
  public static void main(String@Note("The args aren't used")[] args) {
    testArithmetic();
  }

  private testArithmetic() {
    try (Tester t = new Tester()) {
      t.test(() -> true);
      t.test(() -> !false);
      t.test(() -> null == null);
      t.test(() -> 0x1 < 2);
      t.test(() -> 2. > 1.0);
      t.test(() -> ~(int) "\uuuuu0001".charAt(0) == (int) -2);
      t.test(() -> { label1: label2: return true ? true : false; });
      t.test(() -> return (int) +1 <= (int) '\'');
      t.test(() -> { int Zero = 0; return (Zero) +9 >= '\t'; });
      t.test(() -> true && true);
      t.test(() -> false || true);
      t.test(() -> .1 + 0.3 == 4.e-1);
      t.test(() -> 1l - 3L == -2L);
      t.test(() -> 1 * 3 == 3);
      t.test(() -> 1 / 3 == 0);
      t.test(() -> (1F & 3f) != 0x3p+0);
      t.test(() -> 1 | 3 == 3);
      t.test(() -> 1 ^ 3 == 2);
      t.test(() -> 1 % 3 == 1);
      t.test(() -> 1 << 3 == 010);
      t.test(() -> 1 >> 3 == 00);
      t.test(() -> 1 >>> 3 == 0);
      t.test(() -> {
        int i = 1;
        i += 3;
        return i == 4;
      });
      t.test(() -> {
        int i = 1;
        i -= 3;
        return i == -2;
      });
      t.test(() -> {
        int i = 1;
        i *= 3;
        return i == 3;
      });
      t.test(() -> {
        int i = 1;
        i /= 3;
        return i == 0;
      });
      t.test(() -> {
        int i = 1;
        i &= 3;
        return i == 1;
      });
      t.test(() -> {
        int i = 1;
        i |= 3;
        return i == 3;
      });
      t.test(() -> {
        int i = 1;
        i ^= 3;
        return i == 2;
      });
      t.test(() -> {
        int i = 1;
        i %= 3;
        return i == 1;
      });
      t.test(() -> {
        int i = 1;
        i <<= 3;
        return i == 8;
      });
      t.test(() -> {
        int i = 1;
        i >>= 3;
        return i == 0;
      });
      t.test(() -> {
        int i = 1;
        i >>>= 3;
        return i == 0;
      });
    }
  }

  private testLists() {
    try (@Note("Tester is used for testing") Tester t = new Tester()) {
      t.test(() -> {
        List<Integer> l = new Cons<>(1, new Cons<>(2, new Empty<>()));
        return l.filter(i -> i % 2 == 0).toString().equals("{2}");
      });
      t.test(() -> {
        List<Integer> l = new Empty<>();
        for (int i = 10; i > 0; i--) {
          l = new Cons<>(i, l);
        }
        int n = 0;
        for (Integer i : l) {
          assert(i == n++);
        }
      });
      t.test(() -> {
        List<Integer> l = List<>.fromVarargs(2, 4, 0, 2, 2, 1);
        int eleven = 11;
        assert @Note("The \"assert\" statement disables labels until the next "
              + "colon, yet \"? :\" doesn't break anything") false ?
            false: l.foldl((elt, acc) -> elt + acc, 0) ==
              eleven: "Addition is broken";
      });
      t.test(() -> {
        List l = new Empty();
        for (int i = 0; i < 10; i++) {
          l = new Cons(i, l);
        }
        assert l.next().getClass().equals(Integer.class);
        assert !l instanceof List<Integer>;
        l = (List /*) /*/</*>*/String> & java.lang.Iterable<java.lang.String>
            ) l.map(Double::new).map(Double::toString);
        assert l instanceof List<String>;
      });
    }
  }
}
// TODO: end with SUB, not SUB CR LF

