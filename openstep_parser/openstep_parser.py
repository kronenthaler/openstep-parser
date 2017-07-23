# Copyright (c) 2015, Ignacio Calderon
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object
import re


class OpenStepDecoder(object):
    @classmethod
    def ParseFromFile(cls, fp):
        return cls.ParseFromString(fp.read())

    @classmethod
    def ParseFromString(cls, str):
        return OpenStepDecoder()._parse(str)

    def _parse(self, str):
        # parse the comment if any
        index = 0
        if str[0] == '/' and str[1] == '/':
            while str[index] != '{':
                index += 1

        result, index = self._parse_dictionary(str, index)
        return result

    def _parse_dictionary(self, str, index):
        obj = {}

        if str[index] != '{':
            raise Exception("Expected { as dictionary start")

        index = self._parse_padding(str, index + 1)

        while str[index] != '}':
            index = self._parse_dictionary_entry(str, index, obj)
            index = self._parse_padding(str, index)

        index = self._parse_padding(str, index + 1)

        return obj, index

    def _parse_array(self, str, index):
        obj = []

        if str[index] != '(':
            raise Exception("Expected ( as dictionary start")

        index = self._parse_padding(str, index + 1)
        while str[index] != ')':
            index = self._parse_array_entry(str, index, obj)
            index = self._parse_padding(str, index)

        index = self._parse_padding(str, index + 1)

        return obj, index

    def _parse_dictionary_entry(self, str, index, dictionary):
        # adds a entry to the given dictionary
        key, index = self._parse_key(str, index)

        if str[index] != '=':
            raise Exception("Expected = after a key. Found {1} @ {0}".format(index, str[index]))

        index = self._parse_padding(str, index + 1)
        value, index = self._parse_value(str, index)

        if str[index] != ';':
            raise Exception("Expected ; after a value. Found {1} @ {0}".format(index, str[index]))

        dictionary[key] = value
        return index + 1

    def _parse_array_entry(self, str, index, array):
        # parse a: dict, array or value until the ','
        value, index = self._parse_value(str, index)

        if str[index] != ',':
            raise Exception("Expected , after a value. Found {1} @ {0} = {2}".format(index, str[index], value))

        array.append(value)
        return index + 1

    def _parse_padding(self, str, index):
        index = self._ignore_whitespaces(str, index)
        index = self._ignore_comment(str, index)
        index = self._ignore_whitespaces(str, index)
        return index

    def _parse_key(self, str, index):
        # returns the key and the last index.
        index = self._parse_padding(str, index)

        key = ''
        while index < len(str) and not self._is_whitespace(str[index]) and str[index] != ';':
            key += str[index]
            index += 1

        index = self._parse_padding(str, index)
        key = re.sub(r'^"', '', key)
        key = re.sub(r'"$', '', key)
        return key, index

    def _parse_literal(self, str, index):
        # returns the key and the last index.
        index = self._parse_padding(str, index)
        key = ''

        if str[index] == '"':
            index += 1
            # if the literal starts with " then spaces are allowed
            escaped = False
            while index < len(str) and (escaped or str[index] != '"'):
                d = {'"': '"', "'": "'", "0": "\0", "\\": "\\", "n": "\n", "t": "\t"}
                if escaped:
                    key += d[str[index]]
                    escaped = False
                elif not escaped and str[index] == '\\':
                    escaped = True
                else:
                    key += str[index]
                    escaped = False
                index += 1
            index += 1
        else:
            # otherwise stop in the spaces.
            while index < len(str) and not self._is_whitespace(str[index]) and str[index] != ';' and str[index] != ',':
                key += str[index]
                index += 1

        index = self._parse_padding(str, index)
        return key, index

    def _parse_value(self, str, index):
        # return an object depending on the value of the first character.

        if str[index] == '{':
            value, index = self._parse_dictionary(str, index)
        elif str[index] == '(':
            value, index = self._parse_array(str, index)
        else:
            value, index = self._parse_literal(str, index)

        return value, index

    def _ignore_comment(self, str, index):
        # moves the index, to the next character after the close of the comment

        if index + 1 >= len(str) or (str[index] != '/' or str[index + 1] != '*'):
            return index

        # move after the first character in the comment
        index += 2

        while not (str[index] == '*' and str[index + 1] == '/'):
            index += 1

        # move after the first character after the comment
        index += 2

        return index

    def _ignore_whitespaces(self, str, index):
        while index < len(str) and self._is_whitespace(str[index]):
            index += 1

        return index

    def _is_whitespace(self, char):
        return char == ' ' or \
               char == '\t' or \
               char == '\n' or \
               char == '\r'
