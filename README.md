Y Combinator SaaS Companies Scraper

This project is a web scraper designed to collect data about SaaS companies listed on the Y Combinator website. The scraper navigates through the Y Combinator companies page, extracts relevant information about each company, and saves the data in both JSON and CSV formats.

Features

	•	Scrapes company names, URLs, locations, founding dates, descriptions, and more.
	•	Extracts information about the company’s founders, including LinkedIn and Twitter profiles.
	•	Stores the scraped data in both JSON and CSV formats.
	•	Implements random sleep intervals between actions to mimic human behavior and avoid getting blocked.

Technologies Used

	•	Python: Core programming language.
	•	Selenium: WebDriver used for automating browser interactions.
	•	Google Chrome: Web browser used by Selenium for scraping.
	•	JSON: Format used to store the scraped data.
	•	CSV: Format used to store the scraped data.

Setup

Prerequisites

	•	Python 3.x installed on your machine.
	•	Google Chrome installed on your machine.
	•	ChromeDriver matching your Chrome version installed on your machine. Download ChromeDriver

Installation

	1.	Clone this repository:
        git clone https://github.com/yourusername/yc-saas-scraper.git
        cd yc-saas-scraper

    2.	Install the required Python packages:
        pip install -r requirements.txt

    3.	Update the chrome_driver_path variable in the script with the path to your local chromedriver executable.
    
    Running the Scraper

	1.	Ensure that the ChromeDriver path is correctly set in the script:
        chrome_driver_path = "/path/to/your/chromedriver"

    2.	Run the scraper:
        python scraper.py

    3.	The scraped data will be saved to ycombinator_saas_companies.json and ycombinator_saas_companies.csv in the project directory.
    
    How It Works

The script navigates to the Y Combinator companies page filtered by the “SaaS” tag. It then scrolls through the page, loading more companies as it goes, and scrapes data for each company listed. The data is collected in a structured format and saved in both JSON and CSV formats for further analysis.

Functions

	•	scrape_company_details(last_count): Main function that handles the scraping process.
	•	scrapper(start_index, end_index, company_data, companies): Extracts detailed information about each company.
	•	safe_extract(by, value, dri=driver): Safely extracts text from a web element.
	•	safe_extract_attr(by, value, attribute, dri=driver): Safely extracts an attribute from a web element.
	•	dump_json(data): Saves the scraped data to a JSON file.
	•	json_to_csv(data): Converts the JSON data to a CSV file.

Notes

	•	The script includes random sleep intervals between actions to mimic human browsing behavior and reduce the risk of being blocked.
	•	Ensure that your ChromeDriver version matches the version of Chrome you have installed.

Contributing

If you would like to contribute to this project, please feel free to fork the repository and submit a pull request.