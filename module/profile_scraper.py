from selenium.webdriver.common.by import By
import time
import re

def parse_instagram_number(text):
    
    text = text.lower().strip()

    match = re.search(r'([\d\.]+)\s*([kmb]?)', text)
    if not match:
        return 0

    number = float(match.group(1))
    suffix = match.group(2)

    multiplier = {
        '': 1,
        'k': 1_000,
        'm': 1_000_000,
        'b': 1_000_000_000,
    }

    return int(number * multiplier.get(suffix, 1))

def get_profile_info(driver, username):
    driver.get(f'https://www.instagram.com/{username}/')
    time.sleep(15)

    try:
        # Exporting the number of following and followers
        followers_text = driver.find_element(By.XPATH, '//a[contains(@href, "/followers/")]//span').text
        following_text = driver.find_element(By.XPATH, '//a[contains(@href, "/following/")]//span').text

        # Convert to number
        followers = parse_instagram_number(followers_text)
        following = parse_instagram_number(following_text)

        return {"followers": followers, "following": following}
    except Exception as e:
        print(f"Error Extracting Profile Information: {e}")
        return None