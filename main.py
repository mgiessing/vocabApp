import random
import pandas as pd
import unidecode
import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.settings import SettingsWithSidebar
from kivy.config import Config, ConfigParser
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from settingsjson import settings_json

def replace_tones(orig_voc):
    unaccented_voc = unidecode.unidecode(orig_voc)
    return(unaccented_voc)

def get_vocab(hsklevel):
    df = pd.read_excel(r"static/{}.xlsx".format(hsklevel), engine="openpyxl")
    en = df['English']
    zh = df['Chinese']
    pinyin = df['Pinyin']
    return df, en, zh, pinyin

def get_config():
    if os.path.exists('vocabularyTrainer.ini'):
        config = ConfigParser()
        config.read('vocabularytrainer.ini')
        return config.get('example', 'optionsexample'), int(config.get('example', 'wordsexample'))
    else:
        return "HSK1", 10

class MainWindow(Screen):
    userInput = ObjectProperty(None)
    vocab = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        print("Initialized Main!")
        self.hsklevel, _ = get_config()
        self.df, self.en, self.zh, self.pinyin = get_vocab(self.hsklevel)
        self.rd = random.randint(0, self.df.shape[0]-1)
        self.vocab = "HSK Level {}\nWhat is '{}' in Chinese?".format(self.hsklevel, self.en[self.rd])

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
        self.userInput.text = ""
        self.rd = random.randint(0, self.df.shape[0]-1)
        self.vocab = "HSK Level {}\nWhat is '{}' in Chinese?".format(self.hsklevel, self.en[self.rd])
        
    def validate(self, answer):        
        if answer == self.zh[self.rd]:
            return("Well done, even in chinese characters!")
        elif answer == self.pinyin[self.rd]:
            return("Well done, you also got the correct tones!")
        elif answer == replace_tones(self.pinyin[self.rd]):
            return("Well done! Keep in mind the tones '{}'".format(self.pinyin[self.rd]))
        else:
            return("Sorry, that was not correct!\nThe correct vocab is {}".format(self.pinyin[self.rd]))

class QuizWindow(Screen):
    quizHead = ObjectProperty(None)
    quizText = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(QuizWindow, self).__init__(**kwargs)
        print("Initialized Quiz!")
        self.hsklevel, self.words = get_config()
        self.counter = 1
        self.df, _, _, _ = get_vocab(self.hsklevel)
        self.questions = [self.df["English"], self.df["Chinese"], self.df["Pinyin"]]
        self.answers = [None]*self.words
        self.rdList =[random.randrange(0, self.df.shape[0], 1) for i in range(self.words)]
        self.quizHead = "{} Question {}/{}: What is '{}' in Chinese?".format(self.hsklevel, self.counter, self.words, self.questions[0][self.rdList[self.counter-1]])
        print(self.rdList)

    def btn_prev(self):
        if self.counter > 1:
            if self.quizText.text != "":
                self.answers[self.counter-1] = self.quizText.text
                self.quizText.text = ""
            self.counter -= 1
            self.quizHead = "{} Question {}/{}: What is '{}' in Chinese?".format(self.hsklevel, self.counter, self.words, self.questions[0][self.rdList[self.counter-1]])
            if self.answers[self.counter-1] != None:
                print(self.answers[self.counter-1])
                self.quizText.text = self.answers[self.counter-1]
            print(self.counter, self.answers)

    def btn_submit(self):
        if self.quizText.text != "":
                self.answers[self.counter-1] = self.quizText.text
        if self.answers.count(None) == 0:
            print("Submitted quiz/exam - ToDo: Show popup with results")
            self.validate()
            self.__init__()
        else:
            PopupWindow("You haven't answered all questions: {} missing.".format(self.answers.count(None))).open_popup
            print("You haven't answered all questions: {} missing. Submit anyway? - ToDo: Popup erstellen mit 'Submit anyway'/'Go back'".format(self.answers.count(None)))
        print("submit")

    def btn_next(self):
        if self.counter < self.words:
            if self.quizText.text != "":
                self.answers[self.counter-1] = self.quizText.text
                self.quizText.text = ""
            self.counter += 1
            self.quizHead = "{} Question {}/{}: What is '{}' in Chinese?".format(self.hsklevel, self.counter, self.words, self.questions[0][self.rdList[self.counter-1]])
            if self.answers[self.counter-1] != None:
                print(self.answers[self.counter-1])
                self.quizText.text = self.answers[self.counter-1]
            print(self.counter, self.answers)

    def validate(self):
        correct = 0
        for idx, val in enumerate(self.answers):
            print(idx, val)
            print(self.rdList[idx], replace_tones(self.questions[2][self.rdList[idx]]))
            if val == replace_tones(self.questions[2][self.rdList[idx]]):
                correct+=1
        pLabel = ("You got {}/{} correct, which is {:.2f}%".format(correct, len(self.answers), correct/len(self.answers)*100))
        print(pLabel)
        PopupWindow(pLabel).open_popup()

class VocabularyList(Screen):
    def __init__(self, **kwargs):
        super(VocabularyList, self).__init__(**kwargs)
        print("Initialized Vocabulary!")

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        print("Initialized RecycleView!")
        self.hsklevel, _ = get_config()
        self.df, self.en, self.zh, self.pinyin = get_vocab(self.hsklevel)
        print(len(self.en))
        self.data = []
        self.data = [{'spalte1_SP': str(self.en[x]), 'spalte2_SP': str(self.pinyin[x]), 'spalte3_SP': str(self.zh[x])} for x in range(len(self.en))]

class Tabelle(BoxLayout):
    pass

class PopupWindow(FloatLayout):
    def __init__(self, userInput):
        super().__init__()
        self.pLabel.text = userInput
        self.pop = Popup(title="Result", content=self, size_hint=(None, None), size=(400, 400))

    def open_popup(self):
        self.pop.open()

    def close_pop(self):
        self.pop.dismiss()

class MyScreenManager(ScreenManager):
    pass

KV = Builder.load_file("vocabApp.kv")

class VocabularyTrainer(App):
    def __init__(self, **kwargs):
        super(VocabularyTrainer, self).__init__(**kwargs)

    def build_config(self, config):
        config.setdefaults('example', {
            'optionsexample': 'HSK1',
            'wordsexample': '10'})
        config.read('vocabularytrainer.ini')

    def build_settings(self, settings):
        settings.add_json_panel('Panel Name',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print(config, section, key, value)
        print(self.root.ids.sm.screen_names)
        for sc in self.root.ids.sm.screen_names:
            self.root.ids.sm.get_screen(sc).__init__()

    def build(self):
        self.use_kivy_settings = False
        return KV

if __name__ == "__main__":
    app = VocabularyTrainer()
    app.run()