#include "jerryhelper.h"
#include "header.h"

void startJerryscript()
{
    jerry_init(JERRY_INIT_EMPTY);
    jerryx_handler_register_global((const jerry_char_t *)"print",
                                   jerryx_handler_print);
}

void finishJerryscript()
{
    jerry_cleanup();
}

void invokeSetup()
{
    char *script = "benhcmark.setup();";
    jerry_value_t ret_val = jerry_eval((const jerry_char_t *)script,
                                       strlen(script) - 1, JERRY_PARSE_NO_OPTS);
    jerry_release_value(ret_val);
}

void invokeRun()
{
    char *script = "benchmark.run();";
    jerry_value_t ret_val = jerry_eval((const jerry_char_t *)script,
                                       strlen(script) - 1, JERRY_PARSE_NO_OPTS);
    jerry_release_value(ret_val);
}

void invokeBenchmark()
{
    char *tmp1 = "var benchmark = new ";
    char *tmp2 = baseConfigPtr->benchmarkName;
    char *tmp3 = "();";

    char script[strlen(tmp1) + strlen(tmp2) + strlen(tmp3)];

    strcpy(script, tmp1);
    strcat(script, tmp2);
    strcat(script, tmp3);

    jerry_value_t ret_val = jerry_eval((const jerry_char_t *)script,
                                       strlen(script) - 1, JERRY_PARSE_NO_OPTS);
    jerry_release_value(ret_val);
}

void launchScript(char *filename)
{
    char *script = getFileContent(filename);
    jerry_value_t ret_val;
    ret_val = jerry_eval((const jerry_char_t *)script, strlen(script) - 1,
                         JERRY_PARSE_NO_OPTS);
    jerry_release_value(ret_val);
}

char *getFileContent(char *filename)
{
    FILE *fd;
    char *buffer;

    fd = fopen(filename, "rb");
    if (NULL == fd) {
        fprintf(stderr, "Can't open file: %s\n", filename);
        exit(1);
    }

    fseek(fd, 0L, SEEK_END);
    size_t contentSize = ftell(fd);
    rewind(fd);

    buffer = calloc(1, contentSize + 1);
    if (!buffer) {
        fclose(fd);
        fputs("Memory alloc fails\n", stderr);
        exit(1);
    }

    if (1 != fread(buffer, contentSize, 1, fd)) {
        fclose(fd);
        free(buffer);
        fputs("Entire read fails\n", stderr);
        exit(1);
    }

    fclose(fd);
    return buffer;
}
