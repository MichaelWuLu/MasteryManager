from kivy.app import App    
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import os
import json


summonerName = None

class CustomBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(CustomBoxLayout, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(1, 1, 1, 0.4)  # Set background color to red
            self.rect = Rectangle(size=self.size, pos=self.pos)
            
        self.bind(size=self._update_rect, pos=self._update_rect)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MyApp(App):
    def build(self):
        self.title = 'Mastery Manager'
        Window.size = (400, 600)

        # Create a vertical BoxLayout as the root widget
        root = CustomBoxLayout(orientation='vertical')

        
        # Create the header widget
        header = BoxLayout(orientation='horizontal' , size_hint=(1, 0.1))

        # Add the picture to the profiletemp/icon0.jpg
        picture = Image(source='temp/icons/icon0.jpg', size_hint=(0.3, 1))
        header.add_widget(picture)

        # Add the title to the header
        text = BoxLayout(orientation='vertical', size_hint=(0.5, 1))
        title = Label(text=summonerName if summonerName else 'Summoner Name')
        text.add_widget(title)
        mastery = Label(text='Mastery')
        text.add_widget(mastery)
        header.add_widget(text)

        # Add the text input to the search bar
        text_input = TextInput(size_hint=(0.5, None), height=30)
        header.add_widget(text_input)

        # Add the submit button to the search bar
        submit_button = Button(text='Submit', size_hint=(0.2, None), height=30)
        submit_button.bind(on_press=self.summonerName_input)
        header.add_widget(submit_button)

        # Add the header to the root widget
        root.add_widget(header)



        # Create the mastery gallery
        mastery_gallery = ScrollView()
        scroll_body = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Create each row based on images in temp folder
        for i, file in enumerate(os.listdir('temp/champions')):
            # Create the body widget
            if i % 4 == 0:
                body = BoxLayout(orientation='horizontal', spacing=10, padding=10)

            image = Image(source=f"temp/champions/{file}")
            body.add_widget(image)

            # Add the body to the root widget
            if i % 4 == 3:
                scroll_body.add_widget(body)

        scroll_body.add_widget(body)

        # Add the scroll body to the mastery gallery
        mastery_gallery.add_widget(scroll_body)

        # Add the mastery gallery to the root widget
        root.add_widget(mastery_gallery)

        return root


    def summonerName_input(self, instance):
        global summonerName
        summonerName = instance.parent.children[2].text
        print(summonerName)

if __name__ == '__main__':
    MyApp().run()
