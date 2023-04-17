#ifndef THREADMODE_H
#define THREADMODE_H

#include "jerryhelper.h"
#include "stdio.h"
#include <stdbool.h>

/* Main logic of threadmode.
    Return number of run calls. */
int threadMode();

/* Warm up. */
void warmup();

/* Method for final measure of benchmark execution time. */
void measure();

/* Create threads which call invokeRun.
    Part of warm up. */
void threadsCallRun();

/* Method for call run and increment calls' number. */
void *threadLauncher();

/* Call run without counting. */
void *singleThreadIteration();

#endif