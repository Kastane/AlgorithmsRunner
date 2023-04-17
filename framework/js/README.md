# JS Framework

### Getting jerryscript
```
git clone https://github.com/jerryscript-project/jerryscript.git
cd jerryscript
```

### Build jerryscript for Host
```
CC=clang python tools/build.py --line-info=ON --error-messages=ON --mem-heap=512000 --cpointer-32bit=ON --cmake-param="-DCMAKE_INSTALL_PREFIX=$(pwd)/build_device_for_benchmarks/" --builddir=$(pwd)/build_device_for_benchmarks --compile-flag=-fPIC --lto OFF --install
```
### Build jerryscript for Device

* Install Android NDK and add to `ANDROID_NDK_HOME` environment variable
  - Get and install NDK `https://developer.android.com/ndk/downloads`
  - Export path to NDK `$ export ANDROID_NDK_HOME=<path_to_ndk_direcotry>`
  - Export SDK version `$ export ANDROID_SDK_VERSION=$(adb shell getprop ro.build.version.sdk)`

* Build jerryscript
```
CC=${ANDROID_NDK_HOME}/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android${ANDROID_SDK_VERSION}-clang python tools/build.py --line-info=ON --error-messages=ON --mem-heap=512000 --cpointer-32bit=ON --cmake-param="-DCMAKE_INSTALL_PREFIX=$(pwd)/build_device_for_benchmarks/" --builddir=$(pwd)/build_device_for_benchmarks --compile-flag=-fPIC --lto OFF --install
```

### Make framework host
```
export JERRY_HOME=</path/to/jerryscript/build/host>
cd </path/to/vm-benchmarks>/framework/js
make host
```

### Make framework for device
```
export JERRY_HOME=</path/to/jerryscript/build/device>
cd </path/to/vm-benchmarks>/framework/js
make device
```
