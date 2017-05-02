Examining the Comparability of 'Most-Viewed Lists'
====================
Author: Rodrigo Zamith

Description
-----
This repository contains the Python scripts used to download and extract information for the five most viewed items appearing on the homepages of 21 different news organizations at a given time. Additional scripts are offered to help organize the information and produce charts that facilitate an evaluation of the lists of most-viewed items across two dimensions: the rate of change for the list and the median time it takes an item to appear on that list.

These scripts will likely be most useful as a foundation for similar research projects; they will need to be tweaked to adapt them to other websites. If you have any questions, please e-mail me.

The scripts are broken down into three sets:

* Download scripts: These scripts are used to freeze a liquid homepage into a static snapshot with the browser-processed HTML code and a screenshot of the page at the time the script is run.

* Parse scripts: These scripts extract information from the aforementioned snapshots. Specifically, the top five items from the list of most-viewed items and all other links appearing on the page (that fit a given URL pattern) are extracted and stored into a database.

* Dataset scripts: These scripts help to clean and reshape data. Those clean data may then be downloaded from the database, and the R script facilitates an evaluation of the lists of most-viewed items across two dimensions: the rate of change for the list and the median time it takes an item to appear on that list.

Dependencies
-----
These scripts depend on [Python](https://www.python.org/), [MySQL](https://www.mysql.com/), and [Firefox](https://www.mozilla.org/en-US/firefox/products/). Additionally, the [Selenium framework](https://www.seleniumhq.org/) and the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and [PyMSQL](https://github.com/PyMySQL/PyMySQL) libraries, and other standard libraries, are used. For the data analysis scripts, [R](https://www.r-project.org/) is required.

License
-----
All scripts in this repository are licensed under the Mozilla Public License Version 2.0 (see LICENSE file in the root folder). TL;DR: Feel free to use modify it and distribute it as part of either commercial or non-commercial software, provided you disclose both the source code and any modifications you make to it.