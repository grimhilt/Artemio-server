from api import create_api
from screen.ScreenManager import ScreenManager

api = create_api()
screen_manager = ScreenManager().getInstance()

if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5500, debug=True)
    #api.run(host="0.0.0.0", port=5500)


