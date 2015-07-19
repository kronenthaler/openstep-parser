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

import unittest
import openstep_parser as osp

class Parsing(unittest.TestCase):
    def testParseNestedDictionary(self):
        line = '''{ a = { b = b1; }; };'''
        result = osp.OpenStepDecoder()._parse_dictionary(line, 0)
        assert result

    def testParseFileSample1(self):
        result = osp.OpenStepDecoder.ParseFromFile(open('tests/samples/music-cube.pbxproj'))
        assert result

    def testParseFileSample2(self):
        result = osp.OpenStepDecoder.ParseFromFile(open('tests/samples/cloud-search.pbxproj'))
        assert result

    def testParseFileSample3(self):
        result = osp.OpenStepDecoder.ParseFromFile(open('tests/samples/collection-view.pbxproj'))
        assert result

    def testParseFileSample4(self):
        result = osp.OpenStepDecoder.ParseFromFile(open('tests/samples/metal-image-processing.pbxproj'))
        assert result

    def testIgnoreWhitespacesFromBeginning(self):
        parser = osp.OpenStepDecoder()
        index = parser._ignore_whitespaces('   3 ', 0)
        assert index == 3

    def testIgnoreWhitespacesInTheMiddle(self):
        parser = osp.OpenStepDecoder()
        index = parser._ignore_whitespaces('0   3 ', 1)
        assert index == 4

    def testIsWhitespace(self):
        parser = osp.OpenStepDecoder()
        assert not parser._is_whitespace('a')
        assert not parser._is_whitespace('0')
        assert parser._is_whitespace('\t')
        assert parser._is_whitespace('\r')
        assert parser._is_whitespace('\n')
        assert parser._is_whitespace(' ')

    def testIgnoreComment(self):
        parser = osp.OpenStepDecoder()
        index = parser._ignore_comment('/*1234567890*/ ', 0)
        assert index == 14

    def testParsingKey(self):
        parser = osp.OpenStepDecoder()
        line = '    /* some comments */ KEY-NAME '
        key, index = parser._parse_key(line, 0)
        assert key == 'KEY-NAME'
        assert index == len(line)

    def testParsingKeyQuoted(self):
        parser = osp.OpenStepDecoder()
        line = '    /* some comments */ "KEY-NAME" '
        key, index = parser._parse_key(line, 0)
        assert key == 'KEY-NAME'
        assert index == len(line)

    def testDictionaryEntry(self):
        parser = osp.OpenStepDecoder()
        line = '    /* some comments */ KEY-NAME   /* asd */ =   /* adfasdf */  value-1234    /* adfasdf */   ;'
        result = {}
        index = parser._parse_dictionary_entry(line, 0, result)

        assert result['KEY-NAME'] == 'value-1234'

    def testDictionaryEntryMissingEqual(self):
        parser = osp.OpenStepDecoder()
        line = '    /* some comments */ KEY-NAME   /* asd */    /* adfasdf */  value-1234    /* adfasdf */   ;'
        result = {}
        try:
            index = parser._parse_dictionary_entry(line, 0, result)
            assert 1 == 0
        except Exception:
            pass

    def testDictionaryEntryMissingSemicolon(self):
        parser = osp.OpenStepDecoder()
        line = '    /* some comments */ KEY-NAME   /* asd */  =  /* adfasdf */  value-1234    /* adfasdf */   '
        result = {}
        try:
            index = parser._parse_dictionary_entry(line, 0, result)
            assert 1 == 0
        except Exception:
            pass

    def testArrayEntry(self):
        parser = osp.OpenStepDecoder()
        line = '    /* some comments */ KEY-NAME   /* asd */  , '
        result = []
        index = parser._parse_array_entry(line, 0, result)
        assert result[0] == 'KEY-NAME'
        assert len(result) == 1

    def testFullArray(self):
        parser = osp.OpenStepDecoder()
        line = '( ' \
               '    ABC,' \
               '    DEF,' \
               '    GHI,' \
               ')'
        result, index = parser._parse_array(line, 0)
        assert result[0] == 'ABC'
        assert result[1] == 'DEF'
        assert result[2] == 'GHI'

    def testParseWithComment(self):
        line = '// utf-8 \n{}'
        expected = {}
        result = osp.OpenStepDecoder.ParseFromString(line)
        assert result == expected


if __name__ == '__main__':
    unittest.main()