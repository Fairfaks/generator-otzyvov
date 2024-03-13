import os
import csv
import openai

# Данные для доступа к API ChatGPT
API_KEY = 'апишечка'
PROXY = 'http://проксичка'
# ======================================================


def main():
    ai = Ai()
    # Список дял хранения отзыва
    reviews = []
    # Список продуктов
    products = read_file('products.txt')
    # Промт
    promt = read_file('prompt.txt')
    promt = '\n'.join(promt)

    for p in products:
        query = promt.replace('<product>', p)
        print(f"Генерирую отзыв для: {p}")
        text = ai.chatgpt_query(query)
        reviews.append([p, text])

    # Запись отзывов в CSV
    write_csv('reviews.csv', reviews)

    print('Готово!')
    # Эта строка блокирует закрытие окна до нажатия Enter
    input("Нажмите Enter для завершения...")

# ===============================================
def write_csv(file, reviews):
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerows(reviews)

# ===============================================
def read_file(file):
    with open(file, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

# ===============================================
class Ai():
    def __init__(self):
        self.key = API_KEY
        self.proxy = PROXY

    def chatgpt_query(self, query):
        self._set_proxy(self.proxy)
        openai.api_key = self.key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": query}
            ],
            #max_tokens=150,
            #temperature=0.2,
            #top_p=1
        )
        return response['choices'][0]['message']['content']

    def _set_proxy(self, proxy):
        os.environ["http_proxy"] = proxy
        os.environ["https_proxy"] = proxy


# =======================================================
if __name__ == '__main__':
    main()