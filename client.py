import socket
import threading
import json
import os


class Client:

    def __init__(self):

        check1 = open("messages.json", "a")
        check1.close()
        check2 = open("clients.json", "a")
        check2.close()
        check3 = open("connect_data.json", "a")
        check3.close()
        check4 = open("attempt_connect.json", "a")
        check4.close()
        check5 = open("error.json", "a")
        check5.close()
        check6 = open("message.json", "a")
        check6.close()
        self.clients_list = []
        self.connect_err = "connect_err"
        self.lstamp = 0
        self.tstamp = 0
        self.stamp1 = 0
        self.stamp2 = 0
        self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connected = False
        while not connected:
            with open("attempt_connect.json", "r") as a:
                attempt_connect = json.loads(a.read())
            self.tstamp = os.stat('connect_data.json').st_mtime
            if attempt_connect['attempt'] == "false" and self.tstamp != self.lstamp:
                self.lstamp = self.tstamp
                try:
                    with open("connect_data.json", "r") as file_data:
                        connect_data = json.load(file_data)
                    host = connect_data['ip']
                    port = int(connect_data('port'))
                    self.s.connect((host, port))
                    self.username = connect_data['username']
                    self.s.send(self.username.encode())
                    connected = True
                    clients_list = self.s.recv(1204).decode()
                    if "Sorry, that username is taken. Try a different username." in clients_list:
                        with open("error.json", "w") as outfile:
                            outfile.write(self.connect_err)
                        self.s.close()
                    else:
                        with open("clients.json", "w") as outfile:
                            outfile.write(clients_list)
                except:
                    with open("error.json", "w") as outfile:
                        outfile.write(self.connect_err)
        attempt_connect.close()
        with open("attempt_connect.json", "w") as outfile:
            json.dump({"attempt": "true"}, outfile)

        input_handler = threading.Thread(target=self.input_handler, args=())
        input_handler.start()

        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

    def handle_messages(self):
        new_message = self.s.recv(1204).decode()
        with open("clients.json", "r") as clist:
            clients_list = json.loads(clist)
        if "New person joined the room. Username: " in new_message and not(" - " in new_message):
            clients_list.append(new_message[38:])
        if " has left the room." in new_message and not(" - " in new_message):
            clients_list.remove(new_message[:new_message.index(" has")])
        with open("clients.json", "w") as outfile:
            outfile.write(clients_list)
        gui_output = {
            "message": new_message
        }
        json_object = json.dumps(gui_output)
        with open("messages.json", "w") as outfile:
            outfile.write(json_object)

    def input_handler(self):
        self.stamp1 = os.stat('message.json').st_mtime
        while 1:
            if self.stamp1 != self.stamp2:
                self.stamp2 = self.stamp1
                with open('message.json', "r") as message:
                    msg = json.load(message)
                self.s.send((self.username+' - '+msg['message']).encode())


client = Client()
