import sys
import string
import csv
import time
import os
from uuid import uuid4

import sqlalchemy as sa
import pylons.config as config



from ckan.lib.cli import CkanCommand

class CSV2Table(CkanCommand):
    """
    Populate CKAN's tracking_raw table with historic data supplied by CSV

    Usage::
        paster --plugin=ckanext-trak csv2table <file.csv> -c /etc/ckan/default/production.ini
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__


    def __init__(self, name):
        #setup the sqlalchemy engine
        print os.path.realpath(__file__)
        sqlalchemy_url = 'postgresql://ckan_default:pass@localhost/ckan_default'
        self.engine = sa.create_engine(sqlalchemy_url)
        super(CSV2Table, self).__init__(name)


    def tracking_raw_insert(self, url):
        """
         inserts the given url into the tracking_raw table.
        """
        sql = """INSERT INTO tracking_raw
                     (user_key, url, tracking_type, access_timestamp)
                     VALUES (%s, %s, %s, %s)"""

        key = uuid4().hex    #uuid without any hyphens
        url = url
        type = 'page'

        #the 'floor' date from which the CKAN's page tracking system
        #begins looking in tracking_raw for entries
        access_timestamp = '2011-01-01 00:00:00.00'

        self.engine.execute(sql, key, url, type, access_timestamp)


    def command(self):

        if not self.args or len(self.args) != 1:
            print CSV2Table.__doc__
            return

        f = open(self.args[0], 'rt')

        total_start = time.time()

        try:
            reader = csv.reader(f)
            for row in reader:

                if len(row) == 9:
                    page_views = int(row[2].replace(',', ''))
                    url = row[0]

                    #look for /dataset/ will ensure locale e.g /en/dataset/ and /ja/dataset is captured
                    if "/dataset/" in url:
                        row_start = time.time()
                        for x in range(page_views):
                            self.tracking_raw_insert(url)

                        elapsed = time.time() - row_start
                        print "%s with %s pageviews in %s" %(url, str(page_views), elapsed )
        finally:
            f.close()

        elapsed = time.time() - total_start
        print elapsed










