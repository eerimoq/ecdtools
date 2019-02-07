|buildstatus|_
|coverage|_

About
=====

Electronic circuit design in Python 3.

- `IBIS`_ parsing. Currently only a subset of the `IBIS 6.1`_
  specification is supported.

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

Alternatively, with ``transform=True``, the same input as above gives:

.. code-block:: python

   >>> from pprint import pprint
   >>> import ecdtools
   >>> ibs_file = ecdtools.ibis.load_file('tests/files/ibis/pybis/bushold.ibs',
                                          transform=True)
   >>> model = ibs_file.get_model_by_name('TOP_MODEL_BUS_HOLD')
   >>> model.model_type
   'Input'
   >>> pprint(model.gnd_clamp)
   [(Decimal('-2.0000'), Decimal('-6.158E+17'), None, None),
    (Decimal('-1.9000'), Decimal('-1.697E+16'), None, None),
    (Decimal('-1.8000'), Decimal('-4.679E+14'), None, None),
    (Decimal('-1.7000'), Decimal('-1.290E+13'), None, None),
    (Decimal('-1.6000'), Decimal('-3.556E+11'), None, None),
    (Decimal('-1.5000'), Decimal('-9.802E+9'), None, None),
    (Decimal('-1.4000'), Decimal('-2.702E+8'), None, None),
    (Decimal('-1.3000'), Decimal('-7.449E+6'), None, None),
    (Decimal('-1.2000'), Decimal('-2.053E+5'), None, None),
    (Decimal('-1.1000'), Decimal('-5660'), None, None),
    (Decimal('-1.0000'), Decimal('-156.0'), None, None),
    (Decimal('-0.90000'), Decimal('-4.308'), None, None),
    (Decimal('-0.80000'), Decimal('-0.1221'), None, None),
    (Decimal('-0.70000'), Decimal('-0.004315'), None, None),
    (Decimal('-0.60000'), Decimal('-0.0001715'), None, None),
    (Decimal('-0.50000'), Decimal('-0.000004959'), None, None),
    (Decimal('-0.40000'), Decimal('-1.373E-7'), None, None),
    (Decimal('-0.30000'), Decimal('-4.075E-9'), None, None),
    (Decimal('-0.20000'), Decimal('-3.044E-10'), None, None),
    (Decimal('-0.10000'), Decimal('-1.030E-10'), None, None),
    (Decimal('0'), Decimal('0'), None, None),
    (Decimal('5'), Decimal('0'), None, None)]

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

.. _IBIS 6.1: http://ibis.org/ver6.1/ver6_1.pdf
