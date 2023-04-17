#ifndef BENCHMARK_CONTROLLER_H
#define BENCHMARK_CONTROLLER_H

#include <stdbool.h>
#include <time.h>

typedef struct {
    volatile bool warmupState;
    volatile bool measurementState;

    struct timespec startTime;
    struct timespec stopTime;

} BenchmarkController;

void startMeasuring();

void stopMeasuring();

/* return time in nanoseconds */
long getTotalTime();

void startBenchmarkController();

#endif