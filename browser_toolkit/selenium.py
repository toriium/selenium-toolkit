import json
import time
from typing import Self, Any, Union
from http.cookies import SimpleCookie

from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver, WebElement

from browser_toolkit.base_toolkit import BaseBrowserToolkit, BaseWebElement
from browser_toolkit.types import Cookie, BoundingBox, Request, RequestType, Redirect
from browser_toolkit.selenium_toolkit.utils import create_locator


class SeleniumWebElement(BaseWebElement):
    def __init__(self, web_element: WebElement):
        self.web_element = web_element

    async def get_text(self) -> str:
        """
        Gets the text from the element

        :return: str - text of the element
        """
        return self.web_element.text

    async def get_attribute(self, attribute: str) -> str | None:
        """
        Gets the attribute from the element

        :param attribute: string - attribute name
        :return: str - attribute of the element
        """
        return self.web_element.get_attribute(attribute)

    async def get_position(self) -> BoundingBox:
        """
        Gets the position of the element

        :return: BoundingBox - position of the element
        """
        rect = self.web_element.rect
        return BoundingBox(
            x=rect["x"],
            y=rect["y"],
            width=rect["width"],
            height=rect["height"],
        )

    async def click(self, hold_time: int = 0) -> None:
        """
        Clicks the element

        :param hold_time: int - time to keep the mouse button pressed in seconds (default: 0)
        :return:
        """
        self.web_element.click()

    async def click_js(self) -> None:
        """
        Clicks the element using JavaScript

        :return:
        """
        self.web_element.parent.execute_script("arguments[0].click();", self.web_element)

    async def type(self, text: str, interval: float | int = 0, clear_before: bool = False) -> None:
        """
        Fills the element with the text

        :param text: string - text to fill
        :param interval: float or int - time to wait in seconds between each character
        :param clear_before: bool - whether to clear the field before filling
        :return:
        """
        if clear_before:
            await self.clear()

        if interval:
            for character in text:
                self.web_element.send_keys(character)
                time.sleep(interval)
        else:
            self.web_element.send_keys(text)

    async def clear(self) -> None:
        """
        Clears the element

        :return:
        """
        self.web_element.clear()

    async def query(self, selector: str) -> Self | None:
        """
        Queries the web_element and returns the first element matching the selector.
        :param selector:
        :return:
        """
        try:
            if selector[0] == "/":
                element = self.web_element.find_element(By.XPATH, selector)
            else:
                element = self.web_element.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            return None
        return SeleniumWebElement(web_element=element)

    async def query_all(self, selector: str) -> list[Self]:
        """
        Queries the web_element and returns all elements matching the selector.
        :param selector:
        :return:
        """
        if selector[0] == "/":
            elements = self.web_element.find_elements(By.XPATH, selector)
        else:
            elements = self.web_element.find_elements(By.CSS_SELECTOR, selector)
        return [SeleniumWebElement(web_element=element) for element in elements]


class SeleniumToolKit(BaseBrowserToolkit):
    def __init__(self, driver: Union[WebDriver, ChromiumDriver], *args, **kwargs):
        self.driver: Union[WebDriver, ChromiumDriver] = driver

    def _find_element(self, selector: str) -> WebElement:
        if selector[0] == "/":
            return self.driver.find_element(By.XPATH, selector)
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    # --------------------------- START session management ---------------------------

    async def close_page(self) -> None:
        """
        Closes the browser tab
        :return:
        """
        self.driver.close()

    async def close_browser(self) -> None:
        """
        Closes the browser process and all its pages
        :return:
        """
        self.driver.quit()

    # --------------------------- END session management ---------------------------

    # --------------------------- START selectors ---------------------------

    async def query(self, selector: str) -> BaseWebElement | None:
        """
        Queries the page and returns the first element matching the selector.
        :param selector:
        :return: BaseWebElement | None
        """
        try:
            if selector[0] == "/":
                element = self.driver.find_element(By.XPATH, selector)
            else:
                element =  self.driver.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            return None
        return SeleniumWebElement(web_element=element)

    async def query_all(self, selector: str) -> list[BaseWebElement]:
        """
        Queries the page and returns all elements matching the selector.
        :param selector: str
        :return: list[BaseWebElement]
        """
        if selector[0] == "/":
            elements = self.driver.find_elements(By.XPATH, selector)
        else:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        return [SeleniumWebElement(web_element=element) for element in elements]

    # --------------------------- END selectors ---------------------------

    # --------------------------- START Actions ---------------------------

    async def goto(self, url: str, timeout: int = 30) -> None:
        """
        Navigates to URL

        :param url: url to navigate to
        :param timeout: maximum time to wait for the page to load in seconds
        :return:
        """
        self.driver.get(url)

    async def click(self, selector: str, hold_time: int = 0) -> None:
        """
        Clicks the element matching the selector

        :param selector: string - CSS selector or XPath
        :param hold_time: int - time to keep the mouse button pressed in seconds (default: 0)
        :return:
        """
        element = self._find_element(selector=selector)
        element.click()

    async def click_js(self, selector: str) -> None:
        """
        Clicks the element matching the selector using JavaScript

        :param selector: string - CSS selector or XPath
        :return:
        """
        element = self._find_element(selector=selector)
        self.driver.execute_script("arguments[0].click();", element)

    async def type(self, text: str, selector: str, interval: float | int = 0, clear_before: bool = False) -> None:
        """
        Fills the element matching the selector with the text

        :param text: string - text to fill
        :param selector: string - CSS selector or XPath
        :param interval: float or int - time to wait in seconds between each character
        :param clear_before: bool - whether to clear the field before filling
        :return:
        """
        if clear_before:
            await self.clear(selector=selector)

        element = self._find_element(selector=selector)
        if interval:
            for character in text:
                element.send_keys(character)
                time.sleep(interval)
        else:
            element.send_keys(text)

    async def clear(self, selector: str) -> None:
        """
        Clears the element matching the selector

        :param selector: string - CSS selector or XPath
        :return:
        """
        element = self._find_element(selector=selector)
        element.clear()

    async def scroll_to_element(self, selector: str) -> None:
        """
        Scrolls to the element matching the selector

        :param selector: string - CSS selector or XPath
        :return:
        """
        element = self._find_element(selector=selector)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    async def scroll_to_top(self) -> None:
        """
        Scrolls to the top of the page

        :return:
        """
        await self.execute_script(script="window.scrollTo(0, 0)")

    async def scroll_to_bottom(self) -> None:
        """
        Scrolls to the bottom of the page

        :return:
        """
        await self.execute_script(script="window.scrollTo(0, document.body.scrollHeight);")

    async def reload(self) -> None:
        """
        Reloads the page

        :return:
        """
        self.driver.refresh()

    async def hard_reload(self) -> None:
        """
        Hard reloads the page (ignoring cache)

        :return:
        """
        await self.execute_script(script="location.reload(true)")

    # --------------------------- END Actions ---------------------------

    # --------------------------- START page data ---------------------------
    @property
    async def current_url(self) -> str:
        """
        Gets the current URL

        :return: str - current URL
        """
        return self.driver.current_url

    @property
    async def title(self) -> str:
        """
        Gets the page title

        :return: str - page title
        """
        return self.driver.title

    @property
    async def page_source(self) -> str:
        """
        Gets the page source

        :return: str - page source
        """
        return self.driver.page_source

    async def get_text(self, selector: str) -> str:
        """
        Gets the text from the element matching the selector

        :param selector: string - CSS selector or XPath
        :return: str - text of the element
        """
        element = self._find_element(selector=selector)
        return element.text

    async def get_attribute(self, selector: str, attribute: str) -> str | None:
        """
        Gets the attribute from the element matching the selector

        :param selector: string - CSS selector or XPath
        :param attribute: string - attribute name
        :return: str - attribute of the element
        """
        element = self._find_element(selector=selector)
        return element.get_attribute(attribute)

    async def save_screenshot(self, file_path: str) -> None:
        """
        Takes a screenshot of the current page and saves it to the exception directory if it is set
        :param file_path:
        :return:
        """
        self.driver.save_screenshot(file_path)

    # --------------------------- END page data ---------------------------

    # --------------------------- START network ---------------------------

    async def get_network_requests(self) -> list[dict]:
        """
        Get all network Requests
        :return:
        """
        if not isinstance(self.driver, ChromiumDriver):
            raise TypeError("Your driver must be a ChromiumDriver type to use this method")

        logs_raw = self.driver.get_log("performance")
        parsed_logs = [json.loads(log["message"])["message"] for log in logs_raw]
        return parsed_logs

    async def get_network_response_body(self, request_id: str) -> str:
        """
        Gets the response body of the network request with the given request ID

        :param request_id: string - network request ID
        :return: str - response body of the network request
        """
        return await self.execute_cdp_cmd(cmd="Network.getResponseBody", params={"requestId": request_id})

    # --------------------------- END network ---------------------------

    # --------------------------- START scripts ---------------------------
    async def execute_script(self, script: str) -> Any:
        """
        Executes the JavaScript script in the context of the current page

        :param script: string - JavaScript code to execute
        :return:
        """
        return self.driver.execute_script(script)

    async def execute_cdp_cmd(self, cmd: str, params: dict) -> Any:
        """
        Executes the Chrome DevTools Protocol command in the context of the current page

        :param cmd: string - CDP command to execute
        :param params: dict - parameters for the CDP command
        :return:
        """
        # Useful for when executing CDP command in a remote driver
        resource = "/session/%s/chromium/send_command_and_get_result" % self.driver.session_id
        url = self.driver.command_executor._url + resource
        body = json.dumps({"cmd": cmd, "params": params})
        response = self.driver.command_executor._request("POST", url, body)
        return response.get("value")

    # --------------------------- END scripts ---------------------------

    # --------------------------- START wait ---------------------------
    async def element_is_present(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is present

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is present
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(create_locator(selector)))
            return True
        except TimeoutException:
            return False

    async def element_is_visible(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is visible

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is visible
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(create_locator(selector)))
            return True
        except TimeoutException:
            return False

    async def element_is_invisible(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is invisible

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is invisible
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(create_locator(selector)))
            return True
        except TimeoutException:
            return False

    async def element_is_clickable(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is clickable

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is clickable
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(create_locator(selector)))
            return True
        except TimeoutException:
            return False

    async def text_is_present(self, text: str, selector: str, timeout: int) -> bool:
        """
        Checks if the text is present in the element matching the selector

        :param text: string - text to check
        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the text is present in the element
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(create_locator(selector), text_=text)
            )
            return True
        except TimeoutException:
            return False

    async def alert_is_present(self, timeout: int, message: str) -> bool:
        """
        Checks if an alert is present

        :param timeout: int - seconds to wait for the alert
        :param message: str - alert message
        :return: bool - whether an alert is present
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present(), message=message)
            return True
        except TimeoutException:
            return False

    async def page_is_loading(self, timeout: int) -> bool:
        """
        Checks if the page is ready

        :param timeout: int - seconds to wait for the page to be ready
        :return: bool - whether the page is ready
        """
        cmd = "return document.readyState"
        if self.driver.execute_script(cmd) != "complete":
            return True
        else:
            return False

    # --------------------------- END wait ---------------------------

    # --------------------------- START session data ---------------------------
    async def get_all_cookies(self) -> list[Cookie]:
        """
        Gets all cookies
        :return: list[Cookie]
        """
        raw_cookies: list[dict] = self.driver.get_cookies()
        transformed_cookies: list[Cookie] = []
        for raw_cookie in raw_cookies:
            transformed_cookie = Cookie(
                name=raw_cookie.get("name"),
                value=raw_cookie.get("value"),
                url=raw_cookie.get("url"),
                domain=raw_cookie.get("domain"),
                path=raw_cookie.get("path"),
                expires=raw_cookie.get("expiry"),
                httpOnly=raw_cookie.get("httpOnly"),
                secure=raw_cookie.get("secure"),
                sameSite=raw_cookie.get("sameSite"),
                partitionKey=raw_cookie.get("partitionKey"),
            )
            transformed_cookies.append(transformed_cookie)

        return transformed_cookies

    async def add_cookie(self, cookie: Cookie) -> None:
        """
        Adds a cookie to the current session

        :param cookie: Cookie - cookie to add
        :return:
        """
        cookie_dict = {"name": cookie.name, "value": cookie.value}
        if cookie.domain is not None:
            cookie_dict["domain"] = cookie.domain
        if cookie.path is not None:
            cookie_dict["path"] = cookie.path
        if cookie.secure is not None:
            cookie_dict["secure"] = cookie.secure
        if cookie.httpOnly is not None:
            cookie_dict["httpOnly"] = cookie.httpOnly
        if cookie.sameSite is not None:
            cookie_dict["sameSite"] = cookie.sameSite
        if cookie.expires is not None:
            cookie_dict["expiry"] = int(cookie.expires)

        self.driver.add_cookie(cookie_dict)

    async def delete_all_cookies(self) -> None:
        """
        Deletes all cookies from the current session
        :return:
        """
        self.driver.delete_all_cookies()

    async def delete_cookie_by_name(self, name: str) -> None:
        """
        Deletes a cookie by name

        :param name: string - name of the cookie to delete
        :return:
        """
        self.driver.delete_cookie(name)

    async def delete_cookie_filter(
        self, name: str | None = None, domain: str | None = None, path: str | None = None
    ) -> None:
        """
        Deletes cookies by name, domain, and path

        :param name:
        :param domain:
        :param path:
        :return:
        """
        cookies = await self.get_all_cookies()
        for cookie in cookies:
            if name is not None and cookie.name != name:
                continue
            if domain is not None and cookie.domain != domain:
                continue
            if path is not None and cookie.path != path:
                continue
            self.driver.delete_cookie(cookie.name)

    async def get_all_local_storage(self) -> dict:
        """
        Gets all local storage
        :return: dict
        """
        script = "return Object.fromEntries(Object.entries(localStorage));"
        local_storage = self.driver.execute_script(script)
        if not isinstance(local_storage, dict):
            local_storage = {}
        return local_storage

    # --------------------------- END session data ---------------------------

    # --------------------------- START extra methods (not part of BaseBrowserToolkit) ---------------------------
    # ADJUST IMPLEMENTATION
    async def block_urls(self, urls: list) -> None:
        if not isinstance(self.driver, ChromiumDriver):
            TypeError("Your driver must be a ChromiumDriver type to use this method")

        await self.execute_cdp_cmd("Network.setBlockedURLs", {"urls": urls})
        await self.execute_cdp_cmd("Network.enable", {})

    # ADJUST IMPLEMENTATION
    def get_all_requests(self) -> list[dict]:
        """
        !!! ALERT !!!
        For this method works the code below is necessary in the driver's creation

        # selenium < 4.0
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        driver = webdriver.Chrome(desired_capabilities=capabilities

        # selenium > 4.0
        capabilities = {"performance": "ALL"}
        options.set_capability("goog:loggingPrefs", capabilities)
        """

        if not isinstance(self.driver, ChromiumDriver):
            TypeError("Your driver must be a ChromiumDriver type to use this method")

        logs_raw = self.driver.get_log("performance")
        parsed_logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
        return parsed_logs

    # ADJUST IMPLEMENTATION
    def get_requests(self, request_url: str) -> list[Request] | None:
        parsed_logs = self.get_all_requests()
        methods = [
            "Network.responseReceived",
            "Network.requestWillBeSent",
            "Network.requestWillBeSentExtraInfo",
            # "Page.windowOpen"  # I Only see in Redirect, maybe add in the future, does not have request_id
        ]
        received_response_list = [response for response in parsed_logs if response["method"] in methods]

        resp_url = None
        matched_requests_id = set()
        for response in received_response_list:
            urls_to_match = []
            params = response["params"]
            target_request_id = params.get("requestId")
            if params.get("request"):
                urls_to_match.append(params["request"]["url"])
            if params.get("response"):
                urls_to_match.append(params["response"]["url"])
            if params.get("redirectResponse"):
                urls_to_match.append(params["redirectResponse"]["url"])

            for url in urls_to_match:
                if request_url in url:
                    matched_requests_id.add(target_request_id)

        if not matched_requests_id:
            return None

        matched_requests = []
        for target_request_id in matched_requests_id:
            cookies = dict()
            headers = dict()
            url: str = None
            redirect = None
            request_type: RequestType = None
            for response in received_response_list:
                params = response["params"]
                request_id = params.get("requestId")
                method = response.get("method")

                if target_request_id == request_id:
                    if method == "Network.requestWillBeSentExtraInfo":
                        headers = params.get("headers")

                        cookies_string = headers.get("cookie")
                        if not cookies_string:
                            continue

                        cookie_parser = SimpleCookie()
                        cookie_parser.load(cookies_string)
                        cookies = dict(cookie_parser)

                    if method == "Network.requestWillBeSent":
                        url = params["request"]["url"]
                        request_type = RequestType(params["type"])

                        if params.get("redirectResponse"):
                            redirect_url = params["redirectResponse"]["url"]
                            if request_url in redirect_url:
                                redirect = Redirect(url=redirect_url)

            request_data = Request(
                url=url,
                request_id=target_request_id,
                cookies=cookies,
                headers=headers,
                redirect=redirect,
                type=request_type,
            )
            matched_requests.append(request_data)

        return matched_requests

    # ADJUST IMPLEMENTATION
    async def response_data_from_request(self, request_url: str, request_id: str = None) -> str | None:
        if request_id:
            response_body = await self.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
            return response_body

        received_requests = self.get_requests(request_url=request_url)
        if not received_requests:
            return None

        if len(received_requests) > 1:
            raise ValueError("more than one request matched")

        return await self.get_response_body_from_request_id(request_id=received_requests[0].request_id)

    # ADJUST IMPLEMENTATION
    async def get_response_body_from_request_id(self, request_id: str = None) -> str | None:
        try:
            response_body = await self.execute_cdp_cmd(cmd="Network.getResponseBody", params={"requestId": request_id})
        except WebDriverException:
            return None

        return response_body
    # --------------------------- END extra methods (not part of BaseBrowserToolkit) ---------------------------
