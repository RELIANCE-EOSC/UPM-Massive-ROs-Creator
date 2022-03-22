import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time


domain = ""
field = ""
subfield = ""
description_keywords = []
categories = ["Experiment", "Observation", "Model", "Simulation", "Software", "Image"]
#Here you should enter your local chromedriver location
PATH = r'Your local ChromeDriver'
driver = webdriver.Chrome(PATH)
link = "https://archive.sigma2.no/pages/public/search.jsf"

driver.get(link)
time.sleep(1)
advanced_search = driver.find_element_by_id("searchForm:j_idt59:header:inactive")
advanced_search.click()
time.sleep(1)
#driver.get(link)
#Add domain
if (not domain==""):
	domain_menu = Select(driver.find_element_by_id("searchForm:domainMenu"))
	domain_menu.select_by_visible_text(domain)
	time.sleep(0.5)

#Add field
if (not field==""):
	field_menu = Select(driver.find_element_by_id("searchForm:fieldMenu"))
	field_menu.select_by_visible_text(field)
	time.sleep(0.5)

#Add subfield
if (not subfield==""):
	subfield_menu = Select(driver.find_element_by_id("searchForm:subfieldMenu"))
	subfield_menu.select_by_visible_text(subfield)
list_of_ids = {}

#Add description
if (not len(description_keywords)==0):
	for description in description_keywords:	

		for category in categories:
			driver.get(link)
			time.sleep(1)
			
			description_input = driver.find_element_by_name("searchForm:j_idt86")
			description_input.clear()
			description_input.send_keys(description)
			category_menu = Select(driver.find_element_by_xpath("""//*[@id="searchForm:categoryMenu"]"""))
			category_menu.select_by_visible_text(category)
			#excute query
			search_button = driver.find_element_by_name("searchForm:j_idt318").click()
			list_per_category = []
			#scrape list
			try:
				content = driver.find_element_by_id("searchresult-section")
				list_of_content = content.find_elements_by_class_name("rf-edt-c-cnt")
			except:
				NoSuchElementException: print ("There is no results for your search for "+description+ " in "+category)
				continue
				
			for i in range (0, len(list_of_content),5):
				list_of_content[i] = list_of_content[i].get_attribute("innerHTML")
				list_of_content[i+2] = list_of_content[i+2].get_attribute("innerHTML")

				
				list_of_content[i] = list_of_content[i][list_of_content[i].find(""";">""")+3:list_of_content[i].find(""";">""")+22]
				list_of_content[i+2] = list_of_content[i+2][list_of_content[i+2].find(""";">""")+3:list_of_content[i+2].find("""</a>""")]
				new_ro = {"id":list_of_content[i],"title":list_of_content[i+2]}
				#print (list_of_content[i])
				already_exists = False
				for cat in categories:
					if cat in list_of_ids and new_ro in list_of_ids[cat]:
						already_exists = True
				if not already_exists:	
					list_per_category.append(new_ro)

			page_counter = 2

			while (1):
				time.sleep(1)

				try:

					next_page = driver.find_element_by_id ("searchResultForm:j_idt61_ds_"+str(page_counter)).click()
					time.sleep(1)

					#print("breakpoint 1")
					content = driver.find_element_by_id("searchresult-section")
					list_of_content = content.find_elements_by_class_name("rf-edt-c-cnt")
					#print ("este es "+list_of_content[2].get_attribute("innerHTML"))
					for i in range (0, len(list_of_content),5):
						list_of_content[i] = list_of_content[i].get_attribute("innerHTML")
						list_of_content[i+2] = list_of_content[i+2].get_attribute("innerHTML")
						

						list_of_content[i] = list_of_content[i][list_of_content[i].find(""";">""")+3:list_of_content[i].find(""";">""")+22]
						list_of_content[i+2] = list_of_content[i+2][list_of_content[i+2].find(""";">""")+3:list_of_content[i+2].find("""</a>""")]
						#print (list_of_content[i+2])
						#print (list_of_content[i])
						new_ro = {"id":list_of_content[i],"title":list_of_content[i+2]}
						#print (list_of_content[i])

						already_exists = False
						for cat in categories:
							if cat in list_of_ids and new_ro in list_of_ids[cat]:
								already_exists = True
						if not already_exists:	
							list_per_category.append(new_ro)

					page_counter+=1
					#print ("este es "+list_of_content[2])

				except:
					NoSuchElementException:	print ("Please wait while the webpage is being scraped...")
					if category in list_of_ids.keys():
						for resource in list_per_category:
							if not resource in list_of_ids.get(category):
								list_of_ids.get(category).append(resource)
						
					else:
						list_of_ids[category]=list_per_category
					break

else:
	for category in categories:
			driver.get(link)
			time.sleep(1)
			
			category_menu = Select(driver.find_element_by_xpath("""//*[@id="searchForm:categoryMenu"]"""))
			category_menu.select_by_visible_text(category)
			#excute query
			search_button = driver.find_element_by_name("searchForm:j_idt318").click()
			list_per_category = []
			#scrape list
			try:
				content = driver.find_element_by_id("searchresult-section")
				list_of_content = content.find_elements_by_class_name("rf-edt-c-cnt")
			except:
				NoSuchElementException: print ("There is no results for your search in " +category+". Please modify your enteries and try again")
				continue
				
			for i in range (0, len(list_of_content),5):
				list_of_content[i] = list_of_content[i].get_attribute("innerHTML")
				list_of_content[i+2] = list_of_content[i+2].get_attribute("innerHTML")

				
				list_of_content[i] = list_of_content[i][list_of_content[i].find(""";">""")+3:list_of_content[i].find(""";">""")+22]
				list_of_content[i+2] = list_of_content[i+2][list_of_content[i+2].find(""";">""")+3:list_of_content[i+2].find("""</a>""")]
				new_ro = {"id":list_of_content[i],"title":list_of_content[i+2]}
				#print (list_of_content[i])
				already_exists = False
				for cat in categories:
					if cat in list_of_ids and new_ro in list_of_ids[cat]:
						already_exists = True
				if not already_exists:	
					list_per_category.append(new_ro)

			page_counter = 2

			while (1):
				time.sleep(1)

				try:

					next_page = driver.find_element_by_id ("searchResultForm:j_idt61_ds_"+str(page_counter)).click()
					time.sleep(1)

					#print("breakpoint 1")
					content = driver.find_element_by_id("searchresult-section")
					list_of_content = content.find_elements_by_class_name("rf-edt-c-cnt")
					#print ("este es "+list_of_content[2].get_attribute("innerHTML"))
					for i in range (0, len(list_of_content),5):
						list_of_content[i] = list_of_content[i].get_attribute("innerHTML")
						list_of_content[i+2] = list_of_content[i+2].get_attribute("innerHTML")
						

						list_of_content[i] = list_of_content[i][list_of_content[i].find(""";">""")+3:list_of_content[i].find(""";">""")+22]
						list_of_content[i+2] = list_of_content[i+2][list_of_content[i+2].find(""";">""")+3:list_of_content[i+2].find("""</a>""")]
						#print (list_of_content[i+2])
						#print (list_of_content[i])
						new_ro = {"id":list_of_content[i],"title":list_of_content[i+2]}
						#print (list_of_content[i])
						already_exists = False
						for cat in categories:
							if cat in list_of_ids and new_ro in list_of_ids[cat]:
								already_exists = True
						if not already_exists:	
							list_per_category.append(new_ro)

					page_counter+=1
					#print ("este es "+list_of_content[2])

				except:
					NoSuchElementException:	print ("Please wait while the webpage is being scraped...")
					if category in list_of_ids.keys():
						for resource in list_per_category:
							if not resource in list_of_ids.get(category):
								list_of_ids.get(category).append(resource)
						
					else:
						list_of_ids[category]=list_per_category
					break
					
					
print(len(list_of_ids.get("Experiment")))
print(len(list_of_ids.get("Image")))
print(len(list_of_ids.get("Model")))
print(len(list_of_ids.get("Observation")))
print(len(list_of_ids.get("Simulation")))

f = open("Massive-ROs-Creator\ToScrape.json", "w")
f.write(json.dumps(list_of_ids, indent=4, sort_keys=True))
f.close()
driver.quit()
print("Your querey was excuted correctly and information was saved")
exit()




#list_of_content[i].find("</a")
#####################ESTA ES UNA PRUEBA PARA SACAR MÁS DATOS DE LA LISTA######################
#for i in range (0, len(list_of_content)):
#	list_of_content[i] = list_of_content[i].get_attribute("innerHTML")
###
###	list_of_content[i] = list_of_content[i][list_of_content[i].find(""";">""")+3:list_of_content[i].find("</a")]
###	
##for i in range (0, len(list_of_content),5)
#	list	


#print (list_of_content[0].get_attribute("innerHTML"))
#list_of_content = list_of_content.find_elements_by_tag_name("a")

#selection = domain_menu.find_element_by_link_text("Natural sciences")
#domain_menu = domain_menu.find_element_by_link_text("Not defined")

#domain_menu.send_keys(domain)
#domain_menu.send_keys(Keys.RETURN)
#driver.quit()
