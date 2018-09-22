from lib.chat_bot import ChatBot


def main():
    chat = ChatBot()
    while True:
        user_message = input()
        user_message_answer = chat.answer_message(user_message)
        print(user_message_answer)



if __name__ == '__main__':
    main()
