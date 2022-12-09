from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip, requests, json
from .models import Token
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Chrome driver for selenium should in same folder.

@csrf_exempt
def skku_login(request): #POST
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
    url = 'https://canvas.skku.edu/'
    uid = request.GET['id'] #your_id
    upw = request.GET['pw'] #your_password

    # times for check if programe executes correctly

    driver.get(url)
    driver.implicitly_wait(3)

    # id and pasword form
    tag_id = driver.find_element(by=By.XPATH, value='//*[@id="userid"]')
    tag_pw = driver.find_element(by=By.XPATH, value='//*[@id="password"]')

    # input id and password and paste it.
    tag_id.click()
    tag_id.send_keys(uid)
    driver.implicitly_wait(3)

    tag_pw.click()
    tag_pw.send_keys(upw)
    driver.implicitly_wait(3)

    # click login button
    login_btn = driver.find_element(by=By.XPATH, value='//*[@id="btnLoginBtn"]')
    login_btn.click()
    driver.implicitly_wait(3)

    # check if login failed
    try:
        # login failed
        login_error = driver.find_element(by=By.CSS_SELECTOR, value='#err_common > div > p')
        print('로그인 실패 > ', login_error.text)
    except:
        print('로그인 성공')

    # get cookies
    driver_cookies = driver.get_cookies()
    _normandy_session = ""
    
    for cookie in driver_cookies:
      if cookie['name'] == '_normandy_session':
        _normandy_session = cookie['value']
        break
    
    url = "https://canvas.skku.edu/api/v1/users/self/favorites/courses"
    # _normandy_session
    cookie = {'_normandy_session': _normandy_session}
    res = requests.get(url=url, cookies=cookie)
    course_list = json.loads(res.text.lstrip('while(1);'))
    
    user_id = str(course_list[0].get("enrollments")[0].get("user_id"))
    course_id = str(course_list[0].get("id"))

    url = "https://canvas.skku.edu/courses/" + course_id + "/external_tools/1"

    driver.get(url)
    driver.implicitly_wait(3)

    driver_cookies = driver.get_cookies()
    xn_api_token = ""
    
    for cookie in driver_cookies:
      if cookie['name'] == 'xn_api_token':
        xn_api_token = cookie['value']
        break
      
    url = "https://canvas.skku.edu/learningx/api/v1/courses/" + course_id + "/total_learnstatus/users/" + user_id
    xn_api_token = "Bearer " + xn_api_token
    header = {'Authorization': xn_api_token}
    cookie = {'_normandy_session': _normandy_session}
    status_list = json.loads(requests.get(url=url, headers=header, cookies=cookie).text.lstrip('while(1);'))
    student_id = str(status_list.get("item")["user_login"])

    if Token.objects.exists():
      token = Token.objects.first()
      token.header = header
      token.cookie = cookie
      token.user_id = user_id
      token.student_id = student_id
      token.save()

    else:
      Token.objects.create(header=header, cookie=cookie, user_id=user_id, student_id=student_id)

    return HttpResponse("Done")

# skku_login(driver)
