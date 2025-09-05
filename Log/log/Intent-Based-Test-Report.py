# -*- encoding=utf8 -*-
__author__ = "臺灣科技大學 MITLAB"
__title__ = "Intend-Based 測試案例報告"
__desc__ = """
意圖網管系統綜合測試

1. 測試目標
針對「意圖網管系統使用者」，確保意圖網管系統從頭到尾的流程順暢

2. 測試內容
 - 流程完整
 - 各流程完程度

3. 測試操作
修改 test_case_to_run 內想測試的 Use Case 項目

4. 測試項目
 - 註冊
 - 登入
 - 登出
 - 獲取所有對話清單
	 - 無對話清單
	 - 有對話清單
 - 創建對話
 - 取得對話歷史紀錄
 - 更新對話名稱
 - 刪除對話
 - Toggle 渲染
	 - 展開
	 - 收起
 - 主題切換
	 - 黑色
	 - 白色

5. User story
01. 註冊
02. 登入
03. Toggle 渲染(展開)
04. 獲取所有對話清單(無對話清單)
05. Toggle 渲染(收起)
06. 主題切換(白色)
07. 創建對話
07.1 輸入文本 hi，生成對話標題是 `ITRI Network Service`
08. Toggle 渲染(展開)
09. 主題切換(黑色)
10. 獲取所有對話清單(有對話清單)
11. 更新對話名稱
12. 刪除對話
13. 獲取所有對話清單(無對話清單)
14. 創建對話
14.1 輸入文本 `get sinr map`，生成對話標題不是 `ITRI Network Service`
14.2 再輸入 `yes`，渲染文字、圖片
15. 取得對話歷史紀錄
16. 創建對話
16.1 輸入文本 `get UE status`，生成對話標題不是 `ITRI Network Service`
16.2 再輸入 `5.`、`yes`，渲染文字、表格
17. 獲取所有對話清單(有對話清單)
18. 登出

6. Use Case
01. 註冊帳號
02. 登入帳號
03. 獲取所有對話清單
04. 創建新對話
05. 更新對話名稱
06. 刪除對話
07. 取得對話歷史紀錄
08. 登出帳號
09. 展開/收起側邊欄
10. 切換主題為黑/白色
"""

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import LogToHtml
from airtest_selenium.proxy import WebChrome
from selenium.webdriver.common.keys import Keys
import random
import string
import time
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

log_dir = r"./"
export_dir = f"./report/report_{timestamp}"

if not cli_setup():
    auto_setup(
        __file__,
        logdir=log_dir,
        project_root=log_dir
    )

def generate_random_string(length=8):
    """Generates a random string of a given length, consisting of letters and digits."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# 全域變數
random_user = ""
random_email = ""
random_password = ""
FRONT_URL = "http://140.118.162.139:33401/signin"

def setup_driver():
    """Sets up and returns a WebChrome driver instance."""
    global driver
    driver = WebChrome()
    driver.maximize_window()
    driver.implicitly_wait(20)
    driver.get(FRONT_URL)
    return driver

def teardown_driver():
    """Closes the driver."""
    driver.close()

# Gherkin Given Steps (前置條件)
# -------------------------------------------------------------------------------------------------------

def given_not_registered_user():
    """
    Given: A user is not registered.
    Action: Navigate to signup page.
    """
    global random_user, random_email, random_password
    log("=== GIVEN: 位於註冊頁面且未註冊 ===")
    random_user = generate_random_string()
    random_email = f"{random_user}@test.com"
    random_password = random_user
    driver.find_element_by_xpath("//a[@href='/signup']").click()

def given_registered_user():
    """
    Given: A user is registered.
    Action: Perform registration and then navigate back to signin page.
    """
    global random_user, random_email, random_password
    log("=== GIVEN: 帳號已註冊 ===")
    given_not_registered_user()
    driver.find_element_by_id("username").send_keys(random_user)
    driver.find_element_by_id("email").send_keys(random_email)
    driver.find_element_by_id("password").send_keys(random_password)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    assert "Account created successfully" in driver.find_element_by_tag_name("body").text

def given_logged_in_user():
    """
    Given: A user is logged in.
    Action: Perform registration and login.
    """
    log("=== GIVEN: 帳號已登入 ===")
    given_registered_user()
    driver.find_element_by_id("username").send_keys(random_user)
    driver.find_element_by_id("password").send_keys(random_password)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    assert "Login successful!" in driver.find_element_by_tag_name("body").text

def given_logged_in_and_sidebar_expanded():
    """
    Given: A user is logged in and the sidebar is expanded.
    Action: Log in and expand the sidebar.
    """
    log("=== GIVEN: 帳號已登入且側邊欄已展開 ===")
    given_logged_in_user()
    
    sidebar_container = driver.find_element_by_xpath('//div[@data-variant="sidebar"]')
    driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
    assert sidebar_container.get_attribute("data-state") == "expanded"

def given_logged_in_and_sidebar_expanded_and_has_conversation():
    """
    Given: A user is logged in and the sidebar is expanded and has at least one conversation.
    Action: Log in and create a new conversation.
    """
    log("=== GIVEN: 帳號已登入且側邊欄已展開且有對話紀錄 ===")
    given_logged_in_user()
    
    sidebar_container = driver.find_element_by_xpath('//div[@data-variant="sidebar"]')
    driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
    assert sidebar_container.get_attribute("data-state") == "expanded"
    
    driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("hi")
    driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
    driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").click()
    
    driver.find_element_by_xpath("//span[@title='ITRI Network Service']")
    
    
# Test Cases (驗收案例)
# -------------------------------------------------------------------------------------------------------

def test_case_00_full_flow():
    log("=== START TEST CASE 00: 完整流程測試 ===")
    
    # STEP 01: 註冊
    log("--- STEP 01: 註冊 ---")
    driver.find_element_by_xpath("//a[@href='/signup']").click()
    random_user = generate_random_string(8)
    driver.find_element_by_id("username").send_keys(random_user)
    driver.find_element_by_id("email").send_keys(f"{random_user}@test.com")
    driver.find_element_by_id("password").send_keys(random_user)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    assert "Account created successfully" in driver.find_element_by_tag_name("body").text
    
    # STEP 02: 登入
    log("--- STEP 02: 登入 ---")
    driver.find_element_by_id("username").send_keys(random_user)
    driver.find_element_by_id("password").send_keys(random_user)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    assert "Login successful!" in driver.find_element_by_tag_name("body").text
    
    # STEP 03: 側邊欄渲染 (展開)
    log("--- STEP 03: 側邊欄渲染 (展開) ---")
    sidebar_container = driver.find_element_by_xpath('//div[@data-variant="sidebar"]')
    driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
    assert sidebar_container.get_attribute("data-state") == "expanded"

    # STEP 04: 獲取所有對話清單 (無對話清單)
    log("--- STEP 04: 獲取所有對話清單 (無對話清單) ---")
    assert "尚無對話紀錄" in driver.find_element_by_tag_name("body").text

    # STEP 05: 側邊欄渲染 (收起)
    log("--- STEP 05: 側邊欄渲染 (收起) ---")
    driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
    assert sidebar_container.get_attribute("data-state") != "expanded"

    # STEP 06: 主題切換 (白色)
    log("--- STEP 06: 主題切換 (白色) ---")
    button_element = driver.find_element_by_xpath("//button[@aria-label='Switch to light mode']")
    button_element.click()
    assert button_element.get_attribute("aria-label") == "Switch to dark mode"

    # STEP 07: 創建對話
    log("--- STEP 07: 創建對話 ---")
    driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("hi")
    driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
    driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").click()

    # STEP 08: 側邊欄渲染 (展開)
    log("--- STEP 08: 側邊欄渲染 (展開) ---")
    driver.find_element_by_xpath("/html/body/div/main/div/header/button").click()
    assert sidebar_container.get_attribute("data-state") == "expanded"

    # STEP 09: 主題切換 (黑色)
    log("--- STEP 09: 主題切換 (黑色) ---")
    button_element = driver.find_element_by_xpath("//button[@aria-label='Switch to dark mode']")
    button_element.click()
    assert button_element.get_attribute("aria-label") == "Switch to light mode"

    # STEP 10: 獲取所有對話清單 (有對話清單)
    log("--- STEP 10: 獲取所有對話清單 (有對話清單) ---")
    driver.find_element_by_xpath("//span[@title='ITRI Network Service']")

    # STEP 11: 更新對話名稱
    log("--- STEP 11: 更新對話名稱 ---")
    driver.find_element_by_css_selector("button[id^='radix-:r']").click()
    driver.find_element_by_css_selector("[id^='radix-:r'] > div").click()
    driver.find_element_by_css_selector("input.flex-1.border").click()
    driver.find_element_by_css_selector("input.flex-1.border").clear()
    driver.find_element_by_css_selector("input.flex-1.border").send_keys("Change Name" + Keys.ENTER)

    # STEP 12: 刪除對話
    log("--- STEP 12: 刪除對話 ---")
    driver.find_element_by_css_selector("button[id^='radix-:r']").click()
    driver.find_element_by_css_selector("[id^='radix-:r'] > div:nth-of-type(2)").click()

    # STEP 13: 獲取所有對話清單 (無對話清單)
    log("--- STEP 13: 獲取所有對話清單 (無對話清單) ---")
    assert "尚無對話紀錄" in driver.find_element_by_tag_name("body").text

    # STEP 14: 創建對話
    log("--- STEP 14: 創建對話 ---")
    driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/ul/div/button").click()
    driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("get sinr map")
    driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
    driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("yes")
    driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
    driver.find_element_by_xpath("//img[@alt='image-0']").click()
    driver.find_element_by_xpath("//img[@alt='preview']").click()

    # STEP 15: 取得對話歷史紀錄
    log("--- STEP 15: 取得對話歷史紀錄 ---")
    driver.find_element_by_xpath("/html/body/div/main/div/header/button[2]").click()
    driver.find_element_by_css_selector("a[href^='/conversation/']").click()

    # STEP 16: 創建對話
    log("--- STEP 16: 創建對話 ---")
    driver.find_element_by_xpath("/html/body/div/main/div/header/button[2]").click()
    driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("get UE status")
    driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
    driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("5.")
    driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
    driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("yes")
    driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
    driver.find_element_by_xpath("/html/body/div/main/div/div/div/div/div/div/div[7]/div/div[2]/div/div/div[2]")
    driver.find_element_by_xpath("/html/body/div/main/div/div/div/div/div/div/div[7]/div/div[2]/div/div/div[2]/button").click()
    driver.find_element_by_xpath("/html/body/div/main/div/div/div/div/div/div/div[7]/div/div[2]/div/div/div[2]/button").click()

    # STEP 17: 獲取所有對話清單 (有對話清單)
    log("--- STEP 17: 獲取所有對話清單 (有對話清單) ---")
    driver.find_element_by_css_selector("button[id^='radix-:r']")

    # STEP 18: 登出
    log("--- STEP 18: 登出 ---")
    driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[3]/button").click()
    
    log("=== TEST CASE 00 PASSED ===")

def test_case_01_register_account():
    log("=== START TEST CASE 01: 註冊帳號 ===")
    given_not_registered_user()
    
    log("=== WHEN: 輸入資訊並點擊「註冊」 ===")
    driver.find_element_by_id("username").send_keys(random_user)
    driver.find_element_by_id("email").send_keys(random_email)
    driver.find_element_by_id("password").send_keys(random_password)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    
    log("=== THEN: 成功建立帳戶 ===")
    assert "Account created successfully" in driver.find_element_by_tag_name("body").text
    
    log("=== TEST CASE 01 PASSED ===")

def test_case_02_login_account():
    log("=== START TEST CASE 02: 登入帳號 ===")
    given_registered_user()
    
    log("=== WHEN: 輸入資訊並點擊「登入」 ===")
    driver.find_element_by_id("username").send_keys(random_user)
    driver.find_element_by_id("password").send_keys(random_password)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    
    log("=== THEN: 成功登入 ===")
    assert "Login successful!" in driver.find_element_by_tag_name("body").text
    
    log("=== TEST CASE 02 PASSED ===")

def test_case_03_get_all_conversations():
    log("=== START TEST CASE 03: 獲取所有對話清單 ===")
    given_logged_in_and_sidebar_expanded()
    
    log("=== WHEN: 查看對話列表 ===")
    
    log("=== THEN: 列表顯示「尚無對話紀錄」 ===")
    assert "尚無對話紀錄" in driver.find_element_by_tag_name("body").text
    
    driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("hi")
    driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
    driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").click()
    
    log("=== AND: 列表顯示所有已創建的對話 ===")
    driver.find_element_by_xpath("//span[@title='ITRI Network Service']").click()
    assert "ITRI Network Service" in driver.find_element_by_tag_name("body").text
    
    log("=== TEST CASE 03 PASSED ===")

def test_case_04_create_new_conversation():
    log("=== START TEST CASE 04: 創建新對話 ===")
    given_logged_in_and_sidebar_expanded()
    
    log("=== WHEN: 輸入內容並送出 ===")
    driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("get UE status")
    driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
    driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("5.")
    driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
    driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("yes")
    driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
    driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("get SINR map")
    driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
    driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("yes")
    driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
    driver.find_element_by_xpath("//img[@alt='image-0']")
    
    log("=== THEN: 成功創建新對話 ===")
    assert "SINR" in driver.find_element_by_tag_name("body").text 
    
    log("=== TEST CASE 04 PASSED ===")

def test_case_05_update_conversation_name():
    log("=== START TEST CASE 05: 更新對話名稱 ===")
    given_logged_in_and_sidebar_expanded_and_has_conversation()
    
    log("=== WHEN: 點擊編輯並輸入新名稱 ===")
    driver.find_element_by_css_selector("button[id^='radix-:r']").click()
    driver.find_element_by_css_selector("[id^='radix-:r'] > div").click()
    
    new_name = "Change Name"
    input_field = driver.find_element_by_css_selector("input.flex-1.border")
    input_field.clear()
    input_field.send_keys(new_name + Keys.ENTER)
    
    log("=== THEN: 對話名稱成功更新 ===")
    assert new_name in driver.find_element_by_tag_selector("span[title]").text
    
    log("=== TEST CASE 05 PASSED ===")

def test_case_06_delete_conversation():
    log("=== START TEST CASE 06: 刪除對話 ===")
    given_logged_in_and_sidebar_expanded_and_has_conversation()
    
    log("=== WHEN: 點擊刪除按鈕 ===")
    driver.find_element_by_css_selector("button[id^='radix-:r']").click()
    driver.find_element_by_css_selector("[id^='radix-:r'] > div:nth-of-type(2)").click()
    
    log("=== THEN: 對話從列表中消失 ===")
    assert "尚無對話紀錄" in driver.find_element_by_tag_name("body").text
    
    log("=== TEST CASE 06 PASSED ===")

def test_case_07_get_conversation_history():
    log("=== START TEST CASE 07: 取得對話歷史紀錄 ===")
    given_logged_in_and_sidebar_expanded_and_has_conversation()
    
    log("=== WHEN: 創新對話後再點擊對話清單中的某個對話項目 ===")
    driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/ul/div/button").click()
    driver.find_element_by_css_selector("a[href^='/conversation/']").click()
    
    log("=== THEN: 頁面導航到該對話的歷史內容 ===")
    assert "hi" in driver.find_element_by_tag_name("body").text
    
    log("=== TEST CASE 07 PASSED ===")

def test_case_08_logout_account():
    log("=== START TEST CASE 08: 登出帳號 ===")
    given_logged_in_and_sidebar_expanded()
    
    log("=== WHEN: 點擊登出按鈕 ===")
    driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[3]/button").click()
    
    log("=== THEN: 使用者被導航回登入頁面 ===")
    assert "Log in" in driver.find_element_by_tag_name("body").text
    
    log("=== TEST CASE 08 PASSED ===")

def test_case_09_expand_collapse_sidebar():
    log("=== START TEST CASE 09: 展開/收起側邊欄 ===")
    given_logged_in_user()
    
    log("=== WHEN: 點擊展開按鈕 ===")
    sidebar_container = driver.find_element_by_xpath('//div[@data-variant="sidebar"]')
    driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
    
    log("=== THEN: 側邊欄成功展開 ===")
    assert sidebar_container.get_attribute("data-state") == "expanded"
        
    log("=== WHEN: 點擊收起按鈕 ===")
    driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
    
    log("=== THEN: 側邊欄成功收起 ===")
    assert sidebar_container.get_attribute("data-state") != "expanded"
    
    log("=== TEST CASE 09 PASSED ===")

def test_case_10_switch_to_dark_theme():
    log("=== START TEST CASE 10: 切換主題為黑/白色 ===")
    given_logged_in_user()

    log("=== WHEN: 點擊主題切換按鈕 ===")
    button_element = driver.find_element_by_xpath("//button[@aria-label='Switch to light mode']")
    button_element.click()
    
    log("=== THEN: 頁面成功切換為白色主題 ===")
    assert button_element.get_attribute("aria-label") == "Switch to dark mode"
    
    log("=== WHEN: 點擊主題切換按鈕 ===")
    button_element.click()
    
    log("=== THEN: 頁面成功切換為黑色主題 ===")
    assert button_element.get_attribute("aria-label") == "Switch to light mode"
    
    log("=== TEST CASE 10 PASSED ===")

# 主執行區塊
# -------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    
    # === 完整 User Story 測試 ===
    test_case_to_run = [test_case_00_full_flow]
    
    # === Use Case 測試 ===
#     test_case_to_run = [
#         test_case_01_register_account, 
#         test_case_02_login_account, 
#         test_case_03_get_all_conversations, 
#         test_case_04_create_new_conversation,
#         test_case_05_update_conversation_name,
#         test_case_06_delete_conversation,
#         test_case_07_get_conversation_history, 
#         test_case_08_logout_account,
#         test_case_09_expand_collapse_sidebar, 
#         test_case_10_switch_to_dark_theme
#     ]

    for test_case in test_case_to_run:
        try:
            log(f"#################### Running {test_case.__name__} ####################")
            setup_driver()
            test_case()
        except (AssertionError, Exception) as e:
            log(f"#################### {test_case.__name__} FAILED: {e} ####################")
        finally:
            teardown_driver()
            log("Driver closed.")
            time.sleep(1)
            
    try:
        # 建立 LogToHtml 物件
        log_to_html = LogToHtml(
            script_root=__file__,
            log_root=log_dir,
            static_root=None,
            export_dir=export_dir, 
            plugins=['airtest_selenium.report']
        )

        log_to_html.report()

        print(f"Report generated successfully")

    except Exception as e:
        print(f"An error occurred while generating the report: {e}")

# # -*- encoding=utf8 -*-
# __author__ = "臺灣科技大學 MITLAB"
# __title__ = "Intend-Based 測試案例報告"
# __desc__ = """
# 意圖網管系統綜合測試

# 1. 測試目標
# 針對「意圖網管系統使用者」，確保意圖網管系統從頭到尾的流程順暢

# 2. 測試內容
#  - 流程完整
#  - 各流程完程度

# 3. 測試操作
# 修改 test_case_to_run 內想測試的 Use Case 項目

# 4. 測試項目
#  - 註冊
#  - 登入
#  - 登出
#  - 獲取所有對話清單
# 	 - 無對話清單
# 	 - 有對話清單
#  - 創建對話
#  - 取得對話歷史紀錄
#  - 更新對話名稱
#  - 刪除對話
#  - Toggle 渲染
# 	 - 展開
# 	 - 收起
#  - 主題切換
# 	 - 黑色
# 	 - 白色

# 5. User story
# 01. 註冊
# 02. 登入
# 03. Toggle 渲染(展開)
# 04. 獲取所有對話清單(無對話清單)
# 05. Toggle 渲染(收起)
# 06. 主題切換(白色)
# 07. 創建對話
# 07.1 輸入文本 hi，生成對話標題是 `ITRI Network Service`
# 08. Toggle 渲染(展開)
# 09. 主題切換(黑色)
# 10. 獲取所有對話清單(有對話清單)
# 11. 更新對話名稱
# 12. 刪除對話
# 13. 獲取所有對話清單(無對話清單)
# 14. 創建對話
# 14.1 輸入文本 `get sinr map`，生成對話標題不是 `ITRI Network Service`
# 14.2 再輸入 `yes`，渲染文字、圖片
# 15. 取得對話歷史紀錄
# 16. 創建對話
# 16.1 輸入文本 `get UE status`，生成對話標題不是 `ITRI Network Service`
# 16.2 再輸入 `5.`、`yes`，渲染文字、表格
# 17. 獲取所有對話清單(有對話清單)
# 18. 登出

# 6. Use Case
# 01. 註冊帳號
# 02. 登入帳號
# 03. 獲取所有對話清單
# 04. 創建新對話
# 05. 更新對話名稱
# 06. 刪除對話
# 07. 取得對話歷史紀錄
# 08. 登出帳號
# 09. 展開/收起側邊欄
# 10. 切換主題為黑/白色
# """

# from airtest.core.api import *
# from airtest.cli.parser import cli_setup
# from airtest.report.report import LogToHtml
# from airtest_selenium.proxy import WebChrome
# from selenium.webdriver.common.keys import Keys
# import random
# import string
# import time
# import datetime

# timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# log_dir = r"./"
# export_dir = f"./report/report_{timestamp}"

# if not cli_setup():
#     auto_setup(
#         __file__,
#         logdir=log_dir,
#         project_root=log_dir
#     )

# def generate_random_string(length=8):
#     """Generates a random string of a given length, consisting of letters and digits."""
#     characters = string.ascii_letters + string.digits
#     return ''.join(random.choice(characters) for i in range(length))

# # 全域變數
# random_user = ""
# random_email = ""
# random_password = ""
# FRONT_URL = "http://140.118.162.139:33401/signin"

# def setup_driver():
#     """Sets up and returns a WebChrome driver instance."""
#     global driver
#     driver = WebChrome()
#     driver.maximize_window()
#     driver.implicitly_wait(20)
#     driver.get(FRONT_URL)
#     return driver

# def teardown_driver():
#     """Closes the driver."""
#     driver.close()

# # Gherkin Given Steps (前置條件)
# # -------------------------------------------------------------------------------------------------------

# def given_not_registered_user():
#     """
#     Given: A user is not registered.
#     Action: Navigate to signup page.
#     """
#     global random_user, random_email, random_password
#     log("=== GIVEN: 位於註冊頁面且未註冊 ===")
#     random_user = generate_random_string()
#     random_email = f"{random_user}@test.com"
#     random_password = random_user
#     driver.find_element_by_xpath("//a[@href='/signup']").click()
#     time.sleep(1)

# def given_registered_user():
#     """
#     Given: A user is registered.
#     Action: Perform registration and then navigate back to signin page.
#     """
#     global random_user, random_email, random_password
#     log("=== GIVEN: 帳號已註冊 ===")
#     given_not_registered_user()
#     driver.find_element_by_id("username").send_keys(random_user)
#     driver.find_element_by_id("email").send_keys(random_email)
#     driver.find_element_by_id("password").send_keys(random_password)
#     driver.find_element_by_xpath("//button[@type='submit']").click()
#     assert "Account created successfully" in driver.find_element_by_tag_name("body").text
#     time.sleep(1)

# def given_logged_in_user():
#     """
#     Given: A user is logged in.
#     Action: Perform registration and login.
#     """
#     log("=== GIVEN: 帳號已登入 ===")
#     given_registered_user()
#     driver.find_element_by_id("username").send_keys(random_user)
#     driver.find_element_by_id("password").send_keys(random_password)
#     driver.find_element_by_xpath("//button[@type='submit']").click()
#     assert "Login successful!" in driver.find_element_by_tag_name("body").text
#     time.sleep(1)

# def given_logged_in_and_sidebar_expanded():
#     """
#     Given: A user is logged in and the sidebar is expanded.
#     Action: Log in and expand the sidebar.
#     """
#     log("=== GIVEN: 帳號已登入且側邊欄已展開 ===")
#     given_logged_in_user()
    
#     sidebar_container = driver.find_element_by_xpath('//div[@data-variant="sidebar"]')
#     driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
#     assert sidebar_container.get_attribute("data-state") == "expanded"
#     time.sleep(1)

# def given_logged_in_and_sidebar_expanded_and_has_conversation():
#     """
#     Given: A user is logged in and the sidebar is expanded and has at least one conversation.
#     Action: Log in and create a new conversation.
#     """
#     log("=== GIVEN: 帳號已登入且側邊欄已展開且有對話紀錄 ===")
#     given_logged_in_user()
    
#     sidebar_container = driver.find_element_by_xpath('//div[@data-variant="sidebar"]')
#     driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
#     assert sidebar_container.get_attribute("data-state") == "expanded"
    
#     driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("hi")
#     driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
#     time.sleep(3)
#     driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").click()
    
#     driver.find_element_by_xpath("//span[@title='ITRI Network Service']")
    
#     time.sleep(1)

# # Test Cases (驗收案例)
# # -------------------------------------------------------------------------------------------------------

# def test_case_00_full_flow():
#     log("=== START TEST CASE 00: 完整流程測試 ===")
    
#     # STEP 01: 註冊
#     log("--- STEP 01: 註冊 ---")
#     driver.find_element_by_xpath("//a[@href='/signup']").click()
#     random_user = generate_random_string(8)
#     driver.find_element_by_id("username").send_keys(random_user)
#     driver.find_element_by_id("email").send_keys(f"{random_user}@test.com")
#     driver.find_element_by_id("password").send_keys(random_user)
#     driver.find_element_by_xpath("//button[@type='submit']").click()
#     assert "Account created successfully" in driver.find_element_by_tag_name("body").text
    
#     # STEP 02: 登入
#     log("--- STEP 02: 登入 ---")
#     driver.find_element_by_id("username").send_keys(random_user)
#     driver.find_element_by_id("password").send_keys(random_user)
#     driver.find_element_by_xpath("//button[@type='submit']").click()
#     assert "Login successful!" in driver.find_element_by_tag_name("body").text
    
#     # STEP 03: 側邊欄渲染 (展開)
#     log("--- STEP 03: 側邊欄渲染 (展開) ---")
#     sidebar_container = driver.find_element_by_xpath('//div[@data-variant="sidebar"]')
#     driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
#     assert sidebar_container.get_attribute("data-state") == "expanded"

#     # STEP 04: 獲取所有對話清單 (無對話清單)
#     log("--- STEP 04: 獲取所有對話清單 (無對話清單) ---")
#     assert "尚無對話紀錄" in driver.find_element_by_tag_name("body").text
#     time.sleep(1)

#     # STEP 05: 側邊欄渲染 (收起)
#     log("--- STEP 05: 側邊欄渲染 (收起) ---")
#     driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
#     assert sidebar_container.get_attribute("data-state") != "expanded"

#     # STEP 06: 主題切換 (白色)
#     log("--- STEP 06: 主題切換 (白色) ---")
#     button_element = driver.find_element_by_xpath("//button[@aria-label='Switch to light mode']")
#     button_element.click()
#     time.sleep(1)
#     assert button_element.get_attribute("aria-label") == "Switch to dark mode"

#     # STEP 07: 創建對話
#     log("--- STEP 07: 創建對話 ---")
#     driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("hi")
#     driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
#     time.sleep(3)
#     driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").click()

#     # STEP 08: 側邊欄渲染 (展開)
#     log("--- STEP 08: 側邊欄渲染 (展開) ---")
#     driver.find_element_by_xpath("/html/body/div/main/div/header/button").click()
#     assert sidebar_container.get_attribute("data-state") == "expanded"

#     # STEP 09: 主題切換 (黑色)
#     log("--- STEP 09: 主題切換 (黑色) ---")
#     button_element = driver.find_element_by_xpath("//button[@aria-label='Switch to dark mode']")
#     button_element.click()
#     time.sleep(1)
#     assert button_element.get_attribute("aria-label") == "Switch to light mode"

#     # STEP 10: 獲取所有對話清單 (有對話清單)
#     log("--- STEP 10: 獲取所有對話清單 (有對話清單) ---")
#     driver.find_element_by_xpath("//span[@title='ITRI Network Service']")

#     # STEP 11: 更新對話名稱
#     log("--- STEP 11: 更新對話名稱 ---")
#     driver.find_element_by_css_selector("button[id^='radix-:r']").click()
#     driver.find_element_by_css_selector("[id^='radix-:r'] > div").click()
#     driver.find_element_by_css_selector("input.flex-1.border").click()
#     driver.find_element_by_css_selector("input.flex-1.border").clear()
#     driver.find_element_by_css_selector("input.flex-1.border").send_keys("Change Name" + Keys.ENTER)
#     time.sleep(2)

#     # STEP 12: 刪除對話
#     log("--- STEP 12: 刪除對話 ---")
#     driver.find_element_by_css_selector("button[id^='radix-:r']").click()
#     driver.find_element_by_css_selector("[id^='radix-:r'] > div:nth-of-type(2)").click()
#     time.sleep(2)

#     # STEP 13: 獲取所有對話清單 (無對話清單)
#     log("--- STEP 13: 獲取所有對話清單 (無對話清單) ---")
#     assert "尚無對話紀錄" in driver.find_element_by_tag_name("body").text
#     time.sleep(1)

#     # STEP 14: 創建對話
#     log("--- STEP 14: 創建對話 ---")
#     driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/ul/div/button").click()
#     driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("get sinr map")
#     driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
#     time.sleep(5)
#     driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("yes")
#     driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
#     time.sleep(5)
#     driver.find_element_by_xpath("//img[@alt='image-0']").click()
#     time.sleep(1)
#     driver.find_element_by_xpath("//img[@alt='preview']").click()
#     time.sleep(1)

#     # STEP 15: 取得對話歷史紀錄
#     log("--- STEP 15: 取得對話歷史紀錄 ---")
#     driver.find_element_by_xpath("/html/body/div/main/div/header/button[2]").click()
#     time.sleep(2)
#     driver.find_element_by_css_selector("a[href^='/conversation/']").click()
#     time.sleep(2)

#     # STEP 16: 創建對話
#     log("--- STEP 16: 創建對話 ---")
#     driver.find_element_by_xpath("/html/body/div/main/div/header/button[2]").click()
#     time.sleep(2)
#     driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("get UE status")
#     driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
#     time.sleep(5)
#     driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("5.")
#     driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
#     time.sleep(5)
#     driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("yes")
#     driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
#     time.sleep(5)
#     driver.find_element_by_xpath("/html/body/div/main/div/div/div/div/div/div/div[7]/div/div[2]/div/div/div[2]")
#     time.sleep(1)
#     driver.find_element_by_xpath("/html/body/div/main/div/div/div/div/div/div/div[7]/div/div[2]/div/div/div[2]/button").click()
#     time.sleep(1)
#     driver.find_element_by_xpath("/html/body/div/main/div/div/div/div/div/div/div[7]/div/div[2]/div/div/div[2]/button").click()
#     time.sleep(1)

#     # STEP 17: 獲取所有對話清單 (有對話清單)
#     log("--- STEP 17: 獲取所有對話清單 (有對話清單) ---")
#     driver.find_element_by_css_selector("button[id^='radix-:r']")

#     # STEP 18: 登出
#     log("--- STEP 18: 登出 ---")
#     driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[3]/button").click()
#     time.sleep(2)
    
#     log("=== TEST CASE 00 PASSED ===")

# def test_case_01_register_account():
#     log("=== START TEST CASE 01: 註冊帳號 ===")
#     given_not_registered_user()
    
#     log("=== WHEN: 輸入資訊並點擊「註冊」 ===")
#     driver.find_element_by_id("username").send_keys(random_user)
#     driver.find_element_by_id("email").send_keys(random_email)
#     driver.find_element_by_id("password").send_keys(random_password)
#     driver.find_element_by_xpath("//button[@type='submit']").click()
#     time.sleep(1)
    
#     log("=== THEN: 成功建立帳戶 ===")
#     assert "Account created successfully" in driver.find_element_by_tag_name("body").text
    
#     log("=== TEST CASE 01 PASSED ===")

# def test_case_02_login_account():
#     log("=== START TEST CASE 02: 登入帳號 ===")
#     given_registered_user()
    
#     log("=== WHEN: 輸入資訊並點擊「登入」 ===")
#     driver.find_element_by_id("username").send_keys(random_user)
#     driver.find_element_by_id("password").send_keys(random_password)
#     driver.find_element_by_xpath("//button[@type='submit']").click()
#     time.sleep(1)
    
#     log("=== THEN: 成功登入 ===")
#     assert "Login successful!" in driver.find_element_by_tag_name("body").text
    
#     log("=== TEST CASE 02 PASSED ===")

# def test_case_03_get_all_conversations():
#     log("=== START TEST CASE 03: 獲取所有對話清單 ===")
#     given_logged_in_and_sidebar_expanded()
    
#     log("=== WHEN: 查看對話列表 ===")
    
#     log("=== THEN: 列表顯示「尚無對話紀錄」 ===")
#     assert "尚無對話紀錄" in driver.find_element_by_tag_name("body").text
    
#     driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("hi")
#     driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
#     time.sleep(3) # Wait for conversation to be created
#     driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").click()
    
#     log("=== AND: 列表顯示所有已創建的對話 ===")
#     driver.find_element_by_xpath("//span[@title='ITRI Network Service']").click()
#     assert "ITRI Network Service" in driver.find_element_by_tag_name("body").text
#     time.sleep(1)
    
#     log("=== TEST CASE 03 PASSED ===")

# def test_case_04_create_new_conversation():
#     log("=== START TEST CASE 04: 創建新對話 ===")
#     given_logged_in_and_sidebar_expanded()
    
#     log("=== WHEN: 輸入內容並送出 ===")
#     driver.find_element_by_xpath("//textarea[@placeholder='在這裡輸入訊息，按 Enter 即可送出 (Shift+Enter換行)']").send_keys("get UE status")
#     driver.find_element_by_xpath("/html/body/div/main/div/main/div/div[2]/div/button").click()
#     time.sleep(3) # Wait for conversation to be created
#     driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("5.")
#     driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
#     time.sleep(3)
#     driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("yes")
#     driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
#     time.sleep(3)
#     driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("get SINR map")
#     driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
#     time.sleep(3)
#     driver.find_element_by_xpath("//textarea[@placeholder='Type message...']").send_keys("yes")
#     driver.find_element_by_xpath("/html/body/div/main/div/div[2]/div/div/div/button").click()
#     time.sleep(3)
#     driver.find_element_by_xpath("//img[@alt='image-0']")
    
#     log("=== THEN: 成功創建新對話 ===")
#     assert "SINR" in driver.find_element_by_tag_name("body").text 
    
#     log("=== TEST CASE 04 PASSED ===")

# def test_case_05_update_conversation_name():
#     log("=== START TEST CASE 05: 更新對話名稱 ===")
#     given_logged_in_and_sidebar_expanded_and_has_conversation()
#     time.sleep(2)
    
#     log("=== WHEN: 點擊編輯並輸入新名稱 ===")
#     driver.find_element_by_css_selector("button[id^='radix-:r']").click()
#     driver.find_element_by_css_selector("[id^='radix-:r'] > div").click()
    
#     new_name = "Change Name"
#     input_field = driver.find_element_by_css_selector("input.flex-1.border")
#     input_field.clear()
#     input_field.send_keys(new_name + Keys.ENTER)
#     time.sleep(2)
    
#     log("=== THEN: 對話名稱成功更新 ===")
#     assert new_name in driver.find_element_by_tag_selector("span[title]").text
#     time.sleep(1)
    
#     log("=== TEST CASE 05 PASSED ===")

# def test_case_06_delete_conversation():
#     log("=== START TEST CASE 06: 刪除對話 ===")
#     given_logged_in_and_sidebar_expanded_and_has_conversation()
#     time.sleep(2)
    
#     log("=== WHEN: 點擊刪除按鈕 ===")
#     driver.find_element_by_css_selector("button[id^='radix-:r']").click()
#     driver.find_element_by_css_selector("[id^='radix-:r'] > div:nth-of-type(2)").click()
#     time.sleep(2)
    
#     log("=== THEN: 對話從列表中消失 ===")
#     assert "尚無對話紀錄" in driver.find_element_by_tag_name("body").text
#     time.sleep(1)
    
#     log("=== TEST CASE 06 PASSED ===")

# def test_case_07_get_conversation_history():
#     log("=== START TEST CASE 07: 取得對話歷史紀錄 ===")
#     given_logged_in_and_sidebar_expanded_and_has_conversation()
#     time.sleep(2)
    
#     log("=== WHEN: 創新對話後再點擊對話清單中的某個對話項目 ===")
#     driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/ul/div/button").click()
#     time.sleep(2)
#     driver.find_element_by_css_selector("a[href^='/conversation/']").click()
#     time.sleep(2)
    
#     log("=== THEN: 頁面導航到該對話的歷史內容 ===")
#     assert "hi" in driver.find_element_by_tag_name("body").text
    
#     log("=== TEST CASE 07 PASSED ===")

# def test_case_08_logout_account():
#     log("=== START TEST CASE 08: 登出帳號 ===")
#     given_logged_in_and_sidebar_expanded()
#     time.sleep(2)
    
#     log("=== WHEN: 點擊登出按鈕 ===")
#     driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[3]/button").click()
#     time.sleep(2)
    
#     log("=== THEN: 使用者被導航回登入頁面 ===")
#     assert "Log in" in driver.find_element_by_tag_name("body").text
    
#     log("=== TEST CASE 08 PASSED ===")

# def test_case_09_expand_collapse_sidebar():
#     log("=== START TEST CASE 09: 展開/收起側邊欄 ===")
#     given_logged_in_user()
    
#     log("=== WHEN: 點擊展開按鈕 ===")
#     sidebar_container = driver.find_element_by_xpath('//div[@data-variant="sidebar"]')
#     driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
#     time.sleep(1)
    
#     log("=== THEN: 側邊欄成功展開 ===")
#     assert sidebar_container.get_attribute("data-state") == "expanded"
        
#     log("=== WHEN: 點擊收起按鈕 ===")
#     driver.find_element_by_xpath("/html/body/div/main/div/div/header/button").click()
#     time.sleep(1)
    
#     log("=== THEN: 側邊欄成功收起 ===")
#     assert sidebar_container.get_attribute("data-state") != "expanded"
    
#     log("=== TEST CASE 09 PASSED ===")

# def test_case_10_switch_to_dark_theme():
#     log("=== START TEST CASE 10: 切換主題為黑/白色 ===")
#     given_logged_in_user()

#     log("=== WHEN: 點擊主題切換按鈕 ===")
#     button_element = driver.find_element_by_xpath("//button[@aria-label='Switch to light mode']")
#     button_element.click()
#     time.sleep(1)
    
#     log("=== THEN: 頁面成功切換為白色主題 ===")
#     assert button_element.get_attribute("aria-label") == "Switch to dark mode"
    
#     log("=== WHEN: 點擊主題切換按鈕 ===")
#     button_element.click()
#     time.sleep(1)
    
#     log("=== THEN: 頁面成功切換為黑色主題 ===")
#     assert button_element.get_attribute("aria-label") == "Switch to light mode"
#     time.sleep(1)
    
#     log("=== TEST CASE 10 PASSED ===")

# # 主執行區塊
# # -------------------------------------------------------------------------------------------------------

# if __name__ == "__main__":
    
#     # === 完整 User Story 測試 ===
# #     test_case_to_run = [test_case_00_full_flow]
    
#     # === Use Case 測試 ===
#     test_case_to_run = [
#         test_case_01_register_account, 
# #         test_case_02_login_account, 
# #         test_case_03_get_all_conversations, 
# #         test_case_04_create_new_conversation,
# #         test_case_05_update_conversation_name,
# #         test_case_06_delete_conversation,
# #         test_case_07_get_conversation_history, 
# #         test_case_08_logout_account,
# #         test_case_09_expand_collapse_sidebar, 
# #         test_case_10_switch_to_dark_theme
#     ]

#     for test_case in test_case_to_run:
#         try:
#             log(f"#################### Running {test_case.__name__} ####################")
#             setup_driver()
#             test_case()
#         except (AssertionError, Exception) as e:
#             log(f"#################### {test_case.__name__} FAILED: {e} ####################")
#         finally:
#             teardown_driver()
#             log("Driver closed.")
#             time.sleep(1)
            
#     try:
#         # 建立 LogToHtml 物件
#         log_to_html = LogToHtml(
#             script_root=__file__,
#             log_root=log_dir,
#             static_root=None,  # 這是關鍵！將靜態資源內嵌到 HTML 中
#             export_dir=export_dir, 
#             plugins=['airtest_selenium.report']
#         )

#         log_to_html.report()

#         print(f"Report generated successfully")

#     except Exception as e:
#         print(f"An error occurred while generating the report: {e}")