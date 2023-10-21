## AdaptAPI Take Home Project

Salutations, Jacob!

For this most excellent [takehome exercise](https://www.notion.so/adapt-api/Adapt-Engineering-Take-home-c9edda9f51dd4709b4ade053b8f19aff), I have elected to use the awesome library [Scrapy](https://github.com/scrapy/scrapy), which lets you build fast, high-concurrency web spiders that extract and organize the data that you want and/or need extremely efficiently and easily while addressing login, authentication and session concerns.

I'm also using the [Scrapy-Splash](https://github.com/scrapy-plugins/scrapy-splash) plugin which doesn't just run javascript to allow you to wait for dynamic content to load, it also has facilities for doing things like scrolling down for the emulated browser (running in a docker container) to load additional dynamic content.

### Running the Splash engine

First, if you don't already have Docker Desktop, download [here](https://www.docker.com/products/docker-desktop/).

For Mac and Windows, you should then be able download the Splash image in a terminal with the following:

`docker pull scrapinghub/splash`

and then you should be able to run the rendering engine with the following:

`docker run -it -p 8050:8050 --rm scrapinghub/splash`

### Running the spiders

1) Download the code

`git clone git@github.com:damzam/AdaptAPI.git`

2) Change directory into AdaptAPI

`cd AdaptAPI`

3) Create a virtual environment to protect your system python

`python3 -m venv .env`

4) Activate the virtual environment

`source .env/bin/activate`

5) Install dependencies

`pip install scrapy scrapy-splash`

6) cd into the `scraper` directory

`cd scraper`

7) Load the seed urls from `input.json` (copied from the take home assignment) and run the respective spiders to scrape the MOCK_INDEMNITY and PLACEHOLDER_CARRIER content and log it out to the console with the following command:

`make`

## Clean Up

1) Remove the local repo

2) Terminate the docker process and remove the image

`docker rmi scrapinghub/splash`

And you're done!