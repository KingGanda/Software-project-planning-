import os
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER, TOP
import pandas as pd
import requests


class HelloWorld(toga.App): #로그인 화면
    def startup(self):
        self.main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))

        # 로그인 화면 로고
        image_path = 'logo.png'
        image = toga.Image(image_path)

        image_widget = toga.ImageView(image=image, style=Pack(width=200, height=200, padding=(0, 50)))
        self.main_box.add(image_widget)

        name_label = toga.Label(
            'Splash Warriors',
            style=Pack(padding=(0, 10), font_size=20, text_align=CENTER)
        )
        self.main_box.add(name_label)

        self.main_box.add(toga.Box(style=Pack(flex=1)))  # Spacer box to push the button to the bottom

        button_text = 'Log in'
        button = toga.Button(
            button_text,
            on_press=self.show_team_info,
            style=Pack(padding=(10, 15, 10, 15), width=150, alignment=CENTER)
        )
        self.main_box.add(button)

        self.second_screen = SecondScreen(self)

        self.main_window = toga.MainWindow(title=self.formal_name, size=(400, 300))
        self.main_window.content = self.main_box
        self.main_window.show()
        self.main_window.size = (600, 400)  

    def show_team_info(self, widget):
        self.main_window.content = self.second_screen.main_box


class SecondScreen: #로그인 후 메뉴화면
    def __init__(self, app):
        self.app = app
        self.main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=(0, 50)))

        team_info_button = toga.Button(
            'Player Info',
            on_press=self.show_third_screen,
            style=Pack(padding=5, font_size=14, width=100, alignment=CENTER)
        )

        self.main_box.add(team_info_button)
        self.main_box.add(toga.Box(style=Pack(flex=1)))

    def show_third_screen(self, widget):
        third_screen = ThirdScreen(self.app)
        self.app.main_window.content = third_screen.main_box


class ThirdScreen: #선수 정보 화면
    def __init__(self, app):
        self.app = app
        self.main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))

        back_button = toga.Button(
            'Back',
            on_press=self.show_second_screen,
            style=Pack(padding=5, font_size=12, width=100, alignment=CENTER)
        )

        # NBA 공식 데이터 가져오기(api)
        test_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00' \
                   '&PerMode=Totals&Scope=S&Season=2022-23&SeasonType=Regular%20Season&StatCategory=PTS'
        r = requests.get(url=test_url).json()
        table_headers = r['resultSet']['headers']
        data_rows = r['resultSet']['rowSet']
        df = pd.DataFrame(data_rows, columns=table_headers)

        # 데이터를 테이블로 정리하여 보여줌
        table = toga.Table(
            headings=df.columns.tolist(),
            data=df.values.tolist(),
            style=Pack(width=500, height=300, padding=(10, 10), alignment=CENTER),
            missing_value='N/A'  
        )

        self.main_box.add(toga.Box(style=Pack(flex=1)))
        self.main_box.add(table)
        self.main_box.add(back_button)

    def show_second_screen(self, widget):
        self.app.main_window.content = self.app.second_screen.main_box


def main():
    return HelloWorld()


if __name__ == '__main__':
    main().startup()
