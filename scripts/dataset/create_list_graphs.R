##############################################################
# Script name: MV List Changes Graph Creator
# Version: 1.0
# By: Rodrigo Zamith
# License: MPL 2.0 (see LICENSE file in root folder)
# Additional thanks:
##############################################################

### Load libraries
library(ggplot2)
library(scales)
library(lubridate)
library(dplyr)

### Assess Rate of Change
## Load data and clean it up
pop_delta <- read.csv("pop_delta.csv", header=TRUE, na.strings="NULL")
pop_delta$curr_time <- as.POSIXct(pop_delta$curr_time, format="%Y-%m-%d %H:%M:%S")
pop_delta$curr_time_utc <- as.POSIXct(pop_delta$curr_time_utc, format="%Y-%m-%d %H:%M:%S")
pop_delta$pubshort_label <- pop_delta$pubshort_label <- factor(pop_delta$pubshort, levels=c("nyd", "fws", "hsa", "hch", "kcs", "mhe", "jse", "nyt", "ore", "cpd", "ocr", "slt", "sjm", "tst", "slp", "spp", "mst", "dpo", "nsl", "wsj", "wpo"), labels=c("Daily News", "Fort Worth Star-Telegram", "Honolulu Star-Advertiser", "Houston Chronicle", "Kansas City Star", "Miami Herald", "Milwaukee Journal Sentinel", "New York Times", "Oregonian", "Plain Dealer", "Register", "Salt Lake Tribune", "San Jose Mercury News", "Seattle Times", "St. Louis Post-Dispatch", "St. Paul Pioneer Press", "Star Tribune", "The Denver Post", "The Star-Ledger", "Wall Street Journal", "Washington Post"), ordered=TRUE)
pop_delta$activity_group <- ifelse(pop_delta$pubshort=="cpd" | pop_delta$pubshort=="dpo" | pop_delta$pubshort=="mst" | pop_delta$pubshort=="nsl" | pop_delta$pubshort=="ore" | pop_delta$pubshort=="sjm" | pop_delta$pubshort=="slt" | pop_delta$pubshort=="spp", "Good Proxy", ifelse(pop_delta$pubshort=="fws" | pop_delta$pubshort=="jse" | pop_delta$pubshort=="nyd" | pop_delta$pubshort=="ocr" | pop_delta$pubshort=="wsj" | pop_delta$pubshort=="wpo", "Indeterminate Proxy", "Poor Proxy"))

## Look at hourly intervals
by_hour <- group_by(pop_delta, pubshort_label, hour(curr_time))
props <- summarise(by_hour,
                   count = n(),
                   delta = mean(delta, na.rm=TRUE))
names(props) <- c("pubshort_label", "hour", "count", "delta")

## Plot the data
png(filename="Rate_of_Change_Pop.png", width=1800, height=1392, units="px", pointsize=28)
ggplot(props, aes(x=hour, y=delta)) +
  geom_bar(stat="identity") +
  xlab("Time of Day (Hour)") +
  ylab("Average Rate of Change for Items Appearing on the 'Most Viewed' List") +
  scale_x_discrete(breaks=seq(0,23,2), limits=seq(0,23,1)) +
  scale_y_continuous(labels=percent, limits=c(0,1)) +
  theme_bw() +
  theme(text=element_text(size=28)) +
  facet_wrap(~pubshort_label, scales = "free_x")
dev.off()

## Useful descriptive statistics by publication
by_pub <- group_by(pop_delta, pubshort_label)
props <- summarise(by_pub,
                   count = n(),
                   delta = mean(delta, na.rm=TRUE))
names(props) <- c("pubshort_label", "count", "delta")
props_order_des <- props[rev(order(props$delta)),]




### Assess Median Time to List
## Load and adjust data
arts <- read.csv("key_info_by_article.csv", header=TRUE, na.strings="NULL") # For desktop
arts <- subset(arts, pubshort != "slp")
arts$pubshort_label <- factor(arts$pubshort, levels=c("nyd", "fws", "hsa", "hch", "kcs", "mhe", "jse", "nyt", "ore", "cpd", "ocr", "slt", "sjm", "tst", "slp", "spp", "mst", "dpo", "nsl", "wsj", "wpo"), labels=c("Daily News", "Fort Worth Star-Telegram", "Honolulu Star-Advertiser", "Houston Chronicle", "Kansas City Star", "Miami Herald", "Milwaukee Journal Sentinel", "New York Times", "Oregonian", "Plain Dealer", "Register", "Salt Lake Tribune", "San Jose Mercury News", "Seattle Times", "St. Louis Post-Dispatch", "St. Paul Pioneer Press", "Star Tribune", "The Denver Post", "The Star-Ledger", "Wall Street Journal", "Washington Post"), ordered=TRUE)
arts$is_pop <- factor(arts$is_pop, levels=c(0, 1), labels=c("No", "Yes"))
arts$time_on_page_to_pop <- as.numeric(arts$time_on_page_to_pop)
arts$time_on_page_to_pop <- as.numeric(lapply(arts$time_on_page_to_pop, function(x) ifelse(x >= 7200, 7200, x))) # Set the maximum value of an item's time_on_page_to_pop at 7200 (5 days)
arts_poponly <- subset(arts, is_pop == "Yes")
arts_poponly$pubshort_label <- factor(arts_poponly$pubshort_label, levels=rev(sort(unique(arts_poponly$pubshort_label))), ordered=TRUE)

## Create plot
png(filename="Median_Time_to_Pop.png", width=1800, height=1392, units="px", pointsize=28)
ggplot(arts_poponly, aes(x=pubshort_label, y=time_on_page_to_pop, group=pubshort_label)) +
  coord_flip(ylim=c(0, 1600)) +
  geom_boxplot(outlier.shape=NA, na.rm = TRUE, size=1) + # Help hide the outliers
  scale_y_continuous(breaks=seq(0,1600,100)) + # Help hide the outliers
  xlab("") +
  ylab("Time On Page Before Appearing on 'Most Viewed' List (in minutes)") +
  theme_bw() +
  theme(legend.position="none", text=element_text(size=28))
dev.off()

## Useful descriptive statistics
by_pub <- group_by(arts_poponly, pubshort_label)
counted <- summarise(by_pub,
                     median_ttpop = median(time_on_page_to_pop, na.rm=TRUE))
counted_order_des <- counted[rev(order(counted$median_ttpop)),]
