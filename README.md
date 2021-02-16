GoogleCrawler-KakaoTalk
===

Google search engine-based crawler linked with KakaoTalk

Any issues please report to <howard170627@gmail.com>

# Config

- DB config (Modify config.py) 
    + `host` is ip address of DB (default : localhost)
    + `dbname` is name of connected DB
    + `user` is user name of connected DB
    + `password` is password of user (default : password)
    + `port` is port of connected DB (default : 3306)

- Make DB table
    ```python
    python DataBase.py
    ```
- Set Keyword (Modify CrawlerHandler.py)
    + Modify main code 
    ```python
    crawler_handler.addKeywords(['your keyword 1', 'your keyword 2' ... 'your keyword n'])
    ```
  
# Run
   ```python
   python CrawlerHandler.py
   ```