ckanext-trak
===========

Installation
- activate virtualenv
- git clone https://github.com/XVTSolutions/ckanext-trak
- cd ckanext-trak
- python setup.py develop

Configuration (.ini file)
- trak.display_pageviews = true

Page Tracking enabled
- CKAN's built in tracking needs to be enabled. see http://docs.ckan.org/en/latest/maintaining/tracking.html


Operation

This extension provides
1. A paster command to bulk import an exported Google Analytics report
2. Template changes to extend existing Page View front-end presentation

Paster Command

- switch to the CKAN source dir in your virtualenv
paster --plugin=ckanext-trak csv2table <csv_file> -c /path/to/production.ini

csv_file is the exported CSV from Google Analytics. The exported GA file inlcudes several different tables so strip the file down to just the pageview lines

When csv2table is run, an entry is made into the tracking_raw table for each page for the number of times viewed. So if an entry '/dataset/amazing-dataset' has 99 pageviews, then there will be 99 entries made in the tracking_raw table - each with a different uuid.



Two paster tasks need to be run as usual as part of the usual Page Tracking process
- tracking update
- search-index rebuild

Changes the view for page tracking
- shows page views with no minimum number of views (default in CKAN is 10)
- moves page tracking stats to below Package data on dataset list page (search)
- moves page tracking stats to below Resource data on resource list page
- doesn't use flame icon - uses backgrounds with rounded corners


Running the paster task

- pages with local e.g. '/en' are calculated as a view for a dataset
- page views are added to the tracking_raw table for the date '2011-01-01'. This is the 'floor' date - first date which is checked by 'paster tracking update'
- for the sake of not dealing with changes to GA's export or any variations, the input format should be stripped
down to only the list of page views. i.e. all rows should start with '/'
- PageViews column is assumed to be the 3rd column

OTHER
- (put a delete statement for removing entries for 2011-01-01')