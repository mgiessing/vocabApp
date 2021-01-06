import random
import pandas as pd
import unidecode
import os

from kivy.app import App
#from kivy.uix.gridlayout import GridLayout
#from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
#from kivy.uix.actionbar import ActionBar
#from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.settings import SettingsWithSidebar
from kivy.config import Config, ConfigParser
from kivy.clock import Clock

from settingsjson import settings_json


#print(config.get('example', 'optionsexample'))
#Window.size = (400, 600)

class MainWindow(Screen):

    userInput = ObjectProperty(None)
    vocab = ObjectProperty(None)

    if os.path.exists('vocabularyTrainer.ini'):
        config = ConfigParser()
        config.read('vocabularytrainer.ini')
        hsklevel=config.get('example', 'optionsexample')
    else:
        hsklevel="HSK1"
    
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.df = pd.read_excel(r"static/{}.xlsx".format(self.hsklevel), engine="openpyxl")
        self.en = self.df['English']
        self.zh = self.df['Chinese']
        self.pinyin = self.df['Pinyin']
        self.rd = None

    def btn_submit(self):
        print(self.df.shape)
        if self.rd is None:
            pLabel = "Please start before submitting!"
        elif not self.userInput.text:
            pLabel = "Please enter something!"
        else:
            pLabel = self.validate(self.userInput.text)
            self.btn_next()
        PopupWindow(pLabel).open_popup()

    def btn_next(self):
        self.check_hsklevel()
        self.userInput.text = ""
        self.rd = random.randint(0, self.df.shape[0]-1)
        self.vocab.text = "HSK Level {}\nWhat is '{}' in Chinese?".format(self.hsklevel, self.en[self.rd])

    def check_hsklevel(self):
        self.config.read('vocabularytrainer.ini')
        print(self.hsklevel, self.config.get('example', 'optionsexample'))
        print("Debugging Info: Pandas df size: {}".format(self.df.shape))
        if self.hsklevel != self.config.get('example', 'optionsexample'):
            print("Changing HSK...")
            self.df = pd.read_excel(r"static/{}.xlsx".format(self.config.get('example', 'optionsexample')), engine="openpyxl")
            self.en = self.df['English']
            self.zh = self.df['Chinese']
            self.pinyin = self.df['Pinyin']
            self.rd = None
            self.hsklevel=self.config.get('example', 'optionsexample')
        #ToDo: Wenn HSK level anders als im gelesenen config ist -> anpassen!
        
    def validate(self, answer):
        def replace_tones(orig_voc):
            unaccented_voc = unidecode.unidecode(orig_voc)
            return(unaccented_voc)
        
        if answer == self.zh[self.rd]:
            #correct+=1
            return("Well done, even in chinese characters!")
        elif answer == self.pinyin[self.rd]:
            #correct+=1
            return("Well done, you also got the correct tones!")
        elif answer == replace_tones(self.pinyin[self.rd]):
            #correct+=1
            return("Well done! Keep in mind the tones '{}'".format(self.pinyin[self.rd]))
        else:
            return("Sorry, that was not correct!\nThe correct vocab is {}".format(self.pinyin[self.rd]))
        #cnt+=1

class QuizWindow(Screen):
    quizHead = ObjectProperty(None)
    quizText = ObjectProperty(None)

    config = ConfigParser()
    config.read('vocabularytrainer.ini')
    hsklevel=config.get('example', 'optionsexample')
    counter = 1

    def __init__(self, **kwargs):
        super(QuizWindow, self).__init__(**kwargs)
        self.df = pd.read_excel(r"static/{}.xlsx".format(self.hsklevel), engine="openpyxl")
        self.questions = [self.df["English"], self.df["Chinese"], self.df["Pinyin"]]
        self.answers = [None]*10
        self.rdList =[random.randrange(0, self.df.shape[0], 1) for i in range(10)]
        self.quizHead = "Question {}/10: What is '{}' in Chinese?".format(self.counter, self.questions[0][self.rdList[self.counter-1]])
        self.quizText = ""
        print(self.rdList)

    def btn_prev(self):
        if self.counter > 1:
            if self.quizText.text != "":
                self.answers[self.counter-1] = self.quizText.text
                self.quizText.text = ""
            self.counter -= 1
            self.quizHead = "Question {}/10: What is '{}' in Chinese?".format(self.counter, self.questions[0][self.rdList[self.counter-1]])
            if self.answers[self.counter-1] != None:
                print(self.answers[self.counter-1])
                self.quizText.text = self.answers[self.counter-1]
            print(self.counter, self.answers)

    def btn_submit(self):
        if self.quizText.text != "":
                self.answers[self.counter-1] = self.quizText.text
        if self.answers.count(None) == 0:
            print("Submitted quiz/exam - ToDo: Show popup with results")
        else:
            print("You haven't answered all questions: {} missing. Submit anyway? - ToDo: Popup erstellen mit 'Submit anyway'/'Go back'".format(self.answers.count(None)))
        print("submit")

    def btn_next(self):
        if self.counter < 10:
            if self.quizText.text != "":
                self.answers[self.counter-1] = self.quizText.text
                self.quizText.text = ""
            self.counter += 1
            self.quizHead = "Question {}/10: What is '{}' in Chinese?".format(self.counter, self.questions[0][self.rdList[self.counter-1]])
            if self.answers[self.counter-1] != None:
                print(self.answers[self.counter-1])
                self.quizText.text = self.answers[self.counter-1]
            print(self.counter, self.answers)

class PopupWindow(FloatLayout):
    def __init__(self, userInput):
        super().__init__()
        self.pLabel.text = userInput
        self.pop = Popup(title="Result", content=self, size_hint=(None, None), size=(400, 400))

    def open_popup(self):
        self.pop.open()

    def close_pop(self):
        self.pop.dismiss()


class DashboardWindow(Screen):
    pass    


class MyScreenManager(ScreenManager):
    pass


KV = Builder.load_file("vocabApp.kv")

class VocabularyTrainer(App):
    def build_config(self, config):
        config.setdefaults('example', {
            'optionsexample': 'HSK1'})
        config.read('vocabularytrainer.ini')

    def build_settings(self, settings):
        settings.add_json_panel('Panel Name',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print(config, section, key, value)

    def build(self):
        self.use_kivy_settings = False
        return KV

if __name__ == "__main__":
    app = VocabularyTrainer()
    app.run()