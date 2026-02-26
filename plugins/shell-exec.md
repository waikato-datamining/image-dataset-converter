# shell-exec

* generates: str

Executes the external command and forwards the exit code.

```
usage: shell-exec [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] [-e [KEY=VALUE ...]] [-w DIR] [-c CMD]
                  [-C PATH]

Executes the external command and forwards the exit code.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -e [KEY=VALUE ...], --env_vars [KEY=VALUE ...]
                        The environment variable key=value pairs to use for
                        the execution. (default: None)
  -w DIR, --workdir DIR
                        The working directory to use; Supported placeholders:
                        {HOME}, {CWD}, {TMP} (default: None)
  -c CMD, --command CMD
                        The command to execute; Supported placeholders:
                        {HOME}, {CWD}, {TMP} (default: None)
  -C PATH, --command_file PATH
                        The text file with the command to execute; Supported
                        placeholders: {HOME}, {CWD}, {TMP} (default: None)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
