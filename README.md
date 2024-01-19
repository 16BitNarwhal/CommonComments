# CommonComments
Are you drowning in comments and feedback from platforms like Play Store or YouTube? Common Comments is your solution! This program uses advanced techniques—embedding models, vector embeddings, and nearest neighbor clustering—to efficiently condense the cluttered information. Say goodbye to information overload and hello to streamlined insights!

# How it works
## Data Collection
**Most Websites Use JavaScript Alongside HTML/CSS:** Modern websites are often built using a combination of HTML, CSS, and JavaScript. HTML provides the basic structure of pages, CSS is used for presentation, and JavaScript enables interactive features. JavaScript is particularly important because it can dynamically load new content onto the page without the need to refresh the entire page. This is common in features like infinite scrolling, where new content (like comments or posts) loads as you scroll down a page.

**Limitation of BeautifulSoup:** BeautifulSoup is a Python library for parsing HTML and XML documents. It is excellent for extracting data from static web pages – those where the content is directly embedded in the HTML delivered by the server. However, BeautifulSoup cannot execute JavaScript. Therefore, it cannot access content that is loaded dynamically via JavaScript as you interact with the page (like scrolling or clicking buttons).

**Use of Selenium for Dynamic Content:** To scrape data from a website that loads content dynamically with JavaScript (like loading comments when scrolling down), you need a tool that can interact with the webpage just like a real user would. This is where Selenium comes in. Selenium is a tool that automates web browsers. It can simulate actions like clicking, scrolling, and typing.

**Selenium Script for Scrolling:** In this scenario, the Selenium script is programmed to mimic a user scrolling down a webpage. As the script scrolls, the JavaScript on the webpage loads new content (such as additional comments). The script continues this process until it reaches the end of the content or cannot scroll further.

**Reading Loaded Data:** Once the script has scrolled through the page and triggered the loading of all the dynamic content (all the comments in this case), it can then read and extract this data. Since now the content is present in the page's DOM (Document Object Model), Selenium can access and scrape this information.

![scrape](https://github.com/16BitNarwhal/CommonComments/assets/31218485/c67e1a46-9fe5-4f0d-921b-3ff4cb13a20c)
