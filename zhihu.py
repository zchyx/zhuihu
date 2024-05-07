import json
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
def drop_scroll(browser):
    for i in range(1,150,1):
        time.sleep(2)
        j = i/10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        browser.execute_script(js)
def switch_window(browser):
    time.sleep(2)
    windows = browser.window_handles
    browser.switch_to.window(windows[-1])
def switch_window_back(browser):
    windows = browser.window_handles
    browser.switch_to.window(windows[0])
def mybrowser(url):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9200")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    time.sleep(2)
    switch_window_back(browser)
    drop_scroll(browser)
    return browser
def questioninfo():
    url = 'https://www.zhihu.com/topic/27267395/hot'
    answer_urls = []
    browser = mybrowser(url)
    # data = browser.find_element(By.XPATH, "//div[@class='ContentItem AnswerItem']")
    q_urls = browser.find_elements(By.XPATH, "//h2[@class='ContentItem-title']/div/meta[@itemprop='url']")
    for q_url in q_urls:
        answer_url = q_url.get_attribute('content')
        print(answer_url)
        answer_urls.append(answer_url)
    return answer_urls
def answerinfo():
    answer_urls = questioninfo()
    for answer_url in answer_urls:
        answer_browser = mybrowser(answer_url)
        answer_data = answer_browser.find_element(By.XPATH,"//div[@class='ContentItem AnswerItem']")
        answer_dataset = answer_browser.find_elements(By.XPATH,"//div[@class='ContentItem AnswerItem']")
        q_title = answer_browser.find_element(By.XPATH,"//meta[@itemprop='name']")
        keyword = answer_browser.find_element(By.XPATH,"//meta[@itemprop='keywords']").get_attribute("content")
        answercount = answer_browser.find_element(By.XPATH,"//meta[@itemprop='answerCount']").get_attribute("content")
        commentcount = answer_browser.find_element(By.XPATH,"//meta[@itemprop='commentCount']").get_attribute("content")
        createdtime = answer_browser.find_element(By.XPATH,"//meta[@itemprop='dateCreated']").get_attribute("content")
        follower = answer_browser.find_elements(By.XPATH,"//strong[@class='NumberBoard-itemValue']")[0].get_attribute("title")
        view = answer_browser.find_elements(By.XPATH, "//strong[@class='NumberBoard-itemValue']")[1].get_attribute("title")
        answer_names = answer_data.find_elements(By.XPATH,"//div[@class='AuthorInfo']/meta[@itemprop='name']")
        answer_tags = answer_data.find_elements(By.XPATH, "//div[@class='ztext AuthorInfo-badgeText css-14ur8a8']")
        contents = answer_data.find_elements(By.XPATH,"//div[@class='RichContent-inner']")
        times = answer_data.find_elements(By.XPATH,"//div[@class='ContentItem-time']/a/span")
        for answer_time,content,answer_name,answertag,answer_info in zip(times,contents,answer_names,answer_tags,answer_dataset):
            answer_question = []
            title = q_title.get_attribute("content")
            info = json.loads(answer_info.get_attribute("data-za-extra-module"))
            qid = info["card"]["content"]["parent_token"]
            upvotes = info["card"]["content"]["upvote_num"]
            comments = info["card"]["content"]["comment_num"]
            answer_id = json.loads(answer_info.get_attribute("data-zop"))["itemId"]
            answer = answer_name.get_attribute("content")
            answer_content = content.get_attribute("innerText")
            created_time = answer_time.get_attribute("data-tooltip")
            answer_tag = answertag.get_attribute("innerText")
            answer_question.append(title)
            answer_question.append(qid)
            answer_question.append(keyword)
            answer_question.append(answercount)
            answer_question.append(commentcount)
            answer_question.append(createdtime)
            answer_question.append(follower)
            answer_question.append(view)
            answer_question.append(answer)
            answer_question.append(answer_tag)
            answer_question.append(answer_id)
            answer_question.append(answer_content)
            answer_question.append(created_time)
            answer_question.append(upvotes)
            answer_question.append(comments)
            save(answer_question)

"""
title  问题标题
qid    问题ID
keyword  问题关键词
answercount 回复人数
commentcount 评论人数
question_createdtime 创建时间
follower  关注者
view  浏览量
answer 回复者
answer_tag 回复者标签
aid    回复ID
content 回复内容
answer_createdtime 发布时间
upvote   赞成
comment  评论
"""
def save(answer_question):
    with open('LLM.csv', 'a+', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(answer_question)
answerinfo()