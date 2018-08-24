from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import threading
import os


def execution():
    #for domain_name in list1:
        try:
            driver = webdriver.Firefox()

            #domain is indiaralinfo.com/trains
            driver.get("http://indiarailinfo.com/trains")

            #finding dropdown list for railway zone in element
            element=driver.find_elements_by_xpath("//select[@style='color:#0000CC;border:1px solid #0000CC;']")
            #options contain all the elements for dropdown list for railways zone
            options=element[0].find_elements_by_tag_name("option")

            for i in range(1,len(options)):
                #print "hello"
                print "zone option is",options[i].text
                options[i].click()
                try:
                    table_element=driver.find_element_by_xpath("//table[@class='srhres']")
                    table_element_child=table_element.find_element_by_tag_name("tbody")
                    table_rows=table_element_child.find_elements_by_tag_name("tr")
                    for row in table_rows:
                        #printing each row of table
                        print row.text


                except:
                     pass

                #run for each type of trains category as element1 contains train elements
                element1=driver.find_elements_by_xpath("//select[@style='color:#0000CC;border:1px solid #0000CC;']")
                train_element=element1[1].find_elements_by_tag_name("option")
                #print element_train_type.text
                #print len(train_options)
                for j in range(1,len(train_element)):
                    print "train option is\n",train_element[j].text
                    train_element[j].click()
                    try:
                        table_element1=driver.find_element_by_xpath("//table[@class='srhres']")
                        table_element_child1=table_element1.find_element_by_tag_name("tbody")
                        table_rows1=table_element_child1.find_elements_by_tag_name("tr")
                        for row in table_rows1:
                            #printing each row
                            print row.text

                    except:
                        pass

                    element1=driver.find_elements_by_xpath("//select[@style='color:#0000CC;border:1px solid #0000CC;']")
                    train_element=element1[1].find_elements_by_tag_name("option")

                #movind to next element again
                print "next element started"
                element=driver.find_elements_by_xpath("//select[@style='color:#0000CC;border:1px solid #0000CC;']")
                    #print element.text,"\n"
                options=element[0].find_elements_by_tag_name("option")
                #break
                #time.sleep(2)
            driver.quit()
        except:
            pass

#function which executes
execution()