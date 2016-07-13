# --coding: utf8--

import os

from django.core.management.base import BaseCommand

from templated_docs import fill_template


class DocumentGenerationCommand(BaseCommand):
    """
    A management command which generates a document using the context specified
    in the ``get_document_context()`` method.
    """

    def add_arguments(self, parser):
        parser.add_argument('template_name', type=str)
        parser.add_argument('--format', type=str, default='odt',
                            help='Convert a document to specified format')
        parser.add_argument('--output_file', type=str, default=None,
                            help='Put the result into this file.')

    def handle(self, template_name, **options):
        output_format = options['format']
        temp_name = fill_template(
            template_name,
            self.get_document_context(template_name, **options),
            output_format)

        out_file = options['output_file'] or temp_name
        if out_file != temp_name:
            os.rename(temp_name, out_file)
        print(out_file)

    def get_document_context(self, template_name, **options):
        """
        Fill the context for passing in the document template.
        """
        raise NotImplementedError(
            'subclasses of GenerateDocumentCommand must provide a '
            'get_document_context() method')
