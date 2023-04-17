# Algorithms runner

### Targets
* Add Rust platform
* Add js platform
* Add settings for P-core and E-core 
* Octane algorithms for platfoms
* SunSpider algorithms
* Develop mobile runner
* Add more results formats
* Develop GC log
* Optimizing framework part


### Host dependencies
* Java 8 (jre, jdk)
* JerryScript (for java host)
* GCC (for JerryScript)
* cmake (for JerryScript)
* Python modules: scipy


### How to setup
* Clone repo

#### Setup Java
* Run ```cd framework/java && make framework_java```

#### Setup QuickJS
```
git clone https://github.com/bellard/quickjs.git
cd quickjs
make -j16
export QJS_PATH=$PWD/qjs
```

### How to run
* Main runner script is `<src_root>/runner/runner.py`
```
usage: runner.py -t TARGET input
```

`input` could be:
- Algorithm: e.g. <src_root>/algorithms/Test/Test1/java/Test.java
- Folder with algorithms: e.g. <src_root>/algorithms/Test

Supported `TARGET` platforms:
- javahost (jh)
- jshost (jsh)

* Fast start Java 
```python3 runner/runner.py -t jh algorithms/Test/Test1/java/Test.java```

* Fast start JavaScript 
```python3 runner/runner.py -t jsh --js-engine="${QJS_PATH}" algorithms/Test/Test1/js/Test.js```

![screenshot](docs/media/screenshot.png)


### Warmup and Measurement:

* `-wt` (`--warmup-iters`) controls the time of warmup iterations. Default 2 seconds.
* `-mt` (`--measure-iters`) controls the time of measure iterations. Default 2 seconds.


### Result of the Algorithm

Algorithm measures:
- Time for execution of one `operation` in nanoseconds (seconds in case of `-g` flag)
- Time of execution whole algorithm including framework stuff
- Max RSS in kilobytes
- Compile time
- Size of the binary

`None` means that algorithm not works for `TARGET` platform

### Authors
* Dmitrii Pashigrev dpashigrev@gmail.com


### Design
* To reduce the noise of the measurement each algorithm runs several times (~100).

### All runner options

  -t, --target
                        Target to run on
  -wt WARMUP_TIME, --warmup-iters WARMUP_ITERS
                        Time for warmuping
  -mt MEASURE_TIME, --measure-iters MEASURE_ITERS
                        Time for measuring
  -g, --seconds         
                        Output result in seconds
  --timeout
                        Timeout for algorithm
```