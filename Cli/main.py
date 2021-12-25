import os, sys

script_dir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir+"/../Plugins")

plugins = []
os.chdir(script_dir+"/../Plugins")
for i in os.listdir():
	if i.endswith(".py") and i != "PluginCommon.py":
		# Import the plugin and append it to the list
		exec(f"import {i[:-3]}")  # Sorry.
		plugins.append(eval(i[:-3]))

def get_secret_amount(amount):
    return amount if amount else 0

def run_plugin(plugin):
    try:
        while True:
            print("Do you want to encode or decode?")
            choice = input("(E)ncode or (D)ecode: ").lower()
            if choice == "e":
                process = plugin.encode
            elif choice == "d":
                process = plugin.decode
            else:
                print("error: Invalid choice.")
                continue
            text = input("Enter the text to be encoded/decoded: ")
            secrets = []
            for i in range(0, get_secret_amount(plugin.Info().secrets_needed)):
                print(f"{get_secret_label(plugin.Info().secrets_labels, i)}\n====================\n{get_secret_description(plugin.Info().secrets_help_texts, i)}\n====================")
                secrets.append(input(">> "))
            try:
                print("\nOutput: " + str(process(data=text, secrets=secrets))+"\n")
            except Exception as e:
                print(f"\nError: {e}\n")
            choice = input(f"Do you want to continue using {plugin.Info().name}? (y/n): ").lower()
            if choice == "y":
	        continue
            elif choice == "n":
                return
            else:
                print("error: Invalid choice.")
    except KeyboardInterrupt:
        print("\nExiting...")
        return

def get_secret_label(secrets_labels, index):
    if len(secrets_labels) > index:
        return secrets_labels[index]
    else:
        return f"Secret {index}"

def get_secret_description(secrets_descriptions, index):
    if len(secrets_descriptions) > index:
        return secrets_descriptions[index]
    else:
        return "<No description>"

def plugin_selection():
    while True:
        for c,i in enumerate(plugins):
            print(f"{c}:\t{i.Info().name}")
            print(f"\t{i.Info().description}")
            print("==============================")
        print("\n")
        print("To exit, press Ctrl+C.")
        print("Select a plugin to run:")
        try:
            selection = int(input(">> "))
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except:
            print("error: Invalid selection.")
            continue
        if selection < 0 or selection >= len(plugins):
            print("error: Invalid selection.")
            continue
        run_plugin(plugins[selection])

plugin_selection() # Run the plugin selection
