import sublime, sublime_plugin
import os, subprocess, codecs

try:
  import commands
except ImportError:
  pass

PLUGIN_FOLDER = os.path.dirname(os.path.realpath(__file__))
SETTINGS_LINE = 17
NODE_LINE = 39

class HtmlprettifyCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    filePath = self.view.file_name()
    setings = " && ".join([
      "indent_size: 1",
      "indent_char: \t",
      "wrap_line_length: 250",
      "brace_style: collapse",
      "unformatted: ['a', 'sub', 'sup', 'b', 'i', 'u']",
      "preserve_newlines: true",
      "max_preserve_newlines: 5"
    ])

    # Get the current text in the buffer.
    bufferText = self.view.substr(sublime.Region(0, self.view.size()))
    # ...and save it in a temporary file. This allows for scratch buffers
    # and dirty files to be beautified as well.
    tempName = ".__temp__"
    tempPath = PLUGIN_FOLDER + '/' + tempName
    f = codecs.open(tempPath, mode='w', encoding='utf-8')
    f.write(bufferText)
    f.close()

    # Simply using `node` without specifying a path sometimes doesn't work :(
    # http://nodejs.org/#download
    # https://github.com/victorporof/Sublime-JSHint#oh-noez-command-not-found
    node = "node" if exists_in_path("node") else "/usr/local/bin/node"

    try:
      scriptPath = PLUGIN_FOLDER + "/scripts/run.js"
      output = get_output([node, scriptPath, tempPath, filePath or "?", setings])
    except:
      msg = "Node.js was not found in the default path. Please specify the location."
      if sublime.ok_cancel_dialog(msg):
        open_htmlprettify(self.view.window(), NODE_LINE)
      else:
        msg = "You won't be able to use this plugin without specifying the path to Node.js."
        sublime.error_message(msg)
      return

    # We're done with beautifying, remove the temporary file and change the
    # text shown in the current buffer.
    os.remove(tempPath)
    self.view.erase_regions("jshint_errors");

    if len(output) > 0:
      self.view.replace(edit, sublime.Region(0, self.view.size()), output.decode("utf-8"))
    if filePath != None:
      self.view.run_command("save")

class HtmlprettifySetOptionsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    open_htmlprettify(self.view.window(), SETTINGS_LINE)

class HtmlprettifySetNodePathCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    open_htmlprettify(self.view.window(), NODE_LINE)

def exists_in_path(cmd):
  # Can't search the path if a directory is specified.
  assert not os.path.dirname(cmd)
  path = os.environ.get("PATH", "").split(os.pathsep)
  extensions = os.environ.get("PATHEXT", "").split(os.pathsep)

  # For each directory in PATH, check if it contains the specified binary.
  for directory in path:
    base = os.path.join(directory, cmd)
    options = [base] + [(base + ext) for ext in extensions]
    for filename in options:
      if os.path.exists(filename):
        return True

  return False

def get_output(cmd):
  if int(sublime.version()) < 3000:
    if sublime.platform() != "windows":
      # Handle Linux and OS X in Python 2.
      run = '"' + '" "'.join(cmd) + '"'
      return commands.getoutput(run)
    else:
      # Handle Windows in Python 2.
      return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
  else:
    # Handle all OS in Python 3.
    run = '"' + '" "'.join(cmd) + '"'
    return subprocess.check_output(run, stderr=subprocess.STDOUT, shell=True)

def open_htmlprettify(window, line):
  window.open_file(PLUGIN_FOLDER + "/HTMLPrettify.py:" + str(line), sublime.ENCODED_POSITION)
