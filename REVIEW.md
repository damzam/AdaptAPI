## AdaptAPI Take Home Review

### Why Scrapy?

My initial impulse was to use the [Requests](https://requests.readthedocs.io/en/latest/) library in conjunction with [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/), but...

- There's just **so much** prior art in the Python ecosystem for building elegant, extensible, high-concurrency web crawlers.
    - I'd seen/heard of [Scrapy](https://scrapy.org/) on number of occassions and, based on everything that I had read, it seemed pretty awesome...and I really wanted to give it a try. 
    - So I went all in with Scrapy and was **delighted** by the [parsel](https://parsel.readthedocs.io/en/latest/) library that it utilizes for selectors. They seem cleaner and more intuitive than the ones offered by Beautiful Soup (which I'd used in previous projects).
    - It's got a nifty [interactive shell](https://docs.scrapy.org/en/latest/topics/shell.html) that I could use to play around and make sure I was extracting the data that I wanted (while looking at the HTML elements with Chrome's Inspector), and it had some bad-ass [logging functionality](https://docs.scrapy.org/en/latest/topics/logging.html), which I suppressed so that you would just see the organized/munged data in a prettified JSON format.
    - I took advantage of the [Scrapy API](https://docs.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script) to run the spiders programmatically as well as its ability to [run multiple spiders concurrently](https://docs.scrapy.org/en/latest/topics/practices.html#running-multiple-spiders-in-the-same-process).










given that there wasn't any dynamically loaded content on the [mock indemnity](https://scraping-interview.onrender.com/mock_indemnity/a0dfjw9a) or [placeholder carrier](https://scraping-interview.onrender.com/placeholder_carrier/f02dkl4e/policies/1) pages, 





I initially wasn't sure whether or not the content on  was being rendered dynamically...so, even though it wasn't, I thought I should approach the problem with a solution that could access data regardless of whether the HTML was fully rendered server-side or if client-side javascript needed to be executed.


and maybe [Selenium](https://selenium-python.readthedocs.io/) to render dynamic content.


Selenium has been an awesome tool that I've used to run integration tests in the past, but it would have you would have needed to install a [Driver](https://selenium-python.readthedocs.io/installation.html#drivers), which felt like it would be kind of invasive.



Using python with Scrapy and Scrapy-Splash offers a very mature framework for elegant, extensible, high-concurrency web scraping.

### ... enter Scrapy-Splash

Using python with Scrapy and Scrapy-Splash offers a very mature framework for elegant, extensible, high-concurrency web scraping.

The ecosystem includes advanced functionality, but I took some shortcuts to keep things simple.

I put the logic for extracting, organizing, and munging data in the spiders, but a more scalable solution should have utilized the [Item-Pipeline](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) facility offered by Scrapy.

DOM/CSS selectors were more than adequate to access information from the MOCK_INDEMNITY page. Regular expressions were necessary in some cases for PLACEHOLDER_CARRIER. 

Scrapy offers a rich toolset for [extracting links](https://docs.scrapy.org/en/latest/topics/link-extractors.html) that I could have used for the PLACEHOLDER_CARRIER, but instead I just created a simple iterator by checked the DOM to see if there was a link with the text `Next >`, yielding subsequent requests with subsequent URLs with Python's built-in [urlparse function](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse), and then collating and logging out the results when it was clear that all of the data had been extracted.

Remove vestiges of `SEED_URL` that were hard-coded in the `mock_carrier.py` spider

## TO DO

- authentication / secrets AWS Secrets Manager

- task schduling/queueing...make sure to play nice, avoid DoS and check robots.txt
  - what's in a robots.txt file? (see settings.py for throttling)

- persistence: storing semi-structured data timestamped versions in Postgres or Redis (grok vector databases)

- checking for diffs (you can automate the process of detecting and notifying in the event of information loss/change in the event of a modification in data availability or HTML structure)
  - Validations (is it in the set of...)
  - Data additions are more challenging

- We could have used [Lua scripting](https://splash.readthedocs.io/en/stable/scripting-overview.html) for Scrapy-Splash to emulate user actions that would have yielded additional dynamic content was available, but it was unnecessary for this exercise.

- Using Scrapy's built-in `pipelines.py`:



Enhance the scraped data with metadata, such as the date the item was scraped.
Validate the scraped data for errors.
Store the scraped data in a database or other data store.

cleansing HTML data
validating scraped data (checking that the items contain certain fields)
checking for duplicates (and dropping them)
storing the scraped item in a database


