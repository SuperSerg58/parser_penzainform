from bs4 import BeautifulSoup
import re
import requests
import time
from datetime import datetime


keywords = []

SLEEP_DAY = 1800
SLEEP_NIGHT = 3600


# Функция получения номера последнего прочитанного поста
def post_number():
    f_open = open('links.txt', 'r')
    f_list = list(f_open)
    link = str(f_list[0])
    number_id = re.findall(r"\d+", link)
    number = int(number_id[0])
    f_open.close()
    return number


# Функция получения HTML-страницы
def get_html(url):
    r = requests.get(url)
    return r.text


def parse_data(html, number):
    soup = BeautifulSoup(html, 'lxml')
    post = soup.find("div", id="p" + str(number)).text.strip()  # получаем содержимое поста
    date = soup.find('div', id="p" + str(number)).parent.find('div',
                                                              class_='date').text.strip()  # получаем дату публикации
    datapost = {'post': post,
                'date': date}
    return datapost


def write_link(url_1):
    link = open('links.txt', 'w')
    link.write(url_1)
    link.close()


def main():
    error_count = 0
    post_id = post_number()  # Текущий id поста равен результату из функции post_number()

    while post_id < post_id + 2:
        post_id += 1
        url = "http://forum.penzainform.ru/viewtopic.php?p=" + str(post_id)  # Создаем URL который будет парситься
        try:
            html = get_html(url)  # Получаем HTML страницы
            message = parse_data(html, post_id)  # Процесс пасинга, который возвращает словарь datapost
            print('{}\n{}\n{}\n\n'.format(url, message['date'], message['post']))

            for keyword in keywords:
                if keyword in message['post']:
                    date = datetime.now().strftime('%Y-%m-%d %H')
                    # save_dir = os.path.abspath(os.path.dirname(__file__))
                    final = open('/home/serg/Рабочий стол/POST/' + '{}.txt'.format(date), 'a')
                    final.write('{}\n{}\n{}\n\n'.format(url, message['date'], message['post']))
                    final.close()

            write_link(url)

            if message['post']:
                error_count = 0

        except:
            print(url + '\n' + 'ERROR 404\n')
            error_count += 1
            if error_count == 40:
                break


if __name__ == '__main__':
    while True:
        t_time = int(datetime.now().strftime('%H'))
        date = datetime.now().strftime('%Y-%m-%d %H:%M')
        if 9 <= t_time < 18:
            main()
            print('\n{} Следующая проверка через 30 минут.'.format(date))
            time.sleep(SLEEP_DAY)
        else:
            main()
            print('\n{} Следующая проверка через 60 минут.'.format(date))
            time.sleep(SLEEP_NIGHT)
