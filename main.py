from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import random
import string
from mailtm import Email
import re
import time
import threading


def listener(test, message, driver):
    regex = r"\d{6}"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "VerificationCode")))
    print("Content: " + (message['text']
          if message['text'] else message['html']))
    match = re.search(regex, message['text'])
    if match:
        sec_code = match.group()
        print(f"Got security code: {sec_code} from email")
        securitycode = driver.find_element(By.ID, "VerificationCode")
        securitycode.send_keys(sec_code)
        ActionChains(driver)\
            .send_keys(Keys.RETURN)\
            .perform()

        print("do the captcha yourself :)")
        threading.Thread(target=test.stop).start()
        print("Stopped listening for emails...")
        pass
    else:
        print("Couldn't find the security code from\n" + message['text'])


def makeaccount(driver):
    test = Email()

    test.register()
    print("\nEmail Address: " + str(test.address))

    emailbox = driver.find_element(By.ID, "MemberName")
    emailbox.send_keys(test.address)
    ActionChains(driver)\
        .send_keys(Keys.RETURN)\
        .perform()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "PasswordInput")))
    passwordbox = driver.find_element(By.ID, "PasswordInput")

    characters = string.ascii_letters + string.digits
    passwordgen = ''.join(random.choice(characters) for _ in range(15))
    passwordbox.send_keys(passwordgen)
    print("Generated password: " + passwordgen)
    ActionChains(driver)\
        .send_keys(Keys.RETURN)\
        .perform()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "FirstName")))
    fname = driver.find_element(By.ID, "FirstName")
    fname.send_keys("John")
    lname = driver.find_element(By.ID, "LastName")
    lname.send_keys("Doe")
    ActionChains(driver)\
        .send_keys(Keys.RETURN)\
        .perform()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "BirthDay")))
    select_element = driver.find_element(By.ID, 'BirthDay')
    select = Select(select_element)
    select.select_by_index(random.randint(1, 28))

    select_element = driver.find_element(By.ID, 'BirthMonth')
    select = Select(select_element)
    select.select_by_index(random.randint(1, 12))

    year = driver.find_element(By.ID, "BirthYear")
    year.send_keys(str(random.randint(1905, 2004)))
    ActionChains(driver)\
        .send_keys(Keys.RETURN)\
        .perform()
    test.start(lambda message: listener(test, message, driver))
    print("\nWaiting for new emails...")

    emailandpass = test.address + ":" + passwordgen
    print("Added account details to accounts.txt")
    with open("accounts.txt", "a") as file:
        file.write(emailandpass + "\n")
    working = False
    while working == False:
        time.sleep(1)
        if driver.title == "Add security info":
            print("Change your IP to generate more accounts")
            print("Deleting this accounts information")
            with open("accounts.txt", "r") as f:
                data = f.readlines()

            with open("accounts.txt", "w") as f:

                for line in data:

                    if line.strip("\n") != emailandpass:
                        f.write(line)
                        working = True


def main():
    driver = webdriver.Chrome()
    driver.get(r"https://xbox.com")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/header/div/div/div[4]/div[2]/div/a/div/div[1]'))).click()
    if driver.title == "Sign in to your Microsoft account":
        print("Loaded page")
        driver.find_element(By.ID, "signup").click()
        WebDriverWait(driver, 10).until(EC.title_is("Create account"))
    if driver.title == "Create account":
        makeaccount(driver)
    else:
        print("Page not loaded correctly")


if __name__ == "__main__":
    main()
