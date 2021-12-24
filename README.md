# tatt2
TATT is a text encoding/decoding tool

### Do not use CLI yet if the plugin needs secrets

You don't need to install it anywhere.
Just open the respective `main.py` file which can be
found in the Gui (graphical) and Cli (command-line) folders.

Do not move the `main.py` files, because they always import
plugins from the `../Plugins/` directory

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
  data = kwargs[data]
  secrets = kwargs[secrets]
  ...
  result = str()
  return result

def decode(**kwargs):
  data = kwargs[data]
  secrets = kwargs[secrets]
  ...
  result = str()
  return result

if __name__ == '__main__':
  plugin_info = Info()
  CliHandler(plugin_info, encode, decode)
```
