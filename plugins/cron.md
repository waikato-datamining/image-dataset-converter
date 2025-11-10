# cron

* generates: seppl.AnyData

Dummy reader that forwards a string whenever the timestamp defined by the cron-expression is reached. For more information on Cron, see: https://en.wikipedia.org/wiki/Cron

```
usage: cron [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME] -e
            EXPR

Dummy reader that forwards a string whenever the timestamp defined by the
cron-expression is reached. For more information on Cron, see:
https://en.wikipedia.org/wiki/Cron

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -e EXPR, --cron_expr EXPR
                        The cron expression to use: [sec] min hour day month
                        day_of_week (default: None)
```
