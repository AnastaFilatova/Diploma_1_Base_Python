import requests
from pprint import pprint

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()


class VkUser:
    version = '5.130'
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.big_photos = [] # сюда собираются словари с размерами фото 'type': 'z'
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    def get_photos(self, user_id=None):
        if user_id is None:
            user_id = self.owner_id
        fotos_url = self.url + 'photos.get'
        fotos_params = {
            'count': 1000,
            'album_id': 'wall',
            'owner_id': user_id,
            'extended': 1,  # Если был задан параметр extended=1, возвращаются likes — количество отметок Мне нравится
            'photo_sizes': 1,
        }
        self.photos = requests.get(fotos_url, params={**self.params, **fotos_params}).json()

        return self.photos

    def choose_max_photo(self):
        """ Отбирает фото наибольшего формата
            Дает названия для фото на основе количества лайков
        """

        self.photos = self.get_photos()
        # pprint(self.photos)
        # for response in self.photos.keys():
        #     pprint(response['items'][0]['sizes'][-1])
        # pprint(self.photos['response']['items'][0]['sizes'][-1])
        like_count = 0

        for respones in self.photos.values():
            for i in respones['items']:
                pprint(i)
                if i['sizes'][-1]['type'] == 'z':
                    like_count = i['likes']['count']
                    self.big_photos.append(i['sizes'][-1])
                # pprint(i['sizes'][-1])
                # for  i['sizes']
                # pprint(self.big_photos)

        # if ph['response']['items'][0]['sizes'][0]['type'] == 'z':
        #     print(ph['response']['items'][0]['sizes'][0]['type'])
            # self.big_photos.append(photos['response']['items'][0])
            # print(self.big_photos)
        # return self.big_photos
    # def

if __name__ == '__main__':
    vk_client_1 = VkUser(token, '5.130')
    # f = vk_client_1._get_photos()
    vk_client_1.choose_max_photo()
    # pprint(z)
    # pprint(f)
