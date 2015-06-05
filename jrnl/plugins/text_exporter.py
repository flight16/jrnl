#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals
import codecs
from . import BaseExporter
from ..util import u, slugify
from ..Journal import pprint_journal
import os
from ..util import WARNING_COLOR, ERROR_COLOR, RESET_COLOR


class TextExporter(BaseExporter):
    """This Exporter can convert entries and journals into text files."""
    names = ["text", "txt"]
    extension = "txt"

    @classmethod
    def export_entry(cls, entry):
        """Returns a unicode representation of a single entry."""
        return u.__unicode__()

    @classmethod
    def export_journal(cls, journal, filter):
        """Returns a unicode representation of an entire journal."""
        return pprint_journal(journal, filter)

    @classmethod
    def write_file(cls, journal, filter, path):
        """Exports a journal into a single file."""
        try:
            with codecs.open(path, "w", "utf-8") as f:
                f.write(cls.export_journal(journal, filter))
                return "[Journal exported to {0}]".format(path)
        except IOError as e:
            return "[{2}ERROR{3}: {0} {1}]".format(e.filename, e.strerror, ERROR_COLOR, RESET_COLOR)

    @classmethod
    def make_filename(cls, entry):
        return entry.date.strftime("%Y-%m-%d_{0}.{1}".format(slugify(u(entry.title)), cls.extension))

    @classmethod
    def write_files(cls, journal, filter, path):
        """Exports a journal into individual files for each entry."""
        for entry in journal.filtered_entries(filter):
            try:
                full_path = os.path.join(path, cls.make_filename(entry))
                with codecs.open(full_path, "w", "utf-8") as f:
                    f.write(cls.export_entry(entry))
            except IOError as e:
                return "[{2}ERROR{3}: {0} {1}]".format(e.filename, e.strerror, ERROR_COLOR, RESET_COLOR)
        return "[Journal exported to {0}]".format(path)

    @classmethod
    def export(cls, journal, filter, output=None):
        """Exports to individual files if output is an existing path, or into
        a single file if output is a file name, or returns the exporter's
        representation as unicode if output is None."""
        if output and os.path.isdir(output):  # multiple files
            return cls.write_files(journal, filter, output, filter)
        elif output:                          # single file
            return cls.write_file(journal, filter, output, filter)
        else:
            return cls.export_journal(journal, filter)
