from selenium import webdriver
import csv
import time
import codecs

f_csv = codecs.open('ncku_course.csv', 'w', encoding="utf_8_sig")
writer = csv.writer(f_csv)

course_list_name = ['學院','系所名稱', '系號-序號', '課程碼-分班碼', '屬性碼', '年級', '類別',
                    '科目名稱', '學分', '必/選修', '教師姓名', '已選課人數/餘額', '時間', '教室', '課程大綱']
writer.writerow(course_list_name)

profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'zh-TW')    # query chinese page
browser = webdriver.Firefox(firefox_profile=profile)

browser.get('https://course.ncku.edu.tw/index.php?c=qry_all')

college_list = []
depart_list = []
panels = browser.find_elements_by_class_name('panel-default')
panels = panels[:int(len(panels)/2)]  # cut in half

for panel in panels:
    college = panel.find_element_by_class_name('panel-heading')
    departs = panel.find_elements_by_class_name('btn_dept')
    college_list.extend([college.text]*len(departs))
    for depart in departs:
        depart_list.append(depart.text)
      
for i in range(len(depart_list)):
    time.sleep(1)  # wait for 1 second
    college_name = college_list[i]
    depart = browser.find_elements_by_xpath("//*[contains(text(), '%s')]" % depart_list[i])[0]  # use the first one
    depart_name = depart.text
    course_list = [college_name,depart_name]

    depart.click()
    time.sleep(1)   # wait for 1 second
    courses_elements = browser.find_elements_by_xpath("//table[@id = 'A9-table']/tbody/tr/td")
    
    for i, element in enumerate(courses_elements):
        if (i % 10 == 0):  # discard first one
            continue
        elif (i % 10 == 1):
            oldlist = element.text.split()
            if (len(oldlist) == 3):
                dept_seq = oldlist[0]           # 系號-序號
                class_seq = oldlist[1]          # 課程碼-分班碼
                attr_seq = oldlist[2]           # 屬性碼
                course_list.append(dept_seq)  
            else:
                class_seq = oldlist[0]
                attr_seq = oldlist[1]
                course_list.append('')
            course_list.append(class_seq)  
            course_list.append(attr_seq)  
        elif (i % 10 == 5):
            oldlist = element.text.split()
            if (len(oldlist) != 0): 
                units = oldlist[0]
                required = oldlist[1]
                course_list.append(units)       # 學分
                course_list.append(required)    # 必選修
            else:
                course_list.append('')
                course_list.append('')
        elif (i % 10 == 8):
            oldlist = element.text.split()
            if (len(oldlist) != 0):
                class_time = oldlist[0]
                if (len(oldlist) > 1):
                    location = oldlist[1:]
                    course_list.append(class_time) #時間
                    course_list.append(location)   #地點
                else:
                    course_list.append(class_time)
                    course_list.append('')
            else:
                course_list.append('')
                course_list.append('')
        elif (i % 10 == 9):   # the last one is href, it need to be drawed out by css_selector and then use get_attribute
            href = element.find_elements_by_css_selector('a')
            if (len(href) == 0):    # no href exist
                course_list.append('')
            else:
                url = href[0].get_attribute('href')
                if (url[0] != 'h'):    # not a url
                    course_list.append('')
                else:
                    course_list.append(url)
        else:   # we don't need the text of the last one (when i%10 == 9)
            oldlist = element.text.split()
            if (len(oldlist) == 0):
                course_list.append('')
            else:
                course_list.append(oldlist)
        if (i % 10 == 9):    # last one
            writer.writerow(course_list)
            course_list = [college_name, depart_name]
            
    browser.back()

f_csv.close()
browser.quit()