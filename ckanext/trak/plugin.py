import json

import pylons.config as config
import ckan.plugins as plugins
import ckan.lib.base as base
import ckan.model as model
import json



#helper to render a snippet
def tracking_info(data_obj):
    return base.render_snippet('tracking.html', total=data_obj['tracking_summary']['total'], recent=data_obj['tracking_summary']['recent'])


#helper - gets value of trak.display_pageviews in the .ini configuration file
def display_pageviews():
    if config.get('trak.display_pageviews') == 'true':
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

		# This method is called for each dataset when the search index is rebuilt, e.g.
		#
		# paster search-index rebuild -c /etc/ckan/default/production.ini
		#
		# This is the way to get the search index to include the latest tracking data
		# for resources (Dataset tracking is okay - the search indexing already picks up on this)

		str_dict = pkg.get('data_dict')

		data_dict = json.loads(str_dict)

		if data_dict is not None:

			#resources is a List of Dicts
			resources_list = data_dict.get('resources')
			
			if resources_list is not None:
				for res in resources_list:

					#This data should have been updated by the paster tracking update command				
					tracking = model.TrackingSummary.get_for_resource(res.get('url'))

					if tracking is not None:
						res['tracking_summary'] = tracking


		return pkg
