Serving generated documents over HTTP
=====================================

A common task is to serve user a created file. To facilitate this, a handy ``FileResponse`` response class is available::

  from templated_docs.http import FileResponse

  def your_view(self):
      filename = get_my_document()
      return FileResponse(filename, visible_name='document.pdf')

A ``FileResponse`` constructor is a subclass of Django's ``HttpResponse``, providing the following arguments:

* ``actual_file`` - the real filename to serve
* ``visible_name`` - the name a user will see in the browser
* ``delete`` - set this to `False` to skip file deletion

.. Important::
  The `actual_file` **is deleted by default** after being served, as usually this is the wanted behaviour. To keep the file, pass the ``delete=False`` argument to the ``HttpResponse`` constructor.
