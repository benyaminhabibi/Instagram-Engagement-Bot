from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from colorama import Fore, Style
from selenium.webdriver.common.action_chains import ActionChains


def get_posts_data(driver, username, num_posts):
    driver.get(f'https://www.instagram.com/{username}/')
    actions = ActionChains(driver)
    time.sleep(20)

    def scroll_to_load_posts():
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(7)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    scroll_to_load_posts()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "x1iyjqo2")]'))
        )
        post_divs = driver.find_elements(By.CSS_SELECTOR, 'div.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x14z9mp.xzj7kzq.xbipx2v.x1j53mea')[:num_posts]
        if not post_divs:
            print(Fore.RED + "\nNo Posts Found" + Style.RESET_ALL)
            return []

        posts = []
        for div in post_divs:
            # انجام hover روی المان
            actions.move_to_element(div).perform()
            time.sleep(2)
            hoverd_elements = driver.find_elements(By.CSS_SELECTOR, 'li.x972fbf.x10w94by.x1qhh985.x14e42zd.x3nfvp2.x15zctf7.xln7xf2.xk390pu.xdj266r.x1lziwak.x1j4z8aw.x2pibh5.x1j53mea.x1ou96c.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x11njtxf')
            comment_elem = hoverd_elements[1]
            comment = comment_elem.find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'span').text
            print(comment)
            time.sleep(3)
            try:
                link = div.find_element(By.TAG_NAME, 'a').get_attribute('href')
                posts.append({'url': link, 'comments': int(comment.replace(",", ""))})
            except Exception as e:
                print(Fore.RED + f"\nError in extracting links: {e}" + Style.RESET_ALL)
                continue

        for item in posts:
            driver.get(item['url'])
            time.sleep(20)
            try:
                like_element = driver.find_element(By.XPATH, '//a[contains(@href, "/liked_by")]/span/span')
                likes = int(like_element.text.replace(",", ""))
                print(likes)
            except Exception as e:
                print(Fore.RED + f"\nError in extracting likes: {e}" + Style.RESET_ALL)
                likes = 0

            item['likes'] = likes
            driver.back()
            time.sleep(10)
        return posts

    except Exception as e:
        print(Fore.RED + f"\nError in process: {e}" + Style.RESET_ALL)
        return []
