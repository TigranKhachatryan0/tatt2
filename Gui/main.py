from tkinter import *
import os, sys, threading, time

script_dir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir+"/../Plugins")

class Window:
	def __init__(self):
		self.plugins = []
		os.chdir(script_dir+"/../Plugins")
		for i in os.listdir():
			if i.endswith(".py") and i != "PluginCommon.py":
				# Import the plugin and append it to the list
				exec(f"import {i[:-3]}")  # Sorry.
				self.plugins.append(eval(i[:-3]))
		self.root = Tk()
		self.root.title("Main - TATT")
		self.root.geometry("300x600+10+10")
		self.root.protocol("WM_DELETE_WINDOW", self.quit)
		# Create dropdown menu
		self.menu = Menu(self.root)
		self.file_menu = Menu(self.menu, tearoff=0)
		self.file_menu.add_command(label="Open plugin folder", command=lambda: threading.Thread(target=self.open_plugin_folder).start())
		self.file_menu.add_command(label="Reload plugins", command=self.reload_plugins)
		self.file_menu.add_separator()
		self.file_menu.add_command(label="Quit", command=self.quit)
		self.menu.add_cascade(label="File", menu=self.file_menu)
		self.root.config(menu=self.menu)
		# Create a listbox of plugins
		# Create frame for plugin list
		self.plugin_frame = Frame(self.root)
		self.plugin_frame.pack(side=LEFT, fill=BOTH, expand=1)
		self.plugins_listbox = Listbox(self.plugin_frame, height=20, selectmode=SINGLE, exportselection=0)
		self.plugins_listbox.pack(side=LEFT, fill=BOTH, expand=1)
		self.plugins_listbox.pack()
		for i in self.plugins:
			self.plugins_listbox.insert(END, i.Info().name)
		# Wait until window is ready
		self.root.update_idletasks()
		# Create a scrollbar
		sb = Scrollbar(self.root)
		sb.pack(side=RIGHT, fill=Y)
		sb.config(command=self.plugins_listbox.yview)
		self.plugins_listbox.config(yscrollcommand=sb.set)
		# Warn user about beta version
		self.create_msgbox("Warning", "This app is still beta!\n\nKNOWN BUGS:\n* Scrollbar does not work properly in encode/decode screen.")
		# Wait for user to select a plugin
		self.plugins_listbox.bind("<<ListboxSelect>>", self.plugin_selected)
	def create_copy_window(self, parent, input_textbox, output_textbox):
		def copy_text(text):
			copy_window.clipboard_clear()
			copy_window.clipboard_append(text)
		def copy_onclick():
			if copy_target == "Input":
				copy_text(input_textbox.get("1.0", END))
			else:
				copy_text(output_textbox.get("1.0", END))
			copy_button.config(text="Copied to clipboard", state=DISABLED)
			copy_button.after(1000, lambda: copy_button.config(text="Copy", state=NORMAL))
		copy_window = Toplevel(parent)
		copy_window.title("Copy to clipboard - TATT")
		copy_window.resizable(False, False)
		Label(copy_window, text="Choose copy target:").pack(side=LEFT)
		copy_target = StringVar()
		rb1=Radiobutton(copy_window, text="Input", variable=copy_target, value="Input")
		rb1.pack(side=LEFT)
		rb2=Radiobutton(copy_window, text="Output", variable=copy_target, value="Output")
		rb2.pack(side=LEFT)
		rb1.invoke()
		copy_button=Button(copy_window, text="Copy", command=copy_onclick)
		copy_button.pack(side=LEFT)
	def reload_plugins(self):
		self.plugins = []
		os.chdir(script_dir+"/../Plugins")
		for i in os.listdir():
			if i.endswith(".py") and i != "PluginCommon.py":
				# Import the plugin and append it to the list
				exec(f"import {i[:-3]}")  # Sorry.
				self.plugins.append(eval(i[:-3]))
		# Update listbox
		self.plugins_listbox.delete(0, END)
		for i in self.plugins:
			self.plugins_listbox.insert(END, i.Info().name)
		self.create_msgbox("Reload complete", "Plugins were reloaded successfully.")
	def open_plugin_folder(self):
		if os.name == "nt":
			os.startfile(script_dir+"/../Plugins")
		else:
			os.system("xdg-open "+script_dir+"/../Plugins")
	def create_msgbox(self, title, text, custom_buttons={}):
		mb = Toplevel(self.root)
		mb.title(title)
		mb.resizable(False, False)
		l = Label(mb, text=text)
		l.pack()
		if not "OK" in custom_buttons:
			Button(mb, text="OK", command=mb.destroy).pack(side=RIGHT)
		if len(custom_buttons) > 0:
			for i in custom_buttons:
				def command(i=i):
					mb.destroy()
					custom_buttons[i]()
				Button(mb, text=i, command=command).pack(side=RIGHT)
		# Resize window according to label size
		mb.update_idletasks()
		mb.geometry("%dx%d" % (mb.winfo_width()+20, mb.winfo_height()+5))
		mb.focus_set()
		mb.grab_set()
	def plugin_selected(self, event):
		secrets = []
		def wait_for_secrets():
			secret_list = self.create_secrets_input_window(plugin_window, plugin)
			if isinstance(secret_list, list):
				if len(secrets) != 0:
					secrets.clear()
				secrets.extend(secret_list)
				self.create_msgbox("Success", "Secrets saved!")
				rb1.config(state=NORMAL)
				rb2.config(state=NORMAL)
				rb1.invoke()
				#plugin_window.destroy()
			else:
				self.create_msgbox("Warning", "Secrets were not saved, because the window was closed by the user. Please try again.", custom_buttons={"Try again": wait_for_secrets})
		def submit():
			if plugin_mode.get() == 1:
				output_textbox.config(state=NORMAL)
				output_textbox.delete(1.0, END)
				try:
					output_textbox.insert(END, plugin.encode(data=input_textbox.get("1.0", END).strip(), secrets=secrets))
				except Exception as e:
					self.create_msgbox("Error", str(e))
					output_textbox.insert(END, "Error: "+str(e))
				output_textbox.config(state=DISABLED)
			elif plugin_mode.get() == 2:
				output_textbox.config(state=NORMAL)
				output_textbox.delete(1.0, END)
				try:
					output_textbox.insert(END, plugin.decode(data=input_textbox.get("1.0", END).strip(), secrets=secrets))
				except Exception as e:
					self.create_msgbox("Error", str(e))
					output_textbox.insert(END, "Error: "+str(e))
				output_textbox.config(state=DISABLED)
			else:
				self.create_msgbox("Error", "A choice to encode/decode has to be made. Have you provided secrets?")
		def clear_textboxes():
			input_textbox.delete(1.0, END)
			output_textbox.config(state=NORMAL)
			output_textbox.delete(1.0, END)
			output_textbox.config(state=DISABLED)
		# Get selected plugin
		try:
			selected_id = self.plugins_listbox.curselection()[0]
		except:
			print("Warning: ListBox select event occurred, but there is no any selected element, so the plugin_selected() function will not be executed.")
			return
		selected_name = self.plugins_listbox.get(selected_id)
		# Create window
		plugin_window = Toplevel(self.root)
		plugin_window.title(selected_name)
		# Find plugin
		plugin = self.plugins[selected_id]
		# Create two textboxes alongside each other
		# One for input and one for output
		textbox_frame = Frame(plugin_window)
		textbox_frame.pack(side=TOP, fill=BOTH, expand=1)
		input_textbox = Text(textbox_frame, height=20, width=50, wrap=WORD)
		input_textbox.pack(side=LEFT, fill=BOTH, expand=1)
		output_textbox = Text(textbox_frame, height=20, width=50, wrap=WORD, state=DISABLED)
		output_textbox.pack(side=LEFT, fill=BOTH, expand=1)
		# Create a scrollbar
		sb = Scrollbar(textbox_frame)
		sb.pack(side=RIGHT, fill=Y)
		plugin_mode = IntVar()
		# Create two radiobuttons to choose between encoding and decoding in one row
		rb1 = Radiobutton(plugin_window, text="Encode", variable=plugin_mode, value=1)
		rb2 = Radiobutton(plugin_window, text="Decode", variable=plugin_mode, value=2)
		rb1.pack(side=LEFT)
		rb2.pack(side=LEFT)
		if plugin.Info().secrets_needed:
			rb1.configure(state=DISABLED)
			rb2.configure(state=DISABLED)
		else:
			rb1.invoke()
		# Create a button to run the plugin
		Button(plugin_window, text="Submit", command=submit).pack(side=RIGHT)
		# Create a button to provide secrets
		provide_secrets_button=Button(plugin_window, text="Provide Secrets", command=wait_for_secrets, state=DISABLED)
		provide_secrets_button.pack(side=RIGHT)
		if plugin.Info().secrets_needed:
			provide_secrets_button.config(state=NORMAL)
		# Create a button to clear the input textbox with left margin of 10 pixel
		Button(plugin_window, text="Clear", command=clear_textboxes).pack(side=LEFT, padx=10)
		Button(plugin_window, text="Copy...", command=lambda: self.create_copy_window(plugin_window, input_textbox, output_textbox)).pack(side=LEFT)
		plugin_window.focus_set()
		plugin_window.wait_window()
	def create_secrets_input_window(self, parent, plugin):
		secrets = []
		input_window = Toplevel(parent)
		input_window.geometry("600x300+10+10")
		input_window.title(f"Enter secrets for {plugin.Info().name}")
		input_window.resizable(False, False)
		# Create a label to show secret count
		secret_count_label = Label(input_window, text=f"{len(secrets)} out of {plugin.Info().secrets_needed} secrets entered", fg="gray")
		secret_count_label.pack(side=TOP, fill=X)
		# Create a label to show secret label
		secret_label = Label(input_window)
		if len(plugin.Info().secrets_labels) > len(secrets):
			secret_label.config(text=plugin.Info().secrets_labels[len(secrets)])
		else:
			secret_label.config(text=f"Secret {len(secrets)+1}")
		input_window.update_idletasks()
		# Change secret label font size
		secret_label.config(font=("Helvetica", int(secret_label.winfo_reqheight()+1)))
		secret_label.pack(side=TOP, fill=X)
		# Create a word-wrapped label to show secret description
		secret_description_label = Label(input_window, wraplength=input_window.winfo_width()-20)
		if len(plugin.Info().secrets_help_texts) > len(secrets):
			secret_description_label.config(text=plugin.Info().secrets_help_texts[len(secrets)])
		else:
			secret_description_label.config(text="<No description available>")
		secret_description_label.pack()
		# Create a textbox to enter secret
		secret_textbox = Text(input_window, height=10, width=10, wrap=WORD)
		secret_textbox.pack(side=TOP, fill=X)
		def submit_secret():
			# Get secret
			secrets.append(secret_textbox.get("1.0", END).strip())
			# Delete secret from textbox
			secret_textbox.delete(1.0, END)
			if len(secrets) == plugin.Info().secrets_needed:
				# If all secrets are entered, close the window
				input_window.destroy()
			elif len(secrets)+1 == plugin.Info().secrets_needed:
				# If all secrets except the last one are entered, change submit button to "Finish"
				submit_button.config(text="Finish")
			if len(plugin.Info().secrets_labels) > len(secrets):
				# If there is an available label, change the secret label to it 
				secret_label.config(text=plugin.Info().secrets_labels[len(secrets)])
			else:
				# If there is no available label, change the secret label to "Secret X"
				secret_label.config(text=f"Secret {len(secrets)+1}")
			# Update secret count label
			secret_count_label.config(text=f"{len(secrets)} out of {plugin.Info().secrets_needed} secrets entered")
			# Change secret description label
			if len(plugin.Info().secrets_help_texts) > len(secrets):
				# If there is an available description, change the secret description label to it
				secret_description_label.config(text=plugin.Info().secrets_help_texts[len(secrets)])
			else:
				# If there is no available description, change the secret description to "No description available"
				secret_description_label.config(text="<No description available>")
			print(secrets)
		# Create a button to submit secret
		submit_button = Button(input_window, text="Submit", command=submit_secret)
		submit_button.pack(side=TOP)
		# Wait until window is destroyed
		input_window.wait_window()
		return secrets if len(secrets) == plugin.Info().secrets_needed else None
	def quit(self, event=None):
		self.root.destroy()
		sys.exit()

window = Window()
window.root.mainloop()
