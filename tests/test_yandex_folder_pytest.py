from apps.yandex_folder import YandexUploader
import requests


class TestApp:
    @classmethod
    def setup_class(cls):
        print('setup_class')

    @classmethod
    def teardown_class(cls):
        print('teardown_class')

    @staticmethod
    def setup():
        print('setup method')

    @staticmethod
    def teardown():
        print('teardown method')

    def test_token_len(self):
        assert len(YandexUploader().ya_token) == 39

    def test_correct_auth(self):
        response = requests.get('https://cloud-api.yandex.net/v1/disk',
                                headers={'Authorization': f'OAuth {YandexUploader().ya_token}'})
        assert response.status_code == 200

    def test_wrong_token(self):
        response = requests.get('https://cloud-api.yandex.net/v1/disk',
                                headers={'Authorization': f'OAuth {YandexUploader().ya_token}q'})
        assert response.status_code == 401

    def test_create_existing_folder(self):
        ya = YandexUploader()
        path = 'Test1/Folder3'
        ya.create_folder(path)
        assert ya.status == f'По указанному пути "{path}" уже существует папка с таким именем.'
        folder_list = ya.check_folder_name()[1]
        assert 'Folder3' in folder_list

    def test_create_folder_wrong_path(self):
        ya = YandexUploader()
        path = 'Test2/Folder3'
        ya.create_folder(path)
        assert ya.status == f'Указанного пути "{path}" не существует.'

    def test_create_new_folder(self):
        ya = YandexUploader()
        path = 'Test1/Folder7'
        folder_set_before = set(ya.check_folder_name()[1])  # множество из списка папок до создания папки
        ya.create_folder(path)  # создали папку
        assert ya.status == 'Папка создана'
        folder_set_after = set(ya.check_folder_name()[1])  # множество из списка папок ПОСЛЕ создания папки
        assert folder_set_after.difference(folder_set_before) == {'Folder7'}  # проверка что создалась только 1 папка
