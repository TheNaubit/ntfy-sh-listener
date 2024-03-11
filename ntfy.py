from dotenv import load_dotenv
import websocket
import json
import os
import requests

load_dotenv()

ntfy_ws = os.environ["NTFY_WS"]
ntfy_access_control = os.environ.get("NTFY_ACCESS_CONTROL")  # Use .get to handle if not defined
ntfy_topic = os.environ["NTFY_TOPIC"]
telegram_bot = os.environ["TELEGRAM_BOT"]
chat_id = os.environ["TELEGRAM_ID"]

def on_message(ws, message):
    msg = json.loads(message)
    if not 'title' in msg or len(msg['title']) == 0:
       print('\n >>> Ntfy.sh websocket Successfully Passing...! \n')
    else:
        headers = {"content-type": "application/x-www-form-urlencoded"}
        querystring = {"chat_id": chat_id, "text": msg['title'] + "\n\n" +  msg['message']}
        response = requests.request(
                "POST", telegram_bot, headers=headers, params=querystring)
        print("websocket: " + message + "Ntfy: " + response.text)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("\n NTFY websocket Connection closed \n")

def on_open(ws):
    print("\n >> Opened NTFY websocket connection..! \n")

if __name__ == "__main__":
    headers = []
    if ntfy_access_control:  # Add the header only if ntfy_access_control is defined and not empty
        headers.append("Authorization: Bearer " + str(ntfy_access_control))

    wsapp = websocket.WebSocketApp("wss://" + str(ntfy_ws) + ntfy_topic + "/ws",
                                   on_open=on_open,
                                   on_message=on_message,
                                   on_error=on_error,
                                   on_close=on_close,
                                   header=headers)  # headers is now conditionally populated
    wsapp.run_forever()
