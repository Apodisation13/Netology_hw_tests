import requests
from os import path


class YandexUploader:
    def __init__(self):
        with open(path.abspath('token.txt')) as f:
            self.ya_token = f.readline()

        self.status = ''  # сообщение успеха загрузки

    def create_folder(self, folder_name: str):

        response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                                params={'path': folder_name},
                                headers={'Authorization': f'OAuth {self.ya_token}'})
        print(response.json())
        print(response.status_code)
        if "error" in response.json():
            self.status = response.json()['message']
            print(self.status)
        else:
            self.status = 'Папка создана'
            print(self.status)

        # if response.status_code == 201:  # если папка создалась (201) или уже есть (409)
        #     print(f'Папка {folder_name} создана')
        #     self.status = 'Папка создана'
        # elif response.status_code == 409:
        #     # print(f'Папка {folder_name} уже есть')
        #     self.status = 'Такая папка уже есть'
        # else:  # это если она не создалась
        #     self.status = f"Ошибка яндекса - {response.json()['message']}"
        # print(self.status)

    def check_folder_name(self):
        names = []  # список всех доступных файлов в конкретной папке

        files = requests.get('https://cloud-api.yandex.net/v1/disk/resources/',
                             params={'path': 'Test1'},
                             headers={'Authorization': f'OAuth {self.ya_token}'})

        # print(files.json())

        if "error" not in files.json():
            number = files.json()['_embedded']['items']
            # print(len(number))
            for each in number:
                names.append(each['name'])
            print('доступные файлики в папке', names)
            return True, names
        return False, names


if __name__ == '__main__':
    ya = YandexUploader()
    ya.create_folder(f'Test1/Folder6')
    ya.check_folder_name()
