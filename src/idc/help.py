import os

from idc.api import DataTypeSupporter, data_types_help
from idc.registry import REGISTRY
from seppl import OutputProducer, InputConsumer, classes_to_str, get_aliases, has_aliases, Plugin
from seppl.placeholders import PlaceholderSupporter, placeholder_help

HELP_FORMAT_TEXT = "text"
HELP_FORMAT_MARKDOWN = "markdown"
HELP_FORMATS = [
    HELP_FORMAT_TEXT,
    HELP_FORMAT_MARKDOWN,
]


def add_plugins_to_index(heading: str, plugins: dict, help_format: str, lines: list):
    """
    Appends a plugin section to the output list.

    :param heading: the heading of the section
    :type heading: str
    :param plugins: the plugins dictionary to add
    :type plugins: dict
    :param help_format: the type of output to generate
    :type help_format: str
    :param lines: the output lines to append the output to
    :type lines: list
    """
    plugin_names = sorted(plugins.keys())
    if len(plugin_names) == 0:
        return
    if help_format == HELP_FORMAT_MARKDOWN:
        lines.append("## " + heading)
        for name in plugin_names:
            if REGISTRY.is_alias(name):
                continue
            lines.append("* [%s](%s.md)" % (name, name))
        lines.append("")
    elif help_format == HELP_FORMAT_TEXT:
        lines.append(heading)
        lines.append("-" * len(heading))
        for name in plugin_names:
            if REGISTRY.is_alias(name):
                continue
            lines.append("- %s" % name)
        lines.append("")
    else:
        raise Exception("Unsupported format for index: %s" % help_format)


def generate_plugin_usage(plugin_name: str, help_format: str = HELP_FORMAT_TEXT, heading_level: int = 1,
                          output_path: str = None):
    """
    Generates the usage help screen for the specified plugin.

    :param plugin_name: the plugin to generate the usage for (name used on command-line)
    :type plugin_name: str
    :param help_format: the format to use for the output
    :type help_format: str
    :param heading_level: the level to use for the heading (markdown)
    :type heading_level: int
    :param output_path: the directory (automatically generates output name from plugin name and output format) or file to store the generated help in, uses stdout if None
    :type output_path: str
    """
    if help_format not in HELP_FORMATS:
        raise Exception("Unhandled help format: %s" % help_format)

    if plugin_name not in REGISTRY.all_plugins():
        raise Exception("Unknown plugin: %s" % plugin_name)

    plugin = REGISTRY.all_plugins()[plugin_name]

    result = ""
    if help_format == HELP_FORMAT_TEXT:
        suffix = ".txt"
        result += "\n" + plugin_name + "\n" + "=" * len(plugin_name) + "\n"
        if isinstance(plugin, InputConsumer):
            result += "accepts: " + classes_to_str(plugin.accepts(), clean=True) + "\n"
        if isinstance(plugin, OutputProducer):
            result += "generates: " + classes_to_str(plugin.generates(), clean=True) + "\n"
        if has_aliases(plugin):
            result += "alias(es): " + ", ".join(get_aliases(plugin)) + "\n"
        result = result.strip()
        result += "\n\n"
        result += plugin.format_help() + "\n"
        if isinstance(plugin, DataTypeSupporter):
            result += "\n" + data_types_help(markdown=False) + "\n"
        if isinstance(plugin, PlaceholderSupporter):
            result += "\n" + placeholder_help(markdown=False, obj=plugin) + "\n"
    elif help_format == HELP_FORMAT_MARKDOWN:
        suffix = ".md"
        result += "#"*heading_level + " " + plugin_name + "\n"
        result += "\n"
        if isinstance(plugin, InputConsumer):
            result += "* accepts: " + classes_to_str(plugin.accepts(), clean=True) + "\n"
        if isinstance(plugin, OutputProducer):
            result += "* generates: " + classes_to_str(plugin.generates(), clean=True) + "\n"
        if has_aliases(plugin):
            result += "* alias(es): " + ", ".join(get_aliases(plugin)) + "\n"
        result = result.strip()
        result += "\n\n"
        result += plugin.description() + "\n"
        result += "\n"
        result += "```\n"
        result += plugin.format_help()
        result += "```\n"
        if isinstance(plugin, DataTypeSupporter):
            result += "\n" + data_types_help(markdown=True) + "\n"
        if isinstance(plugin, PlaceholderSupporter):
            result += "\n" + placeholder_help(markdown=True, obj=plugin) + "\n"
    else:
        raise Exception("Unhandled help format: %s" % help_format)

    if output_path is None:
        print(result)
    else:
        if os.path.isdir(output_path):
            output_file = os.path.join(output_path, plugin.name() + suffix)
        else:
            output_file = output_path
        with open(output_file, "w") as fp:
            fp.write(result)
