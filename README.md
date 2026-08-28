# browser-toolkit

Browser Toolkit provides a single agnostic interface to interact with different browser automations libraries.


Supported automations include:
- Selenium
- Playwright
- Camoufox (Via Playwright implementation)
- Pydoll

Features that currently browser-toolkit can offer:

- **Async First**
- **More legible automation code**
- **Abstractions of browsers methods**
- **Helpful tools to use when interacting with browsers**



## Install
```
# Pip
pip install browser-toolkit

# Uv
uv add browser-toolkit

# Poetry
poetry add browser-toolkit
```

## Basic
```python
from playwright.async_api import async_playwright
from browser_toolkit.playwright import PlaywrightTollKit
import asyncio

async def main():
    # Create an instance
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Pass instance to BrowserToolKit
        btk = PlaywrightTollKit(browser=browser, page=page)
        
        # Navigate to a website
        await btk.goto('https://www.example.com')
        
        # Create a selector
        se_class = '.class1'
        
        # Use BrowserToolKit to find a web element
        web_element = await btk.selector(selector=se_class)
    
        # With returned web_element use click() method
        await web_element.click()
        
        # Or you can click directly with BrowserToolKit
        await btk.click(selector=se_class)
        
        # close instance with BrowserToolKit
        await btk.close()

if __name__ == "__main__":
    asyncio.run(main())
```


## Methods Supported per Browser Automation Library:

BaseWebElement:

| Method | Pydoll | Selenium | Playwright | Camoufox | Description |
|---|:---:|:---:|:---:|:---:|---|
| `get_text` | ✅ | ✅ | ✅ | ✅ | Gets the element's text |
| `get_attribute` | ✅ | ✅ | ✅ | ✅ | Gets an attribute value |
| `get_position` | ✅ | ✅ | ✅ | ✅ | Gets the element's bounding box |
| `click` | ✅ | ✅ | ✅ | ✅ | Clicks the element |
| `click_js` | ✅ | ✅ | ✅ | ✅ | Clicks via JavaScript |
| `type` | ✅ | ✅ | ✅ | ✅ | Types text into the element |
| `clear` | ✅ | ✅ | ✅ | ✅ | Clears the element |
| `query` | ✅ | ✅ | ✅ | ✅ | Finds the first matching child element |
| `query_all` | ✅ | ✅ | ✅ | ✅ | Finds all matching child elements |


BaseBrowserToolkit:

| Category | Method | Pydoll | Selenium | Playwright | Camoufox | Description |
|---|---|:---:|:---:|:---:|:---:|---|
| Session management | `close_page` | ✅ | ✅ | ✅ | ✅ | Closes the current tab |
| Session management | `close_browser` | ✅ | ✅ | ✅ | ✅ | Closes the browser and all tabs |
| Selectors | `query` | ✅ | ✅ | ✅ | ✅ | Finds the first matching element |
| Selectors | `query_all` | ✅ | ✅ | ✅ | ✅ | Finds all matching elements |
| Actions | `goto` | ✅ | ✅ | ✅ | ✅ | Navigates to a URL |
| Actions | `click` | ✅ | ✅ | ✅ | ✅ | Clicks an element |
| Actions | `click_js` | ✅ | ✅ | ✅ | ✅ | Clicks an element via JavaScript |
| Actions | `type` | ✅ | ✅ | ✅ | ✅ | Types text into an element |
| Actions | `clear` | ✅ | ✅ | ✅ | ✅ | Clears an element |
| Actions | `scroll_to_element` | ✅ | ✅ | ✅ | ✅ | Scrolls to an element |
| Actions | `scroll_to_top` | ✅ | ✅ | ✅ | ✅ | Scrolls to the top of the page |
| Actions | `scroll_to_bottom` | ✅ | ✅ | ✅ | ✅ | Scrolls to the bottom of the page |
| Actions | `reload` | ✅ | ✅ | ✅ | ✅ | Reloads the page |
| Actions | `hard_reload` | ✅ | ✅ | ✅ | ✅ | Reloads the page ignoring cache |
| Page data | `current_url` | ✅ | ✅ | ✅ | ✅ | Gets the current URL |
| Page data | `title` | ✅ | ✅ | ✅ | ✅ | Gets the page title |
| Page data | `page_source` | ✅ | ✅ | ✅ | ✅ | Gets the page's HTML source |
| Page data | `get_text` | ✅ | ✅ | ✅ | ✅ | Gets an element's text |
| Page data | `get_attribute` | ✅ | ✅ | ✅ | ✅ | Gets an element's attribute value |
| Page data | `save_screenshot` | ✅ | ✅ | ✅ | ✅ | Saves a screenshot of the page |
| Network | `get_network_requests` | ✅ | ✅ | ✅ | ✅ | Gets all network requests |
| Network | `get_network_response_body` | ✅ | ✅ | ❌ | ❌ | Gets a request's response body |
| Scripts | `execute_script` | ✅ | ✅ | ✅ | ✅ | Runs JavaScript on the page |
| Scripts | `execute_cdp_cmd` | ❌ | ✅ | ✅ | ✅ | Runs a Chrome DevTools Protocol command |
| Wait | `element_is_present` | ✅ | ✅ | ✅ | ✅ | Waits for an element to exist |
| Wait | `element_is_visible` | ✅ | ✅ | ✅ | ✅ | Waits for an element to be visible |
| Wait | `element_is_invisible` | ✅ | ✅ | ✅ | ✅ | Waits for an element to be invisible |
| Wait | `element_is_clickable` | ✅ | ✅ | ✅ | ✅ | Waits for an element to be clickable |
| Wait | `text_is_present` | ✅ | ✅ | ✅ | ✅ | Waits for text inside an element |
| Wait | `alert_is_present` | ❌ | ✅ | ✅ | ✅ | Waits for a browser alert |
| Wait | `page_is_loading` | ✅ | ✅ | ✅ | ✅ | Checks if the page is still loading |
| Session data | `get_all_cookies` | ✅ | ✅ | ✅ | ✅ | Gets all cookies |
| Session data | `add_cookie` | ✅ | ✅ | ✅ | ✅ | Adds a cookie |
| Session data | `delete_all_cookies` | ✅ | ✅ | ✅ | ✅ | Deletes all cookies |
| Session data | `delete_cookie_by_name` | ❌ | ✅ | ✅ | ✅ | Deletes a cookie by name |
| Session data | `delete_cookie_filter` | ❌ | ✅ | ✅ | ✅ | Deletes cookies matching filters |
| Session data | `get_all_local_storage` | ✅ | ✅ | ✅ | ✅ | Gets all local storage items |

