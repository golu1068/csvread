# -*- coding: utf-8 -*-
import numpy as np
import time
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, NumericProperty,BooleanProperty
from glob import glob
from os.path import dirname, join, basename
import os
from functools import partial
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import BorderImage
from kivy.uix.slider import Slider
from kivy.clock import Clock
from mutagen import File
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import random
from kivy.uix.filechooser import FileChooserListView
try:
    from kivy.garden.filebrowser import FileBrowser
except:
    from filebrowser import FileBrowser
from kivy.utils import platform
from os.path import sep, expanduser, isdir
from kivymd.uix.navigationdrawer import NavigationLayout as NL
from kivymd.theming import ThemeManager
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.button import MDFloatingActionButton as fab
from kivy.graphics import Rectangle, Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.modalview import ModalView
from kivy.factory import Factory
#from buttons import ImgToggleButton_play, ImgButton_pre, ImgButton_next, tbtn
#from mplayer import onpress
#####################################################################
global main_box_self
default_img = r'/home/nagendra/python_code/image_1.jpg'
naviagtion_img = r'/home/nagendra/python_code/menu_image.jpg'
#file_wr = open(r'/storage/emulated/0/text_app.txt', 'w+')
#   r'/storage/emulated/0/'
play_img='play_normal.png'
pause_img='pause_press.png'
prev_normal_img = 'prev_normal.png'
prev_press_img = 'prev_press.png'
next_normal_img = 'next_normal.png'
next_press_img = 'next_press.png'
songlist={};cover_album=[];
window_image=['image_1.jpg']
###########################################################################
class ImgToggleButton_play(ToggleButtonBehavior, Image):
    def __init__(self, img_normal, img_down,**kwargs):
        super(ImgToggleButton_play, self).__init__(**kwargs)
        self.size_hint= (0.33, 1)
        self.pos_hint= {"x":0.30,"bottom":0}
        self.background_normal=''
        self.background_color=(1,1,1,1)
        self.source = img_normal
        self.mipmap = True
        self.img_normal = img_normal
        self.img_down = img_down

    def on_state(self, widget, value):
        print(value)
        if value == 'down':
            self.source = self.img_down
        else:
            self.source = self.img_normal

class ImgButton_pre(ButtonBehavior, Image):
    def __init__(self, img_normal, img_press, **kwargs):
        super(ImgButton_pre, self).__init__(**kwargs)
        self.size_hint= (0.30, 1)
        self.pos_hint= {"left":1,"bottom":0}
        self.background_normal=''
        self.background_color=(1,0,1,1)
        self.normal = img_normal
        self.press = img_press
        self.source = self.normal
        self.allow_stretch = True
        self.mipmap = False
    
    def on_press(self):
        self.source = self.press

    def on_release(self):
        self.source = self.normal
class ImgButton_next(ButtonBehavior, Image):
    def __init__(self, img_normal, img_press, **kwargs):
        super(ImgButton_next, self).__init__(**kwargs)
        self.size_hint= (0.33, 1)
        self.pos_hint= {"right":1,"bottom":0}
        self.background_normal=''
        self.background_color=(1,1,1,1)
        self.normal = img_normal
        self.press = img_press
        self.source = self.normal
        self.allow_stretch = True
        self.mipmap = False
    
    def on_press(self):
        self.source = self.press

    def on_release(self):
        self.source = self.normal
        
class tbtn(ToggleButton):
    global curr_song, pre_song
    def __init__(self, song_index, **kwargs):
        super(tbtn, self).__init__(**kwargs)
        self.song = song_index
        self.background_normal=''
        self.background_color=(0,0,0,0.2)
        self.color=(0,0,1,1)
        self.size_hint=(1,None)
        self.pos_hint = (1,None)
        self.size = (self.width,self.height*2)
        self.group = 'song_button'
        self.border = (1,1,1,1)
        self.pos = (0,self.height/2)

    def on_state(self, instance, value):
        if value == 'down':
          list(self.children)[0].color = (0,0,1,0.5)
        else:
           list(self.children)[0].color = (1,1,1,1)

#####################################################################
slid_val=0;val=0;val_pre=-1;
def slid_bind(self, value):
    global slid_val, val, val_pre
    val = float("{0:0=2d}".format(int(self.value)))
    #file_wr.write('all = '+str(val) + '    '+str(val-val_pre)+'   \n')
    if (val - val_pre != 1 and val != 0 and val - val_pre != 0):
        slid_val = 1        
    val_pre = val
    
    
def slid_func(sound, len_slid, len_btn2):
    global sh
    try:
        sh.cancel()
    except:
        pass
    sh = Clock.schedule_interval(partial(next, sound, len_slid, len_btn2), 1)
    #len_btn2.text = "{0:0=2d}".format(int(len_slid.value))#str(int(self.value)) 

def next(sound, len_slid, len_btn2, self):
    global slid_val, val
    if (len_slid.value > len_slid.max): 
        return False
    if (slid_val == 1):
        sound.seek(val)
        slid_val = 0
    song_pos = sound.get_pos()
    time = song_pos/60
    minu = int(time)
    minu_str = "{0:0=2d}".format(minu)
    seco = int(round((time - minu)*60, 2))
    seco_str = "{0:0=2d}".format(seco)
    len_slid.value = song_pos
    len_btn2.text = minu_str + ':' + seco_str
    
#######################################################################################
other_layout = True;
len_btn='';len_btn2='';
global curr_song, pre_song,pre_sound, song_counter, bt2 
song_counter=0;
def song_btn(index, main_lyt, self):
    global curr_song, pre_song,pre_sound, song_counter, bt2, other_layout, len_btn,len_btn2
    global len_slid, sh, val_pre
    curr_song = index
    file3 = File(songlist[index][0])
    song_length = float(file3.info.pprint().split(',')[-1:][0][:-8])
    time = song_length/60
    minute = int(time)
    min_str = "{0:0=2d}".format(minute)
    second = int(round((time - minute)*60, 2))
    sec_str = "{0:0=2d}".format(second)
########################################################################
    if (other_layout == True):
        grid_2 = GridLayout(cols=3, size_hint=(1,0.05),row_force_default=True, 
                            row_default_height=40, opacity=1)
        b1 = Label(text='00:00', size_hint_x=None,width=main_lyt.width*0.15)
        grid_2.add_widget(b1)
        slid = Slider(min=0, max=100,cursor_width='8dp', cursor_height='8dp',
                      value_track=True,background_width = '8dp',value_track_width = '0.5dp',
                      value_track_color = [0, 1, 1, 1], step=1)
        slid.pos = (1,100)
        grid_2.add_widget(slid)
        b2 = Label(text='min'+':'+'sec',size_hint_x=None,width=main_lyt.width*0.15)
        grid_2.add_widget(b2)
        
        len_btn = b2
        len_btn2 = b1
        len_slid = slid

        slid.bind(value = slid_bind)        

        main_lyt.add_widget(grid_2)
    
    ###################################################################################
        fl = FloatLayout(size_hint=(1,0.1), opacity=1)
      
        bt1 = ImgButton_pre('prev_normal.png', 'prev_press.png',id='pre')
        bt1.bind(on_press = partial(previous_song))
        fl.add_widget(bt1)
        
        bt2 = ImgToggleButton_play(play_img, pause_img, id='pp')
        bt2.bind(on_press = partial(play_pause))
        fl.add_widget(bt2)
        
        bt3 = ImgButton_next('next_normal.png', 'next_press.png',id='next')
        bt3.bind(on_press = partial(next_song))
        fl.add_widget(bt3)
    
        main_lyt.add_widget(fl)
        other_layout = False
        
        
    
    len_btn.text = min_str+':'+sec_str
    len_slid.min = 0
    len_slid.value = 0
    len_slid.max = int(song_length)
    len_btn2.text = '00:00'
    
    try:
        print(songlist[pre_song][0] + '   :    stoped')
        bt2.state = 'normal'
        ImgToggleButton_play.on_state(bt2, 'fwfwf','normal')
        pre_sound.stop()
        pre_sound.unload()
        pre_song = -1
    except:
        pre_song = -1
    if (curr_song != pre_song):
        if (self.state == 'down'):
            sound = SoundLoader.load(songlist[index][0])  # songlist[index]
            bt2.state = 'down'
            ImgToggleButton_play.on_state(bt2, 'fwfwf','down')
            if (sound != None):
                val_pre = -1
                slid_func(sound, len_slid, len_btn2)
                sound.play()
                pre_song = index
                song_counter = index
                pre_sound = sound
                songlist[pre_song][1].state = 'down'
                print(songlist[pre_song][0] + '   :    playing')

song_position = 0.0;            
def play_pause(self):
    global curr_song, pre_song,pre_sound, song_counter, len_slid, len_btn2, sh, song_position
    if (self.state == 'normal'):
        try:
            song_position = pre_sound.get_pos()
            sh.cancel()
            pre_sound.stop()
            #pre_sound.unload()
            songlist[pre_song][1].state = 'normal'
            print(songlist[pre_song][0] + '   :    stoped')
        except:
            pass
    else:
        index = pre_song
        sound = SoundLoader.load(songlist[index][0])
        bt2.state = 'down'
        ImgToggleButton_play.on_state(bt2, 'fwfwf','down')
        
        if (sound != None):
            val_pre = -1
            sound.play()
            #sound.seek(40.0)
            slid_func(sound, len_slid, len_btn2)
            pre_song = index
            song_counter = index
            pre_sound = sound
            songlist[pre_song][1].state = 'down'
            print(songlist[pre_song][0] + '   :    playing')
    
def previous_song(self):
    global curr_song, pre_song,pre_sound, song_counter
    pre_sound.stop()
    pre_sound.unload()
    songlist[song_counter][1].state = 'normal'
    song_counter = song_counter - 1
    if (song_counter < 0):
        song_counter=0
    song_btn(song_counter, 'nvef',self)

def next_song(self):
    global curr_song, pre_song,pre_sound, song_counter
    pre_sound.stop()
    pre_sound.unload()
    songlist[song_counter][1].state = 'normal'
    song_counter = song_counter + 1
    if (song_counter == len(songlist)):
        song_counter=len(songlist) - 1
    song_btn(song_counter, 'vnvv',self)    
    
btn_inst=[];m_image=['m_1.jpg','m_2.jpg','m_3.jpg','m_4.jpg','m_5.jpg','m_6.jpg','m_7.jpg','m_8.jpg','m_9.jpg','m_10.jpg'];
class box(NL):
    global index, bt2, main_box_self;
    def __init__(self, **kwargs):
        super(box, self).__init__(**kwargs)
        global bt1, bt2, bt3,main_box_self ;
        
        main_box = BoxLayout()
        main_box.orientation='vertical'
        main_box_self = main_box
        self.anim_type='slide_above_simple'
        ####################################################################
        self.menu1 = BoxLayout(orientation='vertical', spacing=0.2)
        
        self.im1 = Image(source='image_2.jpg', color=(1,1,1,.5))
        
        self.im1.size_hint = [self.menu1.size_hint[0]*0.3, self.menu1.size_hint[1]*0.3]
#        self.im1.pos  = (self.height*1, self.width*1)
        
        gd_menu = GridLayout(cols=1, spacing=0.1)
        menu_btn = Button(text='change wallpaper',background_color=(0,0,0,0.2), 
                          color=(1,1,1,1), size_hint_y=None)
        menu_btn.bind(on_release= lambda x : self.toggle_nav_drawer())
        menu_btn.bind(on_release= (self.gonext))
        menu_btn.bind(on_release=partial(change_image1.file_manager_open, self))
    
        gd_menu.add_widget(menu_btn)
        
        self.menu1.add_widget(self.im1)
        self.menu1.add_widget(gd_menu)
#        self.menu1.add_widget(gd_menu.menu_btn)
#    
        self.add_widget(self.menu1)

        
        ########################################################
        
        tb = MDToolbar(title='menu',
        background_palette= 'Primary')
        tb.md_bg_color = [0,0,0,0] 
        tb.left_action_items= [['menu', lambda x : self.toggle_nav_drawer()]]
        
        main_box.add_widget(tb)

        gridlayout = GridLayout(cols=1, size_hint_y=None, spacing=2)
        gridlayout.bind(minimum_height = gridlayout.setter('height'))
        index=0;
        main_lyt = main_box
        dirpath = os.getcwd()
        for dirpath, dir_name, filename in os.walk(r'/storage/emulated/0/'):
            if (os.path.basename(dirpath) == 'Download' or os.path.basename(dirpath) == 'audios'):
                for fn in glob(dirpath + '/*.mp3'):
                    btn = tbtn(id='song_btn', song_index=index)
                    btn_inst.append(btn)
                    songlist[index] = [fn, btn]
    #                print(ID3(fn).text)
                    file2 = File(str(fn))
    #                song_length = float(file2.info.pprint().split(',')[-1:][0][:-8])
    #                print(float(song_length))
                    try:
                        pic_name = fn.split('/')[-1:][0][:-4]
                        artwork = file2.tags['APIC:'].data
                        with open(pic_name + '.jpg', 'wb') as img:
                            img.write(artwork)
                        cover_album.append(pic_name+'.jpg')
                    except:
                        rand_val = random.randint(0, 9)
                        cover_album.append(m_image[rand_val])
                    btn.bind(on_press = partial(song_btn, index, main_lyt))
                    index = index + 1
                    gridlayout.add_widget(btn)
                
        for i in range(index):
            img = Image(id='tn',source=cover_album[index-1-i],
#            img = Image(id='tn',source='icon.png',
                        size=(btn_inst[index-1-i].height*0.8,btn_inst[index-1-i].height*0.8),
                    pos= (btn_inst[index-1-i].width-main_box.width*0.8, (btn_inst[index-1-i].size[1]*i)+(main_box.width*0.5)),
                    allow_stretch = False)
            btn_inst[index-1-i].add_widget(img)
            lbl = Label(text=str(songlist[index-1-i][0].split('/')[-1:][0]),
                        text_size = (btn_inst[index-1-i].width*7.5, None),
                        halign = 'left', valign = 'middle', max_lines = 1, shorten  = True,
                        shorten_from = 'right',color=(1,1,1,1),
                        pos=(img.pos[0]*30, (btn_inst[index-1-i].size[1]*i)+(main_box.width)))
            btn_inst[index-1-i].add_widget(lbl)
            
        scrollview = ScrollView()
        scrollview.add_widget(gridlayout)
        main_box.add_widget(scrollview)

        
        with self.menu1.canvas.before:
            Color(1,1,1,.8)
            self.menu1.rect1 = Rectangle(pos = self.menu1.pos, 
                                  size = self.menu1.size)
            self.menu1.rect1.source = 'menu_image.jpg'
        
        with main_box.canvas.before:
            main_box.rect = Rectangle(pos = main_box.pos, 
                                  size =np.array(Window.size))
            main_box.rect.source = 'image_1.jpg'
#                
        def update_rect1(instance, value):
            instance.rect1.pos = instance.pos
            instance.rect1.size = instance.size
            
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
            
        self.menu1.bind(pos=update_rect1, size=update_rect1)
        
        main_box.bind(pos=update_rect, size=update_rect)
            
        self.add_widget(main_box)
        
    def gonext(self,btn_inst ):
        sm.current = "change_image"
        
    def selection_updated(self, main_lyt, filechooser, selection):
            with main_lyt.canvas.before:
                main_lyt.rect = Rectangle(pos = main_lyt.pos, 
                                      size =np.array(Window.size))
                main_lyt.rect.source = selection[0]
            def update_rect(instance, value):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size
            
            main_lyt.bind(pos=update_rect, size=update_rect)
    
class update_image():
    def __init__(self, image_path, **kwargs):
        super(update_image, self).__init__(**kwargs)
        global main_box_self
        path = image_path
        if (path[-4:] == '.jpg' or path[-4:] == '.png' or path[-5:] == '.jpeg'):
            pass
        else:
            return
        with main_box_self.canvas.before:
            main_box_self.rect = Rectangle(pos = main_box_self.pos, 
                                  size =np.array(Window.size))
            main_box_self.rect.source = path
                
        def update_rect(instance, value):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size
        
        main_box_self.bind(pos=update_rect, size=update_rect)
    
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        bo = box()
        print('bo= ',bo)
        self.add_widget(bo)
        
#class change_image1(Screen):
#    def __init__(self, **kwargs):
#        super(change_image1, self).__init__(**kwargs)
#        sc2_box = BoxLayout(orientation='vertical')
#        browser = FileBrowser(select_string='Select',path=r'/storage/emulated/0/')
#        browser.bind(
#                    on_success=self._fbrowser_success,
#                    on_canceled=self._fbrowser_canceled,
#                    on_submit=self._fbrowser_submit)
#        
#        sc2_box.add_widget(browser)
#        
#        
#        with sc2_box.canvas.before:
#            Color(1,1,1,1)
#            sc2_box.rect1 = Rectangle(pos = sc2_box.pos, 
#                                  size = sc2_box.size)
#            sc2_box.rect1.source = 'download.jpg'
#        def update_rect1(instance, value):
#            instance.rect1.pos = instance.pos
#            instance.rect1.size = instance.size
#        sc2_box.bind(pos=update_rect1, size=update_rect1)
#        
#        self.add_widget(sc2_box)
#        
#    def gonext(self ,btn_inst):
#        sm.current = "mainscreen"
#    def _fbrowser_canceled(self, instance):
#        update_image('image_1.jpg')
#        print (instance.selection)
#        sm.current = "mainscreen"
#
#    def _fbrowser_success(self, instance):
#        img_path = instance.selection
#        update_image(str(img_path[0]))
#        print (instance.selection)
#        sm.current = "mainscreen"
#    def _fbrowser_submit(self, instance):
#        img_path = instance.selection
#        update_image(str(img_path[0]))
#        print (instance.selection)
#        sm.current = "mainscreen"
class change_image1(Screen):
    global mai_lyt
    manager_open = BooleanProperty()
    manager = ObjectProperty()
    file_manager = ObjectProperty()
    def __init__(self, **kwargs):
        super(change_image1, self).__init__(**kwargs)
        global scr2_Self
        scr2_Self = self
        return  
    
    def file_manager_open(self, scr_self):
        global scr2_Self
        scr2_Self.manager = ModalView(size_hint=(1, 1), auto_dismiss=False)
        scr2_Self.file_manager = MDFileManager(previous=False, 
                                             exit_manager=scr2_Self.exit_manager, 
                                             select_path=scr2_Self.select_path)
        scr2_Self.manager.add_widget(scr2_Self.file_manager)
        scr2_Self.file_manager.show(r'/storage/emulated/0/')  # output manager to the screen
        scr2_Self.manager_open = True
        scr2_Self.manager.open()
        
    def select_path(self, path):
        img_path = path
        update_image(str(img_path))
        sm.current = "mainscreen"
        self.exit_manager()
        
    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        self.manager.dismiss()
   
sm = ScreenManager()

m1 = MenuScreen(name='mainscreen')
sm.add_widget(m1)

m2 = change_image1(name='change_image')
sm.add_widget(m2)
    
class main(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'

    def build(self):
        return sm

main().run()
#file_wr.close()
