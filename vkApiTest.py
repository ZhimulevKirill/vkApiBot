import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import xml.etree.ElementTree as ET
import json
import os
import sys


def returnCommands(vk, event, random_id):
    print(event)
    print('Новое сообщение:')
    print('Для меня от:', event.obj.message['from_id'])
    print('Текст:', event.obj.message['text'])
    main_message = """Список доступных команд  для бота:
    - - - - - - -
    посчитай (арифметическое выражение с комплексными и действительными)
    Возможные примеры и ответы:
    2*2 = 4
    2*2.5 = 5
    2/3 = 2/3 (несократимая дробь)
    10/26 = 5/13
    pi = 3.141592653589793238462643383279502884197169399375105820974...
    e^(ipi) = -1
    e*pi = 8.539734222673567065463550869546574495034888535765114961879...
    e = 2.718281828459045235360287471352662497757247093699959574966967627724076630353547594571382178525166427
    - - - - - - -
    реши (уравнение, например x^2+2*x+1=0)
    Указание:
    Для возведения в степень используйте знак "^", пример: a^b
    Для умножения числа на переменную используйте знак "*" или не используйте знака вообще, пример: 15x; 15*x;
    Для деления используйте знак "/"
    Для извлечения квадратного корня используйте sqrt(число или переменная) или дробную степень
    Желательно отделять знаки "=", "+" и "-" пробелами с двух сторон
    Для установки правильного порядка действий, используйте скобки "( )"
    Порядок выполнения действий такой же, как обычно
    Очень рекоммендуется использовать в качестве переменной "x" или "y" в любом регистре
    НЕ ИСПОЛЬЗУЙТЕ В КАЧЕСТВЕ ПЕРЕМЕННОЙ "i", поскольку он зарезервирован за мнимой единицей
    - - - - - - -
    статистика(не работает)
    - - - - - - -
    """
    vk.messages.send(user_id=event.obj.message['from_id'],
                     message=main_message,
                     random_id=random_id)


def main():
    vk_session = vk_api.VkApi(
        token="8c41dd93029c04baccab705cde61c329dd56a4dfc3aea533065a915c0895d52553f79cdab48027e78c6ed")

    longpoll = VkBotLongPoll(vk_session, 194656953)
    file_counter = 0
    for event in longpoll.listen():
        file_counter += 1
        if event.type == VkBotEventType.MESSAGE_NEW:
            random_id = random.randint(0, 2 ** 64)
            vk = vk_session.get_api()
            if event.obj.message['text'][:5] == 'test1':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Test1 successful",
                                 random_id=random_id)
            elif event.obj.message['text'][:7] == 'нарисуй':
                content = ''
                if ''.join(event.obj.message['text'][7:].split(' ')) == '':
                    content = "0"
                else:
                    content = '%5E'.join(event.obj.message['text'][8:].split('^'))
                    content = '%20'.join(content.split(' '))
                    content = '%2B'.join(content.split('+'))
                    content = '%3D'.join(content.split('='))
                plot_request = "http://api.wolframalpha.com/v1/simple?appid=3R3XL6-L474YU3HH9&i=graph%20"
                plot_request += content
                plot_response = requests.get(plot_request)
                try:
                    response_file = "plot_file_" + str(file_counter) + ".jpg"
                    with open(response_file, "wb") as file:
                        file.write(plot_response.content)
                    # print(event.obj.message['from_id'])
                    # data = vk.photos.getMessagesUploadServer(event.obj.message['from_id'])
                    data = vk.photos.getMessagesUploadServer(peer_id=event.obj.message['from_id'])
                    # print(data)
                    upload_url = data['upload_url']
                    files = {'photo': open(response_file, 'rb')}
                    response = requests.post(upload_url, files=files)
                    # print(response)
                    result = json.loads(response.text)
                    # print(result)
                    uploadResult = vk.photos.saveMessagesPhoto(server=result['server'],
                                                               photo=result['photo'],
                                                               hash=result['hash'])
                    # print(uploadResult)
                    imageID = json.loads(result["photo"])[0]["photo"]
                    # print(json.loads(result["photo"]))
                    access_key = 0
                    attachment = "photo{}_{}_{}".format(event.obj.message['from_id'],
                                                        uploadResult[0]['id'],
                                                        uploadResult[-1]['access_key'])
                    # print(attachment)
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="randomTextMessage",
                                     attachment=attachment,
                                     random_id=random_id)
                    # print(uploadResult[0])
                    # vk.messages.send(user_id=event.obj.message['from_id'],
                    #                message="randomTextMessage",
                    #                attachment=uploadResult[0]["id"],
                    #                 random_id=random_id)
                except Exception:
                    data = vk.photos.getMessagesUploadServer(peer_id=event.obj.message['from_id'])
                    upload_url = data['upload_url']
                    files = {'photo': open("C:/Users/1/Desktop/unnamed.jpg", 'rb')}
                    response = requests.post(upload_url, files=files)
                    result = json.loads(response.text)
                    uploadResult = vk.photos.saveMessagesPhoto(server=result['server'],
                                                               photo=result['photo'],
                                                               hash=result['hash'])
                    attachment = "photo{}_{}_{}".format(event.obj.message['from_id'],
                                                        uploadResult[0]['id'],
                                                        uploadResult[-1]['access_key'])
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Похоже, что-то пошло не так. Проверьте синтаксис команды или корректность запроса.",
                                     random_id=random_id,
                                     attachment=attachment)
            elif event.obj.message['text'][:8] == "посчитай":
                try:
                    req = '%5E'.join(event.obj.message['text'][9:].split('^'))
                    req = '%20'.join(req.split(' '))
                    req = '%2B'.join(req.split('+'))
                    req = '%3D'.join(req.split('='))
                    request = "http://api.wolframalpha.com/v2/query?input={}&appid=3R3XL6-L474YU3HH9".format(req)
                    request += '&includepodid=Result'
                    request += '&includepodid=DecimalApproximation'
                    if event.obj.message['text'][9:] == 'e':
                        request = "http://api.wolframalpha.com/v2/query?input={}&appid=3R3XL6-L474YU3HH9".format(
                            "e%20to%20100%20digits")
                        request += '&includepodid=Result'
                    response = requests.get(request)
                    if response:
                        answer = ET.fromstring(response.content)
                        out_message = answer[0][0][1].text
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=out_message,
                                         random_id=random_id)
                except Exception:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Похоже, что-то пошло не так. Проверьте синтаксис команды или корректность запроса.",
                                     random_id=random_id)

            elif event.obj.message['text'][:4] == "реши":
                req = '%5E'.join(event.obj.message['text'][5:].split('^'))
                req = '%20'.join(req.split(' '))
                req = '%2B'.join(req.split('+'))
                req = '%3D'.join(req.split('='))
                request = "http://api.wolframalpha.com/v2/query?input={}&appid=3R3XL6-L474YU3HH9".format(req)
                request += "&excludepodid=Input&excludepodid=RootPlot&excludepodid=AlternateForm"
                request += "&excludepodid=NumberLine&excludepodid=RootsInTheComplexPlane"
                response = requests.get(request)

                if response:
                    answer = ET.fromstring(response.content)
                    # root_word_assosiations = ['Solutions', 'Solution', 'Complex Solution', 'Complex Solutions',
                    #                          'Real Solutions', 'Real Solution', 'Numerical solutions', 'Numerical solution']
                    roots = []
                    try:
                        for pod in answer:
                            for i in range(int(pod.attrib['numsubpods'])):
                                roots.append(pod[i][1].text)
                        print(roots)
                        out_message_text = ',\n'.join(roots)
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=out_message_text,
                                         random_id=random_id)
                    except:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Похоже, что-то пошло не так. Проверьте синтаксис команды или корректность запроса.",
                                         random_id=random_id)

                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Похоже, что-то пошло не так. Проверьте синтаксис команды или корректность запроса.",
                                     random_id=random_id)


            elif event.obj.message['text'][:7] == 'команды':
                returnCommands(vk, event, random_id)
            else:
                returnCommands(vk, event, random_id)


if __name__ == '__main__':
    while True:
        main()
