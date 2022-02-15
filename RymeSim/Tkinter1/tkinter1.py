from tkinter import *


def open_connection():
	"""Opens the connection with the server"""

	pass


def close_connection():
	"""Closes the connection with the server"""

	pass


def send_data():
	"""Sends the selected/writen command"""

	if len(entry1.get()) > 0:
		message(entry1.get())
		entry1.delete(0, "end")


def message(msg):
	"""Appends a message into the messages list"""

	if len(messages) >= 10:
		del messages[0]
	messages.append(msg)
	display_msgs()


def display_msgs():
	"""Displays the stored messages into the messages box"""

	msg_string = ""
	for msg in messages:
		msg_string += msg + "\n"

	msg_box["text"] = msg_string


messages = []

win = Tk()
frame1 = Frame()
frame1.grid(column=0, row=0, columnspan=3)

# Centrado de ventana en pantalla
win_w, win_h = 450, 350
screen_w, screen_h = win.winfo_screenwidth(), win.winfo_screenheight()
# win.geometry(f"{win_w}x{win_h}+{int(screen_w*0.5-win_w*0.5)}+{int(screen_h*0.5-win_h*0.5)}")
win.resizable(False, False)

button2 = Button(frame1, text="• Conectar", command=open_connection, fg="#1d8a13")
button2.grid(column=0, row=0, sticky="we", ipadx=12, ipady=5, padx=75, pady=20)
button3 = Button(frame1, text="• Desconectar", command=close_connection, fg="#ff0000")
button3.grid(column=1, row=0, sticky="we", ipady=5, padx=75, pady=20)

label1 = Label(win, text="Inserta comando:")
label1.grid(column=1, row=1, pady=5)

entry1 = Entry(win, width=30, borderwidth=5)
entry1.grid(column=1, row=2, pady=5)

button1 = Button(win, text="Enviar", command=send_data)
button1.grid(column=1, row=3, pady=5)

msg_box = Label(win, text='', bg="#FFFFFF", relief=SUNKEN, width=50, height=10, font="calibri", anchor="nw", padx=5, pady=5, justify="left")
msg_box.grid(column=0, row=4, columnspan=3, padx=20, pady=20)

win.mainloop()
