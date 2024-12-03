"""Selenium scripts for End-To-End testing"""

from collections.abc import Collection
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from decouple import config
from urllib.parse import urlparse, urlunparse
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
                (By.CSS_SELECTOR, "input[type=password]")
            )
        )
        # key in the password and click next
        password_input.send_keys(password)
        browser.find_element(By.ID, "passwordNext").click()
        # accept TOS on the Oauth consent screen
        WebDriverWait(browser, 10).until(
            cond.visibility_of_element_located((By.XPATH, "//span[text()='Continue']"))
        ).click()


class StudentTests(BaseUserActions):
    """Class containing tests for students."""

    def find_most_recent_taskboard(self, tb_list):
        """
        Finds the most recent taskboard.

        :param tb_list: A list of links to taskboards
        :returns: the go to taskboard button for that taskboard
        """
        return sorted(
            tb_list,
            key=lambda x: int(
                urlparse(x.get_attribute("href")).path.strip("/").split("/")[-1]
            ),
            reverse=True,
        )[0]

    def test_create_tasks(self, taskboard_name: str, tasks: Collection[dict]):
        """
        As a student, I want to be able to create tasks.
        So that I can track work that needs to be done.

        Creates tasks on a given taskboard.
        :param taskboard_name: The taskboard the student is using.
        :param tasks: Tasks the student will create
        """
        taskboards = browser.find_elements(
            By.XPATH, f"//*[contains(text(),'{taskboard_name}')]"
        )
        if len(taskboards) > 0:
            #  TODO: add delete previous taskboard
            pass

        create_tb = WebDriverWait(browser, 10).until(
            cond.visibility_of_element_located(
                (By.CSS_SELECTOR, "button[data-bs-toggle=modal]")
            )
        )
        actions.move_to_element(create_tb).click().perform()
        time.sleep(3)

        tb_name_input = WebDriverWait(browser, 10).until(
            cond.visibility_of_element_located((By.ID, "taskboard-title"))
        )

        tb_name_input.send_keys(taskboard_name)
        time.sleep(3)
        browser.find_element(By.ID, "create-tb-btn").click()
        time.sleep(5)
        tb_buttons = browser.find_elements(
            By.CSS_SELECTOR, "a[class='btn btn-info mx-2']"
        )
        taskboard = self.find_most_recent_taskboard(tb_buttons)
        actions.move_to_element(taskboard).click().perform()
        time.sleep(3)
        for task in tasks:
            add_task = WebDriverWait(browser, 10).until(
                cond.visibility_of_element_located((By.ID, "add-task"))
            )
            actions.move_to_element(add_task).click().perform()
            time.sleep(3)

            title_input = WebDriverWait(browser, 10).until(
                cond.visibility_of_element_located((By.NAME, "title"))
            )
            title_input.send_keys(task["title"])
            time.sleep(3)

            if task["status"]:
                status_select = WebDriverWait(browser, 10).until(
                    cond.visibility_of_element_located((By.NAME, "status"))
                )
                status = Select(status_select)
                status.select_by_visible_text(task["status"])
                time.sleep(3)

            if task["due_date"]:
                pass

            if task["time"]:
                time_input = WebDriverWait(browser, 10).until(
                    cond.visibility_of_element_located(
                        (By.CSS_SELECTOR, "input[type=number]")
                    )
                )
                time_input.send_keys(task["time"])
                time.sleep(3)

            if task["detail"]:
                detail_input = WebDriverWait(browser, 10).until(
                    cond.visibility_of_element_located((By.NAME, "details"))
                )
                detail_input.send_keys(task["detail"])
                time.sleep(3)

            create_tb = browser.find_element(By.ID, "create-task-btn")
            actions.move_to_element(create_tb).click().perform()
            time.sleep(3)


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
        cond.visibility_of_element_located((By.CSS_SELECTOR, "input[type=password]"))
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
    StudentTests().test_create_tasks(
        "a",
        [
            {
                "title": "do stuff",
                "status": "In Progress",
                "due_date": "",
                "time": "4",
                "detail": "yay",
            }
        ],
    )

    print("eol")
    while True:
        pass
