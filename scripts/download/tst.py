#!/usr/bin/python3
##############################################################
# Script name: Seattle Times (List Scraper)
# Version: 1.0
# By: Rodrigo Zamith
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks: 
##############################################################

########### Set variables
### Set publication-specific variables # CUSTOM
pubshort = "tst"
puburl = "http://www.seattletimes.com/"
puburl_mv = None
puburl_mv_extraactions = None

### Set data storage variables
root_folder = "../../"
homepages_dir = root_folder + "data/html_src/" + pubshort + "/"
screenshots_dir = root_folder + "data/screenshots/" + pubshort + "/"

########### Load libraries
from selenium import webdriver
from datetime import datetime
from pyvirtualdisplay import Display
import scraperfunctions
import time, sys

### Grab the information from our configuration file
config = scraperfunctions.load_config()

### Get the current time if we don't already have one (and transform into a date object)
curr_time = scraperfunctions.get_curr_time()

### Establish our MySQL Connection (for logging, etc.)
engine, connection, metadata, mysql_table_name, mysql_log_name = scraperfunctions.create_mysql_engine(config)

########### Download actions
try:
    ### Initiate our virtual display
    print("Initiating virtual display")
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    ### Let's start our browser
    browser = scraperfunctions.create_browser()
    
    ### Let's load the page work
    scraperfunctions.load_homepage(browser, pubshort, puburl)
    
    ### See if the MV list requires extra actions
    if puburl_mv_extraactions is not None:
        ### Actions for acquiring MV List
        pass
    
    ### Let's first store the source code
    html_code = browser.page_source
    write_out_file = scraperfunctions.write_out_file("%s" % homepages_dir, "%s_%s.html" % (pubshort, curr_time.strftime("%Y%m%d%H%M")), html_code)
    
    ### See if the MV list is in a separate URL
    if puburl_mv is not None:
        ### Actions for acquiring MV List
        pass
    
    ### Save a screenshot
    scraperfunctions.take_screenshot(browser, screenshots_dir, pubshort, curr_time.strftime("%Y%m%d%H%M"))
    print("Screenshot taken")
    
    ### Close the browser
    scraperfunctions.close_browser(browser)
    
    ### Close our virtual display
    display.stop()
    print("Display closed")
    
    ### Perform closing actions
    print("Successfully downloaded the page!")
    #scraperfunctions.store_mysql_log(mysql_log_name, metadata, pubshort, curr_time, "1", "1", "") # Log success
except:
    scraperfunctions.store_mysql_log(mysql_log_name, metadata, pubshort, curr_time, "1", "0", "") # Log failure