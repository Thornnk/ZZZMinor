import socket
from tkinter import *
import logging


def close_program():
    """Acaba el bucle principal"""

    global running
    running = False


def obtenerCRC_PCE(cadenaOrigen):
    """Acepta cadenaOrigen -> string"""

    sumaASCII = 0
    for i in range(len(cadenaOrigen)):
        sumaASCII += int(ord(cadenaOrigen[i]))
        sumaASCII %= 10000

    return sumaASCII


def componeComandoPCE(comandoOrigen):
    """Acepta comandoOrigen -> string"""

    componerComando = "[;" + comandoOrigen + ";"
    sumaComprobacion = str(obtenerCRC_PCE(componerComando)).zfill(4)# .ToString("D4")
    # print('Resultado funct: ', sumaComprobacion)
    componerComando += sumaComprobacion + ";]"

    return componerComando


def send_data(cmnd=None):
    """Envía comandos a la máquina"""

    try:
        if cmnd is None:
            command = entry_box.get().upper()
            if len(command) > 0:
                socket1.sendall(bytes(componeComandoPCE(command), encoding="utf-8"))
                entry_box.delete(0, "end")
        else:
            socket1.sendall(bytes(componeComandoPCE(cmnd), encoding="utf-8"))

        parse_data()

    except OSError:
        message("No existe ninguna conexión")


def parse_data():
    """Analiza la respuesta de la máquina"""

    raw_msg = ""

    received = socket1.recv(128).decode("utf-8")
    received_splitted = received.split(";")
    message(f'%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s:')

    if received_splitted[1] == "VERSION":
        raw_msg = received_splitted[1]+": "+received_splitted[3]

    elif received_splitted[1] == "ESTADO_MAQUINA":
        raw_msg = received_splitted[1]+": "+received_splitted[2]+", "+received_splitted[3]+", "+received_splitted[4]+", "\
              +received_splitted[5]+", "+received_splitted[6]+", "+received_splitted[7]+", "+received_splitted[8]+", "\
              +received_splitted[9]+", "+received_splitted[10]

    update_log(raw_msg)
    limit_msg(raw_msg, 50)


def limit_msg(txt, limit):
    """Limita y divide el texto recibido"""

    text = ""
    count = 0

    for i in txt:
        text += i
        count += 1
        if count > limit:
            message(text)
            text = ""
            count = 0

    if len(text) > 0:
        message(text)


def update_log(msg):
    """Actualiza el archivo de registro"""

    logging.basicConfig(filename="log.txt", level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',)
    logging.info(msg)


def new_socket():
    """Crea un socket nuevo (conexión)"""

    global socket1
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def check_connection():
    """Comprueba si hay conexión"""

    connection = socket1.connect_ex(address)
    if connection == 0:
        socket1.close()
        new_socket()
        return False
    else:
        return True


def open_connection():
    """Abre conexión con la máquina"""

    if not check_connection():
        message("Conectando con la dirección {}:{}".format(*address))
        socket1.connect(address)
    else:
        message("La conexión ya está establecida")


def close_connection():
    """Cierra conexión con la máquina"""

    if not check_connection():
        message("La conexión ya está cerrada")
    else:
        message("Cerrando conexión")
        socket1.close()
        new_socket()


def message(msg):
    """Agrega un mensaje a la lista de mensajes"""

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


def log_onoff():
    """Activa o desactiva auto-registro"""

    global autolog
    autolog = not autolog
    message(f"Autolog is: {autolog}")


def auto_log():
    """Cuando está activado envía se ejecuta cada cierto tiempo y actualiza el archivo de registro"""

    if autolog:
        print('autolog on')
        send_data("ESTADO_MAQUINA")
    else:
        pass


socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("192.100.30.66", 2000)

running = True

win = Tk()
win.protocol("WM_DELETE_WINDOW", close_program)
win.title("Conexión con máquina")
win.iconbitmap("gear.ico")
win.resizable(False, False)

# Centrado de ventana en pantalla
win_w, win_h = 450, 350
screen_w, screen_h = win.winfo_screenwidth(), win.winfo_screenheight()
# win.geometry(f"{win_w}x{win_h}+{int(screen_w*0.5-win_w*0.5)}+{int(screen_h*0.5-win_h*0.5)}")

autolog = False

frame_top = Frame()
frame_top.grid(column=0, row=0, columnspan=3)

messages = []

button2 = Button(frame_top, text="• Conectar", fg="#1d8a13", command=open_connection)
button2.grid(column=0, row=0, sticky="we", ipadx=12, ipady=5, padx=75, pady=20)
button3 = Button(frame_top, text="• Desconectar", fg="#ff0000", command=close_connection)
button3.grid(column=1, row=0, sticky="we", ipady=5, padx=75, pady=20)

label1 = Label(win, text="Inserta comando:")
label1.grid(column=1, row=1, pady=5)

entry_box = Entry(win, width=30, borderwidth=5)
entry_box.grid(column=1, row=2, pady=5)

button4 = Button(win, text="Auto-registro", command=log_onoff)
button4.grid(column=2, row=2, padx=5, pady=5, rowspan=2)

button1 = Button(win, text="Enviar", command=send_data)
button1.grid(column=1, row=3, pady=5)

msg_box = Label(win, text='', bg="#FFFFFF", relief=SUNKEN, width=50, height=10, font="calibri", anchor="nw",
                padx=5, pady=5, justify="left")
msg_box.grid(column=0, row=4, columnspan=3, padx=20, pady=20)

while running:
    auto_log()
    win.update_idletasks()
    win.update()


# print('loop!')
# win.after(100, auto_log)
# win.mainloop()
