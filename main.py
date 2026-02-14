import sys
import requests
import self
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from requests import HTTPError
from urllib3.util import url


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_level = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_level)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_level.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_level.setObjectName("description_level")

        self.setStyleSheet("""
             QLabel, QPushButton{
               font-family: sans-serif;
             }
             QLabel#city_label{
               font-size: 30px;
             }
             QLineEdit#city_input{
               font-size: 33px;
             }
             QPushButton#get_weather_button{
               font-size: 30px;
               font-weight: bold;
             }
             QLabel#temperature_label{
               font-size: 75px;
             }
             QLabel#emoji_label{
               font-size: 100px;
               font-family: segoe UI emoji;
             }
             QLabel#description_level{
               font-size: 40px;
               font-weight: bold;
             }
        
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "f1ec4cf5a9a47c98e71f2141a8cd3e34"
        city = self.city_input.text()
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
            else:
                self.display_error("City not found!")

        except requests.exceptions.HTTPError as http_error:
           match response.status_code:
               case 400:
                   self.display_error("Bad Request:\nplease check your input again\n")
               case 401:
                   self.display_error("Unauthorized:\nInvalid API_key\n")
               case 403:
                   self.display_error("Forbidden:\nAccess is denied")
               case 404:
                   self.display_error("Not found:\nCity not found\n")
               case 500:
                   self.display_error("Internal server error:\nPlease try again later\n")
               case 502:
                   self.display_error("Bad gateway:\nInvalid response from the server\n")
               case 503:
                   self.display_error("service unavailable:\nserver is down\n")
               case 504:
                   self.display_error("Gateway timeout:\nNo response from the server\n")
               case _:
                   self.display_error (f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nPlease check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nThe request has timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nplease check your url")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Rquest error:\n{req_error}")



    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_level.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_c = data["main"]["temp"]
        temperature_f = temperature_c * 1.8 + 32
        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.temperature_label.setText(f"{temperature_c:.0f}^C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_level.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "☁️"
        elif 500 <= weather_id <= 531:
            return "☔🌧️"
        elif 600 <= weather_id <= 622:
            return "🏂❄️"
        elif 700 <= weather_id <= 741:
            return "💨🍃"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return""



if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
