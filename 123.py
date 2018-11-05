import requests
import datetime
import logging
import pymorphy2
#Установка адреса бота
url = "https://api.telegram.org/bot654218156:AAFd8L_rex4YNmX7IR2qRKHFYifnmHGIrTA/"
morph = pymorphy2.MorphAnalyzer()
start = "Добро пожаловать в бот для нормирования текста!\nДля продолжения введите одно или несколько слов для приведения их в нормальную форму:"
helptext = "Команды:\n/start - Выводит сообщение о том, как управлять и работать с ботом;\n/help - выводит список поддерживаемых команд;"
#Поиск последнего сообщения из массива чата с пользователем Telegram.
def lastUpdate(dataEnd):
        res = dataEnd['result']
        totalUpdates = len(res) - 1
        return res[totalUpdates]
#Получение идентификатора чата Telegram
def getChatID(update):
        chatID = update['message']['chat']['id']
        return chatID
#отправка запроса sendMessage боту
def sendResp(chat, value):
        try:
                settings = {'chat_id': chat, 'text': value}
                resp = requests.post(url + 'sendMessage', data=settings)
                return resp
        except Exception as e:
                logging.error("error: " + str(e) + "date: " + str(datetime.datetime.now()) + " user: " + message['message']['from']['first_name'] + " id: " + str(message['message']['from']['id']) + " text: " + text)        
                return 0
#Get-запрос на обновление информации к боту. Результат – строка json. Метод .json позволяет развернуть ее в массив
def getUpdatesJson(request):
        try:
                settings = {'timeout': 100, 'offset': None}
                response = requests.get(request + 'getUpdates', data=settings)
                return response.json()
        except Exception as e:
                logging.error("error: " + str(e) + "date: " + str(datetime.datetime.now()) + " user: " + message['message']['from']['first_name'] + " id: " + str(message['message']['from']['id']) + " text: " + text)        
                return 0
def pymorphy(text):
        t=text.split()
        b = ""
        for word in t:
                try:
                        p = morph.parse(word)[0]
                        b = b + p.normal_form + " "
                except Exception as e:
                        logging.error("error: " + str(e) + "date: " + str(datetime.datetime.now()) + " user: " + message['message']['from']['first_name'] + " id: " + str(message['message']['from']['id']) + " text: " + text)
                        return "Введена некорректная строка"
        return b
#Главная функция
def main():
        logging.basicConfig(level = logging.INFO, filename = u'mylog.log')
        updateID = lastUpdate(getUpdatesJson(url))['update_id']
#Бесконечный цикл, который отправляет запросы боту на получение обновлений
        while True:
#Если обновление есть, отправляем сообщение 
                if updateID == lastUpdate(getUpdatesJson(url))['update_id']:
                        message = lastUpdate(getUpdatesJson(url));
                        text = message['message']['text']
                        logging.info("date: " + str(datetime.datetime.now()) + " user: " + message['message']['from']['first_name'] + " id: " + str(message['message']['from']['id']) + " text: " + text)
                        if text == '/start':
                                sendResp(getChatID(message), start)
                                updateID += 1
                        else:
                                if text == '/help':
                                        sendResp(getChatID(message), helptext)
                                        updateID += 1
                                else:
                                        sendResp(getChatID(message), pymorphy(text))
                                        updateID += 1
#Запуск главной функции
if __name__ == '__main__':
        main()
