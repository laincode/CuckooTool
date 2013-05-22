#!/usr/bin/python
#
# Copyright (c) 2013/2016 lain <lain@braincakes.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     1) Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#     2) Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#     3) Neither the name of the <organization> nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import json
import urllib
import urllib2
from urllib2 import URLError, HTTPError
from multipartform import *


class Api(object):
    '''
    A python interface into the Cuckoo API
    
    >>> import cuckoo
    >>> api = cuckoo.Api()    
    '''   

    def __init__(self):
        self.host = "http://127.0.0.1:8090"

    def taskCreateFile(self,
                        file,
                        package=None,
                        timeout=None,
                        options=None,
                        machine=None,
                        platform=None,
                        custom=None,
                        memory=None,
                        enforce_timeout=None):
        '''
        Adds a file to the list of pending tasks to be processed and analyzed
        '''
        try:
            f = open(file, 'rb')
            form = MultiPartForm()
            form.add_file('file', file, fileHandle=f)
            if package is not None:
                form.add_field('package',package)
            if timeout is not None:
                form.add_field('timeout',timeout)
            if options is not None:
	        form.add_field('options',options)
            if machine is not None:
                form.add_field('machine',machine)
            if platform is not None:
                form.add_field('platform',platform)
            if custom is not None:
                form.add_field('custom',custom)
            if memory is True:
                form.add_field('memory',"True")
            if enforce_timeout is True:
                form.add_field('enforce_timeout',"True")
            body = str(form)
            self.uri = self.host + "/tasks/create/file"
            request = urllib2.Request(self.uri)
            request.add_header('User-agent', 'Cuckoo')
            request.add_header('Content-type', form.get_content_type())
            request.add_header('Content-length', len(body))
            request.add_data(body)
            response = urllib2.urlopen(request).read()
            responsedata = json.loads(response)
            task_id = responsedata["task_id"]
            return task_id
        except HTTPError as e:
            error = str(e.code)
            if "500" in error:
               return "SE"
        except URLError as u:
            error = str(u.reason)
            if "Operation timed out" in error:
               return "TO"
        except Exception as e:
            return "KO", e
		
    def taskCreateURL(self,
                        url,
                        package=None,
                        timeout=None,
                        options=None,
                        machine=None,
                        platform=None,
                        custom=None,
                        memory=None,
                        enforce_timeout=None):
        '''
        Adds a url to the list of pending tasks to be processed and analyzed
        '''
        try:
            form = MultiPartForm()
            if url is not None:
                form.add_field('url',url)
            if package is not None:
                form.add_field('package',package)
            if timeout is not None:
                form.add_field('timeout',timeout)
            if options is not None:
                form.add_field('options',options)
            if machine is not None:
                form.add_field('machine',machine)
            if platform is not None:
                form.add_field('platform',platform)
            if custom is not None:
                form.add_field('custom',custom)
            if memory is True:
                form.add_field('memory',"True")
            if enforce_timeout is True:
                form.add_field('enforce_timeout',"True")
            body = str(form)
            self.uri = self.host + "/tasks/create/url"
            request = urllib2.Request(self.uri)
            request.add_header('User-agent', 'Cuckoo')
            request.add_header('Content-type', form.get_content_type())
            request.add_header('Content-length', len(body))
            request.add_data(body)
            response = urllib2.urlopen(request).read()
            responsedata = json.loads(response)
            task_id = responsedata["task_id"]
            return task_id
        except HTTPError as e:
            error = str(e.code)
            if "500" in error:
               return "SE"
        except URLError as u:
            error = str(u.reason)
            if "Operation timed out" in error:
               return "TO"
        except Exception as e:
            return "KO"

    def taskList(self):
        '''
        Returns list of tasks
        '''
        try:
            self.uri = self.host + "/tasks/list"
            request = urllib2.Request(self.uri)
            request.add_header('User-agent', 'Cuckoo')
            response = urllib2.urlopen(request).read()
            responsedata = json.loads(response)
            return responsedata
        except HTTPError as e:
            error = str(e.code)
            if "500" in error:
               return "SE"
        except URLError as u:
            error = str(u.reason)
            if "Operation timed out" in error:
               return "TO"
        except Exception as e:
            return "KO"

    def taskView(self, id):
        '''
        Returns details on the task associated with the specified ID
        '''
        try:
            self.uri = self.host + "/tasks/view/" + id
            request = urllib2.Request(self.uri)
            request.add_header('User-agent', 'Cuckoo')
            response = urllib2.urlopen(request).read()
            responsedata = json.loads(response)
            return responsedata
        except HTTPError as e:
            error = str(e.code)
            if "500" in error:
               return "NF"
            if "404" in error:
               return "NF"
        except URLError as u:
            error = str(u.reason)
            if "Operation timed out" in error:
               return "TO"
        except Exception as e:
            return "KO"

    def taskDelete(self, id):
        '''
        Removes the given task from the database and deletes the results
        '''
        try:
            self.uri = self.host + "/tasks/delete/" + id
            request = urllib2.Request(self.uri)
            request.add_header('User-agent', 'Cuckoo')
            response = urllib2.urlopen(request).read()
            responsedata = json.loads(response)
            return responsedata["status"]
        except HTTPError as e:
            error = str(e.code)
            if "500" in error:
               return "NF"
            if "404" in error:
               return "NF"
        except URLError as u:
            error = str(u.reason)
            if "Operation timed out" in error:
               return "TO"
        except Exception as e:
            return "KO"     
    
    def fileView(self, value, type):
        '''
        Returns details on the file matching either the specified MD5 hash, SHA256 hash or ID
        '''
        try:
            if type is "md5":
                self.uri = self.host + "/files/view/md5/" + value
            if type is "sha256":
                self.uri = self.host + "/files/view/sha256/" + value
            if type is "id":
                self.uri = self.host + "/files/view/id/" + value
            request = urllib2.Request(self.uri)
            request.add_header('User-agent', 'Cuckoo')
            response = urllib2.urlopen(request).read()
            responsedata = json.loads(response)
            return responsedata
        except HTTPError as e:
            error = str(e.code)
            if "500" in error:
               return "NF"
            if "404" in error:
               return "NF"
            if "400" in error:
               return "ILT"
        except URLError as u:
            error = str(u.reason)
            if "Operation timed out" in error:
               return "TO"
        except Exception as e:
            return "KO"

    def machinesList(self):
        '''
        Returns a list with details on the analysis machines available to Cuckoo
        '''
        try:
            self.uri = self.host + "/machines/list"
            request = urllib2.Request(self.uri)
            request.add_header('User-agent', 'Cuckoo')
            response = urllib2.urlopen(request).read()
            responsedata = json.loads(response)
            return responsedata
        except HTTPError as e:
            error = str(e.code)
            if "500" in error:
               return "SE"
        except URLError as u:
            error = str(u.reason)
            if "Operation timed out" in error:
               return "TO"
        except Exception as e:
            return "KO"

    def machinesView(self,name):
        '''
        Returns details on the analysis machine associated with the given name
        '''
        try:
            if name is None:
                return "NF"
            self.uri = self.host + "/machines/view/" + name
            request = urllib2.Request(self.uri)
            request.add_header('User-agent', 'Cuckoo')
            response = urllib2.urlopen(request).read()
            responsedata = json.loads(response)
            return responsedata
        except HTTPError as e:
            error = str(e.code)
            if "500" in error:
               return "SE"
            if "404" in error:
               return "ILT"
        except URLError as u:
            error = str(u.reason)
            if "Operation timed out" in error:
               return "TO"
        except Exception as e:
            return "KO"

    def taskReport(self,id):
        '''
        Returns the report associated with the specified task ID
        '''
        try:
            if id is None:
                return "NF"
            self.uri = self.host + "/tasks/report/" + id
            request = urllib2.Request(self.uri)
            request.add_header('User-agent', 'Cuckoo')
            response = urllib2.urlopen(request).read()
            responsedata = json.loads(response)
            return responsedata
        except HTTPError as e:
            error = str(e.code)
            if "500" in error:
               return "SE"
            if "404" in error:
               return "NF"
        except URLError as u:
            error = str(u.reason)
            if "Operation timed out" in error:
               return "TO"
        except Exception as e:
            return "KO"
       
    def fileGet(self, sha256):
        '''
        Returns the binary content of the file matching the specified SHA256 hash
        '''   
        try:
            if sha256 is None:
                return "NF"
            self.uri = self.host + "/files/get/" + sha256
            request = urllib2.Request(self.uri)
            request.add_header('User-agent', 'Cuckoo')
            response = urllib2.urlopen(request).read()
            return response
        except HTTPError as e:
            error = str(e.code)
            if "500" in error:
               return "SE"
            if "404" in error:
               return "NF"
        except URLError as u:
            error = str(u.reason)
            if "Operation timed out" in error:
               return "TO"
        except Exception as e:
            return "KO"
        
    
    


    

