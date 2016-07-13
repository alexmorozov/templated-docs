Useful template tags
====================

To use these template tags, load them first with ``{% load templated_docs_tags %}``.

lolinebreaks
------------

To keep newlines in a multiline text, use this tag instead of a default ``linebreaks`` filter::

  {{ variable|lolinebreaks }}

image
-----

Inserting images from models' ImageField is supported. Assuming you have a ``claim`` model instance with a ``stamp`` ImageField in it::

  {% image claim.stamp %}
