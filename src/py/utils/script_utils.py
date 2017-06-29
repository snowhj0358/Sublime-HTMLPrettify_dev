# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Various utility functions used by this plugin"""

from __future__ import print_function
from sublime import ok_cancel_dialog

from .constants import DIAGNOSTICS_MARKER_BEGIN, DIAGNOSTICS_MARKER_END
from .constants import PRETTIFIED_CODE_MARKER_BEGIN, PRETTIFIED_CODE_MARKER_END
from .paths import get_root_dir, get_plugin_user_dir, get_main_js_file
from .env_utils import NodeNotFoundError, NodeRuntimeError, run_node_command
from .window_utils import get_pref, open_sublime_settings
from .web_utils import file_bug


def run_main_js(args):
    """Runs the main node.js script and returns the generated output"""
    return run_node_command([get_main_js_file()] + args)


def get_output_between(output, first, second):
    """Gets part of the output generated by the node.js scripts between two string markers"""
    start = output.find(first)
    end = output.find(second)
    return output[start + len(first) + 1:end - 1].decode("utf-8")


def get_diagnostics(output):
    """Gets the diagnostics part of the output generated by the node.js scripts"""
    start = DIAGNOSTICS_MARKER_BEGIN
    end = DIAGNOSTICS_MARKER_END
    return get_output_between(output, start, end)


def get_prettified_code(output):
    """Gets the prettified text part of the output generated by the node.js scripts"""
    start = PRETTIFIED_CODE_MARKER_BEGIN
    end = PRETTIFIED_CODE_MARKER_END
    return get_output_between(output, start, end)


def prettify(args):
    """Prettifies the code at the given file path"""
    stdout = run_main_js(args + [get_plugin_user_dir(), get_root_dir()])
    prettified_code = get_prettified_code(stdout)
    output_diagnostics = get_diagnostics(stdout)
    return prettified_code, output_diagnostics


def prettify_verbose(window, args):
    """Prettifies the code at the given file path and handles errors and exceptions"""

    def handle_node_error(err):
        print(err)
        msg = "Node.js was not found in the default path. Please specify the location."
        if ok_cancel_dialog(msg):
            open_sublime_settings(window)
        return None

    def handle_runtime_error(err):
        print(err)
        msg = "A runtime error was encountered in the prettifier. Care to file a bug?"
        if ok_cancel_dialog(msg):
            file_bug()
        return None

    def handle_unknown_error(err):
        print(err)
        msg = "An unhandled error was encountered while prettifying. Care to file a bug?"
        if ok_cancel_dialog(msg):
            file_bug()
        return None

    try:
        prettified_code, output_diagnostics = prettify(args)
    except NodeNotFoundError as err:
        return handle_node_error(err)
    except NodeRuntimeError as err:
        return handle_runtime_error(err)
    except BaseException as err:
        return handle_unknown_error(err)

    if output_diagnostics and get_pref("print_diagnostics"):
        print(output_diagnostics)

    return prettified_code
