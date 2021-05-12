import mock

from apps.secretaty_app import documents, directories
from apps.secretaty_app import get_all_doc_owners_names, add_new_doc, delete_doc


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

    def test_ap_1(self):
        assert get_all_doc_owners_names() == {'Василий Гупкин', 'Аристарх Павлов', 'Геннадий Покемонов'}
        # for each in {'Геннадий Покемонов', 'Василий Гупкин', 'Аристарх Павлов'}:
        #     assert each in get_all_doc_owners_names()

    @mock.patch('builtins.input', side_effect=['11-2'])
    def test_del_doc_exist(self, input):
        deleted_doc, status = delete_doc()

        directories_del = {
            '1': ['2207 876234', '5455 028765'],
            '2': ['10006'],
            '3': []
        }

        documents_del = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]

        assert directories_del == directories
        assert documents_del == documents
        assert deleted_doc == '11-2'
        assert status == True

    @mock.patch('builtins.input', side_effect=['11-4'])  # такой док, которого нету там
    def test_del_doc_nonexist(self, input):

        deleted_doc, status = delete_doc()

        # directories_del = directories.copy()
        # assert directories_del == directories

        assert deleted_doc is None
        assert not status

    @mock.patch('builtins.input', side_effect=['11-11', 'invoice', 'Володя Володьевич', '3'])
    def test_add_doc(self, input):
        """если запускать все 4, этот не пройдёт, так как везде есть изменения документов"""
        add_new_doc()
        directories_add = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': ['11-11']
        }

        documents_add = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
            {"type": "invoice", "number": "11-11", "name": "Володя Володьевич"}
        ]
        # вот здесь супер! Если сделать файл ошибочным, то появится кнопка CLICK TO SEE DIFFERENCE
        # и будут видны все отличия! (окно по типу гита с разными коммитами)!!!
        assert directories_add == directories
        assert documents_add == documents, 'ошибкаааа'  # отображение сообщения в assertion error
