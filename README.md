ckanext-trak
===========

Requires CKAN page tracking to be enabled

Two paster tasks need to be run as usual as part of the usual Page Tracking process
- tracking update
- search-index rebuild

Changes the view for page tracking
- shows page views with no minimum number of views (default in CKAN is 10)
- moves page tracking stats to below Package data on dataset list page (search)
- moves page tracking stats to below Resource data on resource list page
- doesn't use flame icon - uses backgrounds with rounded corners
