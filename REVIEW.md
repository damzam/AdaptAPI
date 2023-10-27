## AdaptAPI Take Home Review

### Key Takeaways

- Writing spiders/crawlers is **FUN**!
- [Scrapy](https://scrapy.org/) is an awesome framework for building spiders/crawlers.
- There's **MUCH** more work to be done!

### Why Scrapy?

- My initial impulse was to use Python's [Requests](https://requests.readthedocs.io/en/latest/) library in conjunction with [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/), but... 
- There's just **so much** prior art in the Python ecosystem for building elegant, extensible, high-concurrency web crawlers.
- I'd seen/heard of [Scrapy](https://scrapy.org/) on number of occassions and, based on everything that I had read, it seemed pretty awesome...and I really wanted to give it a try. 
- So I went all in with Scrapy and was **delighted** by the [parsel](https://parsel.readthedocs.io/en/latest/) library that it utilizes for selectors. They seem cleaner and more intuitive than the ones offered by Beautiful Soup (which I'd used in previous projects).
- It's got a nifty [interactive shell](https://docs.scrapy.org/en/latest/topics/shell.html) that I could play with and make sure I was extracting the data that I wanted (while looking at the HTML elements with Chrome's Inspector), and it had some bad-ass [logging functionality](https://docs.scrapy.org/en/latest/topics/logging.html), which I suppressed so that you would just see the organized/munged data in a prettified JSON format.
- I took advantage of the [Scrapy API](https://docs.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script) to run the spiders programmatically and also its ability to [run multiple spiders concurrently](https://docs.scrapy.org/en/latest/topics/practices.html#running-multiple-spiders-in-the-same-process).

### Where I opted NOT to use Scrapy functionality

- Scrapy offers a rich toolset for [extracting links](https://docs.scrapy.org/en/latest/topics/link-extractors.html) that I could have used for the [placeholder carrier](https://scraping-interview.onrender.com/placeholder_carrier/f02dkl4e/policies/1), but instead I just created a simple iterator by checking the DOM to see if there was a link with the text `Next >`, yielding subsequent requests with URLs with Python's built-in [urlparse](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse) function, and then collating and logging out the results when it was clear that all of the data had been extracted.
- While DOM/CSS selectors were more than adequate to access information from the [mock indemnity](https://scraping-interview.onrender.com/mock_indemnity/a0dfjw9a) page, I used Python's built-in [regular expressions](https://docs.python.org/3/library/re.html) in some cases for [placeholder carrier](https://scraping-interview.onrender.com/placeholder_carrier/f02dkl4e/policies/1) where there were email addresses or dates outside of the DOM. 

### Why Scrapy-Splash?

- Initially I didn't know whether or not there was any dynamically loaded content on the [mock indemnity](https://scraping-interview.onrender.com/mock_indemnity/a0dfjw9a) or [placeholder carrier](https://scraping-interview.onrender.com/placeholder_carrier/f02dkl4e/policies/1) pages or if elements were being populated via Javascript.
- So I decided that I should approach the problem with a solution that could access data regardless of whether the HTML was fully rendered server-side or if client-side javascript needed to be executed.
- I thought about using [Selenium](https://selenium-python.readthedocs.io/) to render dynamic content; Selenium has been an awesome tool that I've used in the past to run integration tests, but you would have needed to install a [Driver](https://selenium-python.readthedocs.io/installation.html#drivers), which felt kind of invasive.
- Running [Scrapy-Splash](https://github.com/scrapy-plugins/scrapy-splash) in a [docker container](https://www.zenrows.com/blog/scrapy-splash#install-docker) to render HTML and execute javascript is relatively non-invasive...and it's pretty f@#$ing cool.
- [Lua scripting](https://splash.readthedocs.io/en/stable/scripting-overview.html) for Scrapy-Splash to emulate user actions that would have yielded additional dynamic content was available (e.g. scrolling down), but it was unnecessary for this exercise.

### Packaging

- Using a [virtual environment](https://docs.python.org/3/library/venv.html) is the standard practice for insulating a python project and its respective dependency installations from the system python.
- I opted not to package the project using a [setup.py](https://www.geeksforgeeks.org/what-is-setup-py-in-python/) file, thinking it would be **fun** for you to go through the process of seeing that only two simple dependencies needed to be installed into the virtual environment with the `pip install scrapy scrapy-splash` command.
- The Makefile wasn't necessary; you could have just executed the code with the command `python3 -m scraper input.json`, but I thought it would be kind of cool to just run `make`.

### Warts to Remove

- Remove vestiges of `SEED_URL` that were hard-coded in the `mock_carrier.py` spider

### Work to Be Done

- Authentication / secrets AWS Secrets Manager

- task schduling/queueing...make sure to play nice, avoid DoS and check robots.txt
  - (see settings.py for throttling)

- persistence: storing semi-structured data timestamped versions in Postgres or Redis (grok vector databases)

- Check for diffs (you can automate the process of detecting and notifying in the event of information loss/change in the event of a modification in data availability or HTML structure)
  - Validations based on domain-specific knowledge (e.g. policy status, endorsement data, etc.)
  - Data additions are more challenging

- We could have used [Lua scripting](https://splash.readthedocs.io/en/stable/scripting-overview.html) for Scrapy-Splash to emulate user actions that would have yielded additional dynamic content was available, but it was unnecessary for this exercise.

- I put the logic for extracting, organizing, and munging data in the spiders, but a more scalable solution should have utilized the [Item-Pipeline](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) facility offered by Scrapy.


