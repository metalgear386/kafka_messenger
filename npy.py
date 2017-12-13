#!/usr/bin/python3
import random
import time
import sys
import curses
from datetime import datetime
import npyscreen
import asyncio
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
        
        self.sub_choice = self.add(npyscreen.TitleSelectOne, name = "Pick One", max_height=4, value = [0,],\
            values = ["Subscribe","Subscribe from beginning", "Unsubscribe"], scroll_exit=True, scroll_end=True)
        self.btn = self.add(execute_button, name = "Execute")
        self.topic_name = self.add(npyscreen.TitleText, scroll_exit=True, name = "Topic Name",)
        #self.date_widget = self.add(npyscreen.Textfield, name = "time", value="", editable=True) 
        self.mypager = self.add(npyscreen.BufferPager, scroll_exit=True, scroll_end=True)
        self.mypager.buffer(["No Data"])

    #def while_editing(self):
    #    self.show_messages()

    def show_messages(self):
        try:
            self.msg_count = self.msg_count + 1
            #print(self.msg_count)
            #time.sleep(0.1)
            #self.msg.count = self.msg_count + 1
            msg = self.parentApp.newrc.check_for_msgs()
            if msg != None:
                self.mypager.buffer([msg])
                self.display()
        except Exception as e:
            pass
            
    def while_editing(self):
        self.show_messages()
        #print(self.msg_count)

    def while_waiting(self):
        self.show_messages()
        #print(self.msg_count)

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
