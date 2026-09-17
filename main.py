from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window


Window.size = (450, 600)


class MenuScreen(Screen):

    def exit_game(self):
        App.get_running_app().stop()

    def go_settings(self, *args):
        self.manager.current = "settings"

    def go_play(self, *args):
        self.manager.current = "play"


class SettingsScreen(Screen):

    def on_pre_enter(self, *args):
        self.ids.difficulty_label.text = (
            "Current: " + self.get_difficulty()
        )

    #повернення у головне меню
    def back_to_menu(self, *args):
        self.manager.current = "menu"

    #виставляння складності гри
    def set_difficulty(self, difficulty):
        app = App.get_running_app()
        app.difficulty = difficulty
        self.ids.difficulty_label.text = (
            "Current: " + self.get_difficulty()
        )

    #отримання складності гри з кнопок для роботи зміни важкості гри
    def get_difficulty(self):
        app = App.get_running_app()
        return app.difficulty.upper()


class Fish(Image):

    fish_current = None
    fish_index = 0
    hp_current = None

    def on_kv_post(self, base_widget):
        self.GAME_SCREEN = self.parent.parent.parent

        return super().on_kv_post(base_widget)

    def new_fish(self, *args):
        app = App.get_running_app()
        self.fish_current = app.LEVELS[app.LEVEL][self.fish_index]
        self.source = app.FISHES[self.fish_current]["source"]
        base_hp = app.FISHES[self.fish_current]["hp"]
        if app.difficulty == "easy":
            self.hp = max(1, base_hp // 2)
        elif app.difficulty == "medium":
            self.hp = base_hp
        elif app.difficulty == "hard":
            self.hp = base_hp * 2

        self.hp_current = self.hp

        self.opacity = 1

    def defeated(self):
        self.opacity = 0

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos) or not self.opacity:
            return
        
        self.hp -= 1
        self.GAME_SCREEN.score += 1

        print(f"Fish HP left: {self.hp}")

        if self.hp <= 0:
            self.defeated()
            app = App.get_running_app()
            if len(app.LEVELS[app.LEVEL]) > self.fish_index + 1:

                self.fish_index += 1
                Clock.schedule_once(self.new_fish, 1.2)
            else:
                Clock.schedule_once(
                    self.GAME_SCREEN.level_complete,
                    1.2
                )
                self.fish_index = 0

        return super().on_touch_down(touch)


class GameScreen(Screen):

    score = NumericProperty(0)

    def on_pre_enter(self, *args):
        self.score = 0
        app = App.get_running_app()
        app.LEVEL = 0
        self.ids.level_complete.opacity = 0
        self.ids.next_level_btn.opacity = 0
        self.ids.level_complete.text = "LEVEL COMPLETE!"
        self.ids.fish.fish_index = 0

        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        self.start_game()
        return super().on_enter(*args)

    def start_game(self):
        self.ids.fish.new_fish()

    def level_complete(self, *args):
        self.ids.level_complete.opacity = 1
        app = App.get_running_app()
        if app.LEVEL < len(app.LEVELS) - 1:

            self.ids.next_level_btn.opacity = 1

        else:
            self.ids.level_complete.text = "GAME COMPLETE!"

    def next_level(self):
        app = App.get_running_app()
        app.LEVEL += 1

        self.ids.level_complete.opacity = 0
        self.ids.next_level_btn.opacity = 0

        self.ids.level_complete.text = "LEVEL COMPLETE!"

        self.ids.fish.fish_index = 0

        self.ids.fish.new_fish()

    def back_to_menu(self, *args):
        self.manager.current = "menu"


class MainApp(App):

    main_button_color = (0.1, 0.5, 0.8, 1)
    LEVEL = 0
    difficulty = "easy"
    FISHES = {
        "fish1": {
            "source": "photo_2026-09-03_18-41-14.jpg",
            "hp": randint(1, 7)
        },

        "fish2": {
            "source": "photo_2026-09-03_18-41-21.jpg",
            "hp": randint(3, 8)
        },
        "fish3": {
            "source": "Angler_Fish.webp",
            "hp": randint(1, 7)
        },

        "fish4": {
            "source": "Arapaima.webp",
            "hp": randint(3, 8)
        },
        "fish5": {
            "source": "Blood_Jelly.webp",
            "hp": randint(1, 7)
        },

        "fish6": {
            "source": "Blue_Jellyfish.webp",
            "hp": randint(3, 8)
        },
        "fish7": {
            "source": "Bone_Biter.webp",
            "hp": randint(1, 7)
        },

        "fish8": {
            "source": "Crab.webp",
            "hp": randint(3, 8)
        },
        "fish9": {
            "source": "fish_eye.webp",
            "hp": randint(1, 7)
        },

        "fish10": {
            "source": "Flesh_Reaver.webp",
            "hp": randint(3, 8)
        },
        "fish11": {
            "source": "Flying_Fish.webp",
            "hp": randint(1, 7)
        },

        "fish12": {
            "source": "Green_Jellyfish.webp",
            "hp": randint(3, 8)
        },
        "fish13": {
            "source": "Pink_Jellyfish.webp",
            "hp": randint(1, 7)
        },

        "fish14": {
            "source": "Sand_Shark.webp",
            "hp": randint(3, 8)
        },
        "fish15": {
            "source": "Sharkron.webp",
            "hp": randint(1, 7)
        },

        "fish16": {
            "source": "Shark.webp",
            "hp": randint(3, 8)
        },
    }

    LEVELS = [
        ["fish1", "fish13", "fish11"],
        ["fish7", "fish3", "fish9", "fish10"],
        ["fish2", "fish5", "fish6", "fish12"],
        ["fish4", "fish8", "fish14"],
        ["fish16", "fish13", "fish15"],
    ]
    def build(self):
        sm = ScreenManager()
        sm.add_widget(
            MenuScreen(name="menu")
        )
        sm.add_widget(
            SettingsScreen(name="settings")
        )
        sm.add_widget(
            GameScreen(name="play")
        )
        return sm

game = MainApp()
game.run()