import argparse
from typing import List

from seppl.io import Writer, Splitter


def init_splitting_params(writer: Writer, split_names: List[str] = None, split_ratios: List[int] = None):
    """
    Initializes the splitting parameters of the writer.

    :param writer: the writer to initialize
    :type writer: Writer
    :param split_names: the names of the splits, no splitting if None
    :type split_names: list
    :param split_ratios: the integer ratios of the splits (must sum up to 100)
    :type split_ratios: list
    """
    writer.split_names = split_names[:] if (split_names is not None) else None
    writer.split_ratios = split_ratios[:] if (split_ratios is not None) else None
    writer.splitter = None


def add_splitting_params(parser: argparse.ArgumentParser):
    """
    Adds the split ratios/names parameters to the parser.

    :param parser: the parser
    :type parser: argparse.ArgumentParser
    """
    parser.add_argument("-r", "--split_ratios", type=int, default=None, help="The split ratios to use for generating the splits (must sum up to 100)", nargs="+")
    parser.add_argument("-n", "--split_names", type=str, default=None, help="The split names to use for the generated splits.", nargs="+")


def transfer_splitting_params(ns: argparse.Namespace, writer: Writer):
    """
    Transfers the splitting parameters from the parsed namespace into the writer.

    :param ns: the namespace to transfer from
    :type ns: argparse.Namespace
    :param writer: the writer to update
    :type writer: Writer
    """
    writer.split_names = ns.split_names[:] if ((ns.split_names is not None) and (len(ns.split_names) > 0)) else None
    writer.split_ratios = ns.split_ratios[:] if ((ns.split_ratios is not None) and (len(ns.split_ratios) > 0)) else None


def initialize_splitting(writer: Writer):
    """
    Initializes the splitting in the writer.

    :param writer: the writer to initialize, if necessary
    :type writer: Writer
    """
    if not hasattr(writer, "split_names"):
        return
    if (getattr(writer, "split_names") is None) or (getattr(writer, "split_ratios") is None):
        return
    writer.splitter = Splitter(split_ratios=writer.split_ratios, split_names=writer.split_names)
    writer.splitter.initialize()
