#!/usr/bin/python3
import random
import time
import sys
import curses
from datetime import datetime
import npyscreen
import receiver as rc
import message_sender as ms

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", FormObject, name = "Kafka Messenger")     
        self.newrc = rc.RECEIVER()

class FormObject(npyscreen.ActionForm):
    
    def create(self):
        self.msg_count = 0
        self.keypress_timeout = 1
        self.topic_name = self.add(npyscreen.TitleText, scroll_exit=True, name = "Topic Subscription")
        self.btn = self.add(execute_button, name = "Execute")
        self.sub_choice = self.add(npyscreen.TitleSelectOne, name = "Pick One", max_height=4,\
            value = [0,], values = ["Subscribe", "Unsubscribe"], scroll_exit=True, scroll_end=True)
        self.username = self.add(npyscreen.TitleText, scroll_exit=True, name = "Username:")
        self.sending_topic = self.add(npyscreen.TitleText, scroll_exit=True, name = "Topic:")
        self.send_msg = self.add(send_msg, scroll_exit=True, name = "Message:")
        #self.msg_input_field = self.add(npyscreen.TitleText, scroll_exit=True, name = "Message:")
        self.mypager = self.add(npyscreen.BufferPager, scroll_exit=True, scroll_end=True,\
            scroll_if_editing=True, editable=False)
        self.mypager.buffer(["Subcribe to a topic to get started..."])

    def show_messages(self):
        message_not_received = True 
        try:
            msgs = self.parentApp.newrc.check_for_msgs()
            if msgs:
                self.mypager.buffer(msgs)
                self.display()
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
            
    def send_message(self, args):
        #print(args)
        SENDER = ms.LOGSENDER()
        USER = self.username.value
        MESSAGE = [self.send_msg.value]
        TOPIC = self.sending_topic.value
        SENDER.send_list_of_logs(SENDER, USER, MESSAGE, TOPIC)
        self.send_msg.value = ''
        self.display() 

class send_msg(npyscreen.Textfield):
    def set_up_handlers(self):
        super(send_msg, self).set_up_handlers()
        self.handlers.update({
            10 : self.parent.send_message,
            13 : self.parent.send_message
        })
        

class execute_button(npyscreen.MiniButtonPress):
    def whenPressed(self):
        if self.parent.sub_choice.get_selected_objects()[0] == 'Subscribe':
            self.parent.parentApp.newrc.subscribe_to_topic(str(self.parent.topic_name.value))
            self.parent.mypager.buffer(["Subscribed to " + str(self.parent.topic_name.value) ])
        if self.parent.sub_choice.get_selected_objects()[0] == 'Unsubscribe':
            self.parent.parentApp.newrc.unsubscribe_from_topic(str(self.parent.topic_name.value))
            self.parent.mypager.buffer(["Unsubscribed from " + str(self.parent.topic_name.value) ])
            

        self.parent.display()
        
if __name__ == "__main__":
    App = App().run()
