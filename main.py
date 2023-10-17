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


def listener(test, message):
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


def makeaccount():
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
    select.select_by_index(12)

    select_element = driver.find_element(By.ID, 'BirthMonth')
    select = Select(select_element)
    select.select_by_index(9)

    year = driver.find_element(By.ID, "BirthYear")
    year.send_keys("2001")
    ActionChains(driver)\
        .send_keys(Keys.RETURN)\
        .perform()
    test.start(lambda message: listener(test, message))
    print("\nWaiting for new emails...")

    emailandpass = test.address + ":" + passwordgen
    print("Added account details to accounts.txt")
    with open("accounts.txt", "a") as file:
        file.write(emailandpass + "\n")

    while True:
        time.sleep(1)


driver = webdriver.Chrome()
driver.get(r"https://www.xbox.com/en-US/auth/msa?action=logIn&returnUrl=https%3A%2F%2Fwww.xbox.com%2Fen-US%2F&ru=https%3A%2F%2Fwww.xbox.com%2Fen-US%2F")
title = driver.title

time.sleep(2)

if driver.title == "Sign in to your Microsoft account":
    print("Loaded page")
    driver.find_element(By.ID, "signup").click()
    WebDriverWait(driver, 10).until(EC.title_is("Create account"))
    if driver.title == "Create account":
        makeaccount()
else:
    print("Page not loaded correctly")
