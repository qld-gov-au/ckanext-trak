import json

import pylons.config as config
import ckan.plugins as plugins
import ckan.lib.base as base



#helper to render a snippet
def tracking_info(data_obj):
    return base.render_snippet('tracking.html', total=data_obj['tracking_summary']['total'], recent=data_obj['tracking_summary']['recent'])


#helper - gets value of trak.display_pageviews in the .ini configuration file
def display_pageviews():
    if config.get('trak.display_pageviews') == 'true':
        print 'it true'
        return True
    return False


class TrakPluginClass(plugins.SingletonPlugin):
    """
    Setup plugin
    """

    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)

    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, 'templates')

    def get_helpers(self):
        return {'tracking_info': tracking_info,
                'display_pageviews': display_pageviews}

    def before_index(self, pkg):

        #this method is called for each dataset when the search index is rebuilt
        #   paster search-index rebuild -c /etc/ckan/default/production.ini
        #this is the way to get the search index to include the latest tracking data
        # for resources (Dataset tracking is okay - the search indexing already picks up on this)

        #the 'pkg' is a flattened python dict. It needs to be unflattened, changed to inlcude
        # tracking info for the resource (taken from database) and returned

        #this operation needs to be fairly efficient as it will be called for _every_ dataset whenever the search-index is updated

        #you should be able to access the tracking_summary table to get the tracking counts for resources using
        # import ckan.models.tracking_summary?
        # if not, you can go the long way round like i did in 'commands.py' to get the tracking_raw table

        return pkg
