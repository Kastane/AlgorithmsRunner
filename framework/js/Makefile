TARGET = Framework.out

OUT_HOST = host
OUT_DEVICE = device

CC_HOST = clang
CC_DEVICE = $(ANDROID_NDK_HOME)/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android$(ANDROID_SDK_VERSION)-clang

JERRY_DIR = $(JERRY_HOME)

INCLUDE_DIR = include
SRC_DIR = src

SRC := $(wildcard $(SRC_DIR)/*)

CFLAGS = \
	-pthread \
	-rdynamic \
	-I$(INCLUDE_DIR)

HOST_FLAGS = -fPIC
DEVICE_FLAGS = -pie

LIB = \
	-ldl \
	-L$(JERRY_DIR)/lib \
	-I$(JERRY_DIR)/include \
	-ljerry-core \
	-ljerry-port-default \
	-ljerry-ext \
	-ljerry-math

.PHONY = all $(OUT_HOST) $(OUT_DEVICE) clean

all: $(OUT_HOST)

$(OUT_HOST): clean
	mkdir -p $(OUT_HOST)
	$(CC_HOST) -o $(OUT_HOST)/$(TARGET) \
	$(SRC) $(CFLAGS) $(HOST_FLAGS) $(LIB)

$(OUT_DEVICE): clean
	mkdir -p $(OUT_DEVICE)
	$(CC_DEVICE) -o $(OUT_DEVICE)/$(TARGET) \
	$(SRC) $(CFLAGS) $(DEVICE_FLAGS) $(LIB)

clean:
	@rm -rf $(OUT_HOST)
	@rm -rf $(OUT_DEVICE)
