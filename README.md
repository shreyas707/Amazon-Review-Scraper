# Amazon Review Scraper
This is a simple python library that scrapes reviews from amazon.com and writes it into a csv file.

---

## Installation
```pip install amazon-review-scraper```

---

## Usage
1. Instantiating the object:

>```scraper = amazon_review_scraper.amazon_review_scraper(url, start_page, end_page, time)```

   * ```url```: In the product's page, scroll down to the end of the reviews and click **see all reviews**. Click on that and copy the ```url```. This ```url``` is your first parameter. Example: ```https://www.amazon.com/Apple-iPhone-Factory-Unlocked-Phone/product-reviews/B00NQGP42Y/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews```

   * ```start page```: This is the second parameter. Mention the page from which you want to scrape.

   * ```end page```: This is the third parameter. Mention at what page the scraper has to stop scraping.

   * ```time(in seconds)```: This is the 4th argument. Amazon might block your IP if it receives too many requests every second. To prevent that, you can mention ```time``` (in seconds). The scraper will wait anywhere from ```0``` to the ```time``` before scraping every page. If you don't want to wait before scraping every page, give the value as **0**.


2. Run the scraper:

>```scraper.scrape()```


3. Write to CSV:

>```scraper.write_csv(file_name)```

   * ```file_name```: Enter the file name of the CSV that you want the program to generate.

---

## Example Code

```
from amazon_review_scraper import amazon_review_scraper

url = input("Enter URL: ")
start_page = input("Enter Start Page: ")
end_page = input("Enter End Page: ")
time_upper_limit = input("Enter upper limit of time range (Example: Entering the value 5 would mean the program will wait anywhere from 0 to 5 seconds before scraping a page. If you don't want the program to wait, enter 0): ")
file_name = "iphone6"

scraper = amazon_review_scraper.amazon_review_scraper(url, start_page, end_page, time_upper_limit)
scraper.scrape()
scraper.write_csv(file_name)
```