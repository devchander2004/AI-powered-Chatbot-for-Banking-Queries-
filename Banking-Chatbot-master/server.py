from threading import Thread
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from chatbot import get_response, get_response2
from flask import Flask, render_template


class ChatServer(WebSocket):

    def handleMessage(self):
        message = self.data

        response = get_response(message)
        a = get_response2(message)

        self.sendMessage(response)
        self.sendMessage(a)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')  # Ensure index.html in templates folder


def run_flask():
    app.run(debug=True, use_reloader=False)  # Prevent duplicate threads


def run_ws():
    server = SimpleWebSocketServer('', 8000, ChatServer)
    print("🚀 WebSocket Server started at ws://localhost:8000")
    server.serveforever()


if __name__ == '__main__':
    t1 = Thread(target=run_flask)
    t2 = Thread(target=run_ws)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
