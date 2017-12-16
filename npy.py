#!/usr/bin/python3
import random
import time
import sys
import curses
from datetime import datetime
import npyscreen
import receiver as rc

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", FormObject, name = "Topic Subscriber")     
        self.newrc = rc.RECEIVER()
    
class FormObject(npyscreen.ActionForm):
    
    def create (self):
        self.msg_count = 0
        self.keypress_timeout = 1
        
        #self.keybindings = {curses.ascii.ESC: self.on_cancel, "^Q":self.on_cancel }
        self.topic_name = self.add(npyscreen.TitleText, scroll_exit=True, name = "Topic Name")
        self.sub_choice = self.add(npyscreen.TitleSelectOne, name = "Pick One", max_height=4, value = [0,],\
            values = ["Subscribe","Subscribe from beginning", "Unsubscribe"], scroll_exit=True, scroll_end=True)
        self.btn = self.add(execute_button, name = "Execute")
        self.getmsgs = self.add(get_messages, name = "Get Messages")
 
        #self.date_widget = self.add(npyscreen.Textfield, name = "time", value="", editable=True) 
        self.mypager = self.add(npyscreen.BufferPager, scroll_exit=True, scroll_end=True)
        self.mypager.buffer(["No Data"])

    def show_messages(self):
        message_not_received = True 
        #while message_not_received:
        try:
            #print("starting")
            msgs = self.parentApp.newrc.check_for_msgs()
            if msgs:
            #print("mid")
                self.mypager.buffer(msgs)
                self.display()
                #message_not_received = False
        except Exception as e:
            self.display()
            #print("ending exception")
            #pass
        #print("ending--")
        
    def while_editing(self):
        self.show_messages()
        #print(self.msg_count)

    def while_waiting(self):
        self.show_messages()
        #print(self.msg_count)
            
class get_messages(npyscreen.MiniButtonPress):
    def whenPressed(self):
        self.parent.show_messages()
        #self.parent.display()

class execute_button(npyscreen.MiniButtonPress):
    def whenPressed(self):
        self.parent.mypager.clearBuffer()
        #self.parent.mypager.buffer(["Tacos!"])
        if self.parent.sub_choice.get_selected_objects()[0] == 'Subscribe':
            self.parent.parentApp.newrc.subscribe_to_topic(str(self.parent.topic_name.value))
            self.parent.mypager.buffer(["Subscribed to " + str(self.parent.topic_name.value) ])
        #self.parent.mypager.buffer([str(self.parent.sub_choice.get_selected_objects()) + " subscribed!"])
        self.parent.display()
        #self.show_messages(self.parent.newrc)
        
if __name__ == "__main__":
    App = App().run()

    #print(npyscreen.wrapper_basic(App().run()))
