from PIL import Image
import numpy as np
import requests
import os
from bs4 import BeautifulSoup


# Установите адрес хоста и порт вашего прокси-сервера
# proxy_host = "10.109.18.4"
# proxy_port = 3128
# proxy = {"http": f"http://{proxy_host}:{proxy_port}", "https": f"http://{proxy_host}:{proxy_port}"}
# requests_proxies = {"http": f"http://{proxy_host}:{proxy_port}", "https": f"http://{proxy_host}:{proxy_port}"}
proxy = None

def change_image(path, new_size, new_path):
    """
    Изменяет размер изображения.

    :param путь_к_изображению: Путь к исходному изображению.
    :param новые_размеры: Кортеж (ширина, высота) нового размера.
    :param путь_к_выходному_изображению: Путь к выходному изображению.
    """

    # Открываем изображение
    image = Image.open(path)
    # Определяем минимальную сторону
    a_min = min(image.size)

    # Обрезаем изображение, чтобы сделать его квадратным
    image = image.crop((0, 0, a_min, a_min))

    # Изменяем размер
    new_image = image.resize(new_size)

    # Сохраняем измененное изображение

    new_image.save(new_path)


def split_image(new_path, piece_size):
    """
    Разбивает изображение на кусочки заданного размера и создает словарь.

    :param путь_к_изображению: Путь к исходному изображению.
    :param размер_кусочка: Кортеж (ширина, высота) размера кусочка.
    :return: Словарь с индексами и соответствующими кусочками изображения.
    """
    # Открываем изображение
    image = Image.open(new_path)
    width, height = image.size

    # Преобразуем изображение в массив NumPy
    image_array = np.array(image)

    # Разбиваем изображение на кусочки
    pieces = [image_array[i:i + piece_size[1], j:j + piece_size[0]]
              for i in range(0, height, piece_size[1])
              for j in range(0, width, piece_size[0])]

    # Создаем словарь с кортежами в виде (0, 0), (0, 1), (0, 2), и так далее
    l = int(len(pieces) ** 0.5)
    n = 0
    pieces_dict = dict()
    for i in range(l):
        if len(str(i)) < 2:
            row = '0' + str(i)
        else:
            row = str(i)
        for j in range(l):
            if len(str(j)) < 2:
                col = '0' + str(j)
            else:
                col = str(j)
            pieces_dict[f'{row}{col}'] = pieces[n]
            n += 1

    return pieces_dict


def req(url: str, header: dict) -> str:
    '''Получение рандомного изображения с https://www.generatormix.com'''

    response = requests.get(url, header, proxies=proxy)
    # response = requests.get(url, headers=header, proxies=proxy)
    # print(response.status_code)

    # Убедитесь, что запрос успешен
    try:
        # if response.raise_for_status() is None:
        if response.status_code == 200:
            # Создаем объект BeautifulSoup для парсинга HTML
            response = response.text

            soup = BeautifulSoup(response, 'html.parser')
            # находим ссылку на картинку
            img = soup.find('img', class_="lazy thumbnail")
            img_src = img.get('data-src')
            # сохраняем картинку
            # Отправить HTTP-запрос для получения содержимого изображения
            response = requests.get(img_src, proxies=proxy)

            # Проверить успешность запроса
            if response.status_code == 200:
                # Получить содержимое изображения и сохранить в файл
                with open("ai.jpg", "wb") as file:
                    file.write(response.content)
                print("Изображение сохранено успешно.")
            else:
                print(f"Ошибка при получении изображения. Код статуса: {response.status_code}")
                print('Увага!',
                      "Запит не пройшов, перевірте з'єднання з інтернетом, чи правильність написання міста.111")
            path = os.getcwd()
            os.chdir(path)
            path += '/ai.jpg'
            return path

        else:
            print('Увага!', "Запит не пройшов, перевірте з'єднання з інтернетом, чи правильність написання міста.112")
            path = os.getcwd()
            os.chdir(path)
            path += '/ai.jpg'
            return path
    except:

        print('Увага!', "Запит не пройшов, перевірте з'єднання з інтернетом, чи правильність написання міста.")
        path = os.getcwd()
        os.chdir(path)
        path += '/ai.jpg'
        return path


def main(n, size):


    url = "https://www.generatormix.com/random-image-generator"
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
              'User-Agent': 'Mozilla / 5.0(X11; Ubuntu; Linux x86_64; rv: 109.0) Gecko / 20100101 Firefox / 119.0'
              }
    path = req(url, header)

    # path = "/home/vladimiregorov/PycharmProjects/Numbers/ai.jpg"
    new_size = (size * n, size * n)  # Замените на желаемые размеры
    new_path = "output_img.jpg"
    Image.open("ai.jpg").convert("RGB").save("ai.jpg")  # в случае получения файла png конвертируем его в jpeg
    change_image(path, new_size, new_path)

    piece_size = (size, size)  # по размеру кнопки

    # Теперь словарь_кусочков содержит индексы и соответствующие кусочки изображения
    dict_piece = split_image(new_path, piece_size)

    # Сохраняем каждый кусочек в формате JPEG
    # for i, p in dict_piece.items():
    #     i_p = Image.fromarray(p)
    #     paths = os.path.join(os.getcwd(), f"кусочек_{i + 1}.jpg")
    #     i_p.save(paths)

    # переделываем ключи словаря на строки
    b = dict_piece.keys()

    c = [Image.fromarray(i) for i in dict_piece.values()]

    dict_pieces = dict(zip(b, c))

    return dict_pieces


if __name__ == '__main__':
    n = 8
    main(n, 40)