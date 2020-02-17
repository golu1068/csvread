from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.uix.filemanager import MDFileManager
from kivymd.theming import ThemeManager
from kivy.uix.modalview import ModalView
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.lang import Builder
from kivy.factory import Factory
from functools import partial

class ScreenOne(Screen):
    global main_self
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        box = BoxLayout()
        box.orientation = 'vertical'
        b1 = Button(text='qhfiq')
        b1.size = (box.width*0.5, box.height*0.5)
        b1.bind(on_press=self.gonext)
        b1.bind(on_release=partial(ScreenTwo.file_manager_open, self))
        box.add_widget(b1)
        self.add_widget(box)
        
    def gonext(self, af):
        sm.current = "screen_two"

class ScreenTwo(Screen):
    global mai_lyt
    manager_open = BooleanProperty()
    manager = ObjectProperty()
    file_manager = ObjectProperty()
    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)
        global mai_lyt
        mai_lyt = self
        print('done3', (self))
        return
    def file_manager_open(self, scr_self):
        global mai_lyt
        print('done1', (mai_lyt))
        print('done', (self))
        mai_lyt.manager = ModalView(size_hint=(1, 1), auto_dismiss=False)
        mai_lyt.file_manager = MDFileManager()
        mai_lyt.manager.add_widget(mai_lyt.file_manager)
        mai_lyt.file_manager.show('/')  # output manager to the screen
        mai_lyt.manager_open = True
        mai_lyt.manager.open()
        
    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.
        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.exit_manager()
    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        self.manager.dismiss()



sm  = ScreenManager()
sm.add_widget(ScreenOne(name ="screen_one")) 
sm.add_widget(ScreenTwo(name ="screen_two")) 



class mytest(MDApp):
#    theme_cls = ThemeManager()
#    theme_cls.primary_palette = "Teal"
    
    def build(self):
        return sm
    

mytest().run()
