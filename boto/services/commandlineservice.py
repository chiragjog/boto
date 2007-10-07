# Copyright (c) 2006,2007 Mitch Garnaat http://garnaat.org/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from boto.services.service import Service
import popen2, os, StringIO

class CommandLineService(Service):

    def log_command(self, output_fp):
        log_file_name = self.__class__.__name__ + '.log'
        log_file_name = os.path.join(self.working_dir, log_file_name)
        log_fp = open(log_file_name, 'a')
        output_fp.seek(0)
        log_fp.write(output_fp.read())
        log_fp.close()
        output_fp.close()
        
    def run_command(self, command, msg):
        log_fp = StringIO.StringIO()
        log_fp.write('\n---------------------------\n')
        log_fp.write('running:\n%s\n' % command)
        p = popen2.Popen4(command)
        status = p.wait()
        log_fp.write(msg.get_body())
        log_fp.write('\n')
        log_fp.write(p.fromchild.read())
        log_fp.write('\n')
        exit_code = os.WEXITSTATUS(status)
        # only log unsuccessful commands
        if exit_code != 0:
            self.log_command(log_fp)
        return exit_code
        