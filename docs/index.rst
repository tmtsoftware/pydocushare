PyDocuShare
===========

This is the top page of PyDocuShare, python API to interact with your Xerox DocuShare site. It is distributed under `GNU General Public License version 2 <https://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_. The source code is available at `GitHub <https://github.com/tmtsoftware/pydocushare>`_.

.. image:: images/example_collection.png
           
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   getting-started
   docushare

Restriction
-----------

This API has been tested with DocuShare version 7.0.0. The implementation of this API does not use DocuShare HTTP/XML interface. It rather parses the same HTML pages as the users see in their Web browsers. Therefore, it may not work with different versions or if the DocuShare configuration is different from what the author assumes.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
