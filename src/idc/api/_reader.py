import seppl.io
from seppl import Initializable


class Reader(seppl.io.Reader, Initializable):
    """
    Ancestor for dataset readers.
    """
    pass


def parse_reader(reader: str) -> Reader:
    """
    Parses the command-line and instantiates the reader.

    :param reader: the command-line to parse
    :type reader: str
    :return: the reader
    :rtype: Reader
    """
    from seppl import split_args, split_cmdline, args_to_objects
    from idc.registry import available_readers

    if reader is None:
        raise Exception("No reader command-line supplied!")
    valid = dict()
    valid.update(available_readers())
    args = split_args(split_cmdline(reader), list(valid.keys()))
    objs = args_to_objects(args, valid, allow_global_options=False)
    if len(objs) == 1:
        if isinstance(objs[0], Reader):
            result = objs[0]
        else:
            raise Exception("Expected instance of Reader but got: %s" % str(type(objs[0])))
    else:
        raise Exception("Expected to obtain one reader from '%s' but got %d instead!" % (reader, len(objs)))
    return result
