# this code is not mine i have taken this code from book
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase
from kivy.uix.gridlayout import GridLayout
class GridlayoutdesignApp(App):
    def build(self):
        return Mainwindow()
class Mainwindow(GridLayout):
    pass
if __name__ == '__main__':




    LabelBase.register(name='Modern Pictograms',
                       fn_regular='modernpics.ttf')

    GridlayoutdesignApp().run()
