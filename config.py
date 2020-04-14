#! /usr/bin/env python

import os
import yaml

from utils.with_logger import WithLogger


class Config(WithLogger):
    config_fname = "configuration.yaml"

    def __init__(self, config_fname=None):
        config_fname = config_fname or self.config_fname
        fo = open(config_fname, "r")
        blob = fo.read()
        fo.close()
        self.config = yaml.load(blob)

    def __getattr__(self, attrname):

        upper_attrname = attrname.upper()
        envvar = os.getenv(upper_attrname)
        if envvar is not None:
            self.logger.warning("The `%s` environment variable is deprecated in favor of the `DESTALINATOR_%s` environment variable", upper_attrname, upper_attrname)
        else:
            envvar = os.getenv('DESTALINATOR_' + upper_attrname)
        if envvar is not None:
            # allow certain types (e.g. warning, closure text) to be used as-is
            if "RAW" in upper_attrname:
                return envvar
            else:
                split_envvar = [x.strip() for x in envvar.split(',') if x] if ',' in envvar else envvar
                return split_envvar

        file_based_config = self.config.get(attrname, '')
        return file_based_config

    def get(self, attrname, fallback=None):
        return self.config.get(attrname, fallback)


_config = Config()


def get_config():
    return _config


class WithConfig(object):
    @property
    def config(self):
        return get_config()
