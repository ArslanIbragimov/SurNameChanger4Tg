

import signal
import time
from pyrogram import Client, filters
from pyrogram.raw import functions

class NameSurnameChanger:
    def __init__(self, api_id, api_hash, name_surname_pairs):
        self.api_id = api_id
        self.api_hash = api_hash
        self.name_surname_pairs = name_surname_pairs
        self.original_name_surname = None
        self.current_name_surname = None
        self.app = Client("SurName-Changer", api_id=self.api_id, api_hash=self.api_hash)

    def get_original_name_surname(self):
        with self.app:
            user = self.app.get_me()
            self.original_name_surname = (user.first_name, user.last_name)
            print(f"Текущее имя: {self.original_name_surname[0]}, Текущая фамилия: {self.original_name_surname[1]}")

    def change_name_surname(self):
        with self.app:
            for name, surname in self.name_surname_pairs:
                self.current_name_surname = (name, surname)
                try:
                    self.app.invoke(functions.account.UpdateProfile(
                        first_name=name,
                        last_name=surname
                    ))
                    print(f"Изменено имя на {name} и фамилия на {surname}")
                except Exception as e:
                    print(f"Ошибка при изменении имени и фамилии: {e}")
                time.sleep(5)  # Задержка 5 секунд

    def restore_original_name_surname(self):
        if self.original_name_surname:
            with self.app:
                try:
                    self.app.invoke(functions.account.UpdateProfile(
                        first_name=self.original_name_surname[0],
                        last_name=self.original_name_surname[1]
                    ))
                    print(f"Восстановлено исходное имя и фамилия: {self.original_name_surname[0]} {self.original_name_surname[1]}")
                except Exception as e:
                    print(f"Ошибка при восстановлении исходного имени и фамилии: {e}")

    def signal_handler(self, sig, frame):
        print("Получен сигнал завершения программы")
        self.restore_original_name_surname()
        exit(0)

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.get_original_name_surname()
        self.change_name_surname()

if __name__ == "__main__":
    name_surname_pairs = [
        (".", ""),
        ("..", ""),
        ("...", ""),
    ]
    changer = NameSurnameChanger(api_id='', api_hash='', name_surname_pairs=name_surname_pairs)
    while True:
        changer.run()