from selenium import webdriver #to work with website
from bs4 import BeautifulSoup #to scrap data
from selenium.webdriver.common.action_chains import ActionChains #to initiate hovering
from selenium.webdriver.common.keys import Keys #to input value

PROXY = "10.3.100.207:8080" # IP:PORT or HOST:PORT
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

#ask for input
company_name=input("tell the company name")

#import website
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get("https://www.mptax.mp.gov.in/mpvatweb/")

#perform hovering to show hovering
element_to_hover_over = browser.find_element_by_css_selector("#mainsection > form:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(3) > a:nth-child(1)")

hover = ActionChains(browser).move_to_element(element_to_hover_over)
hover.perform()

#click on dealer search from dropdown menu
browser.find_element_by_css_selector("#dropmenudiv > a:nth-child(1)").click()

#we are now on the leftmenu page

#click on radio button
browser.find_element_by_css_selector("#byName").click()

#input company name
inputElement = browser.find_element_by_css_selector("#showNameField > td:nth-child(2) > input:nth-child(1)")
inputElement.send_keys(company_name)

#submit form
inputElement.submit() 

#now we are on dealerssearch page

#scrap data
soup=BeautifulSoup(browser.page_source,"lxml")

#get the list of values we need
list=soup.find_all('td',class_="tdBlackBorder")

#check length of 'list' and on that basis decide what to print 
if(len(list)!=0):
	#company name at index=9
	#tin no. at index=10
	#registration status at index=11
	#circle name at index=15

	#store the values
	name=list[9].get_text()
	tin=list[10].get_text()
	status=list[11].get_text()
	circle=list[15].get_text()

	#make dictionary
	Company_Details={"TIN":tin ,"Firm name":name ,"Circle_Name":circle, "Registration_Status":status}

	print(Company_Details)
else:
	Company_Details={"VAT RC No":"Not found in database"}

	print(Company_Details)

#close the chrome 
browser.stop_client()
browser.close()
browser.quit()
