pleno-proj API reference
================================

.. note::
    This is auto-generated, this is HIGHLY EXPERIMENTAL

Application
===========================
.. note::
    This section is mostly for developers of pleno-proj, not for users.


.. automodule:: pleno_common.__main__
    :members:
    :undoc-members:
    :imported-members:
    :show-inheritance:

.. automodule:: pleno_common.infra
    :members:
    :imported-members:
    :undoc-members:
    :show-inheritance:


Droid Components
===========================

A droid component is an abstract interface type that defines some basic behavior such as registering a config option with the glboal command-line args parser as well as the config dictionary.
All components that make up a droid pipeline are derived from this abstract interface.

Derived classes must implement the following methods:

.. automethod:: pleno_common.components.component.Component.register_configs
.. automethod:: pleno_common.components.component.Component.validate_configs

.. automodule:: pleno_common.components
    :members:
    :undoc-members:
    :imported-members:
    :show-inheritance:


Algorithms
===========================

.. automodule:: pleno_common.algorithms
    :members:
    :undoc-members:
    :imported-members:
    :show-inheritance:


Math
===========================

.. automodule:: pleno_common.math
    :members:
    :undoc-members:
    :imported-members:
    :show-inheritance:
