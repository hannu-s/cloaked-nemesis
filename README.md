README
======

Purpose
-------
Search information related to search parameter from HTML page reddit. 

Design
------

###HTTP Requests
Use Restful API to collect data from site. Follow promising links to the site, store site link and the site HTML body, for later inspection. Don't follow anylinks outside reddit.

###Word Marking
Mark often occured words in good information containing sites as 'keywords'. Also mark often occured words in poor / no information containing sites as 'avoids'.

###Manual Inspection
User has to manually inspect sites and mark them as useful / useless. When site is marked, Reddit link, page title, headings, (stylized text?) are stored in the Database. User can dismiss page, thus no changes occure.

###Automatic Inspection
Search for 'keywords' and 'avoids' especially in the reddit link, site headings and stylized text. Check that same link has not already been searched, or the exact page visited.
Sort most promising links at first. Present findings in XML Form.

###Word occurance
When word times_useful / times_useless ratio is not close 1, word is associated with with 'keywords' or 'avoids'. If the ratio changes word will lose / change its association.

###Score system

'Keywords' add and 'avoids' substract from link specific score.
Very often occuring words with 'keywords' or 'avoids' association, change score very little or not at all. 
If score does not reach specific score, the site will not be presented.

####Keywords
Each 'keyword' add link specific score for

+ In reddit link
  - 100
+ In title of the site  
  - 50
+ In headings
  - 25
+ In stylized text
  - 5
+ In Body
  - 1

####Avoids
Each 'avoids' substract link specific score for

+ In reddit link
  - 100
+ In title of the site  
  - 50
+ In headings
  - 25
+ In stylized text
  - 5
+ In Body
  - 1

Structure & Process
-------------------

###Parent (amount: 1)

1. XML Query for 'keywords', 'avoids', 'urls', linksToSearch
2. Starts child processes each child searches different subreddit. 
  - Initial values are urls visited, 'keywords' & 'avoids'. 
  - Parent communicates through pipe when running.
  - Wait for link urls reported from children
  - If multiple identical urls, only first is allowed, tells child to remove the link
3. Wait for every child to finish 
4. Create new MasterInspection.XML
5. Add every childrens findings in the MasterInspection.XML
6. Call sorter class
7. Store MasterInspection.XML
8. Notify readiness for manual inspection of MasterInspection.XML

###Child (amount: n)

1. Search subreddit
2. Inspect set amount newest links, skip visited
3. Store link and relevant page data as a file
4. Calculate Link score system
5. Pipes Link URLS to parent
6. If certain URL are already reported by different child, parent tells to remove it 
  - Removes also data file corresponding the removed link / url 
7. Stores findings in XML
8. Notify parent for findings ready for inspection

###Inspector

Independet class. Presents Inspection.XML and MasterInspection.XML in http server. Start browser and directs it to server address. User gets to vote for useful/useless or dismiss the site. 
Every vote calls for Updater class with initial values: link, vote. Afterwards calls Sorter to resort the file and updates the server.

###Updater

1. Class starts with Link and useful/useless vote
2. Load page data corresponding the link
3. Store words and usefulness from link, title, headers, (stylized text?) in to db
4. Recalculate 'keywords' and 'avoids'
5. Update 'good sites' and 'useless sites'

###Sorter

Class starts with list of links and scores. Sorts them in descending order. Returns sorted list
Also capable to store sorted xml.

MYSQL - DB
----------

+ Words 
  - occurance 
  - times_useful 
  - times_useless
+ General
  - word_average
  - average_ratio

XML
---

* configure
* keywords
  - occurance
* avoids
  - occurance
* forced keywords
* forced avoids
* good sites	
* useless sites
* findings
