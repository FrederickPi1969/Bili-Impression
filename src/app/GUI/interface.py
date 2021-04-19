from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from src.backend.scraper.scraper import start_scraping
from kivy.config import Config
import json
from bson import json_util


Config.set('kivy', 'default_font', [
            'msgothic',
            r'C:\Coding\sp21-cs242-project\src\frontend\GUI\Droid-Sans-Fallback.ttf'])


class InstructionScreen(Screen):
    def __init__(self, **kwargs):
        super(InstructionScreen, self).__init__(**kwargs)

        self.words = TextInput(
            text="This software is used for scraping popular videos on Bilibili according to the given " \
                 "keyword and generate related analysis.\n Following is the selections used in subarea " \
                 "options in scraping:\n [0] All Subarea (choose this if you have no clue) \n [1] Animation" \
                 " \n [2] Bangumi \n [3] Domestic \n [4] Music \n [5] Dance \n [6] Game \n [7] Knowledge \n" \
                 " [8] Digital Tech \n [9] Lifestyle \n [10] Food \n [11] Autotune Remix \n [12] Fashion \n" \
                 " [13] News \n [14] Entertainment \n [15] Television \n [16] Documentary \n " \
                 "[17] Film and Movie \n [18] TV Series",
            background_color=(1, 1, 1, 0.7),
            multiline=True,
            font_size=18,
            size_hint=(.8, .8),
            pos_hint={'x': 0.1, 'y': 0.15}
        )
        self.add_widget(self.words)


class ResultScreen(Screen):
    """ define screen for showing scraping result """
    def set_text(self):
        self.textArea.text = "Scraping..."

    def scrape(self):
        req = self.manager.request
        print(req)
        result = start_scraping(req[0], req[1], req[2], req[3], req[4], req[5])
        self.textArea.text = str(result[0])
        with open('../data1.txt', 'w') as f1:
            json.dump(result[0], f1, default=json_util.default)
        with open('../data2.txt', 'w') as f2:
            json.dump(result[1], f2, default=json_util.default)

    def clean(self):
        self.textArea.text = "Press button to start scraping"


class MainScreen(Screen):
    """ define main screen """
    def __init__(self, **kw):
        super().__init__(**kw)
        self.rankOrder = "0"
        self.sortOpt = "1"

    def press(self):
        self.manager.request = []
        self.manager.request.append(self.keyword.text)
        if not self.maxPage.text.isnumeric() or not self.maxVideo.text.isnumeric() or not self.subarea.text.isnumeric():
            print("Wrong! max page number, max video number, and subarea must be integer!")
            return 1
        self.manager.request.append(int(self.maxPage.text))
        self.manager.request.append(int(self.maxVideo.text))
        self.manager.request.append(self.rankOrder)
        self.manager.request.append(self.subarea.text)
        self.manager.request.append(self.sortOpt)
        return 0

    def set_rank_order(self, num):
        self.rankOrder = num


class WindowManager(ScreenManager):
    request = ObjectProperty(None)
    mainScreen = MainScreen()
    resultScreen = ResultScreen()
    instructionScreen = InstructionScreen()


# kv = Builder.load_file('view.kv')
with open('view.kv', encoding='utf8') as f:
    kv = Builder.load_string(f.read())



class Interface(App):
    def build(self):
        Window.clearcolor = (255/260, 135/260, 181/260, 1)
        return kv


if __name__ == '__main__':
    Interface().run()
