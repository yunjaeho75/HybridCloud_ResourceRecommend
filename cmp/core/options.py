
class OptionsBase(object):
  """Base class for representing a set of tf.data options.
  Attributes:
    _options: Stores the option values.
  """

  def __init__(self):
    # NOTE: Cannot use `self._options` here as we override `__setattr__`
    object.__setattr__(self, "_options", {})

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    for name in set(self._options) | set(other._options):  # pylint: disable=protected-access
      if getattr(self, name) != getattr(other, name):
        return False
    return True

  def __ne__(self, other):
    if isinstance(other, self.__class__):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __setattr__(self, name, value):
    if hasattr(self, name):
      object.__setattr__(self, name, value)
    else:
      raise AttributeError(
          "Cannot set the property %s on %s." % (name, type(self).__name__))

  def _to_proto(self):
    """Convert options to protocol buffer."""
    raise NotImplementedError("%s._to_proto()" % type(self).__name__)

  def _from_proto(self, pb):
    """Convert protocol buffer to options."""
    raise NotImplementedError("%s._from_proto()" % type(self).__name__)

def create_option(name, ty, docstring, default_factory=lambda: None):
  """Creates a type-checked property.
  Args:
    name: The name to use.
    ty: The type to use. The type of the property will be validated when it
      is set.
    docstring: The docstring to use.
    default_factory: A callable that takes no arguments and returns a default
      value to use if not set.
  Returns:
    A type-checked property.
  """

  def get_fn(option):
    # pylint: disable=protected-access
    if name not in option._options:
      option._options[name] = default_factory()
    return option._options.get(name)

  def set_fn(option, value):
    if not isinstance(value, ty):
      raise TypeError("Property \"%s\" must be of type %s, got: %r (type: %r)" %
                      (name, ty, value, type(value)))
    option._options[name] = value  # pylint: disable=protected-access

  return property(get_fn, set_fn, None, docstring)




class estimator(OptionsBase):
    ml = create_option(
      name="ml estimator",
      ty=str,
      docstring="ml estimator",
      default_factory='ml estimator')
   
    pso = create_option(
      name="pso estimator",
      ty=str,
      docstring="pso model estimator",
      default_factory='pso estimator')


class service(OptionsBase):
    learner = create_option(
      name="learner",
      ty=str,
      docstring="model learner",
      default_factory='learner')

    estimator = create_option(
      name="estimator",
      ty=str,
      docstring="model estimator",
      default_factory='estimator')
