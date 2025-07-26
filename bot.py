import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from flask import Flask, request
import re

TOKEN = "vk1.a.ZRJmWUQbDga9FSpNVkuy0m8nF_nRPwCacecCL7GacBT1hp7Oo05_SIMFYMQEUFQ93OyRQ0D7G0C3QvK9tRUk0ZKI83bBslA1YWb0J5SorzCZCwOD487aqlCmT-J3DYKYWA5mozii5hJcTUZKP0dBWDo9ElBC_CoNrbgb196vx5_iEHzxkC4vHj8X72ZJK6v8_J_J59dgGC_ilerRTg05OQ"
GROUP_ID = 231800195
CONFIRMATION_TOKEN = ""

BAD_WORDS = ["блять", "сука", "хуй", "пизда", "ебать", "тварь", "чмо", "гандон", "мразь","бля", "пиздец"]

FAQ_ANSWERS = {
    "как выбрать проект": "Вы можете выбрать проект на странице https://education.vk.company/education_projects. Наведите курсор на интересующий проект и нажмите 'Подробнее'.",
    "какой файл загрузить": "Вы можете загрузить PDF, DOCX или ZIP-файл с решением проекта на соответствующей платформе или по инструкции к проекту.",
    "где найти информацию о вебинарах": "Информацию о вебинарах можно найти в разделе 'Мероприятия' или в Telegram-канале VK Education.",
    "можно ли взять несколько проектов": "Да, вы можете взять несколько проектов, если успеваете выполнять их в срок.",
}


def detect_bad_language(text):
    return any(re.search(word, text.lower()) for word in BAD_WORDS)


def generate_answer(message):
    message = message.lower()

    if detect_bad_language(message):
        return "Пожалуйста, соблюдайте уважительный тон. Ваш вопрос содержит неприемлемую лексику."

    for keyword, answer in FAQ_ANSWERS.items():
        if keyword in message:
            return answer

    if message.startswith("можно ли") or message.startswith("возможно ли"):
        return "Да, это возможно."

    return (
        "Я пока не знаю ответа на этот вопрос, но вы можете посмотреть информацию здесь: "
        "https://education.vk.company/education_projects или задать вопрос напрямую модераторам."
    )


# Flask-приложение для Callback API
app = Flask(__name__)


@app.route("/callback", methods=["POST"])
def callback():
    data = request.json

    if data["type"] == "confirmation":
        return CONFIRMATION_TOKEN

    if data["type"] == "message_new":
        vk_session = vk_api.VkApi(token=TOKEN)
        vk = vk_session.get_api()

        user_id = data["object"]["message"]["from_id"]
        text = data["object"]["message"]["text"]
        response = generate_answer(text)

        vk.messages.send(user_id=user_id, message=response, random_id=0)

    return "ok"