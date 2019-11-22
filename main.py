from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from private import *

driver = webdriver.Chrome("./chromedriver")
wait_time_max = WebDriverWait(driver, 300)

product_id = ""
product_price = ""
product_title = ""
product_description = ""

run_count = 0

def main():
	print("Start time : %dsec"%((int)(time_end-time_start)))
	time_start = time.time()
	product_list = []
	product_list = get_csv_data()
	for product in product_list :
		if product[0] == "Product ID" :
			print ("CSV Load complete")
			continue
		pid = product[0]
		price = product[6]
		title = product[4].split("; ",3)[1]
		description = product[4].split("; ",3)[2]
		set_product_data(pid, price, title, description)
		run()
	time_end = time.time()
	print("All jobs are done : %dsec"%((int)(time_end-time_start)))
	

def set_product_data(pid, price, title, description):
	global product_id
	global product_price
	global product_title
	global product_description

	product_id = pid
	product_price = price
	product_title = title
	product_description = description

def get_csv_data():
	list_from_csv = []
	with open("./" + iap_product_csv) as csvfile:
		reader = csv.reader(csvfile)
		list_from_csv = list(reader)
	return list_from_csv


def run():
	global run_count
	init()
	if run_count == 0 :
		pause(message="Please login manually & press ENTER in console") #login manually
	create_add_on()
	submmit_add_on()
	run_count += 1

def init():
	driver.get("https://partner.microsoft.com/ko-kr/dashboard/products/" + app_id + "/addons")
	d_wait()

def create_add_on():
	d_wait()
	#Button : Create a new add-on
	d_click(xpath='//*[@id="pageMainContent"]/div/div/ng-component/div/iaps/section/div/iap-list/div/div/section/div/div[1]/div[1]/div/a')
	#Radio : Developer-managed consumable
	d_click(xpath='//*[@id="pageMainContent"]/div/div/ng-component/form/section[1]/div/div[1]/label/span')
	#Input : Product ID
	d_input("productId", product_id)
	print("product_id(sku) : %s" %product_id)

def submmit_add_on():
	d_wait()	
	#Button : Create add-on
	d_click(xpath='//*[@id="pageMainContent"]/div/div/ng-component/form/div/button')
	#Button : Start your submission
	d_click(xpath='//*[@id="pageMainContent"]/div/div/ng-component/div/product-overview/submission-list/div/div/section/div/div[1]/div/button')
	submission_save_property()
	submission_save_pricing()
	submission_store_listings()
	d_wait(20)
	#Button : Submit to the Store
	d_click_id(cid='submitButton')
	print("[COMPLETE] submmit_add_on : %s" %product_id)


def submission_save_property():
	print("[START] submission_save_property")
	d_wait()
	#Radio : Properties
	d_click(xpath='//*[@id="appSubmissionAppPropertiesLink"]')
	d_wait()
	time.sleep(1)
	#Dropdown : Content type - Online data storage/services
	d_click(xpath='//*[@id="ContentType"]//option[@value="OnlineDataStorage"]')
	#Input : Privacy policy URL%d
	d_input("PrivatePolicyUrl", privacy_policy_url)
	#Radio : Support Info - YES
	d_click(xpath='//*[@id="privacypolicy_yes"]')
	#Button : Save
	d_click(xpath='//*[@id="idFormCategory"]/div[2]/div/button')
	print("[DONE] submission_save_property")

def submission_save_pricing():
	print("[START] submission_save_pricing")
	d_wait()
	#Radio : Pricing and availability
	d_click(xpath='//*[@id="Availability"]/div/div/div[1]/a/h3')
	d_wait()
	time.sleep(1)
	#Radio : Visibility - Hidden in the Microsoft Store
	d_click(xpath='//*[@id="visibility-selection"]/div[2]/div[2]/div[2]/label/span')
	#Dropdown : Pricing - Base price
	xpath_price = '//*[@id="idPrice"]/div[1]/div[1]/div/div[1]/select//option[@label="' + product_price + ' USD"]'
	print("xpath_price : " + xpath_price)
	d_click(xpath=xpath_price)
	#Button : Selecet markets for base price override
	d_click(xpath='//*[@id="idPrice"]/div[3]/button')
	#Button : Market selection - Select all
	d_click(xpath='/html/body/div[3]/div[1]/div[2]/ng-view/div[5]/price/section/div/div[4]/div[2]/div/div/div/div[2]/div[2]/div[1]/a[1]/span[1]')
	#Button : Create
	d_click(xpath='/html/body/div[3]/div[1]/div[2]/ng-view/div[5]/price/section/div/div[4]/div[2]/div/div/div/div[3]/button[1]')
	time.sleep(1)
	#Button : Pricing - Remove 242 markets
	d_click(xpath='//*[@id="idPrice"]/div[2]/div[1]/div/div[3]/a')
	#Button : Save draft
	d_click_id(cid='saveButtonPricing')
	print("[DONE] submission_save_pricing")

def submission_store_listings():
	print("[START] submission_save_listings")
	d_wait()
	#Button : Store listings - Add/remove langueages
	d_click_id(cid='appSubmissionAppDescription_ManageLanguages')
	d_wait()
	time.sleep(1)
	#Button : Manage languages
	d_click_id(cid='languageModalLink')
	#Checkbox : English
	d_click_id(cid='checkbox_1')
	#Button : Update
	d_click_id(cid='updateLangsButton')
	time.sleep(1)
	#Button : Save
	d_click_id(cid='manageLanguagesSave')
	#Button : English
	#d_click(xpath='//*[@id="appSubmissionAppDescription_English"]')
	d_click(xpath='//*[@id="appSubmissionAppDescription_영어"]')
	d_wait()
	time.sleep(1)
	#Input : Title
	d_input("Title", product_title)
	print("Title : %s" %product_title)
	#Input : Description
	d_input("Description", product_description)
	#Button : Save
	d_click_id(cid='iapSaveButtonDescription')
	print("[DONE] submission_save_listings")



# Function for selenium command or some actions

def d_input(name, value):
	time.sleep(0.01)
	d_wait_name(name)
	driver.find_element_by_name(name).send_keys(value)

def d_click_id(cid = ''):
	time.sleep(0.01)
	d_wait_id(cid)
	wait_sec = 0
	max_sec = 30
	while (wait_sec < max_sec) :
		try:
			driver.find_element_by_id(cid).click()
			break
		except Exception as ec:
			print("Fail to click [%s] (%d/%d) %s" %(cid,(wait_sec+1), max_sec, ec))
			time.sleep(1)
			wait_sec += 1

def d_click(xpath = ''):
	time.sleep(0.01)
	d_wait_xpath(xpath)
	wait_sec = 0
	max_sec = 30
	while (wait_sec < max_sec) :
		try:
			driver.find_element_by_xpath(xpath).click()
			break
		except Exception as ec:
			print("Fail to click [%s] (%d/%d) %s" %(xpath,(wait_sec+1), max_sec, ec))
			time.sleep(1)
			wait_sec += 1

def d_wait(sec = 10):
	driver.implicitly_wait(sec)

def d_wait_name(value):
	try:
		element = wait_time_max.until(EC.presence_of_element_located((By.NAME, value)))
	except:
		print("*** TIME OUT : " + value)
	d_wait(2)


def d_wait_id(value):
	try:
		element = wait_time_max.until(EC.element_to_be_clickable((By.ID, value)))
	except:
		print("*** TIME OUT : " + value)
	d_wait(2)


def d_wait_xpath(value):
	try:
		element = wait_time_max.until(EC.element_to_be_clickable((By.XPATH, value)))
	except:
		print("*** TIME OUT : " + value)
	d_wait(2)



def pause(message = "Press ENTER in console to next step"):
	input(message)




main()