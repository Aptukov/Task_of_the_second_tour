# Импортирование необходимых библиотек
import streamlit as st
import fitz  # PyMuPDF
import tempfile
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

Authorization_key = input('Введите ваш ключ авторизации Gigachat API')
# Авторизация в сервисе GigaChat
chat = GigaChat(credentials=Authorization_key, scope='GIGACHAT_API_PERS', model='GigaChat', streaming=True)

# Заголовок приложения
st.title("Резюме статей из PDF")

# Загрузка файла
uploaded_file = st.file_uploader("Загрузите PDF-файл", type="pdf")


# Функция для извлечения текста из PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")  # Открываем PDF-файл из потока
    text = ""
    for page in doc:
        text += page.get_text()  # Извлекаем текст из каждой страницы
    return text


if uploaded_file is not None:
    # Извлечение текста из PDF
    full_text = extract_text_from_pdf(uploaded_file)

    # Проверяем длину текста
    if full_text:
        messages = [
            SystemMessage(content="Вы являетесь помощником для резюмирования текста. Выдавайте ответы всегда на русском, независимо от языка самой статьи. Используйте не болeе 400 слов и будьте лаконичны в ответе."),
            HumanMessage(content=full_text)
        ]

        # Получаем краткое содержание
        res = chat(messages)

        # Вывод ответа
        st.subheader("Краткое резюме:")
        st.write(res.content)
    else:
        st.write("Не удалось извлечь текст из PDF.")
