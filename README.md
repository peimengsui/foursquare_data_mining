# foursquare_data_mining

This repo includes work for data mining on foursquare data. It includes the script doing web scraping automatically, and analysis python code on data we are interested in. The ultimate result can help us understand neighborhood-wise shopping preference. 

## The foursquare_pipeline folder contains all the scraping part. 

You can run scraping.py to get structured data automatically about venues' statistics and tips as you can see on the foursquare.com. An example of command line input is:

python scraping.py "shopping"

The default code will read location (town names) from a csv file, here is nytownnames.csv, and search for shopping venues on foursquare.com then scrape the structured data automatically finally pickled it for further analysis in python. You can use another list of townnames with your choice.

## The fousquare_analysis folder contains two main analysis on the scraped data which we find very interesting and relevant to our case. 

1. SmithHavenShopping.ipynb: This Report is Smith Haven Mall local (Lake Grove) shopping. 
2. SuffoldShopping.ipynb: This report is Suffolk County local (including 33 villages) shopping.

The detailed result and future work are listed in the notebook. 

Ideally, this location-based analysis should be scaled up to the entire country so that it can be integrated in our map-based product. 
