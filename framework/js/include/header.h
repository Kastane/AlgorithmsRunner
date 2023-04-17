#ifndef HEADER_H
#define HEADER_H

#include <stdbool.h>

struct BaseConfig {
    bool longBenchmark;
    int threadAmount;
    int asyncAmount;
    char *benchmarkName;
    char *workDir;
};

extern char *scriptPath;
extern char *benchPath;
extern struct BaseConfig *baseConfigPtr;

#endif