# tatt2
TATT is a text encoding/decoding tool

You don't need to install it anywhere.
Just open the respective `main.py` file which can be
found in the Gui (graphical) and Cli (command-line) folders.

Do not move the `main.py` files, because they always import
plugins from the `../Plugins/` directory

Plugins' `encode()` and `decode()` functions need to **ALWAYS return strings (str)**

Example plugin:

```py
from PluginCommon import *

class Info(PluginInfo):
  def __init__(self):
    self.name = "My plugin"
    self.description = "A short description about my plugin"
    self.secrets_needed = 2
    self.secrets_labels = ["Label for Secret 1", "Label for Secret 2"]
    self.secrets_help_texts = ["A description about Secret 1", "A description about Secret 2"]

def encode(**kwargs):
  data = kwargs["data"]
  secrets = kwargs["secrets"]
  ...
  result = f"Encoding works!\nSecrets: {secrets}"
  return result

def decode(**kwargs):
  data = kwargs["data"]
  secrets = kwargs["secrets"]
  ...
  result = f"Decoding works!\nSecrets: {secrets}"
  return result

if __name__ == '__main__':
  plugin_info = Info()
  CliHandler(plugin_info, encode, decode)
```

It is possible for your plugin to not require any secrets at all:
```py
from PluginCommon import *

class Info(PluginInfo):
  def __init__(self):
    self.name = "My second plugin"
    self.description = "A short description about my second plugin"

def encode(**kwargs):
  data = kwargs["data"]
  result = "Encoding works!"
  return result

def decode(**kwargs):
  data = kwargs["data"]
  result = "Decoding works!"
  return result

if __name__ == '__main__':
  plugin_info = Info()
  CliHandler(plugin_info, encode, decode)
```
