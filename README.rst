|buildstatus|_
|coverage|_

About
=====

Electronic circuit design in Python 3.

- `IBIS`_ parsing.

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
