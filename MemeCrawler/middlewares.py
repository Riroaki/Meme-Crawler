from random import choice, random
from time import sleep
import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from .settings import UA_LIST, DRIVER_PATH, TIMEOUT, POLL_FREQUENCY, \
    RANDOM_SLEEP_BASE
from .logger import logger


class RandomUserAgentMiddlware(object):
    """Modify random user-agent each request."""

    def __init__(self, _):
        super(RandomUserAgentMiddlware, self).__init__()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    @staticmethod
    def process_request(request, spider):
        _ = spider  # Use this to silent warning
        # Change User-Agent
        if len(UA_LIST) > 0:
            new_ua = choice(UA_LIST)
            request.headers['User-Agent'] = new_ua


class SeleniumMiddleware(object):
    """Middleware of browsing pages by selenium."""

    def __init__(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        # Set window size and position
        driver.set_window_position(0, 0)
        driver.set_window_size(1400, 1000)
        # Set timeout parameters
        driver.set_page_load_timeout(TIMEOUT)
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=TIMEOUT,
                                  poll_frequency=POLL_FREQUENCY)
        logger.info('Selenium driver is starting...')

    def __del__(self):
        if self.driver is not None:
            self.driver.close()

    def process_request(self, request: scrapy.Request,
                        spider: scrapy.Spider) -> HtmlResponse:
        _ = spider
        try:
            self.driver.get(request.url)
            # Use random sleep
            sleep(random() * RANDOM_SLEEP_BASE)
            # 404 not found
            if self.driver.page_source.count('这个页面找不到了') > 0:
                response = HtmlResponse(url=request.url,
                                        request=request,
                                        status=404)
            # 200 success
            # Moss CAPTCHA
            elif self.driver.page_source.count('hello moss') > 0:
                # You can try manually do the CAPTCHA
                sleep(10)
                # Jiki will be closed
                response = HtmlResponse(url=request.url,
                                        body=self.driver.page_source,
                                        request=request,
                                        encoding='utf-8',
                                        status=200)
            else:
                # Get item height
                card = self.wait.until(
                    expected_conditions.presence_of_element_located(
                        (By.CSS_SELECTOR, '.full-card')))
                height = card.size['height']
                # Scroll page
                scroll = ('var q=document.documentElement'
                          '.scrollTop={};').format(height * random())
                self.driver.execute_script(scroll)
                # Click comment button
                comment = self.wait.until(
                    expected_conditions.element_to_be_clickable(
                        (By.CSS_SELECTOR, '.comment')))
                comment.click()
                response = HtmlResponse(url=request.url,
                                        body=self.driver.page_source,
                                        request=request,
                                        encoding='utf-8',
                                        status=200)
        except TimeoutException as e:
            logger.warning(e)
            response = HtmlResponse(url=request.url,
                                    request=request,
                                    status=500)
        except Exception as e:
            logger.warning(e)
            response = HtmlResponse(url=request.url,
                                    request=request,
                                    status=404)
        # Use random sleep after comments are shown
        sleep(random() * RANDOM_SLEEP_BASE)
        return response

    @classmethod
    def from_crawler(cls, crawler):
        _ = crawler  # Use this line to silent warning
        return cls()
