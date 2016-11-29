# foursquare_data_mining

This repo includes work for data mining on foursquare data. It includes the script doing web scraping automatically, and analysis python code on data we are interested in. The ultimate result can help us understand neighborhood-wise shopping preference. 

## The foursquare_pipeline file contains all the scraping part. 

You can run scraping.py to get structured data automatically about venues' statistics and tips as you can see on the foursquare.com. An example of command line input is:

python scraping.py "shopping"

The default code will read location (town names) from a csv file, here is nytownnames.csv, and search for shopping venues on foursquare.com then scrape the structured data automatically. You can use another list of townnames with your choice.



