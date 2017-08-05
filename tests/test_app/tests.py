# --coding: utf8--

import os

from django.test import TestCase

from templated_docs import fill_template


class InternalsTestCase(TestCase):
    def test_fill_correct_template(self):
        """
        Creating a document from a correct template doesn't raise any
        exception.
        """
        filename = fill_template('correct_template.odt', {'name': 'John'},
                                 output_format='pdf')
        os.unlink(filename)

    def test_fill_flat_correct_template(self):
        """
        test for flat file format fodt
        """
        filename = fill_template('correct_template.fodt', {'name': 'John'},
                                 output_format='pdf')
        os.unlink(filename)
