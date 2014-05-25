import ckan.plugins as plugins
import ckan.lib.base as base

def tracking_info(data_obj):
    return base.render_snippet('tracking.html', total=data_obj['tracking_summary']['total'], recent=data_obj['tracking_summary']['recent'])

class TrakPluginClass(plugins.SingletonPlugin):
    """
    Setup plugin
    """

    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, 'templates')


    def get_helpers(self):
        return {'tracking_info': tracking_info}