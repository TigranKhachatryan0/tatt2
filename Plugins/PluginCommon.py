import argparse

class PluginInfo:
    name               = "Unidentified Plugin"
    description        = "<No description>"
    secrets_needed     = None
    secrets_labels     = []
    secrets_help_texts = []

class Info(PluginInfo):
    def __init__(self):
        pass

def encode(**kwargs):
    raise NotImplementedError("This plugin does not support encoding")

def decode(**kwargs):
    raise NotImplementedError("This plugin does not support decoding")

def CliHandler(plugin_info, encode_function, decode_function):
    args = argparse.ArgumentParser(description=plugin_info.description)
    args.add_argument("-d", "--decode", action="store_true", help="Decode data")
    args.add_argument("data", nargs="?", help="Data to encode/decode")
    args.add_argument("secret", nargs="*", help="Secret(s) to use")
    args = args.parse_args()
    secrets = args.secret
    try:
        if args.decode:
            result=decode_function(data=args.data, secrets=secrets)
        else:
            result=encode_function(data=args.data, secrets=secrets)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
