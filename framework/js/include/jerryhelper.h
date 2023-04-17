#ifndef JSUTILS_H
#define JSUTILS_H

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "jerryscript-ext/handler.h"
#include "jerryscript.h"

/* Run js files */
void launchScript(char *filename);

/* Use jerryscript engine to call setup() method from script */
void invokeSetup();

/* Use jerryscript engine to call run() method from script */
void invokeRun();

/* Create new benchmark object */
void invokeBenchmark();

/* Init Jerryscrypt */
void startJerryscript();

/* Release all values */
void finishJerryscript();

/* Load file content into char buffer */
char *getFileContent(char *filename);

#endif