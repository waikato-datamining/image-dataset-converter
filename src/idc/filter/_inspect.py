import argparse
import os
import sys
from typing import List

from seppl import get_metadata, AnyData
from seppl.io import Filter
from wai.logging import LOGGING_WARNING
from idc.api import make_list, flatten_list

MODE_INTERACTIVE = "interactive"
MODE_NONINTERACTIVE = "non-interactive"
MODES = [
    MODE_INTERACTIVE,
    MODE_NONINTERACTIVE,
]

OUTPUT_STDOUT = "stdout"
OUTPUT_STDERR = "stderr"
OUTPUT_LOGGER = "logger"
OUTPUT_FILE = "file"
OUTPUTS = [
    OUTPUT_STDOUT,
    OUTPUT_STDERR,
    OUTPUT_LOGGER,
    OUTPUT_FILE,
]


class Inspect(Filter):
    """
    Allows inspecting the data flowing through the pipeline.
    """

    def __init__(self, mode: str = MODE_INTERACTIVE, output: str = OUTPUT_STDOUT,
                 output_file: str = None, meta_data_keys: List[str] = None, show_image: bool = False,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param mode: the mode to operate in
        :type mode: str
        :param output: how to output the data
        :type output: str
        :param output_file: the file to store the data in (in case of OUTPUT_FILE)
        :type output_file: str
        :param meta_data_keys: the keys of the meta-data value to output
        :type meta_data_keys: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)

        if mode not in MODES:
            raise Exception("Unsupported mode: %s" % mode)
        if output not in OUTPUTS:
            raise Exception("Unsupported output: %s" % output)

        self.mode = mode
        self.output = output
        self.output_file = output_file
        self.meta_data_keys = meta_data_keys
        self.show_image = show_image

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "inspect"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Allows inspecting the data flowing through the pipeline."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [AnyData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [AnyData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-m", "--mode", choices=MODES, default=MODE_INTERACTIVE, help="The mode to operate in.")
        parser.add_argument("-o", "--output", choices=OUTPUTS, default=OUTPUT_STDOUT, help="How to output the data.")
        parser.add_argument("--output_file", type=str, default=None, help="The file to store the data in, in case of output '" + OUTPUT_FILE + "'.")
        parser.add_argument("-k", "--meta-data-key", metavar="KEY", type=str, help="The meta-data value to output", required=False, nargs="*")
        parser.add_argument("-i", "--show_image", action="store_true", help="Whether to display the image.")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.mode = ns.mode
        self.output = ns.output
        self.output_file = ns.output_file
        self.meta_data_keys = ns.meta_data_key
        self.show_image = ns.show_image

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if (self.output == OUTPUT_FILE) and ((self.output_file is None) or (self.output_file == "")):
            raise Exception("No output file provided!")
        if (self.output == OUTPUT_FILE) and (os.path.exists(self.output_file)):
            if os.path.isdir(self.output_file):
                raise Exception("Output file points to directory: %s" % self.output_file)
            os.remove(self.output_file)

    def _assemble_data(self, data) -> str:
        """
        Assembles the requested data from the record.

        :param data: the record to get the data from
        :return: the generated string
        :rtype: str
        """
        result = []

        if self.meta_data_keys is not None:
            meta = get_metadata(data)
            if meta is not None:
                for key in self.meta_data_keys:
                    if key in meta:
                        result.append("meta[%s]: %s" % (key, meta[key]))

        return "\n".join(result)

    def _output_data(self, data: str):
        """
        Outputs the requested data.
        """
        if self.output == OUTPUT_STDOUT:
            print(data)
        elif self.output == OUTPUT_STDERR:
            print(data, file=sys.stderr)
        elif self.output == OUTPUT_FILE:
            with open(self.output_file, "a") as fp:
                fp.write(data)
                fp.write("\n")
        else:
            raise Exception("Unsupported output: %s" % self.output)

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            self._output_data(self._assemble_data(item))

            if self.show_image:
                img = item.image
                if img is None:
                    self.logger().error("Failed to obtain image for display!")
                else:
                    img.show()

            if self.mode == MODE_INTERACTIVE:
                while True:
                    print("Continue (yes/no/skip)? ")
                    answer = input()
                    answer = answer.lower()
                    if (answer == "no") or (answer == "n"):
                        sys.exit(0)
                    elif (answer == "skip") or (answer == "s"):
                        break
                    elif (answer == "yes") or (answer == "y"):
                        result.append(item)
                        break
                    else:
                        print("Invalid choice!")
            else:
                result.append(item)

        return flatten_list(result)
