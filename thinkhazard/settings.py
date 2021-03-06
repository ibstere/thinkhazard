import os
import ConfigParser
import yaml
from pyramid.paster import get_appsettings


def load_full_settings(config_uri, name='admin', options={}):
    """Load app settings, processing settings and local settings.
    Fallback to admin app by default as this should mainly be used by admin
    scripts.
    """
    settings = get_appsettings(config_uri,
                               name=name,
                               options=options)
    load_local_settings(settings, name)
    load_processing_settings(settings)
    return settings


def load_processing_settings(settings):
    """Load processing specific settings.
    """
    processing_settings_path = settings['processing_settings_path']
    with open(processing_settings_path, 'r') as f:
        settings.update(yaml.load(f.read()))


def load_local_settings(settings, name):
    """ Load local/user-specific settings.
    """
    local_settings_path = os.environ.get(
        'LOCAL_SETTINGS_PATH', settings.get('local_settings_path'))
    if local_settings_path and os.path.exists(local_settings_path):
        config = ConfigParser.ConfigParser()
        config.read(local_settings_path)
        settings.update(config.items('app:{}'.format(name)))
