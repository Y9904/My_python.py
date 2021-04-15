from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome(executable_path='F:\python集\python爬虫\自动化\浏览器驱动\chromedriver.exe')
driver.get('https://qzone.qq.com/')
# 隐式等待
wait = WebDriverWait(driver, 10)
# 先切换到内嵌的窗口中
iframe = driver.find_element_by_id('login_frame')
driver.switch_to.frame(iframe)
# 在内嵌的窗口中找到账号密码登陆
anthor = driver.find_element_by_id('switcher_plogin')
anthor.click()
# 输入账号
username_input = driver.find_element_by_id('u')
username_input.send_keys('442868909')
# 输入密码
password_input = driver.find_element_by_name('p')
password = input('密码：')
password_input.send_keys(password)
# 登陆
login_button = driver.find_element_by_id('login_button')
login_button.click()
# 截屏
screen_image = driver.get_screenshot_as_file('a.png')
# 返回cookies
cookies = driver.get_cookies()
print(cookies)
