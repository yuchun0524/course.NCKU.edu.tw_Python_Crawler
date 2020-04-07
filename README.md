# course.NCKU.edu.tw-Python-Crawler

### 使用工具
1. selenium: 可以實際開啟 browser 去開啟網站，做到點選、上一頁...等動作
    * 解決抓取網頁原始碼問題: js 產生網頁碼用 reqeusts 工具抓不到
        * browser 右鍵，點選"檢視網頁原始碼看不到"
        * 按 F12 才看的到
2. Firefox(真的 browser), [geckodriver](https://github.com/mozilla/geckodriver/releases)
2. xpath: 節點搜尋

### 一些注意的點
1. 以下兩段程式碼效果不同: xpath 好像不能連續搜尋(我沒有仔細查，不過用起來是這樣)
```python=
browser = browser.find_elements_by_xpath("//table[@id = 'A9-table']/tbody/tr/td")
```
* 所以底下的第一句如同不存在，第二句會搜尋到整篇的 \<td>
```python=
browser = browser.find_elements_by_xpath("//table[@id = 'A9-table']/tbody/tr")
browser = browser.find_elements_by_xpath("//td")
```
2. 當點選頁面之後，回到上一頁，原本搜尋的東西都不能用了，要重新搜尋
```python=
depart = browser.find_elements_by_xpath("//*[contains(text(), '%s')]" % depart_list[i])
depart[0].click()
.
.
browser.back()
depart = browser.find_elements_by_xpath("//*[contains(text(), '%s')]" % depart_list[i])
```
3. 解決出現英文頁面問題: 要求中文 'zh-CN'
```python=
profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'zh-CN')    # query chinese page
browser = webdriver.Firefox(firefox_profile = profile)
```

### 參考資料(紀錄幾個不錯的網站，但不見得有用到)
[BeautifulSoup](https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/)
[requests](https://blog.gtwang.org/programming/python-requests-module-tutorial/)

