import smtplib
import ssl
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from typing import Optional

from config import URLS, EMAILS, SENDER_EMAIL, PASSWORD


def bus_exist(url: str) -> Optional[bool]:
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser = webdriver.Firefox(
        options=options, executable_path='./geckodriver')
    browser.get(url)

    try:
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[1]/main/div/div/section/div[1]/div[2]/p"))
        )
    except TimeoutError as e:
        print(e)
        send_email(EMAILS[:1])
        return None

    html = browser.page_source
    browser.quit()

    soup = BeautifulSoup(html, "lxml")

    try:
        # print(soup.body.main.section.find("div"))
        if soup.body.main.section.find("div").get_text() == " موجودی اتوبوس‌ها در این تاریخ به اتمام رسیده است. ":
            return False
        return True
    except Exception as e:
        return True


def send_email(email_list: list[str]) -> None:

    port = 465  # For SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        for email in EMAILS:
            server.sendmail(SENDER_EMAIL, email, "BUUUUUUUUUUUUUUUS!!!")


def main():
    for url in URLS:
        if bus_exist(url):
            send_email(EMAILS)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)
