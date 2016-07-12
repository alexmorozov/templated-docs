# --coding: utf8--

import os

from django.core.management.base import BaseCommand
from django.template import Context

from templated_docs import fill_template


class Command(BaseCommand):
    help = 'Generate a document from the specified template'

    def add_arguments(self, parser):
        parser.add_argument('template_name', type=str)
        parser.add_argument('--format', type=str, default='odt',
                            help='Convert a document to specified format')
        parser.add_argument('--output_file', type=str, default=None,
                            help='Put the result into this file.')

    def handle(self, template_name, **options):
        context = Context()

        output_format = options['format']
        temp_name = fill_template(template_name, context, output_format)

        out_file = options['output_file'] or temp_name
        if out_file != temp_name:
            os.rename(temp_name, out_file)
        print(out_file)
