# CommonComments
Are you drowning in comments and feedback from platforms like Play Store or YouTube? Common Comments is your solution! This program uses advanced techniques—embedding models, vector embeddings, and nearest neighbor clustering—to efficiently condense the cluttered information. Say goodbye to information overload and hello to streamlined insights!

# How it works
## 📥 Data Collection
I specifically chose to focus on platforms that feature user-based comments and reviews. This includes popular sites like YouTube, IMDb, and Amazon. These platforms are rich sources of user opinions, feedback, and discussions, making them ideal for gathering diverse and extensive datasets for analysis.

**Most Websites Use JavaScript Alongside HTML/CSS:** Modern websites are often built using a combination of HTML, CSS, and JavaScript. HTML provides the basic structure of pages, CSS is used for presentation, and JavaScript enables interactive features. JavaScript is particularly important because it can dynamically load new content onto the page without the need to refresh the entire page. This is common in features like infinite scrolling, where new content (like comments or posts) loads as you scroll down a page.

**Limitation of BeautifulSoup:** BeautifulSoup is a Python library for parsing HTML and XML documents. It is excellent for extracting data from static web pages – those where the content is directly embedded in the HTML delivered by the server. However, BeautifulSoup cannot execute JavaScript. Therefore, it cannot access content that is loaded dynamically via JavaScript as you interact with the page (like scrolling or clicking buttons).

**Use of Selenium for Dynamic Content:** To scrape data from a website that loads content dynamically with JavaScript (like loading comments when scrolling down), you need a tool that can interact with the webpage just like a real user would. This is where Selenium comes in. Selenium is a tool that automates web browsers. It can simulate actions like clicking, scrolling, and typing.

**Selenium Script for Scrolling:** In this scenario, the Selenium script is programmed to mimic a user scrolling down a webpage. As the script scrolls, the JavaScript on the webpage loads new content (such as additional comments). The script continues this process until it reaches the end of the content or cannot scroll further.

**Reading Loaded Data:** Once the script has scrolled through the page and triggered the loading of all the dynamic content (all the comments in this case), it can then read and extract this data. Since now the content is present in the page's DOM (Document Object Model), Selenium can access and scrape this information.

![scrape](https://github.com/16BitNarwhal/CommonComments/assets/31218485/c67e1a46-9fe5-4f0d-921b-3ff4cb13a20c)

## 🧼 Data PreProcessing
After collecting the comments data using Selenium, the next crucial step is to preprocess this data to ensure its quality and relevance for analysis.

**Handling Empty Entries:** Often, the data scraping process may result in some entries being blank or null. These entries do not contribute to our analysis and can, in fact, skew the results. To address this, we employ the dropna() function in our processing pipeline. This function is a part of the pandas library in Python and is very effective in removing any rows in our dataset that contain missing or null values, ensuring that we only work with complete data entries.

**Removing Non-Alphanumeric Characters:** Our focus is primarily on extracting meaningful textual content from the comments. Non-alphanumeric characters often include punctuation, special characters, and other non-essential symbols that may not contribute to understanding the sentiment or content of the comments. To clean our data, we use regular expressions (regex) to filter out these non-alphanumeric characters. This step cleans up the text, making it more uniform and easier to analyze.

**Challenge with Multilingual Data:** While our current approach effectively removes most non-English characters, it does not entirely segregate comments in languages that use the same alphanumeric system as English, like French. This presents a challenge as non-English comments can introduce noise into our analysis, which is primarily designed for English text.

**Future Plans - Language Translation:** To further refine the data quality and make our analysis more robust, we are planning to incorporate a translation feature. This feature will identify non-English comments and translate them into English. This approach will not only help in managing the "pollution" caused by multilingual data but also provide insights from non-English comments, thereby enriching our dataset.
