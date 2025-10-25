from pathlib import Path
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, CardTransition
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Rectangle
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
import ctypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
screenWidth = user32.GetSystemMetrics(0)
screenHeight = user32.GetSystemMetrics(1)


def CreateButton(text):
    btn = Button(
        text=text,
        size_hint=(None, None),
        size=(150, 50),
    )
    return btn


class LogPanel(BoxLayout):
    def __init__(self, max_logs=100, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.max_logs = max_logs
        self.logs = []
        self.logContainer = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=[5, 5, 5, 5])
        self.logContainer.bind(minimum_height=self.logContainer.setter('height'))
        self.scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        self.scroll.add_widget(self.logContainer)
        self.add_widget(self.scroll)

    def addLog(self, text):
        label = Label(text=text, size_hint_y=None, height=25, text_size=(self.width, None), halign='left', valign='top')

        def updateText(*_):
            label.text_size = (self.scroll.width - 20, None)

        label.bind(width=updateText, texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
        self.scroll.bind(width=updateText)
        updateText()
        self.logContainer.add_widget(label)
        self.logs.append(label)
        if len(self.logs) > self.max_logs:
            old = self.logs.pop(0)
            self.logContainer.remove_widget(old)
        Clock.schedule_once(self.scrollDown, 0.05)

    def scrollDown(self, *args):
        self.scroll.scroll_y = 0


class SplashScreen(Screen):
    def __init__(self, preloaded, **kwargs):
        super().__init__(**kwargs)
        preloaded.allow_stretch = False
        preloaded.keep_ratio = True
        self.add_widget(preloaded)

    def on_enter(self):
        Clock.schedule_once(self.showMainForm, 3)

    def showMainForm(self, dt):
        app = App.get_running_app()
        app.root.transition = FadeTransition(duration=0.4)
        app.root.current = 'main_menu'


class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        with self.canvas.before:
            self.bg = Rectangle(source="C:/Users/user/OneDrive/Pictures/dauntless background (1).jpg", size=self.size, pos=self.pos)
        self.bind(size=self.update_bg, pos=self.update_bg)
        anchor = AnchorLayout()
        box = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None))
        startBtn = CreateButton("New Game")
        loadBtn = CreateButton("Load")
        optionBtn = CreateButton("Option")
        startBtn.pos_hint = {"center_x": 0.5}
        optionBtn.pos_hint = {"center_x": 0.5}
        loadBtn.pos_hint = {"center_x": 0.5}
        startBtn.bind(on_release=self.goToGame)
        isEmpty = not any(app.dataDir.iterdir())
        if isEmpty:
            loadBtn.disabled = True
            loadBtn.background_color = (0.5, 0.5, 0.5, 1)
        else:
            loadBtn.disabled = False
        box.add_widget(startBtn)
        box.add_widget(loadBtn)
        box.add_widget(optionBtn)
        anchor.add_widget(box)
        self.add_widget(anchor)

    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def goToGame(self, instance):
        self.manager.transition = FadeTransition(duration=0.5)
        self.manager.current = "character_creation"


class CharacterCreation(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        boxMain = BoxLayout(orientation='vertical')
        boxTop = BoxLayout(orientation='horizontal', size_hint_y=0.7)
        boxTopLeft = BoxLayout(orientation='vertical', size_hint_x=0.85)
        boxTopRight = BoxLayout(orientation='vertical', size_hint_x=0.15)
        boxBottom = BoxLayout(orientation='vertical', size_hint_y=0.3)
        textAnchor = AnchorLayout(anchor_x='left', anchor_y='center', padding=[10, 15, 0, 0])
        textBox = BoxLayout(orientation='vertical', size_hint=(None, None), spacing=10)
        startBtn = CreateButton("New Game")
        startBtn.size_hint = (None, None)

        self.characterName = TextInput(
            hint_text="Enter you name...",
            multiline=False,
            font_size=20,
            size_hint=(None, None),
            width=300,
            height=50
        )
        dropdown = DropDown()
        for classInfo in ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]:
            btn = Button(text=classInfo, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, text=classInfo: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        classButton = Button(text="Choose Class", size_hint=(None, None), size=(300, 50))
        classButton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, value: setattr(classButton, 'text', value))
        self.race = TextInput(
            hint_text="Enter you name...",
            multiline=False,
            font_size=20,
            size_hint=(None, None),
            width=300,
            height=50
        )
        self.alignment = TextInput(
            hint_text="Enter you name...",
            multiline=False,
            font_size=20,
            size_hint=(None, None),
            width=300,
            height=50
        )

        startBtn.bind(on_release=self.Hello)
        # anchorRight = AnchorLayout(anchor_x='right', anchor_y='top')
        self.logPanel = LogPanel(max_logs=100)
        x = 0
        while x < 30:
            x += 1
            self.logPanel.addLog(f"this is {x}")

        # anchorRight.add_widget(self.logPanel)
        # self.add_widget(anchorRight)
        textBox.add_widget(self.characterName)
        # textBox.add_widget(startBtn)
        textBox.add_widget(classButton)
        textBox.add_widget(self.race)
        textBox.add_widget(self.alignment)
        textAnchor.add_widget(textBox)
        boxTopLeft.add_widget(textAnchor)
        boxTopRight.add_widget(self.logPanel)
        boxTop.add_widget(boxTopLeft)
        boxTop.add_widget(boxTopRight)
        boxMain.add_widget(boxTop)
        boxMain.add_widget(boxBottom)

        self.add_widget(boxMain)

    def Hello(self, instance):
        self.logPanel.addLog("Button is pressed")



class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        anchor = AnchorLayout()
        box = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None))
        box.add_widget(Label(text="Game Screen",
                             halign="center",
                             valign="middle"))
        back_btn = CreateButton("Back to Menu")
        back_btn.bind(on_release=self.go_back)
        box.add_widget(back_btn)
        anchor.add_widget(box)
        self.add_widget(anchor)

    def go_back(self, instance):
        self.manager.transition = CardTransition(direction="up", duration=0.6)
        self.manager.current = "main_menu"


class MainForm(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.splash = Image(source="C:/Users/user/OneDrive/Pictures/WhatsApp Image 2025-10-22 at 20.27.18_e9962413.jpg")
        _ = self.splash.texture

    def build(self):
        self.checkFiles()
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash', preloaded=self.splash))
        sm.add_widget(MainMenu(name="main_menu"))
        sm.add_widget(GameScreen(name="game_screen"))
        sm.add_widget(CharacterCreation(name="character_creation"))

        sm.current = 'splash'
        return sm

    def on_start(self):
        Window.size = (screenWidth * 0.6, screenHeight * 0.5)
        Window.top = (screenHeight - screenHeight * 0.6)/2
        Window.left = (screenWidth - screenWidth * 0.6)/2
        Window.minimum_width, Window.minimum_height = screenWidth * 0.6, screenHeight * 0.5

    def checkFiles(self):
        baseDir = Path(__file__).resolve().parent
        self.dataDir = Path(baseDir)/"CharacterInfo"
        self.dataDir.mkdir(exist_ok=True)


MainForm().run()
