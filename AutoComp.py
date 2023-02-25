try:  
    from telethon import TelegramClient, sync, errors
    from time import sleep
    from lxml import html
    from functools import partial
    import requests, random, sys, traceback, re


    def scrabThePage(page_number, complCollection): 
        print('https://datki.net/komplimenti/zhenshine/page/' + str(
            page_number) + '/') 
        page = requests.get(
            'https://datki.net/komplimenti/zhenshine/page/' + str(page_number) + '/')
        tree = html.fromstring(page.content) 
        complCollection.extend(tree.xpath('//a[@class="post-copy btn"]/@data-clipboard-text'))


    def message(internal_compliments, internal_api_id, internal_api_hash): 
        internal_client = TelegramClient('Compliments', internal_api_id, internal_api_hash) 
        internal_client.start()  
        rand_compl = random.choice(
            internal_compliments)
        internal_client.send_message(sendToUsername, rand_compl)
        internal_client.disconnect()
        print('ОТПРАВЛЕН КОМПЛИМЕНТ: ' + str(rand_compl)) 


    api_id = 3885864 
    api_hash = '1a0bcdc2020d36fbecb3f5a6a58dafa1'
    defaultRecipient = 'VladimirPutin'
    defaultMinComplimentLength = '70'

    all_compliments = [] 
    print('Сбор комплиментов:', end='\n') 
    i = 1  
    while i <= 6: 
        scrabThePage(i, all_compliments)
        i += 1  
    print('Сбор комплиментов... [OK]', end='\n\n')  

    mask = re.compile(
        '[a-zA-Z0-9_]') 
    is_correct_input = False  
    sendToUsername = 'empty' 
    while (not is_correct_input) and (
    not sendToUsername == ''):  
        sendToUsername = input('Введите имя пользователя: ')  
        is_correct_input = mask.search(
            sendToUsername)
        if (not is_correct_input) and (
        not sendToUsername == ''): 
            print('Введенное имя пользователя содержит недопустимые символы [ERROR]',
                  end='\n\n')

    if (sendToUsername == ''):
        sendToUsername = defaultRecipient 
        print('Имя пользователя: ' + sendToUsername + ' [AUTO]', end='\n\n')
    else:
        print('Имя пользователя: ' + sendToUsername + ' [OK]',
              end='\n\n')

    compliments = []
    while (len(compliments) == 0):
        mask = re.compile('[0-9]')
        is_correct_input = False  
        min_compl_len = '0'  
        while (not is_correct_input) and (
        not min_compl_len == ''): 
            min_compl_len = input('Введите минимальную длину комплимента: ')
            is_correct_input = mask.search(
                min_compl_len)  
            if (not is_correct_input) and (
            not min_compl_len == ''):  
                print('Введенное значение содержит недопустимые символы (должно содержать только цифры) [ERROR]',
                      end='\n\n')  
        if (min_compl_len == ''):  
            min_compl_len = defaultMinComplimentLength  
            print('Минимальная длина комплимента: ' + min_compl_len + ' [AUTO]',
                  end='\n\n')  
        else: 
            print('Минимальная длина комплимента: ' + min_compl_len + ' [OK]',
                  end='\n\n')  
        for compliment in all_compliments: 
            if (len(compliment) >= int(
                    min_compl_len)): 
                compliments.append(compliment)  
        if (len(
                compliments) == 0): 
            print(
                'Для указанной минимальной длины не найдено ни одного комплимента. Попробуйте уменьшить значение. [ERROR]',
                end='\n\n') 
    print('Ожидание нажатия кнопки...', end='\n\n')  
    while True:  
        input()  
        message(compliments, api_id, api_hash)
except KeyboardInterrupt:  
    print(
        'Завершено пользователем [OK]')
except ValueError: 
    print(
        'Возникла ошибка при попытке отправить сообщение указанному адресату [ERROR]')  
except:  
    print('Произошла неизвестная ошибка [ERROR]')  
    print('\n=======ИНФОРМАЦИЯ ОБ ОШИБКЕ=========') 
    traceback.print_exc(limit=2, file=sys.stdout)  
    print('========КОНЕЦ========')
