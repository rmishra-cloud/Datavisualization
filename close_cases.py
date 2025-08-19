import argparse
import csv
import sys
import time
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def read_ack_numbers(excel_path: str, sheet_name: str, ack_column: str) -> list:
    """
    Read acknowledgement numbers from an Excel sheet and return as a list of strings.
    """
    dataframe = pd.read_excel(excel_path, sheet_name=sheet_name)
    if ack_column not in dataframe.columns:
        raise ValueError(
            f"Column '{ack_column}' not found in sheet '{sheet_name}'. Available columns: {list(dataframe.columns)}"
        )
    ack_values = (
        dataframe[ack_column]
        .dropna()
        .astype(str)
        .map(lambda v: v.strip())
        .tolist()
    )
    return ack_values


def create_webdriver(headless: bool) -> webdriver.Chrome:
    """
    Create and return a configured Chrome WebDriver instance.
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    return driver


def maybe_login(
    driver: webdriver.Chrome,
    wait: WebDriverWait,
    do_login: bool,
    username: str | None,
    password: str | None,
    username_selector: str | None,
    password_selector: str | None,
    login_button_selector: str | None,
    post_login_wait_seconds: float,
) -> None:
    """
    Optionally perform login if selectors and credentials are provided.
    """
    if not do_login:
        return

    if not (username and password and username_selector and password_selector and login_button_selector):
        raise ValueError(
            "Login requested but username/password/selectors not fully provided."
        )

    username_el = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, username_selector)))
    username_el.clear()
    username_el.send_keys(username)

    password_el = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, password_selector)))
    password_el.clear()
    password_el.send_keys(password)

    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, login_button_selector)))
    login_btn.click()

    if post_login_wait_seconds > 0:
        time.sleep(post_login_wait_seconds)


def close_case_for_ack(
    driver: webdriver.Chrome,
    wait: WebDriverWait,
    ack_value: str,
    dry_run: bool,
    search_input_xpath: str,
    close_button_xpath: str,
    comments_textarea_xpath: str,
    submit_button_xpath: str,
    comment_text: str,
) -> str:
    """
    Attempt to close a case for a single acknowledgement number. Returns a status string.
    """
    # Enter AckNo in search box
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, search_input_xpath)))
    search_box.clear()
    search_box.send_keys(ack_value)
    search_box.send_keys(Keys.RETURN)

    # Wait for Close Case button and click
    close_button = wait.until(EC.element_to_be_clickable((By.XPATH, close_button_xpath)))
    if dry_run:
        return "DRY_RUN - would click Close Case"
    close_button.click()

    # Enter comment
    comment_box = wait.until(EC.element_to_be_clickable((By.XPATH, comments_textarea_xpath)))
    comment_box.clear()
    comment_box.send_keys(comment_text)

    # Submit
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
    submit_button.click()

    # Optionally, wait a moment for server to accept
    time.sleep(1)
    return "Closed successfully"


def main() -> int:
    parser = argparse.ArgumentParser(description="Close cases from AckNos in an Excel sheet via Selenium.")
    parser.add_argument(
        "--excel",
        required=False,
        default=str(
            Path(
                r"\\kcoverseaseducation.sharepoint.com@SSL\DavWWWRoot\sites\UKTeam\Shared Documents\KC-UK SP\UK Team\UK - Shared Services Team\Offer Team\Case Closed\Case Closure 2025\Case Closure- Offer Follow Up Sheet.xlsx"
            )
        ),
        help="Path to the Excel file (can be local path).",
    )
    parser.add_argument("--sheet", default="Sheet1", help="Excel sheet name.")
    parser.add_argument(
        "--ack-column", default="AckNo", help="Column name containing AckNos.")
    parser.add_argument(
        "--url", default="https://www.coursefinder.ai/Application", help="Target URL.")
    parser.add_argument(
        "--headless", action="store_true", help="Run Chrome in headless mode.")
    parser.add_argument(
        "--timeout", type=int, default=20, help="Explicit wait timeout in seconds.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not click Close/Submit; only exercise the flow until just before actions.",
    )
    parser.add_argument(
        "--comment",
        default="Closed - Student not interested to pay",
        help="Comment text to add when closing the case.",
    )
    parser.add_argument(
        "--search-input-xpath",
        default="//input[@placeholder='Enter AckNo']",
        help="XPath for the AckNo search input.",
    )
    parser.add_argument(
        "--close-button-xpath",
        default="//button[contains(text(),'Close Case')]",
        help="XPath for the 'Close Case' button.",
    )
    parser.add_argument(
        "--comments-textarea-xpath",
        default="//textarea[@placeholder='Enter comments']",
        help="XPath for the comments textarea.",
    )
    parser.add_argument(
        "--submit-button-xpath",
        default="//button[contains(text(),'Submit')]",
        help="XPath for the 'Submit' button.",
    )
    parser.add_argument("--do-login", action="store_true", help="Perform login before actions.")
    parser.add_argument("--username", help="Username for login (if --do-login).")
    parser.add_argument("--password", help="Password for login (if --do-login).")
    parser.add_argument(
        "--username-selector",
        help="CSS selector for username input (if --do-login).",
    )
    parser.add_argument(
        "--password-selector",
        help="CSS selector for password input (if --do-login).",
    )
    parser.add_argument(
        "--login-button-selector",
        help="CSS selector for login button (if --do-login).",
    )
    parser.add_argument(
        "--post-login-wait",
        type=float,
        default=3.0,
        help="Seconds to sleep after clicking login to allow navigation.",
    )
    parser.add_argument(
        "--results-csv",
        default=str(Path.cwd() / "close_results.csv"),
        help="Path to write the results CSV.",
    )

    args = parser.parse_args()

    excel_path = Path(args.excel)
    if not excel_path.exists():
        print(
            f"ERROR: Excel file not found at '{excel_path}'. Provide a valid local path with --excel.",
            file=sys.stderr,
        )
        return 2

    try:
        ack_numbers = read_ack_numbers(str(excel_path), args.sheet, args.ack_column)
    except Exception as exc:
        print(f"ERROR reading Excel: {exc}", file=sys.stderr)
        return 2

    if not ack_numbers:
        print("No AckNos found to process.")
        return 0

    driver = create_webdriver(args.headless)
    driver.get(args.url)
    wait = WebDriverWait(driver, args.timeout)

    # Optional login
    try:
        maybe_login(
            driver=driver,
            wait=wait,
            do_login=args.do_login,
            username=args.username,
            password=args.password,
            username_selector=args.username_selector,
            password_selector=args.password_selector,
            login_button_selector=args.login_button_selector,
            post_login_wait_seconds=args.post_login_wait,
        )
    except Exception as exc:
        driver.quit()
        print(f"ERROR during login: {exc}", file=sys.stderr)
        return 3

    results_rows: list[dict] = []

    try:
        for ack in ack_numbers:
            status = ""
            try:
                status = close_case_for_ack(
                    driver=driver,
                    wait=wait,
                    ack_value=str(ack),
                    dry_run=args.dry_run,
                    search_input_xpath=args.search_input_xpath,
                    close_button_xpath=args.close_button_xpath,
                    comments_textarea_xpath=args.comments_textarea_xpath,
                    submit_button_xpath=args.submit_button_xpath,
                    comment_text=args.comment,
                )
                print(f"AckNo {ack}: {status}")
            except Exception as exc:
                status = f"FAILED - {exc}"
                print(f"AckNo {ack}: {status}")
            results_rows.append({"AckNo": ack, "Status": status})
    finally:
        driver.quit()

    # Write results
    try:
        with open(args.results_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["AckNo", "Status"])
            writer.writeheader()
            writer.writerows(results_rows)
        print(f"Results written to {args.results_csv}")
    except Exception as exc:
        print(f"WARNING: Failed to write results CSV: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

