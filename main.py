from selenium import webdriver
from private import app_id

driver = webdriver.Chrome("./chromedriver")

def run():
	init()
	pause(message="Please login manually & press ENTER in console") #login manually
	create_add_on()

def init():
	driver.get("https://partner.microsoft.com/ko-kr/dashboard/products/" + app_id + "/addons")
	d_wait(3)

def create_add_on():
	#Button : Create a new add-on
	d_click(xpath='//*[@id="pageMainContent"]/div/div/ng-component/div/iaps/section/div/iap-list/div/div/section/div/div[1]/div[1]/div/a')
	#Radio : Developer-managed consumable
	d_click(xpath='//*[@id="pageMainContent"]/div/div/ng-component/form/section[1]/div/div[1]/label/span')
	#Input : Product ID
	d_input("productId", "com.com")
	#Button : Create add-on
	d_click(xpath='//*[@id="pageMainContent"]/div/div/ng-component/form/div/button')


# Function for selenium command or some actions

def d_input(name, value):
	driver.find_element_by_name(name).send_keys(value)

def d_click(xpath = ''):
	driver.find_element_by_xpath(xpath).click()

def d_wait(sec):
	driver.implicitly_wait(sec)

def pause(message = "Press ENTER in console to next step"):
	input(message)

run()