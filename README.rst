===============================
Templated-docs
===============================


.. image:: https://badge.fury.io/py/templated-docs.svg
        :target: https://pypi.python.org/pypi/templated_docs

.. image:: https://img.shields.io/travis/alexmorozov/templated-docs.svg
        :target: https://travis-ci.org/alexmorozov/templated-docs

.. image:: https://readthedocs.org/projects/templated-docs/badge/?version=latest
        :target: https://templated-docs.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://requires.io/github/alexmorozov/templated-docs/requirements.svg?branch=master
        :target: https://requires.io/github/alexmorozov/templated-docs/requirements?branch=master
        :alt: Dependencies


Generate templated documents within Django in any format supported by
LibreOffice: texts, spreadsheets, presentations etc.


* Free software: MIT license
* Documentation: https://templated-docs.readthedocs.io.


Requirements
------------

* Python 2.7 or 3.4+
* Django >= 1.8
* A recent LibreOffice version (>=4.3.0) supporting LibreOfficeKit API.

.. include:: docs/partial/libffi-warning.rst

Example usage
-------------

Create a ``sample.odt`` document (make sure it's in OpenDocument format) and
put it in your Django templates folder. It should look something like this:

.. image:: https://github.com/alexmorozov/templated-docs/raw/master/docs/document-template.png

Then write a view to generate documents from this template:

    .. code-block:: python

        from templated_docs import fill_template
        from templated_docs.http import FileResponse

        def get_document(request):
            """
            A view to get a document filled with context variables.
            """
            context = {'user': request.user}  # Just an example

            filename = fill_template('sample.odt', context, output_format='pdf')
            visible_filename = 'greeting.pdf'

            return FileResponse(filename, visible_filename)

Navigate to the url your view is connected to, and you'll see a rendered and converted document:

.. image:: https://github.com/alexmorozov/templated-docs/raw/master/docs/generated-document.png

For more examples, see the ``examples/`` subfolder in the repository. More detailed documentation is available on https://templated-docs.readthedocs.io.

Credits
---------

Templated-docs was written by `Alex Morozov`_.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _pylokit: https://github.com/xrmx/pylokit
.. _`Alex Morozov`: http://morozov.ca
