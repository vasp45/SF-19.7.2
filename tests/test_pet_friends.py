import pytest
from api import PetFriends
from settings import valid_email, valid_password


class TestPetFriends:
    """
    все тесты можно запустить вместе в одной сессии,
    они будут проходить последовательно, используя один api ключ и информацию
    из предыдущих тестов, например удаляя питомца добавленного ранее;
    кроме этого, все тесты можно запускать отдельно

    есть ошибка в документации:
    '/api/pets' и '/api/create_pet_simple' возвращают словарь с одним лишним ключом: '_id'
    """

    api_key = None
    new_pet_id = None

    def setup_method(self):
        self.pf = PetFriends()

    def test_get_api_key(self, email=valid_email, password=valid_password):
        """ получение ключа; get '/api/key' """
        status, result = self.pf.get_api_key(email, password)
        assert status == 200
        assert type(result) == dict
        assert len(result) == 1
        self.__class__.api_key = result.get('key')
        assert self.api_key is not None

    def test_get_api_key_neg(self, email=valid_email, password='----'):
        """ получение ключа; негативный тест; get '/api/key' """
        status, _ = self.pf.get_api_key(email, password)
        assert status != 200

    def test_create_pet_simple(self,
                               name='Дружок',
                               animal_type='пёс',
                               age='3'):
        """ создание питомца без фото; post '/api/create_pet_simple' """

        # для независимого запуска
        if self.api_key is None:
            self.api_key = self.get_api_key(self.pf)
            assert self.api_key is not None

        status, result = self.pf.create_pet_simple(self.api_key, name, animal_type, age)
        assert status == 200
        assert type(result) == dict
        assert len(result) == 8  # ошибка, должно быть 7 ключей, лишний ключ: '_id'
        assert result["age"] == age
        assert result["animal_type"] == animal_type
        assert result["name"] == name
        assert result["pet_photo"] == ""
        assert type(result["created_at"]) == str
        assert result["user_id"] == self.api_key
        self.__class__.new_pet_id = result.get("id")
        assert self.new_pet_id is not None

    def test_create_pet_simple_neg(self,
                                   name='Дружок',
                                   animal_type='пёс',
                                   age='3'):
        """ создание питомца без фото; без api ключа; post '/api/create_pet_simple' """

        status, result = self.pf.create_pet_simple('', name, animal_type, age)
        assert status != 200

    def test_set_photo(self, pet_photo='img/ph_02.jpg'):
        """ добавление фото; post '/api/pets/set_photo/{pet_id}' """

        # для независимого запуска
        if self.api_key is None:
            self.api_key = self.get_api_key(self.pf)
            assert self.api_key is not None
        if self.new_pet_id is None:
            self.new_pet_id = self.create_pet(self.pf, self.api_key)

        status, result = self.pf.set_photo(self.api_key, self.new_pet_id, pet_photo)
        assert status == 200
        assert type(result) == dict
        assert len(result) == 8  # ошибка, должно быть 7 ключей, лишний ключ: '_id'
        assert result["pet_photo"].startswith('data:image')
        assert result["user_id"] == self.api_key
        assert result["id"] == self.new_pet_id

    def test_update_pet_info(self,
                             name='Мухтар',
                             animal_type='щенок',
                             age='0'):
        """ обновление информации; put '/api/pets/{pet_id}' """

        # для независимого запуска
        if self.api_key is None:
            self.api_key = self.get_api_key(self.pf)
            assert self.api_key is not None
        if self.new_pet_id is None:
            self.new_pet_id = self.create_pet(self.pf, self.api_key)

        status, result = self.pf.update_pet_info(self.api_key, self.new_pet_id, name, animal_type, age)
        assert status == 200
        assert type(result) == dict
        assert len(result) == 7
        assert result["age"] == age
        assert result["animal_type"] == animal_type
        assert result["name"] == name
        assert result["user_id"] == self.api_key
        assert result["id"] == self.new_pet_id

    def test_create_pet(self,
                        name='Пушок',
                        animal_type='кот',
                        age='1',
                        pet_photo='img/ph_01.jpg'):
        """ создание питомца с фото; post '/api/pets' """

        # для независимого запуска
        if self.api_key is None:
            self.api_key = self.get_api_key(self.pf)
            assert self.api_key is not None

        status, result = self.pf.create_pet(self.api_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert type(result) == dict
        assert len(result) == 8  # ошибка, должно быть 7 ключей, лишний ключ: '_id'
        assert result["age"] == age
        assert result["animal_type"] == animal_type
        assert result["name"] == name
        assert result["pet_photo"].startswith('data:image')
        assert type(result["created_at"]) == str
        assert result["user_id"] == self.api_key
        self.__class__.new_pet_id = result.get("id")
        assert self.new_pet_id is not None

    def test_get_pets(self, filter=''):
        """ получение списка питомцев; get '/api/pets' """

        # для независимого запуска
        if self.api_key is None:
            self.api_key = self.get_api_key(self.pf)
            assert self.api_key is not None

        status, result = self.pf.get_pets(self.api_key, filter)
        assert status == 200
        assert type(result) == dict
        assert len(result) == 1
        assert len(result['pets']) > 0

    def test_delete_pet(self):
        """ удаление питомца; delete '/api/pets/{pet_id}' """

        # для независимого запуска
        if self.api_key is None:
            self.api_key = self.get_api_key(self.pf)
            assert self.api_key is not None
        if self.new_pet_id is None:
            self.new_pet_id = self.create_pet(self.pf, self.api_key)

        status, result = self.pf.delete_pet(self.api_key, self.new_pet_id)
        assert status == 200

    def test_not_valid_delete(self):
        """ удаление питомца без api ключа; delete '/api/pets/{pet_id}' """

        # на случай, если питомцев в базе нет
        if self.api_key is None:
            self.api_key = self.get_api_key(self.pf)
            assert self.api_key is not None
        self.create_pet(self.pf, self.api_key)

        _, result = self.pf.get_pets(self.api_key, '')
        status, _ = self.pf.delete_pet('', result["pets"][0]["id"])
        assert status != 200

    # методы для независимого запуска
    @staticmethod
    def get_api_key(pf):
        _, api_key = pf.get_api_key(valid_email, valid_password)
        return api_key.get("key")

    @staticmethod
    def create_pet(pf, api_key):
        _, pet_id = pf.create_pet_simple(api_key, 'Шарик', 'пёс', '2')
        return pet_id.get("id")
