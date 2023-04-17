#include "benchmarkcontroller.h"
#include "header.h"
#include "threadmode.h"
#include <dlfcn.h>
#include <inttypes.h>
#include <math.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>

#define _GNU_SOURCE

BenchmarkController bController = {false, false, 0, 0, 0};

void startMeasuring()
{
    clock_gettime(CLOCK_REALTIME, &bController.startTime);
}

void stopMeasuring()
{
    clock_gettime(CLOCK_REALTIME, &bController.stopTime);
}

long getTotalTime()
{
    return 1000000000 *
               (bController.stopTime.tv_sec - bController.startTime.tv_sec) +
           (bController.stopTime.tv_nsec - bController.startTime.tv_nsec);
}

struct BaseConfig *baseConfigPtr;

void startBenchmarkController()
{
    void *handle = dlopen("GeneratedConfig.so", RTLD_LOCAL | RTLD_LAZY);
    if (handle == NULL) {
        fprintf(stderr, "Library is absent\n");
        exit(-1);
    }

    baseConfigPtr = (struct BaseConfig *)dlsym(handle, "baseConfig");
    if (baseConfigPtr == NULL) {
        fprintf(stderr, "baseConfig is failed");
    }

    fprintf(stderr, "Current benchmark: %s\n", baseConfigPtr->benchmarkName);

    if (0 != baseConfigPtr->asyncAmount) {
        fputs("async case not implemented for this framework\n", stderr);
        exit(0);
    } else {
        if (0 != baseConfigPtr->threadAmount) {
            if (baseConfigPtr->threadAmount > 1) {
                fputs("Warning: JS framework doesn't support multithreading. "
                      "Exit\n",
                      stderr);
                exit(0);
            }
            fputs("threading case\n", stderr);
            int total = threadMode();
            if (0 != total)
                printf("Benchmark result: %s %f\n",
                       baseConfigPtr->benchmarkName,
                       ((double)getTotalTime() / total));
            else
                fputs("Threadmode failed\nRun method never called\n", stderr);
        } else {
            fputs("threadAmount and asyncAmount can't be 0 at same time\n",
                  stderr);
        }
    }
}
