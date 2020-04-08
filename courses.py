from selenium import webdriver
import csv
import time

f_csv = open('ncku_course.csv', 'w', newline='', encoding="utf-8")
writer = csv.writer(f_csv)
#f = open('ncku_course_data','w')

course_list_name = ['系所名稱', '系號-序號', '課程碼-分班碼', '屬性碼', '年級', '類別',
                    '科目名稱', '學分', '必/選修', '教師姓名', '已選課人數/餘額', '時間', '教室', '課程大綱']
writer.writerow(course_list_name)

profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'zh-TW')    # query chinese page
browser = webdriver.Firefox(firefox_profile=profile)

browser.get('https://course.ncku.edu.tw/index.php?c=qry_all')

# have to type in the complete class=' '
departs = browser.find_elements_by_xpath("//*[@class='btn_dept']")
depart_list = []
for depart in departs:
    depart_list.append(depart.text)

for i in range(int(len(depart_list)/2)):
#for i in range(3):
    time.sleep(2)
    depart = browser.find_elements_by_xpath("//*[contains(text(), '%s')]" % depart_list[i])
    depart_name = depart[0].text
    depart[0].click()
    time.sleep(2)
    courses_elements = browser.find_elements_by_xpath("//table[@id = 'A9-table']/tbody/tr/td")

    course_list = [depart_name]

    """ used for write csv (start) """
    for i, element in enumerate(courses_elements):
        if (i % 10 == 0):  # discard first one
            continue
        elif (i % 10 == 1):
            oldlist = element.text.split()
            if len(oldlist) == 3:
                dept_seq = oldlist[0]
                class_seq = oldlist[1]
                attr_seq = oldlist[2]
                course_list.append(dept_seq)  # 系號-序號
            else:
                class_seq = oldlist[0]
                attr_seq = oldlist[1]
                course_list.append('')
            course_list.append(class_seq)  # 課程碼-分班碼
            course_list.append(attr_seq)  # 屬性碼
        elif (i % 10 == 5):
            oldlist = element.text.split()
            if len(oldlist) != 0: 
                units = oldlist[0]
                required = oldlist[1]
                course_list.append(units)  # 學分
                course_list.append(required)  # 必選修
            else:
                course_list.append('')
                course_list.append('')
        elif (i % 10 == 8):
            oldlist = element.text.split()
            if len(oldlist) != 0:
                class_time = oldlist[0]
                if len(oldlist) > 1:
                    location = oldlist[1:]
                    course_list.append(class_time)
                    course_list.append(location)
                else:
                    course_list.append(class_time)
                    course_list.append('')
            else:
                course_list.append('')
                course_list.append('')
        elif (i % 10 == 9):   # the last one is href, it need to be drawed out by css_selector and then use get_attribute
            href = element.find_elements_by_css_selector('a')
            if (len(href) == 0):    # no href exits
                course_list.append('')
            else:
                url = href[0].get_attribute('href')
                if (url[0] != 'h'):    # not a url
                    course_list.append('')
                else:
                    course_list.append(url)
        else:   # we don't need the text of the last one (when i%10 == 9)
            course_list.append(element.text.split())
        if (i % 10 == 9):    # last one
            writer.writerow(course_list)
            course_list = [depart_name]
            
    """ used for write csv (end) """

    """ used for write txt file 
    for i,element in enumerate(courses_elements):
        if (i%10 == 0): # discard first one
            continue
        elif (i%10 == 9):   # the last one is href, it need to be drawed out by css_selector and then use get_attribute
            href = element.find_elements_by_css_selector('a')
            href = [href[0].get_attribute('href')] # convert from string to list, because .extend() accept list
            course_list.extend(href)
        else:   # we don't need the text of the last one (when i%10 == 9)
            course_list.extend(element.text.split())
        if (i%10 == 9):    # last one
            for j,item in enumerate(course_list):
                if (j == len(course_list)-1):
                    f.write(item + '\n')
                    break 
                else:
                    f.write(item + ',')
            course_list = [depart_name]
    """
    browser.back()
f_csv.close()
# f.close()
browser.quit()
