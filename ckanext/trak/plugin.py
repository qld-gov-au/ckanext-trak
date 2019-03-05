import json
import pylons.config as config
import ckan.plugins as plugins
import ckan.lib.base as base
import ckan.plugins.toolkit as toolkit


def tracking_info(data_obj):
    """
    Helper to render a snippet
    """
    #print data_obj
    total = -1
    recent = -1
    if 'tracking_summary' in data_obj:
        tracking_summary = data_obj['tracking_summary']
        if 'total' in tracking_summary:
            total = tracking_summary['total']
        if 'recent' in tracking_summary:
            recent = tracking_summary['recent']
    else:
        if 'views_total' in data_obj:
            total = data_obj['views_total']
        if 'views_recent' in data_obj:
            recent = data_obj['views_recent']
    return base.render_snippet('tracking.html', total=total, recent=recent)


def display_pageviews():
    """
    Return value of trak.display_pageviews in the .ini configuration file
    """
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
        """
        Have the search index include the latest tracking data

        Modified in 2.4.X as tracking info is not returned by default

        This method is called for each dataset when the search index is
        rebuilt, e.g.::
            paster search-index rebuild -c /etc/ckan/default/production.ini

        This is the way to get the search index to include the latest tracking
        data for resources (Dataset tracking is okay - the search indexing
        already picks up on this)
        """
        get_package_action = toolkit.get_action('package_show')
        # Need to get tracking summary
        package = get_package_action({}, {'id': pkg['id'],
                                     'include_tracking': 'true'})
        pkg['validated_data_dict'] = json.dumps(package)
        return pkg
