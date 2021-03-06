from vegchill.extension import VegChillPlugin, VegChillInitExt

class GlobalInitializerExt(VegChillInitExt):
    """global initilizer
    """

    def __init__(self):
        """
        Initialize job here
        """
        if self.vegchill.environ['debugger'] == 'gdb':
            import gdb
            # gdb settings
            gdb.execute('set history save on')
            gdb.execute('set history filename ~/.gdbhistory')
            gdb.execute('set output-radix 0x10')
            gdb.execute('handle SIGALRM print nopass')
        else:
            raise NotImplemented('lldb settings not implemented yet')

    @classmethod
    def name(cls):
        return 'initializer'


class Plugin(VegChillPlugin):

    @classmethod
    def init_ext(cls):
        return [GlobalInitializerExt]

    @classmethod
    def cmd_ext(cls):
        return []
