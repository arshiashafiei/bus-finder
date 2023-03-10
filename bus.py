import smtplib
import ssl
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

from config import URLS, EMAILS, SENDER_EMAIL, PASSWORD


def bus_exist(url: str) -> bool:
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser = webdriver.Firefox(
        options=options, executable_path='./geckodriver')
    browser.get(url)

    try:
        # connection error cannot happen here
        x_path = "/html/body/div[1]/div[1]/main/div/div" \
                 "/section/div[1]/div[2]/p"
        WebDriverWait(browser, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, x_path))
        )
    except TimeoutException as e:
        print(e)
        return True

    html = browser.page_source
    browser.quit()

    soup = BeautifulSoup(html, "lxml")

    try:
        # print(soup.body.main.section.find("div"))
        alert_text = " موجودی اتوبوس‌ها در این تاریخ به اتمام رسیده است. "
        if soup.body.main.section.find("div").get_text() == alert_text:
            return False
        return True
    except Exception as e:
        return True


def send_email(email_list: list[str], message: str) -> None:

    port = 465  # For SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        for email in email_list:
            server.sendmail(SENDER_EMAIL, email, message)


def main() -> bool:
    for url in URLS:
        if bus_exist(url):
            send_email(EMAILS, "OTOOOOOOOOOOBOOS!!!")
            return True
        else:
            print("No Bus Found!")

    print("Retrying...")
    return False


if __name__ == "__main__":
    while True:
        found: bool = main()
        if found:
            break
        time.sleep(60)
