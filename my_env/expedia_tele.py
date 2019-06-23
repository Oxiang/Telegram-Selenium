# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:04:02 2019

@author: xiangong
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep
import datetime
import os
from calendar import monthrange
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.options import Options

#Set up chrome bin for heroku
#chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
#opts = ChromeOptions()
#opts.binary_location = chrome_bin
#options = Options()
#options.add_argument("--headless")
#GOOGLE_CHROME_BIN = "/app/.apt/usr/bin/google-chrome"
#options.binary_location = GOOGLE_CHROME_BIN
#options.add_argument('--disable-gpu')
#options.add_argument('--no-sandbox')

#Setting origin, destination
origin_country = " Singapore"
destination_country = " Taipei"
travel_days = 6
travel_month = 8
max_extraction = 3
travel_year = 2019

#Create main dataframe
main_df = pd.DataFrame()

def initialise_page(start_date, end_date,driver):
    #switch to flight only
    flight_elem = driver.find_element_by_id("tab-flight-tab-hp")
#    page = requests.get(driver.current_url)
#    soup = BeautifulSoup(page.content, 'html.parser')
#    print(soup.prettify())
    sleep(1)
    flight_elem.click()
    print("switching to flight only tab")
    
    #Enter input
    origin_elem = driver.find_element_by_id("flight-origin-hp-flight")
    sleep(1)
    origin_elem.clear()
    sleep(1)
    origin_elem.send_keys(origin_country)
    sleep(1)
    origin_elem.send_keys(Keys.ENTER)
    sleep(1)
    print("Entered origin country")
    
    destination_elem = driver.find_element_by_id("flight-destination-hp-flight")
    sleep(1)
    destination_elem.clear()
    sleep(1)
    destination_elem.send_keys(destination_country)
    sleep(1)
    destination_elem.send_keys(Keys.ENTER)
    sleep(1)
    print("Entered destiantion country")
    
    dep_elem = driver.find_element_by_id("flight-departing-hp-flight")
    dep_elem.clear()
    dep_elem.send_keys(start_date.strftime("%d/%m/%Y"))
    print("Entered flight date of {}".format(start_date.strftime("%d/%m/%Y")))
    
    arr_elem = driver.find_element_by_id("flight-returning-hp-flight")
    for i in range(11):
            arr_elem.send_keys(Keys.BACKSPACE)
    arr_elem.send_keys(end_date.strftime("%d/%m/%Y"))
    print("Entered return date of {}".format(end_date.strftime("%d/%m/%Y")))
    
    #Search
    submit_elem = driver.find_element_by_xpath('//*[@id="gcw-flights-form-hp-flight"]/div[8]/label/button')
    submit_elem.click()
    sleep(10)
    print("Serching for results")


def single_page_extraction(start_date,end_date,driver):
    #Create dataframe
    df = pd.DataFrame()
    id_date = start_date.strftime("%d/%m/%Y")
    
    #Extract info
    try:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[@data-test-id='departure-time']")))
    finally:
        pass
    print("loaded searched result webpage for {}".format(id_date))
    #Departure date
    dep_date_list = [start_date.strftime("%d/%m/%Y") for i in range(max_extraction)]
    
    #Return date
    ret_date_list = [end_date.strftime("%d/%m/%Y") for i in range(max_extraction)]
    
    #Departure time
    dep_times = driver.find_elements_by_xpath("//span[@data-test-id='departure-time']")
    dep_times_list = [dep_times[i].text for i in range(max_extraction)]
        
    #Arrival time
    arr_times = driver.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
    arr_times_list = [arr_times[i].text for i in range(max_extraction)]
    
    #airline name
    airlines = driver.find_elements_by_xpath("//span[@data-test-id='airline-name']")
    airline_list = [airlines[i].text for i in range(max_extraction)]
    
    #Prices
    prices = driver.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
    price_list = [prices[i].text.split('$')[1] for i in range(max_extraction)]
    
    #durations
    durations = driver.find_elements_by_xpath("//span[@data-test-id='duration']")
    durations_list = [durations[i].text for i in range(max_extraction)]
    
    #stops
    stops = driver.find_elements_by_xpath("//span[@class='number-stops']")
    stops_list = [stops[i].text for i in range(max_extraction)]
    
    #layovers
    layovers = driver.find_elements_by_xpath("//span[@data-test-id='layover-airport-stops']")
    layovers_list = [layovers[i].text for i in range(max_extraction)]
    
    #Return lists
    return_dep_list = []
    return_arr_list = []
    return_airline_list = []
    return_price_list = []
    return_duration_list = []
    return_stops_list = []
    return_layovers_list = []
    
    #Obtaining return offer
    for i in range(len(dep_times_list)):
        print("obtaining #{} return offers".format(i+1))
        try:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test-id='select-button']")))
        finally:
            returns = driver.find_elements_by_xpath("//button[@data-test-id='select-button']")
            return_button = returns[i]
            return_button.click()
            sleep(2)
            try:
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[@data-test-id='listing-price-dollars']")))
            finally:
                #Return departure time
                return_dep_times = driver.find_elements_by_xpath("//span[@data-test-id='departure-time']")
                return_dep_list.append(return_dep_times[0].text)
                
                #Return arrival time
                return_arr_times = driver.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
                return_arr_list.append(return_arr_times[0].text)
                
                #Return airline
                return_airlines = driver.find_elements_by_xpath("//span[@data-test-id='airline-name']")
                return_airline_list.append(return_airlines[0].text)
                
                #Return price
                return_prices = driver.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
                return_price_list.append(return_prices[0].text.split('$')[1])
                
                #Return duration
                return_durations = driver.find_elements_by_xpath("//span[@data-test-id='duration']")
                return_duration_list.append(return_durations[0].text)
                
                #return stop over
                return_stopovers = driver.find_elements_by_xpath("//span[@class='number-stops']")
                return_stops_list.append(return_stopovers[0].text)
                
                #Return layovers
                return_layovers = driver.find_elements_by_xpath("//span[@data-test-id='layover-airport-stops']")
                return_layovers_list.append(return_layovers[0].text)
                driver.back()
                sleep(5)
    
    #Compiling
    print("Compiling the lists into dataframe")
    for i in range(len(dep_times_list)):
        try:
            df.loc[i, 'departure date'] = dep_date_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'return date'] = ret_date_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'departure time'] = dep_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'arrival time'] = arr_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'airline'] = airline_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'price'] = price_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'duration'] = durations_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'stops'] = stops_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'layover'] = layovers_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'return departure time'] = return_dep_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'return arrival time'] = return_arr_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'return airline'] = return_airline_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'return price'] = return_price_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'return duration'] = return_duration_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'return stops'] = return_stops_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'layover'] = return_layovers_list[i]
        except Exception as e:
            pass
    
    global main_df
    #Concat the df to the main df
    main_df = pd.concat([main_df,df])
        
#-------------------------------------------------------------------------------

def test_main():
    #Starting
    #Settle timing
    
    #Start driver
    3#driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=options)
    driver = webdriver.Chrome(executable_path="chromedriver")
    driver.implicitly_wait(20)
    driver.get("https://www.expedia.com.sg/")
    print("Driver up and running")
    sleep(1.5)

    #start_date_str = str(travel_month)+"/01/2019" 
    start_date = datetime.datetime(travel_year, travel_month, 1)
    
    end_date = start_date + datetime.timedelta(days=travel_days)
    
    total_days_in_month = monthrange(travel_year, travel_month)[1]
    print(start_date.strftime("%d/%m/%Y"))
    print(end_date.strftime("%d/%m/%Y"))
    
    number_of_loops = total_days_in_month - travel_days
    
    #Start selenium
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--incognito")
    #driver = webdriver.Chrome(chrome_options=chrome_options)

    initialise_page(start_date,end_date,driver)
    #Page extraction
    single_page_extraction(start_date,end_date,driver)
    
    
    for i in range(number_of_loops):
        #Next dates
        start_date += datetime.timedelta(days=1)
        end_date += datetime.timedelta(days=1)
        
        print("Starting the #{} of search for {} to {}".format(i+1, start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y")))
        #ensure the page can load
        dep_elem = driver.find_element_by_id("departure-date-1")
        dep_elem.clear()
        dep_elem.send_keys(start_date.strftime("%d/%m/%Y"))
        print("Entered flight date of {}".format(start_date.strftime("%d/%m/%Y")))
        
        arr_elem = driver.find_element_by_id("return-date-1")
        for i in range(11):
                arr_elem.send_keys(Keys.BACKSPACE)
        arr_elem.send_keys(end_date.strftime("%d/%m/%Y"))
        print("Entered return date of {}".format(end_date.strftime("%d/%m/%Y")))
        
        #Search
        submit_elem = driver.find_element_by_id('flight-wizard-search-button')
        submit_elem.click()
        sleep(10)
        print("Searching ...")
        
        #Extraction
        single_page_extraction(start_date,end_date,driver)
        
    
    print("Scraping finished for trip to {} from {}, {} days on the the #{} month with {} results".format(destination_country,
          origin_country,travel_days,travel_month, main_df.shape[0]))
            
    main_df.to_csv("{}_to_{}.csv".format(origin_country, destination_country))
    #print(main_df.iloc[0,5])
    extracted_df = main_df.copy()
    extracted_df = extracted_df.sort_values(['price'])
    print(type(extracted_df.iloc[0,5]))
    driver.quit()
    return extracted_df.iloc[0,5]

        
if __name__ == "__main__":
    test_main()
        
        
        
        
        