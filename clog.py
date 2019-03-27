import functools
import inspect
import logging
import os.path
import sys

# Note: Anything declared outside of the Clog class won't be accessible within
# the class due to the module replacement at the end.


class Clog(object):
  FORMAT = '%(levelname)1.1s [ %(filename)s:%(lineno)s - %(funcName).12s() ] %(asctime)s - %(message)s'

  def __init__(self, **kwargs):
    self.root_module = None
    self._imports = kwargs
    self._src_file = os.path.normcase(self.__init__.__code__.co_filename)

  def get_caller_name(self):
    '''The caller's module name, like 'module.submodule'.'''
    inspect = self._imports['inspect']
    os = self._imports['os']

    f = inspect.currentframe().f_back.f_back
    while True:
      if (os.path.normcase(f.f_code.co_filename) != self._src_file and
          f.f_locals):
        break
      f = f.f_back
    return f.f_locals.get('__name__', 'unknown')

  def init(self, log_file=None, log_format=None, file_handler=None):
    '''Configure a top-level logger for the module from which this was called.'''
    logging = self._imports['logging']

    log_format = log_format or self.FORMAT
    file_handler = file_handler or logging.FileHandler

    self.root_module = self.get_caller_name()
    top_logger = logging.getLogger(self.root_module)
    top_logger.setLevel(logging.DEBUG)
    top_logger.propagate = False

    formatter = logging.Formatter(log_format)

    if log_file is not None:
      f_handler = file_handler(log_file)
      f_handler.setFormatter(formatter)
      top_logger.addHandler(f_handler)

    c__handler = logging.StreamHandler()
    c__handler.setFormatter(formatter)
    top_logger.addHandler(c__handler)

  def __getattr__(self, name):
    '''Pass on calls to the logger for the calling module.'''
    functools = self._imports['functools']
    inspect = self._imports['inspect']
    logging = self._imports['logging']

    if self.root_module is None:
      raise Exception(
          'Cannot call `clog.{}` since clog was not initialized.'.format(name)
      )

    module = self.get_caller_name()

    if not module.startswith(self.root_module):
      raise Exception(
          'Cannot call `clog.{}` from module `{}` since it is not a submodule '
          'of `{}` where clog was initialized.'
          ''.format(name, module, self.root_module)
      )

    logger = logging.getLogger(module)
    attr = getattr(logger, name)

    try:
      argspec = inspect.getargspec(attr)
    except TypeError:
      pass
    else:
      if 'extra' in argspec.args or argspec.keywords is not None:
        extra_fields = {
            # TODO: I don't have a use case for this yet.
        }
        return functools.partial(attr, extra=extra_fields)

    return attr


# Swap out the module for an instance of Clog.
sys.modules[__name__] = Clog(
    functools=functools,
    inspect=inspect,
    logging=logging,
    os=os,
)
