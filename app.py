# Импортирование необходимых библиотек
import streamlit as st
import fitz  # PyMuPDF
import tempfile
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

# Заголовок приложения
st.title("Приложение для резюмирования научных статей в формате PDF")

# Получение ключа авторизации пользователя
Authorization_key = st.text_area('Введите ваш ключ авторизации Gigachat API')

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials=Authorization_key, scope='GIGACHAT_API_PERS', model='GigaChat', streaming=True)

# Загрузка файла
uploaded_file = st.file_uploader("Загрузите PDF-файл", type="pdf")


# Функция для извлечения текста из PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")  # Открываем PDF-файл
    text = ""
    for page in doc:
        text += page.get_text()  # Извлекаем текст из каждой страницы
    return text

if uploaded_file is not None:
    try:
        # Извлечение текста из PDF
        full_text = extract_text_from_pdf(uploaded_file)

        # Проверяем длину текста
        if full_text:
            messages = [
                SystemMessage(content="Вы являетесь помощником для резюмирования текста. Выдавайте ответы всегда на русском, независимо от языка самой статьи. Используйте не болeе 200 слов и будьте лаконичны в ответе."),
                HumanMessage(content=full_text)
            ]

            # Получаем краткое содержание
            res = chat(messages)

            # Вывод ответа
            st.subheader("Краткое резюме:")
            st.write(res.content)
        else:
            st.write("Не удалось извлечь текст из PDF.")

    except Exception as e:
        st.subheader('Вы не ввели свой ключ авторизации, либо он неверный.')
