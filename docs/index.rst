.. templated_docs documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Templated-docs: office documents for Django
===========================================

**Templated-docs** is a Django package that allows you to generate documents,
including texts, spreadsheets and presentations, from templates. It utilises
LibreOffice as an underlying conversion document mechanism.

Features
--------

* Generate any LibreOffice-supported document from within Django.
* Use Django template language inside office documents.
* Create custom generation management commands to integrate with other systems.


Installation
------------

To install templated-docs:

1. Make sure you have LibreOffice >= 4.3.0 installed on the same machine
2. Install a package with ``pip install templated-docs``
3. Add ``templated_docs`` to ``INSTALLED_APPS``

.. include:: partial/libffi-warning.rst

Usage
-----

To generate a document from a template ``sample.odt`` you can write a view
like this:

.. code:: python

  from templated_docs import fill_template
  from templated_docs.http import FileResponse

  def get_document(request):
    """
    A view to get a document filled with context variables.
    """
    context = {'user': request.user, 'foo': 'bar'}
    filename = fill_template('sample.odt', context, output_format='pdf')
    visible_filename = 'greeting.pdf'
    return FileResponse(filename, visible_filename)

``templated_docs.fill_template(template_name, context, output_format='odt')``
  Fill a template ``template_name`` using a ``context`` dictionary as a context, optionally converting it to the ``output_format``. Returns a filename of a generated file.


More information
----------------

.. toctree::
  :maxdepth: 2

  templates
  templatetags
  http
  management-commands
  settings
