import os
import time
import json
import random
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import CONFIG
from xpaths import XPATHS

from mailtm import MailTM

class IMMI:
    def __init__(self) -> None:
        # self.driver = self.create_driver()
        pass

    def get_element(self, driver, XPATH: str):
        return driver.find_element(
            by=By.XPATH,
            value=XPATH,
        )

    def wait_and_find_element(self, driver, XPATH: str, timeout=100):
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    XPATH,
                )
            )
        )

        return driver.find_element(
            by=By.XPATH,
            value=XPATH,
        )
    
    def create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument(
            "--no-first-run --no-service-autorun --password-store=basic"
        )

        driver = webdriver.Chrome(options=options)

        return driver
    
    def create_mailtm(self):
        self.mailtm = MailTM()
        while True:
            try:
                domain = self.mailtm.get_domains()
                print(domain)
            except:
                time.sleep(5)
                continue
            
            email_password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890') for i in range(15))
            email_password = email_password + '!@#?'

            email_address, address_id = self.mailtm.create_account(domain, email_password)
            print(email_address)
            if email_address == False:
                time.sleep(5)
                continue

            email_user = email_address.split('@')[0]
            if email_user.isnumeric():
                continue
            else:
                break

        email_token = self.mailtm.get_token(email_address, email_password)

        return email_address, email_password, email_token
    
    def random_name(self):
        with open(CONFIG.VIETNAMESE_NAME_LIST, 'r', encoding='utf8') as f:
            names_data = json.load(f)

        random_name = random.choice(names_data)
        full_name = random_name['full_name']

        # remove vietnamese accent

        full_name = self.remove_accents(full_name)
        
        return full_name
    
    def remove_accents(self, input_str):
        s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
        s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
        s = ''
        
        for c in input_str:
            if c in s1:
                s += s0[s1.index(c)]
            else:
                s += c
        return s
    
    def random_phone_number(self):
        # create random phone number with +84
        phone_number = '+84'
        for i in range(9):
            phone_number += str(random.randint(0, 9))

        return phone_number

    def create_account(self):
        try:
            email_address, email_password, email_token = self.create_mailtm()

            self.driver = self.create_driver()
            
            self.driver.get('https://online.immi.gov.au/lusc/register')
            # input('Press any key to continue...')
            
            self.wait_and_find_element(self.driver, XPATHS.FAMILY_NAME).send_keys(self.random_name())
            self.wait_and_find_element(self.driver, XPATHS.PHONE_NUMBER).send_keys(self.random_phone_number())
            self.wait_and_find_element(self.driver, XPATHS.EMAIL_ADDRESS).send_keys(email_address)
            self.wait_and_find_element(self.driver, XPATHS.CONFIRM_EMAIL).send_keys(email_address)
            self.wait_and_find_element(self.driver, XPATHS.CONTINUE).click()

            self.wait_and_find_element(self.driver, XPATHS.PASSWORD).send_keys(email_password)
            self.wait_and_find_element(self.driver, XPATHS.RE_TYPE_PASSWORD).send_keys(email_password)
            self.wait_and_find_element(self.driver, XPATHS.QUESTION_1).click()
            self.wait_and_find_element(self.driver, XPATHS.ANSWER_1).send_keys(self.random_name())
            self.wait_and_find_element(self.driver, XPATHS.QUESTION_2).click()
            self.wait_and_find_element(self.driver, XPATHS.ANSWER_2).send_keys(self.random_name())
            self.wait_and_find_element(self.driver, XPATHS.QUESTION_3).click()
            self.wait_and_find_element(self.driver, XPATHS.ANSWER_3).send_keys(self.random_name())
            self.wait_and_find_element(self.driver, XPATHS.ACCEPT_TERMS).click()
            # input('Press any key to continue...')
            self.wait_and_find_element(self.driver, XPATHS.SECURITY_BOT).click()
            self.wait_and_find_element(self.driver, XPATHS.SUBMIT).click()

            self.wait_and_find_element(self.driver, XPATHS.CONTINUE_2).click()

            with open(CONFIG.CLONE_LIST, 'a', encoding='utf8') as f:
                f.write(f'{email_address}:{email_password}\n')

            # input('Press any key to continue...')

            self.driver.quit()

            return email_address, email_password
        except:
            self.driver.quit()
            return False, False
        

    def start_check(self, email: str, password: str):
        # try:
            self.driver = self.create_driver()
            self.driver.get('https://online.immi.gov.au/lusc/login')
            # login
            self.wait_and_find_element(self.driver, XPATHS.LOGIN_EMAIL).send_keys(email)
            self.wait_and_find_element(self.driver, XPATHS.PASSWORD).send_keys(password)
            self.wait_and_find_element(self.driver, XPATHS.LOGIN_BTN).click()
            # input('Press any key to continue...')
            self.wait_and_find_element(self.driver, XPATHS.LOGIN_CONTINUE).click()
            # input('Press any key to continue...')
            # check
            self.wait_and_find_element(self.driver, XPATHS.NEW_APPLICATION).click()
            self.driver.get('https://online.immi.gov.au/elp/app?action=new&formId=WHV-AP-462')
            # self.wait_and_find_element(self.driver, XPATHS.WORKING_HOLIDAY).click()
            # time.sleep(2)
            # self.wait_and_find_element(self.driver, XPATHS.WHV_462).click()
            self.wait_and_find_element(self.driver, XPATHS.AGREE_TERM).click()
            self.wait_and_find_element(self.driver, XPATHS.NEXT_1).click()
            self.wait_and_find_element(self.driver, XPATHS.VIETNAM_CHOICE).click()
            
            self.wait_and_find_element(self.driver, XPATHS.ACCOMPANIED_CHOICE).click()
            self.wait_and_find_element(self.driver, XPATHS.GRANTED_CHOICE).click()
            self.wait_and_find_element(self.driver, XPATHS.FIRST_WORK_CHOICE).click()
            self.wait_and_find_element(self.driver, XPATHS.BEEN_GRANRED_CHOICE).click()
            # get current date like 02 Sep 2023
            current_date = datetime.now().strftime("%d %b %Y")
            current_date = datetime.strptime(current_date, "%d %b %Y")
            current_date = current_date.replace(month=current_date.month + 3)
            current_date = current_date.strftime("%d %b %Y")
            self.wait_and_find_element(self.driver, XPATHS.DATE_2_INPUT).send_keys(current_date)
            time.sleep(2)
            self.wait_and_find_element(self.driver, XPATHS.CITIZEN_CHOICE).click()
            self.wait_and_find_element(self.driver, XPATHS.REGISTRATION_BEFORE_CHOICE).click()
            self.wait_and_find_element(self.driver, XPATHS.GOVERNMENT_SUPPORT).click()
            self.wait_and_find_element(self.driver, XPATHS.NEXT_2).click()
            input('Press any key to continue...')





    
        

if __name__ == '__main__':
    # current_date = datetime.now().strftime("%d %b %Y")
    # # plus 3 months
    # current_date = datetime.strptime(current_date, "%d %b %Y")
    # current_date = current_date.replace(month=current_date.month + 3)
    # current_date = current_date.strftime("%d %b %Y")
    # print(current_date)
    immi = IMMI()
    immi.start_check('2xhptcqax39f7na@diginey.com', 'cmatcfnfhy9xxi6!@#?')
#     immi.create_account()