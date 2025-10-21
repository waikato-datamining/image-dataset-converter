# get-email

* generates: str

Retrieves emails from the specified IMAP folder, saves the attachments in the specified folder and forwards the file names of the saved attachments as list. If the number of polls without any new messages reaches the 'poll_count' threshold, the polling switches from the 'poll_wait' interval to 'poll_wait_slow'. It will automatically reset the next time a new message is encountered.

```
usage: get-email [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [-d FILE] [-f FOLDER] [-u] [-R] [-r REGEXP]
                 -o DIR [-w SECONDS] [-W SECONDS] [-c THRESHOLD] [-m MAX]
                 [-F PLACEHOLDER] [-S PLACEHOLDER]

Retrieves emails from the specified IMAP folder, saves the attachments in the
specified folder and forwards the file names of the saved attachments as list.
If the number of polls without any new messages reaches the 'poll_count'
threshold, the polling switches from the 'poll_wait' interval to
'poll_wait_slow'. It will automatically reset the next time a new message is
encountered.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -d FILE, --dotenv_path FILE
                        The .env file to load the IMAP environment variables
                        form (IMAP_HOST|IMAP_PORT|IMAP_USER|IMAP_PW); tries to
                        load .env from the current directory if not specified;
                        Supported placeholders: {HOME}, {CWD}, {TMP} (default:
                        None)
  -f FOLDER, --folder FOLDER
                        The IMAP folder to obtain emails from. (default:
                        INBOX)
  -u, --only_unseen     Whether to only retrieve unseen/new emails. (default:
                        False)
  -R, --mark_as_read    Whether to mark the emails as read after retrieval.
                        (default: False)
  -r REGEXP, --regexp REGEXP
                        The regular expression that the attachment file names
                        must match. (default: None)
  -o DIR, --output_dir DIR
                        The directory to store the attachments in; Supported
                        placeholders: {HOME}, {CWD}, {TMP} (default: None)
  -w SECONDS, --poll_wait SECONDS
                        The poll interval in seconds (default: 30.0)
  -W SECONDS, --poll_wait_slow SECONDS
                        The poll interval in seconds during slow operation
                        (default: 180.0)
  -c THRESHOLD, --poll_count THRESHOLD
                        The maximum number of 'empty' polls that are allowed
                        before switching from 'poll_wait' to 'poll_wait_slow'.
                        (default: 10)
  -m MAX, --max_poll MAX
                        The maximum number of times to poll the folder; use <=
                        for infinite polling. (default: None)
  -F PLACEHOLDER, --from_placeholder PLACEHOLDER
                        The optional placeholder name to store the FROM email
                        address under, without curly brackets. (default: None)
  -S PLACEHOLDER, --subject_placeholder PLACEHOLDER
                        The optional placeholder name to store the SUBJECT
                        under, without curly brackets. (default: None)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
