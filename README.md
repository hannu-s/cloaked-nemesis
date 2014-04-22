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
Inspection is done via browser. browser loads index.html which presents master_inspection.xml.
User has to manually inspect sites and mark them as useful / useless. When site is marked, Reddit link, page title, headings, (stylized text?) are stored in the Database. User can dismiss page, thus no changes occure.

###Automatic Search
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
4. Create new MasterInspection element
5. Add every childrens findings in the MasterInspection.XML
6. Call sorter class
7. Store MasterInspection.XML
8. Notify readiness for manual inspection of MasterInspection.XML

###Child (amount: n)  

1. Search subreddit
2. Inspect set amount newest links, skip visited
3. Store link and relevant page data as a file
  - Data is stored in pages directory
  - Words seperated by whitespace " " 
  - 1st row reddit link
  - 2nd row page title
  - 3rd row page headers
  - 4th row stylized texts
  - 5th row rest
4. Pipes Link URLS to parent
5. If certain URL are already reported by different child, parent tells to remove it 
  - Removes also data file corresponding the removed link / url
6. Calls PageToXML class
7. Notify parent for findings ready for inspection

###Server & Index.html  

Currently expects to find server in localhost:80/tracker/. 

- Index.html uses javascript to load master_insptector.xml.
  * UI uses ajax to send user inputs to PHP server. 
1. Server validates inputs and afterwards executes Updater with userinput as its parameter.
2. Server waits for Updater to finish
3. Triggers page refresh with new master_inspection.xml

###Updater  

1. Starts with id and user vote of the master_inspector node as its parameters.
2. If voted useful or useless
  * Calls Main_Updater with id, vote parameters
3. Gets main_inspection.xml content from xmlInspections
4. Removes node from master_inspector xml
5. Writes master_inspection.xml
6. Notifies that task is finished

###Main_Updater  

1. Class starts with id and useful/useless vote
2. Load page data corresponding the id
3. Regex validation for page datas words
4. Store words and usefulness from link, title, headers, (stylized text?) in to xml
5. Remove read page file
6. Recalculate 'keywords' and 'avoids'
7. Update 'good sites' and 'useless sites'
8. Calculate all scores from existing page data files
9. Return xmlInspections list to Updater

###PageToXML 

1. Starts with name of the wanted xml and a list containing inspection elements
2. Calculate all scores from existing page data files
3. Order calculated data with descending score
4. Write data to XML

###Sorter  

Class starts with list of links and scores. Sorts them in descending order. Returns sorted list.


Ideas For Future Development
----------------------------

- Search parameters create sha-0 hash, which is then used to seperate different search term results.
  - allows long search terms saved as easily as short ones

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
* Words 
  - occurance 
  - times_useful 
  - times_useless
* General
  - word_average
  - average_ratio

Classes
=======

Associations
------------
Contains Keywords class elements in list
- setParam(keywords, avoids, forcedKeywords, forcedAvoids)

Child
-----
reddit links and pages to xml

Configure
---------
Conf.xml
- setParam(sites, params, pagesToSearch)

Connector
---------
Parent to child. ConnectorManager class for connections

Inspection
----------
Class for master_inspection.xml & ch_inspection.xml's.
Variables link, score, url, fil, ID

Inspector
---------
- getInspections(xmls)  return list of Inspection elements in xml list
- getInspectionsStr(xml)  returns elements from single xml

ListTool
--------
Several list modification tools

MainUpdater
-----------
Called from Updater class. Used to handle voting changes such as keywords and words list

OSTool
------
Several os library tools

PageLoader
----------
Reads page.txt file created from child class.
- init(path)
- isReadable()    return boolean
- read()          fills variables

Parent
------
Main business logic. Handles all the processes, afterwards directs browser to server.

Server.php
----------
Handles post id and vote, validates inputs and starts updater class.

Sites
-----
Contains good_sites and bad_sites lists
- setParam(gdSites, bdSites)

Sorter
------
- sortInspectionList(li)    return inspection list sorted by score, in descending order

Updater
-------
Started by server, starts MainUpdater. Removes voted element from master_inspection.xml

WordList
--------
Class containing list of Word classes. Word class has word, occ, usef, usel variables.
- append(word, usef, usel)      Word occ is increased by 1, if does not exists, creates new
- set(word, occ, usef, usel)    Word occ is manually set. If does not exiests, creates new

XMLParser
---------
Reads tree elemets and returns readable values

XMLReader
---------
Reads xml, returns tree

XMLWriter
---------
Writes xml
