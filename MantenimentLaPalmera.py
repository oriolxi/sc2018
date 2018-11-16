import BotHandler as BH

def main():
    fucodema = -319219660
    
    bot = BH.BotHandler("762999554:AAGPzzwkNnFVwPrirg3TJghN3ZRgrUDMOM0")
    bot.clean_income()
    
    while True:
        last_update = bot.get_next_update()
        if last_update:
            usr = last_update['message']['from']['id']
            message_id = last_update['message']['message_id']
            bot.forward_message(fucodema, usr, message_id)
            #bot.print_message(last_update)
 
main()
