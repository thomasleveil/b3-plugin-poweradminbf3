# -*- encoding: utf-8 -*-
import sys
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from mock import Mock # http://www.voidspace.org.uk/python/mock/mock.html
from poweradminbf3 import Poweradminbf3Plugin


class Test_issue_17_load_server_config(unittest.TestCase):

    def setUp(self):
        self.console = Mock()
        self.p = Poweradminbf3Plugin(self.console)

    def test_write_cvars_no_result(self):
        self.console.write.return_value = []
        self.p = self.p
        client = Mock()
        self.p.load_server_config(client, "theConfName", (
            "## some comment line",
            "",
            ' vars.serverMessage "Welcome to our Server Play as a team" ',
            "   ",
        ))
        self.assertEqual(1,self.console.write.call_count)
        self.console.write.assert_any_call(('vars.serverMessage', '"Welcome to our Server Play as a team"'))


if __name__ == '__main__':
    unittest.main(verbosity=2)