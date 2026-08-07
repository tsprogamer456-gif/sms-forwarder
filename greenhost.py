"""
Data Processing and Notification System (Low-RAM Request-Based Version)
This script runs efficiently on server environments by using HTTP sessions instead of heavy browsers.
"""

import time
import re
import json
import os
import requests
from bs4 import BeautifulSoup

# ====== Configuration (Loaded from Environment Variables) ======
BOT_TOKEN = os.getenv("BOT_TOKEN", "8020298281:AAEl9qyc0D7kvVMUJPireGjLCbHm_7sMQt0")
CHAT_ID = os.getenv("CHAT_ID", "-1003752154815")
USERNAME = os.getenv("APP_USERNAME", "Shifathossain")
PASSWORD = os.getenv("APP_PASSWORD", "Shifathossain")

LOGIN_URL = "http://139.99.9.4/ints/login"
DATA_URL = "http://139.99.9.4/ints/agent/SMSCDRStats"

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

def solve_captcha_from_html(html_text):
    """Extract math captcha from HTML source."""
    match = re.search(r'What is (\d+)\s*[\+\-\*]\s*(\d+)', html_text)
    if match:
        num1, num2 = int(match.group(1)), int(match.group(2))
        return num1 + num2 if '+' in match.group(0) else num1 - num2
    return None

def authenticate_session():
    """Login using requests Session to avoid Selenium RAM usage."""
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    session.headers.update(headers)
    
    try:
        resp = session.get(LOGIN_URL, timeout=10)
        captcha_ans = solve_captcha_from_html(resp.text)
        
        if captcha_ans is None:
            print("❌ Captcha not found on login page!")
            return None

        login_data = {
            'username': USERNAME,
            'password': PASSWORD,
            'answer': str(captcha_ans)
        }
        
        post_resp = session.post(LOGIN_URL, data=login_data, timeout=10)
        if "login" not in post_resp.url and post_resp.status_code == 200:
            print("✅ HTTP Login Successful!")
            return session
        else:
            print("❌ HTTP Login Failed!")
            return None
    except Exception as e:
        print(f"⚠️ Auth error: {e}")
        return None

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
                "copy_text": {"text": code}
            })
        if message_text.strip():
            inline_keyboard_buttons.append({
                "text": "📋 FULL SMS",
                "copy_text": {"text": message_text}
            })
        if inline_keyboard_buttons:
            payload['reply_markup'] = json.dumps({"inline_keyboard": [inline_keyboard_buttons]})
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data=payload, timeout=5)
        print(f"✅ Sent OTP: {code} → {number}")
        return True
    except Exception as e:
        print(f"⚠️ Notification error: {e}")
        return False

# ====== Main Execution ======
if __name__ == "__main__":
    print("🚀 Ultra Low-RAM OTP Forwarder Running...")
    print("=" * 50)
    
    session = authenticate_session()
    if not session:
        print("❌ Could not authenticate. Exiting...")
        exit(1)

    sent_items = set()
    
    # ১. স্ক্রিপ্ট চালুর মুহূর্তে পেজে থাকা আগের সব OTP ডাটা মেমরিতে লক করা (পাঠাবে না)
    try:
        resp = session.get(DATA_URL, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = soup.select("table tbody tr")
        
        for row in rows:
            cols = [td.text.strip() for td in row.find_all("td")]
            if len(cols) >= 7:
                timestamp, number, message_text = cols[0], cols[2], cols[5]
                code = extract_code_from_text(message_text)
                if code:
                    sent_items.add(f"{number}_{code}_{timestamp}")
        print(f"📦 Successfully ignored {len(sent_items)} past OTPs.")
    except Exception as e:
        print(f"⚠️ Error fetching history: {e}")

    start_time = time.time()
    ONE_HOUR = 3600

    # ২. পলিং লুপ (যাতে ব্রাউজারের কোনো RAM খরচ হবে না)
    while True:
        # ১ ঘণ্টা পূর্ণ হলে বন্ধ হওয়া (Railway auto-restart করবে)
        if time.time() - start_time >= ONE_HOUR:
            print("⏰ 1 hour execution completed. Restarting app via Railway...")
            break

        try:
            resp = session.get(DATA_URL, timeout=10)
            
            # সেশন এক্সপায়ার হয়ে গেলে পুনরায় লগইন
            if "login" in resp.url:
                print("⚠️ Session expired! Refreshing auth session...")
                session = authenticate_session()
                continue
                
            soup = BeautifulSoup(resp.text, 'html.parser')
            rows = soup.select("table tbody tr")
            
            for row in rows:
                cols = [td.text.strip() for td in row.find_all("td")]
                if len(cols) >= 7:
                    timestamp, number, message_text = cols[0], cols[2], cols[5]
                    
                    if not message_text:
                        continue
                        
                    code = extract_code_from_text(message_text)
                    if code:
                        unique_id = f"{number}_{code}_{timestamp}"
                        
                        # নতুন OTP আসলেই কেবল টেলিগ্রামে ফরওয়ার্ড হবে
                        if unique_id not in sent_items:
                            send_notification(number, code, message_text)
                            sent_items.add(unique_id)
                            
        except Exception as e:
            print(f"⚠️ Fetching error: {e}")

        time.sleep(3)

    print("✅ Graceful shutdown. Container will now restart.")
    exit(0)
