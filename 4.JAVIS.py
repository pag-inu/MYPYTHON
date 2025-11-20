import subprocess
from weather import get_weather_api

#STTからテキストを受け取って、コマンドを出力
def exsecute_command_javis_from_STT(stt_output :str):
    
    command_map = {
        "天気を教えて" : ask_weather,
    }

    for key, action in command_map.items():
        if key in stt_output:
            try:
                return action()
            except Exception as e:
                return print(f"対応するコマンドがありませんでした: {e}")


def ask_weather():
    place = input("どこの天気を知りたいですか？: ")
    print(get_weather_api(place))

if __name__ == "__main__":
    stt_result = "天気を教えて"
    exsecute_command_javis_from_STT(stt_result)