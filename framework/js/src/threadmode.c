#include "threadmode.h"
#include "benchmarkcontroller.h"
#include "header.h"
#include <pthread.h>
#include <unistd.h>

#define MAXSIZE 800
#define SCRIPTNAME "generated.js"

long sleepTime = 2; // seconds
double percentOfDecreasing = 0.9999;

bool interrupted = false;
pthread_mutex_t lock;

/* Number of threads obtained from config */
int threadAmount;

/* Number of run method calls */
int countOfRun = 0;

void *threadLauncher()
{
    int cnt = 0;
    while (!interrupted) {
        cnt++;
        invokeRun();
    }
    pthread_mutex_lock(&lock);
    countOfRun += cnt;
    pthread_mutex_unlock(&lock);
    pthread_exit(NULL);
}

void *singleIteration()
{
    invokeRun();
    pthread_exit(NULL);
}

void warmup()
{
    pthread_t thread;
    if (baseConfigPtr->longBenchmark) {
        pthread_create(&thread, NULL, singleIteration, NULL);
    } else {
        startMeasuring();
        threadsCallRun();
        stopMeasuring();

        long lastMeasure;
        long currentMeasure = getTotalTime();

        do {
            startMeasuring();
            threadsCallRun();
            stopMeasuring();

            lastMeasure = currentMeasure;
            currentMeasure = getTotalTime();
        } while (currentMeasure <= lastMeasure * percentOfDecreasing);
    }
}

void measure()
{
    pthread_t thread;
    startMeasuring();
    pthread_create(&thread, NULL, threadLauncher, NULL);
    sleep(sleepTime);
    interrupted = true;
    pthread_join(thread, NULL);
    stopMeasuring();
}

void threadsCallRun()
{
    pthread_t thread;
    int ret_value = pthread_create(&thread, NULL, singleIteration, NULL);
    if (ret_value) {
        fputs("Multhithread execution failed\n", stderr);
        exit(-1);
    }
    pthread_join(thread, NULL);
}

int threadMode()
{
    char scriptPath[MAXSIZE];
    getcwd(scriptPath, MAXSIZE);
    strcat(scriptPath, "/");
    strcat(scriptPath, SCRIPTNAME);

    startJerryscript();

    launchScript(scriptPath);
    invokeBenchmark();

    invokeSetup();

    fputs("Warmup started\n", stderr);
    warmup();
    fputs("Warmup finished\n", stderr);

    measure();

    fputs("Measurement finished\n", stderr);

    finishJerryscript();

    return countOfRun;
}
