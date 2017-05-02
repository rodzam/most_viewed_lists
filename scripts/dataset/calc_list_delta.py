#!/usr/bin/python3
##############################################################
# Program name: Get Most Viewed List Delta
# Version: 1.0
# By: Rodrigo Zamith
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks: 
##############################################################

### Load libraries
import pymysql, datetime, datasetfunctions

### Set script-specific variables
list_type = "pop" # 'pop' for popularity

### Load settings
config = datasetfunctions.load_config()

### Prepare our database
conn, cur, mysql_table_name, mysql_log_name = datasetfunctions.create_mysql_conn(config)
mysql_table_name = "adj_link_data"
delta_table_name = "%s_delta" % list_type

### Grab list of unique publications
unique_pubs = cur.execute("SELECT DISTINCT(pubshort) FROM `%s`;" % (mysql_table_name))
unique_pubs = cur.fetchall()
unique_pubs = [x[0] for x in unique_pubs]
unique_pubs_len = len(unique_pubs)

for publication in unique_pubs:
    ### Grab list of unique snapshots
    first_snap = cur.execute("SELECT curr_time FROM `%s` WHERE pubshort='%s' ORDER BY curr_time LIMIT 1;" % (mysql_table_name, publication))
    first_snap = cur.fetchall()
    first_snap = datetime.datetime.combine(first_snap[0][0].date(), datetime.datetime.min.time())
    last_snap = cur.execute("SELECT curr_time FROM `%s` WHERE pubshort='%s' ORDER BY curr_time DESC LIMIT 1;" % (mysql_table_name, publication))
    last_snap = cur.fetchall()
    last_snap = datetime.datetime.combine(last_snap[0][0].date(), datetime.datetime.max.time())
    
    insert_statements = []
    current_snap = first_snap
    ### For each unique snapshot
    while current_snap < last_snap:
        print("Processing snapshot %s (%s)" % (current_snap, publication))
        
        # Calculate datetime for the subsequent hour
        current_snap_lag = current_snap+datetime.timedelta(hours=1)
        
        # Get the popularity items and rankings for the current time
        list_rank_list_curr = cur.execute("SELECT article, %s_rank, curr_time, curr_time_utc FROM `%s` WHERE pubshort='%s' AND is_%s = '1' AND curr_time = '%s' ORDER BY %s_rank;" % (list_type, mysql_table_name, publication, list_type, current_snap, list_type))
        list_rank_list_curr = cur.fetchall()
        if not list_rank_list_curr:
            print("Couldn't find list_rank at current time")
            current_snap = current_snap_lag
            continue # Snapshot missing POP data, so skip
        list_rank_list_curr_len = len(list_rank_list_curr)
        if list_rank_list_curr_len != 5:
            print("list_rank not 5 items at current time")
            current_snap = current_snap_lag
            continue # Skip this if there's no prominence
        curr_time = list_rank_list_curr[0][2]
        curr_time_utc = list_rank_list_curr[0][3]
        list_rank_list_curr = [[x[0], x[1]] for x in list_rank_list_curr]
        list_rank_list_curr_tuple = set(tuple((x, y) for x, y in list_rank_list_curr))
        
        # Get the popularity items and rankings for the lagged time
        list_rank_list_lag = cur.execute("SELECT article, %s_rank FROM `%s` WHERE pubshort='%s' AND is_%s = '1' AND curr_time = '%s' ORDER BY %s_rank;" % (list_type, mysql_table_name, publication, list_type, current_snap_lag, list_type))
        list_rank_list_lag = cur.fetchall()
        if not list_rank_list_lag:
            print("Couldn't find list_rank at lagged time")
            current_snap = current_snap_lag
            continue # Skip to the next time point
        list_rank_list_lag_len = len(list_rank_list_lag)
        if list_rank_list_lag_len != 5:
            print("list_rank not 5 items at lagged time")
            current_snap = current_snap_lag
            continue # Skip to the next time point
        list_rank_list_lag = [[x[0], x[1]] for x in list_rank_list_lag]
        list_rank_list_lag_tuple = set(tuple((x, y) for x, y in list_rank_list_lag))
        
        # Calculate the Intersection
        intersection = len(set.intersection(list_rank_list_curr_tuple, list_rank_list_lag_tuple))
        delta = (5-intersection)/5
        
        # Add it to our list of insert statements
        insert_statements.append([publication, curr_time, curr_time_utc, delta])
        
        # Make the lagged snap the current snap
        current_snap = current_snap_lag
    
    ### Insert the items
    stmt = "INSERT INTO pro_delta (pubshort, curr_time, curr_time_utc, delta) VALUES (%s, %s, %s, %s);"
    cur.executemany(stmt, insert_statements)
    conn.commit()
