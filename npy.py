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
        self.addForm("MAIN", FormObject, name = "Kafka Messenger")     
        self.newrc = rc.RECEIVER()
    
class FormObject(npyscreen.ActionForm):
    
    def create(self):
        self.add_handlers({
            "^A": self.send_message("asdf")
        })
        self.msg_count = 0
        self.keypress_timeout = 1
        
        self.topic_name = self.add(npyscreen.TitleText, scroll_exit=True, name = "Topic Subscription")
        self.sub_choice = self.add(npyscreen.TitleSelectOne, name = "Pick One", max_height=4,\
            value = [0,], values = ["Subscribe","Subscribe from beginning", "Unsubscribe"],\
            scroll_exit=True, scroll_end=True)
        self.btn = self.add(execute_button, name = "Execute")
        #self.getmsgs = self.add(get_messages, name = "Get Messages")
        self.username = self.add(npyscreen.TitleText, scroll_exit=True, name = "Username:")
        self.sending_topic = self.add(npyscreen.TitleText, scroll_exit=True, name = "Topic:")
        self.msg_input_field = self.add(npyscreen.TitleText, scroll_exit=True, name = "Message:")
        self.mypager = self.add(npyscreen.BufferPager, scroll_exit=True, scroll_end=True,\
            scroll_if_editing=True, editable=False)
        self.mypager.buffer(["Subribe to a topic to get started..."])

#self.msg_input_field.value
    def show_messages(self):
        message_not_received = True 
        try:
            msgs = self.parentApp.newrc.check_for_msgs()
            if msgs:
                self.mypager.buffer(msgs)
                #self.display()
        except Exception as e:
            #self.display()
            pass
        
    def while_editing(self):
        self.show_messages()
        self.display()
        #print(self.msg_count)

    def while_waiting(self):
        self.show_messages()
        self.display()
        #print(self.msg_count)
            
    def send_message(self, message):
        print(message)
        self.display() 

    def clear_msgsend_buffer(self):
        pass

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
        self.parent.display()
        
if __name__ == "__main__":
    App = App().run()

    #print(npyscreen.wrapper_basic(App().run()))
