# send-email

* accepts: seppl.AnyData

Attaches the incoming file(s) and sends them to the specified email address(es).

```
usage: send-email [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] [--skip] [-d FILE] -f EMAIL -t EMAIL
                  [EMAIL ...] [-s SUBJECT] [-b TEXT]

Attaches the incoming file(s) and sends them to the specified email
address(es).

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -d FILE, --dotenv_path FILE
                        The .env file to load the SMTP environment variables
                        form
                        (SMTP_HOST|SMTP_PORT|SMTP_STARTTLS|SMTP_USER|SMTP_PW);
                        tries to load .env from the current directory if not
                        specified; Supported placeholders: {HOME}, {CWD},
                        {TMP}, {INPUT_PATH}, {INPUT_NAMEEXT},
                        {INPUT_NAMENOEXT}, {INPUT_EXT}, {INPUT_PARENT_PATH},
                        {INPUT_PARENT_NAME} (default: None)
  -f EMAIL, --email_from EMAIL
                        The email address to use for FROM; placeholders get
                        automatically expanded. (default: None)
  -t EMAIL [EMAIL ...], --email_to EMAIL [EMAIL ...]
                        The email address(es) to send the email TO;
                        placeholders get automatically expanded. (default:
                        None)
  -s SUBJECT, --subject SUBJECT
                        The SUBJECT for the email; placeholders get
                        automatically expanded. (default: None)
  -b TEXT, --body TEXT  The email body to use; placeholders get automatically
                        expanded. (default: None)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
* `{INPUT_PATH}`: The directory part of the current input, i.e., `/some/where` of input `/some/where/file.txt`.
* `{INPUT_NAMEEXT}`: The name (incl extension) of the current input, i.e., `file.txt` of input `/some/where/file.txt`.
* `{INPUT_NAMENOEXT}`: The name (excl extension) of the current input, i.e., `file` of input `/some/where/file.txt`.
* `{INPUT_EXT}`: The extension of the current input (incl dot), i.e., `.txt` of input `/some/where/file.txt`.
* `{INPUT_PARENT_PATH}`: The directory part of the parent directory of the current input, i.e., `/some` of input `/some/where/file.txt`.
* `{INPUT_PARENT_NAME}`: The name of the parent directory of the current input, i.e., `where` of input `/some/where/file.txt`.
