#自動登入TWITTER 2032/05/29


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import csv
import time
import requests


accounts = []                                # 讀取ACCOUNTS.CSV將每一行內容轉為字典形式 並將字典添加至一個列表
with open('accounts.csv', 'r') as file:      # 創一個空列表，儲存用戶訊息用以讀取
    reader = csv.reader(file, delimiter=':') # 創建一個 CSV reader 並指定 ':' 為分隔符號
    for row in reader:                       # 遍歷 CSV 文件的每一行
        account = {                          # 创建一个字典，存储每一行的账户信息
            'twitter_username': row[0],      # 使用第一列的值作为 Twitter 用户名
            'twitter_password': row[1],      
            'outlook_username': row[2],  
            'outlook_password': row[3]
        }
        accounts.append(account)

# 設定Chrome瀏覽器的路徑
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# 設定登入帳號                      ####設定開啟瀏覽器####
user_data_dir = r"C:\Users\01\Desktop\01\02/65.0"

# 建立ChromeOptions物件
chrome_options = Options()

# 設定使用者資料目錄
chrome_options.add_argument("--user-data-dir=" + user_data_dir)

# 建立ChromeDriver服務
service = Service(r"C:\Users\01\Desktop\chromedriver.exe")  # 替換為實際的ChromeDriver路徑

# 建立ChromeDriver物件，並指定ChromeOptions和Service
driver = webdriver.Chrome(service=service, options=chrome_options)


    ##動作開始##


time.sleep(3)
# 自动登录Twitter帐号
def login_twitter(username, password):
    # 打开 Twitter 登录页面
    driver.get("https://twitter.com/login")
    time.sleep(2)
    
    # 找到并填写用户名输入框
    twitter_username_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'))
)
    twitter_username_input.send_keys(username)
    #點擊確認框  
    time.sleep(2)
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'))
)
    element.click()

    
    # 找到并填写密码输入框
    twitter_password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'))
    )
    twitter_password_input.send_keys(password)

    # 点击登录按钮
    time.sleep(1)
    twitter_login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"]'))
    )
    twitter_login_button.click()
    
    #開啟新分頁
driver.execute_script("window.open()")
driver.switch_to.window(driver.window_handles[0])




# 自動登入Outlook帳號

driver.execute_script("window.open()")
driver.switch_to.window(driver.window_handles[2])



def login_outlook(username, password):
    # 跳转到登录页面
    driver.get("https://outlook.live.com/owa/")
    wait = WebDriverWait(driver, 10)

    # 判断是否已经登录，检查页面是否存在指定元素
    try:
        outlook_logo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[alt="Outlook"]')))
    except TimeoutException:
        print("Outlook logo not found, proceeding to next page...")

    # 点击登录按钮
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/header/div/aside/div/nav/ul/li[2]/a')))
    login_button.click()

    # 输入账号
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'loginfmt'))
    )
    email_input.clear()
    email_input.send_keys(username)

    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'idSIButton9'))
    )
    continue_button.click()

    # 输入密码
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'passwd'))
    )
    password_input.clear()
    password_input.send_keys(password)

    signin_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'idSIButton9'))
    )
    signin_button.click()

    # 密码下一个步骤
    buttons = ['#iCancel', '#id__0', '#idSIButton9', '#iShowSkip', '//*[@id="id__0"]']
    for _ in range(4):
        for button in buttons:
            try:
                # 使用 CSS 选择器定位按钮元素
                element = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, button))
                )
                # 增加一个0.3秒的等待时间
                time.sleep(0.3)
                element.click()
            except NoSuchElementException:
                print("Button was not found, proceeding to next page...")
            except Exception as e:
                print(f"Error: {str(e)}")


             ####設定要登入第幾個推特####
login_account_index = 65


# 自动登录指定帐号的Outlook帐号
outlook_username = accounts[login_account_index - 1]['outlook_username']
outlook_password = accounts[login_account_index - 1]['outlook_password']


# 先登入 Twitter
twitter_username = accounts[login_account_index - 1]['twitter_username']
twitter_password = accounts[login_account_index - 1]['twitter_password']

login_twitter(twitter_username, twitter_password)

# 打开一个新的浏览器标签页以登录 Outlook
driver.execute_script("window.open()")
driver.switch_to.window(driver.window_handles[1])

# 然后登录 Outlook
outlook_username = accounts[login_account_index - 1]['outlook_username']
outlook_password = accounts[login_account_index - 1]['outlook_password']

login_outlook(outlook_username, outlook_password)

# 循环查找按钮并等待接收验证码
while True:
    user_input = input('Do you want to proceed to the next functionality? (Y/N/O): ')
    if user_input.lower() == 'o':
        # 在新的分頁中自动登录Twitter
        twitter_username = accounts[login_account_index - 1]['twitter_username']
        twitter_password = accounts[login_account_index - 1]['twitter_password']

        twitter_login_url = "https://twitter.com/login"
        driver.get(twitter_login_url)

        twitter_username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="session[username_or_email]"]'))
        )
        twitter_username_input.send_keys(twitter_username)

        twitter_password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="session[password]"]'))
        )
        twitter_password_input.send_keys(twitter_password)

        twitter_login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"]'))
        )
        twitter_login_button.click()

        # 在這裡添加您要在Twitter上執行的任何操作
        # TODO: 添加要在Twitter上執行的任何操作的程式碼
        pass

        # 關閉新分頁
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    elif user_input.lower() == 'n':
        break

