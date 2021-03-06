from .compat import *
from .environ import Environ
import importlib
import os
from appdirs import user_data_dir

APP_NAME = 'VegChill'
APP_AUTHOR = 'Anciety'

CONFIG_DEFAULT_PATH = os.path.join(user_data_dir(APP_NAME, APP_AUTHOR), 'config')

# global object
veg = None

def depends_resolve(vegchill, exts_with_import_path):
            """does topology sort to resolve dependencies
            """
            class Vert(object):
                def __init__(self, ext, import_path):
                    self.ext = ext
                    self.import_path = import_path
                    self.in_cnt = len(ext.dependency)

                def __str__(self):
                    return '%s - %d' % (self.ext.name(), self.in_cnt)

            class Edge(object):
                def __init__(self, frm, to):
                    self.frm = frm
                    self.to = to
            vert_table = {}
            for ext, import_path in exts_with_import_path:
                path = '%s:%s' % (import_path, ext.name())
                vert_table[path] = Vert(ext, import_path)
                vegchill.debug('setup vert for %s' % path)
            edges = set()
            for ext, import_path in exts_with_import_path:
                # check if all depends can be resolved
                path = '%s:%s' % (import_path, ext.name())
                vert = vert_table[path]
                ignoring = False
                for dep in ext.dependency:
                    if dep not in vert_table:
                        vegchill.warn(
                            'Dependency %s of %s not found, ignored.' % (dep, path)
                        )
                        ignoring = True
                        break
                if ignoring:
                    continue
                else:
                    edges |= set(map(lambda x: Edge(vert_table[x], vert), ext.dependency))

            # topology sort
            seq = []
            while len(vert_table):
                # FIXME this can be optimized to not to loop each time but
                # filter it out in count calculation
                no_deps = list(filter(lambda x: x[1].in_cnt == 0, vert_table.items()))
                no_dep_keys = set()
                no_dep_vals = set()
                for k, v in no_deps:
                    no_dep_keys.add(k)
                    no_dep_vals.add(v)
                seq += list(map(lambda x: x[1], no_deps))
                edges_associated = filter(lambda x: x.frm in no_dep_vals, edges)
                for e in edges_associated:
                    e.to.in_cnt -= 1
                edges -= set(edges_associated)
                vert_table = {
                    k: vert_table[k] for k in filter(lambda x: x not in no_dep_keys, vert_table)
                }
                if len(no_deps) == 0 and len(vert_table) > 0:
                    vegchill.emer('Unresolvable dependencies, nothing will be loaded')
                    return []
            return map(lambda x: (x.ext, x.import_path), seq)


class VegChill(object):
    """VegChill Main Class
    """

    LOG_EMER = 0 # emergency log level
    LOG_ERR = 1 # error log level
    LOG_WARN = 2 # warning log level
    LOG_INFO = 3 # information log level
    LOG_DEBUG = 4 # debug log level

    def logging(self, level, content):
        if level <= self.log_level:
            self.do_logging(level, content)

    def do_logging(self, level, content):
        if level == 0:
            print('[X] %s' % content)
        elif level == 1:
            print('[x] %s' % content)
        elif level == 2:
            print('[!] %s' % content)
        elif level == 3:
            print('[*] %s' % content)
        else:
            print('[DEBUG] %s' % content)

    def emer(self, content):
        """emergency logging
        """
        self.logging(self.LOG_EMER, content)

    def err(self, content):
        """error logging
        """
        self.logging(self.LOG_ERR, content)

    def warn(self, content):
        """warning logging
        """
        self.logging(self.LOG_WARN, content)

    def info(self, content):
        """information logging
        """
        self.logging(self.LOG_INFO, content)

    def debug(self, content):
        """debug logging
        """
        self.logging(self.LOG_DEBUG, content)

    def __init__(self, config, debugger_name):
        """inits the `VegChill` Class, mainly covers what an extension might need
        Args:
            config (object): a `ConfigParser` object
        """
        self.environ = Environ.from_config(config)
        self.init_exts = {}
        self.cmd_ext_class = {}
        self.log_level = self.environ['log_level']
        self.environ['debugger'] = debugger_name

        plugins = []
        # load plugins and extensions, but not instantiate anything until
        # dependency and priority resolve phase.
        init_ext_class = []
        for plugin_import_path in config.options('plugin'):
            try:
                plugin = importlib.import_module(plugin_import_path).plugin
                # load all init extension classes, they will be instantiated
                # after dependency and priority resolve.
                exts = plugin.init_ext()
                if type(exts) != list:
                    exts = [exts]
                # associate classes with import path
                # generates list of (ext_class, import_path) tuples
                for ext in exts:
                    ext.set_vegchill(self)
                    init_ext_class.append((ext, plugin_import_path))

                # cmd extensions don't worry about dependency, as they don't need to
                # be instantiated for now
                exts = plugin.cmd_ext()
                if type(exts) != list:
                    exts = [exts]

                for ext in exts:
                    if self.cmd_ext_class.get(ext.cmd()):
                        self.warn('command %s already exists! Rewritten' % ext.cmd())
                    ext.set_vegchill(self)
                    self.cmd_ext_class[ext.cmd()] = ext
            except AttributeError as e:
                self.warn('Plugin %s load fail, ignored.' % plugin_import_path)
                self.debug(e)
        self.debug('init extension classes: ' + str(init_ext_class))

        init_ext_class = depends_resolve(self, init_ext_class)
        for ext, import_path in init_ext_class:
            path = '%s:%s' % (import_path, ext.name())
            self.init_exts[path] = ext()

        self.debug('loaded init extensions: ' + str(self.init_exts))


def init_vegchill(config_path, debugger_name):
    from six.moves import configparser as ConfigParser
    config = ConfigParser.ConfigParser()
    # this is for adding environ plugin, since it must be prior to any others
    config.add_section('plugin')

    # add default modules
    import pkgutil
    for _, plugin_name, _ in pkgutil.iter_modules(['vegchill/plugins']):
        config.set('plugin', 'vegchill.plugins.%s' % plugin_name, '1')

    config.read(config_path)

    vegchill = VegChill(config, debugger_name)
    return vegchill


def lldb_init_module(debugger, internal_dict, config_path=CONFIG_DEFAULT_PATH):
    global veg
    import lldb

    vegchill = init_vegchill(config_path, 'lldb')
    veg = vegchill
    
    # add commands
    has_imported = False
    for cmd_name in vegchill.cmd_ext_class:
        if not has_imported:
            lldb.debugger.HandleCommand('command script import vegchill')
            has_imported = True
        cmd_ext = vegchill.cmd_ext_class[cmd_name]
        module_path = '%s.%s' % (cmd_ext.__module__, cmd_ext.__name__)
        cmd = 'command script add -c %s %s' % (module_path, cmd_name)
        lldb.debugger.HandleCommand(cmd)

def gdb_init_module(config_path=CONFIG_DEFAULT_PATH):
    global veg
    import gdb
    vegchill = init_vegchill(config_path, 'gdb')
    veg = vegchill

    for cmd_name in vegchill.cmd_ext_class:
        cls = vegchill.cmd_ext_class[cmd_name]
        cls(cmd_name, cls.gdb_command_class())
