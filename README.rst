|buildstatus|_
|coverage|_

About
=====

Electronic circuit design in Python 3.

- `IBIS`_ parsing.

Project homepage: https://github.com/eerimoq/ecdtools

Documentation: http://ecdtools.readthedocs.org/en/latest

Installation
============

.. code-block:: python

    pip install ecdtools

Example usage
=============

In this example we load an IBS-file and access some of its content.

.. code-block:: python

   >>> from pprint import pprint
   >>> import ecdtools
   >>> ibs_file = ecdtools.ibis.load_file('tests/files/ibis/pybis/bushold.ibs')
   >>> model = ibs_file.get_model_by_name('TOP_MODEL_BUS_HOLD')
   >>> model.model_type
   'Input'
   >>> pprint(model.gnd_clamp)
   [('-2.0000e+00', '-6.158e+17', 'NA', 'NA'),
    ('-1.9000e+00', '-1.697e+16', 'NA', 'NA'),
    ('-1.8000e+00', '-4.679e+14', 'NA', 'NA'),
    ('-1.7000e+00', '-1.290e+13', 'NA', 'NA'),
    ('-1.6000e+00', '-3.556e+11', 'NA', 'NA'),
    ('-1.5000e+00', '-9.802e+09', 'NA', 'NA'),
    ('-1.4000e+00', '-2.702e+08', 'NA', 'NA'),
    ('-1.3000e+00', '-7.449e+06', 'NA', 'NA'),
    ('-1.2000e+00', '-2.053e+05', 'NA', 'NA'),
    ('-1.1000e+00', '-5.660e+03', 'NA', 'NA'),
    ('-1.0000e+00', '-1.560e+02', 'NA', 'NA'),
    ('-9.0000e-01', '-4.308e+00', 'NA', 'NA'),
    ('-8.0000e-01', '-1.221e-01', 'NA', 'NA'),
    ('-7.0000e-01', '-4.315e-03', 'NA', 'NA'),
    ('-6.0000e-01', '-1.715e-04', 'NA', 'NA'),
    ('-5.0000e-01', '-4.959e-06', 'NA', 'NA'),
    ('-4.0000e-01', '-1.373e-07', 'NA', 'NA'),
    ('-3.0000e-01', '-4.075e-09', 'NA', 'NA'),
    ('-2.0000e-01', '-3.044e-10', 'NA', 'NA'),
    ('-1.0000e-01', '-1.030e-10', 'NA', 'NA'),
    ('0.', '0', 'NA', 'NA'),
    ('5', '0', 'NA', 'NA')]

Contributing
============

#. Fork the repository.

#. Install prerequisites.

   .. code-block:: text

      pip install -r requirements.txt

#. Implement the new feature or bug fix.

#. Implement test case(s) to ensure that future changes do not break
   legacy.

#. Run the tests.

   .. code-block:: text

      make test

#. Create a pull request.

.. |buildstatus| image:: https://travis-ci.org/eerimoq/ecdtools.svg?branch=master
.. _buildstatus: https://travis-ci.org/eerimoq/ecdtools

.. |coverage| image:: https://coveralls.io/repos/github/eerimoq/ecdtools/badge.svg?branch=master
.. _coverage: https://coveralls.io/github/eerimoq/ecdtools

.. _IBIS: http://ibis.org
