from seppl import Initializable
import seppl.io


class BatchWriter(seppl.io.BatchWriter, Initializable):
    """
    Ancestor for dataset batch writers.
    """
    pass


class StreamWriter(seppl.io.StreamWriter, Initializable):
    """
    Ancestor for dataset stream writers.
    """
    pass
