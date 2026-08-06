"""
Data Processing and Notification System
This script processes incoming data from a web source and forwards it to a messaging platform.
All operations are performed in headless mode for server compatibility.
"""

import time
import re
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ====== Configuration ======
BOT_TOKEN = "8020298281:AAEl9qyc0D7kvVMUJPireGjLCbHm_7sMQt0"
CHAT_ID = "-1003752154815"
USERNAME = "Shifathossain"
PASSWORD = "Shifathossain"

LOGIN_URL = "http://139.99.9.4/ints/login"
DATA_URL = "http://139.99.9.4/ints/agent/SMSCDRStats"

# ====== Browser Setup (Headless Mode) ======
def create_browser():
    """Initialize headless browser for data processing."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(options=options)

driver = create_browser()
wait = WebDriverWait(driver, 30)

# ====== Country Data ======
COUNTRY_CODES = {
    "1": ("USA/Canada", "🇺🇸"), "7": ("Russia", "🇷🇺"), "20": ("Egypt", "🇪🇬"),
    "27": ("South Africa", "🇿🇦"), "30": ("Greece", "🇬🇷"), "31": ("Netherlands", "🇳🇱"),
    "32": ("Belgium", "🇧🇪"), "33": ("France", "🇫🇷"), "34": ("Spain", "🇪🇸"),
    "36": ("Hungary", "🇭🇺"), "39": ("Italy", "🇮🇹"), "40": ("Romania", "🇷🇴"),
    "41": ("Switzerland", "🇨🇭"), "43": ("Austria", "🇦🇹"), "44": ("UK", "🇬🇧"),
    "45": ("Denmark", "🇩🇰"), "46": ("Sweden", "🇸🇪"), "47": ("Norway", "🇳🇴"),
    "48": ("Poland", "🇵🇱"), "49": ("Germany", "🇩🇪"), "51": ("Peru", "🇵🇪"),
    "52": ("Mexico", "🇲🇽"), "53": ("Cuba", "🇨🇺"), "54": ("Argentina", "🇦🇷"),
    "55": ("Brazil", "🇧🇷"), "56": ("Chile", "🇨🇱"), "57": ("Colombia", "🇨🇴"),
    "58": ("Venezuela", "🇻🇪"), "60": ("Malaysia", "🇲🇾"), "61": ("Australia", "🇦🇺"),
    "62": ("Indonesia", "🇮🇩"), "63": ("Philippines", "🇵🇭"), "64": ("New Zealand", "🇳🇿"),
    "65": ("Singapore", "🇸🇬"), "66": ("Thailand", "🇹🇭"), "81": ("Japan", "🇯🇵"),
    "82": ("South Korea", "🇰🇷"), "84": ("Vietnam", "🇻🇳"), "86": ("China", "🇨🇳"),
    "90": ("Turkey", "🇹🇷"), "91": ("India", "🇮🇳"), "92": ("Pakistan", "🇵🇰"),
    "93": ("Afghanistan", "🇦🇫"), "94": ("Sri Lanka", "🇱🇰"), "95": ("Myanmar", "🇲🇲"),
    "212": ("Morocco", "🇲🇦"), "213": ("Algeria", "🇩🇿"), "216": ("Tunisia", "🇹🇳"),
    "218": ("Libya", "🇱🇾"), "220": ("Gambia", "🇬🇲"), "221": ("Senegal", "🇸🇳"),
    "222": ("Mauritania", "🇲🇷"), "223": ("Mali", "🇲🇱"), "224": ("Guinea", "🇬🇳"),
    "225": ("Côte d'Ivoire", "🇨🇮"), "226": ("Burkina Faso", "🇧🇫"), "227": ("Niger", "🇳🇪"),
    "228": ("Togo", "🇹🇬"), "229": ("Benin", "🇧🇯"), "230": ("Mauritius", "🇲🇺"),
    "231": ("Liberia", "🇱🇷"), "232": ("Sierra Leone", "🇸🇱"), "233": ("Ghana", "🇬🇭"),
    "234": ("Nigeria", "🇳🇬"), "235": ("Chad", "🇹🇩"), "236": ("CAR", "🇨🇫"),
    "237": ("Cameroon", "🇨🇲"), "238": ("Cape Verde", "🇨🇻"), "239": ("São Tomé", "🇸🇹"),
    "240": ("Equatorial Guinea", "🇬🇶"), "241": ("Gabon", "🇬🇦"), "242": ("Congo", "🇨🇬"),
    "243": ("DR Congo", "🇨🇩"), "244": ("Angola", "🇦🇴"), "245": ("Guinea-Bissau", "🇬🇼"),
    "248": ("Seychelles", "🇸🇨"), "249": ("Sudan", "🇸🇩"), "250": ("Rwanda", "🇷🇼"),
    "251": ("Ethiopia", "🇪🇹"), "252": ("Somalia", "🇸🇴"), "253": ("Djibouti", "🇩🇯"),
    "254": ("Kenya", "🇰🇪"), "255": ("Tanzania", "🇹🇿"), "256": ("Uganda", "🇺🇬"),
    "257": ("Burundi", "🇧🇮"), "258": ("Mozambique", "🇲🇿"), "260": ("Zambia", "🇿🇲"),
    "261": ("Madagascar", "🇲🇬"), "262": ("Réunion", "🇷🇪"), "263": ("Zimbabwe", "🇿🇼"),
    "264": ("Namibia", "🇳🇦"), "265": ("Malawi", "🇲🇼"), "266": ("Lesotho", "🇱🇸"),
    "267": ("Botswana", "🇧🇼"), "268": ("Eswatini", "🇸🇿"), "269": ("Comoros", "🇰🇲"),
    "351": ("Portugal", "🇵🇹"), "352": ("Luxembourg", "🇱🇺"), "353": ("Ireland", "🇮🇪"),
    "354": ("Iceland", "🇮🇸"), "355": ("Albania", "🇦🇱"), "356": ("Malta", "🇲🇹"),
    "357": ("Cyprus", "🇨🇾"), "358": ("Finland", "🇫🇮"), "359": ("Bulgaria", "🇧🇬"),
    "370": ("Lithuania", "🇱🇹"), "371": ("Latvia", "🇱🇻"), "372": ("Estonia", "🇪🇪"),
    "373": ("Moldova", "🇲🇩"), "374": ("Armenia", "🇦🇲"), "375": ("Belarus", "🇧🇾"),
    "380": ("Ukraine", "🇺🇦"), "381": ("Serbia", "🇷🇸"), "382": ("Montenegro", "🇲🇪"),
    "385": ("Croatia", "🇭🇷"), "386": ("Slovenia", "🇸🇮"), "387": ("Bosnia", "🇧🇦"),
    "389": ("North Macedonia", "🇲🇰"), "880": ("Bangladesh", "🇧🇩"), "886": ("Taiwan", "🇹🇼"),
    "960": ("Maldives", "🇲🇻"), "961": ("Lebanon", "🇱🇧"), "962": ("Jordan", "🇯🇴"),
    "963": ("Syria", "🇸🇾"), "964": ("Iraq", "🇮🇶"), "965": ("Kuwait", "🇰🇼"),
    "966": ("Saudi Arabia", "🇸🇦"), "967": ("Yemen", "🇾🇪"), "968": ("Oman", "🇴🇲"),
    "970": ("Palestine", "🇵🇸"), "971": ("UAE", "🇦🇪"), "972": ("Israel", "🇮🇱"),
    "973": ("Bahrain", "🇧🇭"), "974": ("Qatar", "🇶🇦"), "975": ("Bhutan", "🇧🇹"),
    "976": ("Mongolia", "🇲🇳"), "977": ("Nepal", "🇳🇵"), "992": ("Tajikistan", "🇹🇯"),
    "993": ("Turkmenistan", "🇹🇲"), "994": ("Azerbaijan", "🇦🇿"), "995": ("Georgia", "🇬🇪"),
    "996": ("Kyrgyzstan", "🇰🇬"), "998": ("Uzbekistan", "🇺🇿"),
}

def get_country_info(number):
    """Extract country information from phone number."""
    try:
        digits = re.sub(r'\D', '', str(number))
        if not digits:
            return "Unknown", "🏳️"
        for prefix_length in (4, 3, 2, 1):
            prefix = digits[:prefix_length]
            if prefix in COUNTRY_CODES:
                return COUNTRY_CODES[prefix]
        return "Unknown", "🏳️"
    except:
        return "Unknown", "🏳️"

def extract_code_from_text(text):
    """Extract 6-digit code from message text."""
    match = re.search(r'\b\d{6}\b', text)
    return match.group(0) if match else None

# ====== Data Processing Functions ======
def process_captcha():
    """Extract and solve mathematical captcha from page source."""
    try:
        print("🔍 Processing captcha...")
        page_source = driver.page_source
        print(f"📄 Page source length: {len(page_source)}")
        
        match = re.search(r'What is (\d+)\s*[\+\-\*]\s*(\d+)', page_source)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            if '+' in match.group(0):
                result = num1 + num2
                operator = '+'
            elif '-' in match.group(0) or '−' in match.group(0):
                result = num1 - num2
                operator = '-'
            else:
                result = num1 + num2
                operator = '+'
            
            print(f"🔢 Captcha: {num1} {operator} {num2} = {result}")
            
            answer_field = None
            for selector in [By.NAME, By.ID, By.XPATH]:
                try:
                    if selector == By.NAME:
                        answer_field = driver.find_element(By.NAME, "answer")
                    elif selector == By.ID:
                        answer_field = driver.find_element(By.ID, "answer")
                    elif selector == By.XPATH:
                        answer_field = driver.find_element(By.XPATH, "//input[@placeholder='Answer']")
                    if answer_field:
                        break
                except:
                    continue
            
            if answer_field:
                answer_field.clear()
                answer_field.send_keys(str(result))
                print(f"✅ Captcha solved: {result}")
                return True
            else:
                print("❌ Answer field not found!")
                return False
        else:
            print("❌ Captcha not found!")
            return False
    except Exception as e:
        print(f"⚠️ Captcha error: {e}")
        return False

def authenticate():
    """Perform authentication to access data source."""
    try:
        print("\n🔐 Authenticating...")
        driver.get(LOGIN_URL)
        time.sleep(5)
        
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.clear()
        username_field.send_keys(USERNAME)
        print("✅ Username entered")
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(PASSWORD)
        print("✅ Password entered")
        
        if not process_captcha():
            print("⚠️ Captcha solving failed. Exiting...")
            driver.quit()
            return False
        
        print("🔄 Submitting form...")
        js_code = """
        var form = document.querySelector('form');
        if (form) {
            form.submit();
            return true;
        }
        var buttons = document.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++) {
            if (buttons[i].textContent.trim().toUpperCase() === 'LOGIN') {
                buttons[i].click();
                return true;
            }
        }
        var submitBtn = document.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.click();
            return true;
        }
        return false;
        """
        result = driver.execute_script(js_code)
        if result:
            print("✅ Form submitted successfully")
        else:
            print("❌ Submission failed!")
            driver.quit()
            return False
        
        time.sleep(5)
        current_url = driver.current_url
        print(f"📌 Current URL: {current_url}")
        
        if "login" in current_url:
            print("❌ Authentication failed!")
            return False
        
        print("✅ Authentication successful!")
        return True
    except Exception as e:
        print(f"⚠️ Authentication error: {e}")
        return False

def send_notification(number, code, message_text):
    """Send notification to messaging platform."""
    try:
        country_name, country_flag = get_country_info(number)
        service = "Unknown"
        if "PayPal" in message_text:
            service = "PayPal"
        elif "Google" in message_text:
            service = "Google"
        elif "Facebook" in message_text:
            service = "Facebook"
        
        msg_text = (
            "🔑 *OTP RECEIVED!*\n\n"
            f"🔢 *Number:* `{number}`\n\n"
            f"🌍 *Country:* {country_flag} {country_name}\n\n"
            f"👤 *Service:* {service}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        
        payload = {
            'chat_id': CHAT_ID,
            'text': msg_text,
            'parse_mode': 'Markdown'
        }
        
        inline_keyboard_buttons = []
        if code:
            inline_keyboard_buttons.append({
                "text": f"🔑 {code}",
                "style": "success",
                "copy_text": {"text": code}
            })
        if message_text.strip():
            inline_keyboard_buttons.append({
                "text": "📋 FULL SMS",
                "style": "success",
                "copy_text": {"text": message_text}
            })
        if inline_keyboard_buttons:
            reply_markup = {"inline_keyboard": [inline_keyboard_buttons]}
            payload['reply_markup'] = json.dumps(reply_markup)
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data=payload, timeout=5)
        print(f"✅ OTP: {code} → {number}")
        return True
    except Exception as e:
        print(f"⚠️ Notification error: {e}")
        return False

# ====== Main Execution ======
if __name__ == "__main__":
    print("🚀 Data Processing and Notification System (Headless Mode)")
    print("=" * 50)
    
    if not authenticate():
        print("❌ Authentication failed! Shutting down...")
        driver.quit()
        exit()
    
    driver.get(DATA_URL)
    time.sleep(5)
    
    print("🚀 Monitoring started... (checking every 3 seconds)")
    sent_items = set()
    
    try:
        while True:
            if "login" in driver.current_url:
                print("⚠️ Session expired! Re-authenticating...")
                authenticate()
                driver.get(DATA_URL)
                continue
            
            driver.refresh()
            time.sleep(2)
            
            rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
            
            for row in rows:
                try:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 7:
                        timestamp = cols[0].text.strip()
                        number = cols[2].text.strip()
                        message_text = cols[5].text.strip()
                        
                        if not message_text:
                            continue
                        
                        code = extract_code_from_text(message_text)
                        if code:
                            unique_id = f"{number}_{code}_{timestamp}"
                            if unique_id not in sent_items:
                                send_notification(number, code, message_text)
                                sent_items.add(unique_id)
                                if len(sent_items) > 500:
                                    sent_items = set(list(sent_items)[-250:])
                except:
                    continue
            
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"⚠️ Error: {e}")
        time.sleep(5)
    
    driver.quit()
    print("✅ Shutdown complete.")