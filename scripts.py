"""Selenium scripts for End-To-End testing"""\

from collections.abc import Collection
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.action_chains import ActionChains
from decouple import config
import time


HEADLESS = config("HEADLESS", cast=bool, default=False)
STUDENT_EMAIL = config("STUDENT_EMAIL", default="littleTimmy@mytcas.com")
STUDENT_PASSWORD = config("STUDENT_PASSWORD", default="lollygagging123")


class Browser:
    """Provide access to an instance of a Selenium web driver.

    Methods:
    get_browser(cls)  class method that returns an instance of a WebDriver
    """

    _driver = None

    @classmethod
    def get_browser(cls):
        """Get an instance of a Chrome webdriver."""
        if cls._driver:
            return cls._driver
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        cls._driver = driver
        return driver

    @classmethod
    def get_action_chain(cls):
        """Inject the current browser into the action chain API."""
        if cls._driver:
            return ActionChains(cls._driver)
        browser = cls.get_browser()
        return ActionChains(browser)


class BaseUserActions:
    """Class containing basic actions a user might preform."""

    @staticmethod
    def login_to_google(self, email: str, password: str):
        """Authenticate the current user with their Google Oauth credentials."""
        browser.get("https://a-plus-management.onrender.com/")
        time.sleep(3)
        # find the login with Google button
        login = WebDriverWait(browser, 10).until(
            cond.visibility_of_element_located((By.TAG_NAME, "button"))
        )
        # click the button
        actions.move_to_element(login).click().perform()
        time.sleep(3)
        # find the email input
        email_input = WebDriverWait(browser, 10).until(
            cond.visibility_of_element_located((By.ID, "identifierId"))
        )
        # key in email and click next
        email_input.send_keys(email)
        browser.find_element(By.ID, "identifierNext").click()
        time.sleep(3)
        # find the password input
        password_input = WebDriverWait(browser, 10).until(
            cond.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[type=password]"))
        )
        # key in the password and click next
        password_input.send_keys(password)
        browser.find_element(By.ID, "passwordNext").click()
        # accept TOS on the Oauth consent screen
        WebDriverWait(browser, 10).until(
            cond.visibility_of_element_located(
                (By.XPATH, "//span[text()='Continue']"))
        ).click()


class StudentTests(BaseUserActions):
    """Class containing tests for students."""

    def test_create_tasks(self, taskboard_name: str, tasks: Collection[dict]):
        """
        As a student, I want to be able to create tasks.
        So that I can track work that needs to be done.

        Creates tasks on a given taskboard.
        :param taskboard_name: The taskboard the student is using.
        :param tasks: Tasks the student will create
        """
        pass


def login_to_google(email: str, password: str):
    """Authenticate the current user with their Google Oauth credentials."""
    browser.get("https://a-plus-management.onrender.com/")
    time.sleep(3)
    # find the login with Google button
    login = WebDriverWait(browser, 10).until(
        cond.visibility_of_element_located((By.TAG_NAME, "button"))
    )
    # click the button
    actions.move_to_element(login).click().perform()
    time.sleep(3)
    # find the email input
    email_input = WebDriverWait(browser, 10).until(
        cond.visibility_of_element_located((By.ID, "identifierId"))
    )
    # key in email and click next
    email_input.send_keys(email)
    browser.find_element(By.ID, "identifierNext").click()
    time.sleep(3)
    # find the password input
    password_input = WebDriverWait(browser, 10).until(
        cond.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[type=password]"))
    )
    # key in the password and click next
    password_input.send_keys(password)
    browser.find_element(By.ID, "passwordNext").click()
    # accept TOS on the Oauth consent screen
    WebDriverWait(browser, 10).until(
        cond.visibility_of_element_located((By.XPATH, "//span[text()='Continue']"))
    ).click()


if __name__ == "__main__":
    driver = Browser()
    browser = driver.get_browser()
    actions = driver.get_action_chain()
    login_to_google(STUDENT_EMAIL, STUDENT_PASSWORD)

    print("eol")
    while(True):
        pass