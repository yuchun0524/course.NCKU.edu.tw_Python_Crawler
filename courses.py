from selenium import webdriver
import time

f = open('ncku_course_data','w')

profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'zh-CN')    # query chinese page
browser = webdriver.Firefox(firefox_profile = profile)

browser.get('https://course.ncku.edu.tw/index.php?c=qry_all') 

departs = browser.find_elements_by_xpath("//*[@class='btn_dept']") # have to type in the complete class=' '
depart_list = []
for depart in departs:
    depart_list.append(depart.text)

#for i in range(int(len(depart_list)/2)):
for i in range(3):
    depart = browser.find_elements_by_xpath("//*[contains(text(), '%s')]" % depart_list[i])
    depart_name = depart[0].text
    depart[0].click()
    courses_elements = browser.find_elements_by_xpath("//table[@id = 'A9-table']/tbody/tr/td")

    course_list = [depart_name]
    for i,element in enumerate(courses_elements):
        if(i%10 == 0):
            continue
        course_list.extend(element.text.split())
#        course_list.append(element.text)

        if (i%10 == 9):    # last one
            for j,item in enumerate(course_list):
                if (j == len(course_list)-3):   # we don't need the last two items
                    f.write(item + '\n')
                    break
                else:
                    f.write(item + ',')
            course_list = [depart_name]

    browser.back()

browser.quit()
f.close()

