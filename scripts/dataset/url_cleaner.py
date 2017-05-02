#!/usr/bin/python3
##############################################################
# Script name: URL Cleanup Script
# Version: 1.0
# By: Rodrigo Zamith
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks: 
##############################################################

### Load libraries
import pymysql, datasetfunctions
import datetime, re

### Set variables
pubshort_list = [["dpo", "/ci_[0-9]+", "/ci_(\d+)/?"], ["sjm", "/ci_[0-9]+", "/ci_(\d+)/?"], ["spp", "/ci_[0-9]+", "/ci_(\d+)/?"]] # Publications followed by regular expression (MySQL) and same regular expression (Python)
link_data_table = "adj_link_data" # Table containing the link data

### Load settings
config = datasetfunctions.load_config()

### Prepare our database
conn, cur, mysql_table_name, mysql_log_name = datasetfunctions.create_mysql_conn(config)
mysql_table_name = link_data_table

### For each publication
for publication in pubshort_list:
    pubshort = publication[0]
    regex = publication[1]
    regex_python = publication[2]
    
    print("Creating connection with %s" % (pubshort))
    
    ### Get list of entries
    try:
        matches = cur.execute("SELECT id, article FROM `%s` WHERE pubshort = '%s' AND article REGEXP '%s';" % (mysql_table_name, pubshort, regex))
        matches = cur.fetchall()
    except:
        print("Failed to get entries with statement: SELECT id, article FROM `%s` WHERE pubshort = '%s' AND article REGEXP '%s';" % (mysql_table_name, pubshort, regex))
    
    print("Found %s matches, proceeding to replace..." % (len(matches)))
    pos = 1
    
    for match in matches:
        print("Working on match %s" % pos)
        pos += 1
        
        # Get column values for each row
        m_id = match[0]
        m_article = match[1]
        
        # Replace the values where we find matches
        try:
            m_article = re.search(regex_python, m_article).group(1)
        except:
            print("Failed to fix article id %s" % m_id)
            pass
        
        # Update the table
        try:
            cur.execute("UPDATE `%s` SET article = '%s' WHERE id = '%s';" % (mysql_table_name, m_article, m_id))
        except:
            print("Failed to update the table with statement: UPDATE `%s` SET article = '%s' WHERE id = '%s';" % (mysql_table_name, m_article, m_id))
            
    conn.commit()
    print("Matches committed for %s" % (pubshort))