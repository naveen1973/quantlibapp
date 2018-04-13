.. image:: https://www.quantransform.co.uk/static/assets/images/quantransform.jpg


quantlibapp 
====================================

quantlibapp is currently in alpha stage - if you find a bug, please submit an issue.


What is quantlibapp?
-----------

**quantlibapp** is a framework to use QuantLib-Python (version 1.12). Currently, 
one application is developed:

1. Calculate loan (annuity) schedule, similar to **numpy.pmt**, but this application
takes real date and consider UK holiday too. 

Please note that this version ONLY works on jupyterlab or jupyter notebook as it takes
input directly from the notebook,

Installing quantlibapp
-------------

The easiest way to install ``quantlibapp`` using ``pip`` or ``easy_insatll``:

.. code-block:: bash

    $ pip install git+https://github.com/quantransform/quantlibapp

Please also install qgrid on https://github.com/quantopian/qgrid

License
-------

MIT