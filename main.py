import os
import json
import time
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

# TODO: move to config
TIMEDELTA_IN_DAYS = 6


def main():
    start_time = time.time()

    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    init_url = os.getenv("INIT_URL")
    config = json.loads(os.getenv("CONFIG_JSON"))

    today = datetime.today()
    day_of_the_week = today.strftime("%A")
    print(f"Today is: {today}")
    print(f"Day of the week: {day_of_the_week}")

    class_date = (today + timedelta(days=TIMEDELTA_IN_DAYS))

    class_date_format_1 = class_date.strftime("%Y-%m-%d")
    class_date_format_2 = class_date.strftime("%-d %b %Y")
    class_date_format_3 = class_date.strftime("%A %-d %B")

    print(f"Date: {class_date_format_1}; {class_date_format_2}; {class_date_format_3}")

    classnames = config["day_of_the_week"]
    for classname in classnames:
        print(f"Classname: {classname}")

        for hour in classnames[classname]:
            print(f"Hour: {hour}")

            with sync_playwright() as p:
                for browser_type in [p.chromium]:
                    browser = browser_type.launch()
                    page = browser.new_page()
                    page.goto(init_url)

                    page.wait_for_selector("#login_step_login_username")

                    page.fill("#login_step_login_username", email)

                    page.click("#login_step_login_submit")

                    page.wait_for_selector("#_password")

                    page.fill("#_password", password)

                    page.click("#submit")

                    page.wait_for_selector("button[value='1']")

                    page.click("button[value='1']")

                    page.click(f"button[value='{class_date_format_1}']")

                    page.wait_for_selector(f"ul:has-text('{class_date_format_2}') div.MuiGrid-root:has-text('{class_date_format_3}') div:has-text('{classname}') button:has-text('Book')")

                    page.click(f"ul:has-text('{class_date_format_2}') div.MuiGrid-root:has-text('{class_date_format_3}') div:has-text('{classname}') button:has-text('Book')")

                    browser.close()

    finish_time = time.time()
    print(f"It took {finish_time - start_time}.")


if __name__ == "__main__":
    main()
