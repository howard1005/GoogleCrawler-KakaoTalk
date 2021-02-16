import os
import json
import requests
import webbrowser

class KakaoTalk():
    code_path = 'accounts/code.txt'
    token_path = 'token.txt'
    def __init__(self):
        self.rest_api_key = "720e4f2ac0b1f44552cbc00c7803bd31"
        self.redirect_url = "http://127.0.0.1:8000/account/login/kakao/callback"
        self.code = self._readTextFile(self.code_path)
        self.token = self._readTextFile(self.token_path)
        if self.code == "" or self.token == "":
            self.refreshCodeAndToken()

    def _readTextFile(self, path):
        if not os.path.isfile(path):
            return ""
        f = open(path, 'r')
        txt = f.read()
        f.close()
        return txt

    def _getAccessCode(self, api_key, redirect_url):
        code_path = self.code_path
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        url = (f"https://kauth.kakao.com/oauth/authorize?"
               f"client_id={api_key}"
               f"&redirect_uri={redirect_url}"
               f"&response_type=code")
        if os.path.isfile(code_path):
            os.remove(code_path)
        webbrowser.get(chrome_path).open(url)
        while not os.path.isfile(code_path):
            pass
        code = self._readTextFile(self.code_path)
        return code

    def _getAccessToken(self, access_code):
        token_path = self.token_path
        url = "https://kauth.kakao.com/oauth/token"
        payload = (f"grant_type=authorization_code"
                    f"&client_id={self.rest_api_key}"
                    f"&redirect_uri={self.redirect_url}"
                    f"&code={access_code}")
        if os.path.isfile(token_path):
            os.remove(token_path)
        print("payload : {}".format(payload))
        headers = {'Content-Type': "application/x-www-form-urlencoded", 'Cache-Control': "no-cache", }
        reponse = requests.request("POST", url, data=payload, headers=headers)
        access_token = json.loads(((reponse.text).encode('utf-8')))
        print("access_token : {}".format(access_token))
        # save token
        f = open(token_path, 'w')
        f.write(access_token['access_token'])
        f.close()
        return access_token['access_token']

    def refreshCodeAndToken(self):
        self.code = self._getAccessCode(self.rest_api_key, self.redirect_url)
        self.token = self._getAccessToken(self.code)

    def sendToMeMessage(self, text):
        push_tag = "[#KUB@] "
        header = {"Authorization": 'Bearer ' + self.token}
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"  # 나에게 보내기 주소
        post = {
            "object_type": "text",
            "text": push_tag + text,
            "link": {
                "web_url": "https://developers.kakao.com",
                "mobile_web_url": "https://developers.kakao.com"
            },
            "button_title": "바로 확인"
        }
        data = {"template_object": json.dumps(post)}
        res = requests.post(url, headers=header, data=data)
        if res.status_code != 200:
            print("fail sendToMeMessage => retry!")
            self.refreshCodeAndToken()
            self.sendToMeMessage(text)



if __name__ == "__main__":
    kakao = KakaoTalk()
    ret = kakao.sendToMeMessage("test1")
    print(ret)
