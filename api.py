import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email, password):
        add = '/api/key'
        headers = {'email': email, 'password': password}
        res = requests.get(self.base_url + add, headers=headers)
        status, result = res.status_code, None
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_pets(self, auth_key, filter):
        add = '/api/pets'
        headers = {'auth_key': auth_key}
        filter = {'filter': filter}
        res = requests.get(self.base_url + add, headers=headers, params=filter)
        status, result = res.status_code, None
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def create_pet(self, auth_key, name, animal_type, age, pet_photo):
        add = '/api/pets'
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        with open(pet_photo, 'rb') as b_file:
            b_file = b_file.read()
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, b_file, 'image/jpeg')
            })
        headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
        res = requests.post(self.base_url + add, headers=headers, data=data)
        status, result = res.status_code, None
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def create_pet_simple(self, auth_key, name, animal_type, age):
        add = '/api/create_pet_simple'
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
        res = requests.post(self.base_url + add, headers=headers, data=data)
        status, result = res.status_code, None
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def set_photo(self, auth_key, pet_id, pet_photo):
        add = f'/api/pets/set_photo/{pet_id}'
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        with open(pet_photo, 'rb') as b_file:
            b_file = b_file.read()
        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, b_file, 'image/jpeg')})
        headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
        res = requests.post(self.base_url + add, headers=headers, data=data)
        status, result = res.status_code, None
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key, pet_id, name, animal_type, age):
        add = f'/api/pets/{pet_id}'
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key, 'Content-Type': data.content_type}
        res = requests.put(self.base_url + add, headers=headers, data=data)
        status, result = res.status_code, None
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key, pet_id):
        add = f'/api/pets/{pet_id}'
        headers = {'auth_key': auth_key}
        res = requests.delete(self.base_url + add, headers=headers)
        status, result = res.status_code, None
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
