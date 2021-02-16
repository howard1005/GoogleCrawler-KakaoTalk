# views.py
from django.shortcuts import redirect
import urllib
import webbrowser


# code 요청
def kakao_login(request):
    app_rest_api_key = '720e4f2ac0b1f44552cbc00c7803bd31'
    redirect_uri = "http://127.0.0.1:8000/account/login/kakao/callback"
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    webbrowser.get(chrome_path).open(url)
    #return redirect(
    #    f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    #)
#https://kauth.kakao.com/oauth/authorize?client_id=720e4f2ac0b1f44552cbc00c7803bd31&redirect_uri=http://127.0.0.1:8000/account/login/kakao/callback&response_type=code


# access token 요청
def kakao_callback(request):
    params = urllib.parse.urlencode(request.GET)
    print('params : ' + str(params))
    file = open('code.txt', 'w')
    file.write(params[5:])  # 파일에 문자열 저장
    file.close()
    return params
    #return redirect(f'http://127.0.0.1:8000/account/login/kakao/callback?{params}')


if __name__ == "__main__":
    kakao_login({})
