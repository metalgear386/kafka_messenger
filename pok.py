#!/usr/bin/python3
import random
import time
import sys
import npyscreen
import receiver as rc
 
class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", FormObject, name = "Topic Subscriber")
 
class FormObject(npyscreen.ActionForm):
    def create (self):
        #self.keybindings = {curses.ascii.ESC: self.on_cancel, "^Q":self.on_cancel }
        self.topic_name = self.add(npyscreen.TitleText, name = "Topic Name:")
        self.sub_choice = self.add(npyscreen.TitleSelectOne, max_height=4, value = [0,], name="Pick One",
            values = ["Subscribe","Subscribe from beginning", "Unsubscribe"], scroll_exit=True, scroll_end=True, scroll_if_editing=False)
        self.btn = self.add(execute_button, name = "Execute")
        #self.txt = self.add(npyscreen.TitleText, name = "txt1", value = "Default")
        self.mypager = self.add(npyscreen.BufferPager, scroll_exit=True)
        self.mypager.buffer(["No Data"])
 
 
class execute_button(npyscreen.MiniButtonPress):
    def whenPressed(self):
        newrc = rc.RECEIVER()
        self.parent.mypager.clearBuffer()
        #self.parent.mypager.buffer(["Tacos!"])
        if self.parent.sub_choice.get_selected_objects()[0] == 'Subscribe':
            newrc.subscribe_to_topic(str(self.parent.topic_name.value))
            self.parent.mypager.buffer(["Subscribed to " + str(self.parent.topic_name.value) ])
        #self.parent.mypager.buffer([str(self.parent.sub_choice.get_selected_objects()) + " subscribed!"])
        self.parent.display()
        self.show_messages(newrc)
 
    def show_messages(self, newrc):
        while True:
        #self.parent.notify_wait("Update")
            self.parent.mypager.buffer([newrc.check_for_msgs()])
            self.parent.display()
        
    #def while_waiting(self):
    #    npyscreen.notify_wait("Update")
 
 
if __name__ == "__main__":
    App = App().run()
 
    #print(npyscreen.wrapper_basic(TestApp.run()))
