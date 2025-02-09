from openai import OpenAI

from .card import Card
from .deck import Deck
from .config import Config

class TarotReading:
    def __init__(self, tarot_cards: list[Card], question_asked: str, response: str):
        self.__tarot_cards = tarot_cards
        self.__question_asked = question_asked
        self.__response = response

    @property
    def tarot_cards(self) -> list[Card]:
        return self.__tarot_cards

    @property
    def question_asked(self) -> str:
        return self.__question_asked

    @property
    def response(self) -> str:
        return self.__response

class TarotReader:
    __init_question: str = 'You are a intelligent assistant who specializes in tarot card readings.'

    def __init__(self, open_ai_api_key: str, model_name: str):
        self.config = Config()
        self.__messages: list[dict[str, str]] = list()
        self.__model_name: str = model_name
        self.__open_ai_api_key: str = open_ai_api_key

        self.__client = OpenAI(api_key=self.__open_ai_api_key)
        self.__write_using_stream = self.config.chatgpt_write_using_stream

    def set_ai_model(self, model_name: str) -> None:
        self.__model_name = model_name

    def get_reading(self, question: str, additional_context: list[str] = None, num_cards: int = 3) -> TarotReading:
        deck = Deck()
        cards_drawn: list[Card] = list()

        for i in range(num_cards):
            cards_drawn.append(deck.draw_card())

        self.__load_client()

        # Initial question
        self.__append_user_msg(question)

        # Context
        if additional_context:
            self.__append_user_msg('The next messages provide additional context to enhance your reading so that it is '
                                   'tailored to this context.')
            for context in additional_context:
                self.__append_user_msg(context)

        card_string = ', '.join(
            f'{card} in {"reversed" if card.is_reversed else "upright"} position' for card in cards_drawn
        )

        self.__append_user_msg(f'The following cards are drawn: {card_string}')

        chat_completion = self.__client.chat.completions.create(
            model=self.__model_name, messages=self.__messages, stream=self.__write_using_stream
        )

        assistant_reply = chat_completion.choices[0].message.content

        self.__append_user_msg(assistant_reply)

        return TarotReading(
            tarot_cards=cards_drawn,
            question_asked=question,
            response=assistant_reply
        )

    def __load_client(self):
        self.__start_new_thread()

    def __append_user_msg(self, message: str) -> None:
        self.__messages.append({'role': 'user',
                                'content': message})

    def __append_assistant_msg(self, message: str) -> None:
        self.__messages.append({'role': 'assistant',
                                'content': message})

    def __append_system_msg(self, message: str) -> None:
        self.__messages.append({'role': 'system',
                                'content': message})

    def __start_new_thread(self):
        self.__clear_messages()
        self.__append_system_msg(self.__init_question)

    def __clear_messages(self) -> None:
        self.__messages.clear()
