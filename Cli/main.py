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

def run_plugin(plugin):
    while True:
        print("Do you want to encode or decode?")
        choice = input("(E)ncode or (D)ecode: ").lower()
        if choice == "e":
            process = plugin.encode
            break
        elif choice == "d":
            process = plugin.decode
            break
        else:
            print("error: Invalid choice.")
            continue
    try:
        text = input("Enter the text to be encoded/decoded: ")
        secrets = []
        for i in range(0, plugin.Info().secrets_needed):
            print(f"{get_secret_label(plugin.Info().secrets_labels, i)}\n====================\n{get_secret_description(plugin.Info().secrets_help_texts, i)}\n====================")
            secrets.append(input(">> "))
        try:
            print("Output: " + process(data=text, secrets=secrets))
        except Exception as e:
            print(f"Error: {e}")
        choice = input("Do you want to continue? (y/n): ").lower()
        if choice == "y":
            run_plugin(plugin)
        elif choice == "n":
            return
        else:
            print("error: Invalid choice.")
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()

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
        should_exit = input("Do you want to exit? (y/n): ").lower()
        if should_exit == "y":
            break
        elif should_exit == "n":
            continue
        else:
            print("error: Invalid choice.")
            continue

plugin_selection() # Run the plugin selection
