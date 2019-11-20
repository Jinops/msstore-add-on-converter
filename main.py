from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from private import *

driver = webdriver.Chrome("./chromedriver")
wait_time_max = WebDriverWait(driver, 60)

product_id = "com.test.3"

def run():
	init()
	pause(message="Please login manually & press ENTER in console") #login manually
	create_add_on()
	submmit_add_on()

def init():
	driver.get("https://partner.microsoft.com/ko-kr/dashboard/products/" + app_id + "/addons")
	d_wait(3)

def create_add_on():
	#Button : Create a new add-on
	d_click(xpath='//*[@id="pageMainContent"]/div/div/ng-component/div/iaps/section/div/iap-list/div/div/section/div/div[1]/div[1]/div/a')
	#Radio : Developer-managed consumable
	d_click(xpath='//*[@id="pageMainContent"]/div/div/ng-component/form/section[1]/div/div[1]/label/span')
	#Input : Product ID
	d_input("productId", product_id)

def submmit_add_on():
	#Button : Create add-on
	d_click(xpath='//*[@id="pageMainContent"]/div/div/ng-component/form/div/button')
	#Button : Start your submission
	d_click(xpath='//*[@id="pageMainContent"]/div/div/ng-component/div/product-overview/submission-list/div/div/section/div/div[1]/div/button')
	submission_save_property()


def submission_save_property():
	#Button : Properties
	d_click(xpath='//*[@id="appSubmissionAppPropertiesLink"]')
	#Dropdown : Content type - Online data storage/services
	d_click(xpath='//*[@id="ContentType"]/option[8]')
	#Radio : Support Info - YES
	d_click(xpath='//*[@id="privacypolicy_yes"]')
	#Input : Privacy policy URL
	d_input("PrivatePolicyUrl", privacy_policy_url)
	#Button : Save
	d_click(xpath='//*[@id="idFormCategory"]/div[2]/div/button')



# Function for selenium command or some actions

def d_input(name, value):
	d_wait_name(name)
	driver.find_element_by_name(name).send_keys(value)

def d_click(xpath = ''):
	d_wait_xpath(xpath)
	driver.find_element_by_xpath(xpath).click()

def d_wait(sec):
	driver.implicitly_wait(sec)

def d_wait_name(value):
	try:
		element =wait_time_max.until(EC.presence_of_element_located((By.NAME, value)))
	except:
		print("*** TIME OUT : " + value)

def d_wait_xpath(value):
	try:
		element =wait_time_max.until(EC.element_to_be_clickable((By.XPATH, value)))
	except:
		print("*** TIME OUT : " + value)



def pause(message = "Press ENTER in console to next step"):
	input(message)

run()