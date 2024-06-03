from flask import Flask, request, jsonify, abort
from random import choice


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


about_me = {
    "name": "Вадим",
    "surname": "Шиховцов",
    "email": "vshihovcov@specialist.ru"
}


quotes = [
    {
        "id": 3,
        "author": "Rick Cook",
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
        "rating": 2
    },
    {
        "id": 5,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы  на только что отполированном полу людей с острыми бритвами в руках.",
        "rating": 3 
    },
    {
        "id": 6,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
        "rating": 1
    },
    {
        "id": 8,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так.",
        "rating": 5
    },
]


@app.route("/")
def hello_world():
    return "Hello, World!"



@app.route("/about")
def about():
    return about_me


# сериализация
@app.route("/quotes")
def get_all_quotes():
    return quotes


# Задание 1-2
@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote, 200
    return f"Quote with id={quote_id} not found", 404


# Задание 3
# dict --> str
@app.get("/quotes/count")
def quotes_count():
    return {
        "count": len(quotes)
    }

# Задание 4
# dict --> str
@app.route("/quotes/random", methods=["GET"])
def random_quote():
    return choice(quotes)

#Практика: Часть-2  Задания
@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    last_quote = quotes[-1]
    new_id = last_quote["id"] + 1
    new_quote["id"] = new_id
    if new_quote.get("rating") is None or new_quote.get('rating') not in range(1,6):
        new_quote["rating"] = 1
    quotes.append(new_quote)
    return new_quote, 201


@app.route("/quotes/<int:quote_id>", methods=["PUT"])
def edit_quote(quote_id):
    new_quote = request.json
    for quote in quotes:
        if quote["id"] == quote_id:
            if new_quote["author"]:
                quote["author"] = new_quote["author"]
            elif new_quote["text"]:
                quote["text"] = new_quote["text"]
            return new_quote, 200
        return f"Quote with id={quote_id} not found", 404
    

@app.route("/quotes/<int:quote_id>", methods=["DELETE"])
def delete_quote(quote_id):
    new_quote = request.json
    for quote in quotes:
        if quote["id"] == quote_id:
            if new_quote["author"]:
                del quote["author"]
                return f"Author in quote with id={quote_id} was delete", quote, 200
            elif new_quote["text"]:
                del quote["text"]
                return f"Text in quote with id={quote_id} was delete", quote, 200
        return f"Quote with id={quote_id} not found", 404

@app.route("/quotes/rating/<int:quote_rating>", methods=["GET"])
def get_quote_rating():
    for quote in quotes:
        quote["rating"] = "1"
    new_quote = request.json
    if new_quote["rating"] <= 5:
        quote["rating"] = new_quote["rating"]
        return quotes, 200
    else:
        quote["rating"] = "1"
        return f"This rating of Quote not valide. Rating is 1", 404


@app.route("/quotes/filter")
def get_quotes_by_filter():
    args = request.args
    print(f'{args = }')
    result = []
    for quote in quotes:
        if all(True if args.get(key, type=type(quote[key])) == quote[key] else False for key in args):
            result.append(quote)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
