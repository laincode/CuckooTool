#!/usr/bin/python
#
# Copyright (c) 2013/2017 lain
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

import os
import sys
import hashlib
import optparse
import cuckooapi


class CuckooMain:

    def __init__(self):
        self.ini = ""   
 
    def submitFile(self, file, package=None, timeout=None, options=None, machine=None, platform=None, custom=None, memory=None, enforce_timeout=None):
        api = cuckooapi.Api()
        task_id = api.taskCreateFile(file=file, package=package, timeout=timeout, options=options, machine=machine, platform=platform, custom=custom, memory=memory, enforce_timeout=enforce_timeout)
        if task_id is "TO" or task_id is None:
            print "Error - Connection timeout"
        elif task_id is "SE":
            print "Error - Review parameters"
        elif task_id is "KO":
            print "Error - Non Controlled error"
        else:
            print "-------------------------------------------"
            print "File:", file
            print "Submit OK - Task ID:", task_id 
            print "-------------------------------------------"

    def submitDir(self, dir, package=None, timeout=None, options=None, machine=None, platform=None, custom=None, memory=None, enforce_timeout=None):
        if dir[-1] is not "/":
            dir = dir + "/"
        api = cuckooapi.Api()
        print "-------------------------------------------"
        print "Directory:", dir
        print "-------------------------------------------"
        files = os.listdir(dir)
        for f in files:
            file = dir + f
            task_id = api.taskCreateFile(file=file, package=package, timeout=timeout, options=options, machine=machine, platform=platform, custom=custom, memory=memory, enforce_timeout=enforce_timeout)
            if task_id is "TO" or task_id is None:
                print "Error - Connection timeout"
                sys.exit(1)
            elif task_id is "SE":
                print "Error - Review parameters"
                sys.exit(1)
            elif task_id is "KO":
                print "Error - Non Controlled error"
                sys.exit(1)
            else:    
                print "File:", file
                print "Submit OK - Task ID:", task_id        
                print "-------------------------------------------"

    def submitURL(self, url, package=None, timeout=None, options=None, machine=None, platform=None, custom=None, memory=None, enforce_timeout=None):
        api = cuckooapi.Api()
        task_id = api.taskCreateURL(url=url, package=package, timeout=timeout, options=options, machine=machine, platform=platform, custom=custom, memory=memory, enforce_timeout=enforce_timeout)
        if task_id is "TO" or task_id is None:
            print "Error - Connection timeout"
        elif task_id is "SE":
            print "Error - Review parameters"
        elif task_id is "KO":
            print "Error - Non Controlled error"
        else:
            print "-------------------------------------------"
            print "URL:", url
            print "Submit OK - Task ID:", task_id
            print "-------------------------------------------"

    def taskDelete(self, id):
        api = cuckooapi.Api()
        result = api.taskDelete(id=id)
        if result is "NF":
            print "Error - Unable to delete the task"
        elif result is "TO" or result is None:
            print "Error - Connection timeout"
        elif result is "KO":
            print "Error - Non controlled error"
        else:
            print "-------------------------------------------"
            print "Task ID:", id, "removed", result
            print "-------------------------------------------"


    def taskFilesView(self, md5=None, sha256=None, id=None):
        api = cuckooapi.Api()
        if md5 is not None:
            result = api.fileView(value=md5, type="md5")
        if sha256 is not None:
            result = api.fileView(value=sha256, type="sha256")
        if id is not None:
            result = api.fileView(value=id, type="id")
        if result is "NF":
            print "Error - File not found"
        elif result is "ILT":
            print "Error - Invalid lookup term"
        elif result is "TO" or result is None:
            print "Error - Operation timeout"
        elif result is "KO":
            print "Error - Non controlled error"
        else: 
            print "-------------------------------------------"
            print "Sample ID: ", result["sample"].get("id") 
            print "SHA1: ", result["sample"].get("sha1")
            print "SHA256: ", result["sample"].get("sha256")
            print "SHA512: ", result["sample"].get("sha512")
            print "MD5: ", result["sample"].get("md5")
            print "CRC32: ", result["sample"].get("crc32")
            print "SSDeep: ", result["sample"].get("ssdeep")
            print "File type: ", result["sample"].get("file_type")
            print "File size: ", result["sample"].get("file_size")
            print "-------------------------------------------"

    def taskView(self, id):
        api = cuckooapi.Api()
        result = api.taskView(id=id)
        if result is "NF":
            print "Error - Task not found"
        elif result is "TO" or result is None:
            print "Error - Connection timeout"
        elif result is "KO":
            print "Error - Non controlled error"
        else:
            print "-------------------------------------------"
            print "Task ID: ", result["task"].get("id")
            print "Target: ", result["task"].get("target")
            print "Category: ", result["task"].get("category")
            print "Priority: ", result["task"].get("priority")
            print "Package: ", result["task"].get("package")
            print "Memory: ", result["task"].get("memory")
            print "Custom: ", result["task"].get("custom")
            print "Machine: ", result["task"].get("machine")
            print "Platform: ", result["task"].get("platform")
            print "Added on: ", result["task"].get("added_on")
            print "Started on: ", result["task"].get("started_on")
            print "Shutdown on: ", result["task"].get("guest").get("shutdown_on")
            print "Completed on: ", result["task"].get("completed_on")
            print "Enforce timeout: ", result["task"].get("enforce_timeout")
            print "Timeout: ", result["task"].get("timeout")
            print "Options: ", result["task"].get("options")
            print "Manager: ", result["task"].get("guest").get("manager")
            print "Name: ", result["task"].get("guest").get("name")
            print "Status: ", result["task"].get("status")
            if len(result["task"].get("errors")) > 0:
                print "Errors: ", result["task"].get("errors").pop()
            print "-------------------------------------------"

    def taskList(self):
        api = cuckooapi.Api()
        result = api.taskList()
        if result is "TO" or result is None:
            print "Error - Connection timeout"
        elif result is "SE":
            print "Error - Server Error"
        elif result is "KO":
            print "Error - Non controlled error"
        else:
            tasklist = result["tasks"]
            if len(tasklist) == 0:
                print "Error - Task list is empty"
            else:
                print "-------------------------------------------"
                for t in tasklist:
                    print "Task ID: ", t.get("id")
                    print "Target: ", t.get("target")
                    print "Category: ", t.get("category")
                    print "Priority: ", t.get("priority")
                    print "Package: ", t.get("package")
                    print "Memory: ", t.get("memory")
                    print "Custom: ", t.get("custom")
                    print "Machine: ", t.get("machine")
                    print "Platform: ", t.get("platform")
                    print "Added_on: ", t.get("added_on")
                    print "Started on: ", t.get("started_on")
                    print "Shutdown on: ", t.get("guest").get("shutdown_on")
                    print "Completed on: ", t.get("completed_on")
                    print "Enforce timeout: ", t.get("enforce_timeout")
                    print "Timeout: ", t.get("timeout")
                    print "Options: ", t.get("options")
                    print "Manager: ", t.get("guest").get("manager")
                    print "Name: ", t.get("guest").get("name")
                    print "Status: ", t.get("status")
                    if len(t.get("errors")) > 0:
                        print "Errors: ", t.get("errors").pop()
                    print "-------------------------------------------"

    def taskReport(self, id):
        api = cuckooapi.Api()
        result = api.taskReport(id)
        if result is "TO" or result is None:
            print "Error - Connection timeout"
        elif result is "SE":
            print "Error - Server Error"
        elif result is "KO":
            print "Error - Non controlled error"
        elif result is "NF":
            print "Error - Report not found"
        else:   
            print "-------------------------------------------"
            print "-- Info --"
            print "Report ID: ", result["info"].get("id")
            print "Category: ", result["info"].get("category")
            print "Started: ", result["info"].get("started")
            print "Ended: ", result["info"].get("ended")
            print "Version: ", result["info"].get("version")
            print "Duration: ", result["info"].get("duration")
            print ""
            print "Signatures: ", result["signatures"]
            print "Static: ", result["static"]
            print "Dropped: ", result["dropped"]
            print ""
            print "-- Behavior --"
            print "Processes: ", result["behavior"].get("processes")
            print "Processtree: ", result["behavior"].get("processtree")
            print "Files: ", result["behavior"].get("summary").get("files")
            print "Keys: ", result["behavior"].get("summary").get("keys")
            print "Mutexes: ", result["behavior"].get("summary").get("mutexes")
            print ""
            print "-- Target --"
            print "Category: ", result["target"].get("category")
            print "Name: ", result["target"].get("file").get("name")
            print "Type: ", result["target"].get("file").get("type")
            print "Path: ", result["target"].get("file").get("path")
            print "Size: ", result["target"].get("file").get("size")
            print "SHA1: ", result["target"].get("file").get("sha1")
            print "SHA256: ", result["target"].get("file").get("sha256")
            print "SHA512: ", result["target"].get("file").get("sha512")
            print "CRC32: ", result["target"].get("file").get("crc32")
            print "SSDeep: ", result["target"].get("file").get("ssdeep")
            print "MD5: ", result["target"].get("file").get("md5")
            print "Yara: ", result["target"].get("file").get("yara")
            print ""
            print "-- Debug --"
            print "Errors: ", result["debug"].get("errors")
            print "Log: ", result["debug"].get("log")
            print ""
            print "Strings: ", result["strings"]
            print ""
            print "Network: ", result["network"] 
        
    def getFile(self,sha256):
        try:
            api = cuckooapi.Api()
            result = api.fileGet(sha256=sha256)
            if result is "TO" or result is None:
                print "Error - Connection timeout"
            elif result is "SE":
                print "Error - Server Error"
            elif result is "KO":
                print "Error - Non controlled error"
            elif result is "NF":
                print "Error - File not found"
            else:
                name = sha256 + ".bin"
                file = open(name,"wb")
                file.write(result)
                file.close()
                print "File is saved as: ", name
        except Exception:
            print "Error - Getting File", e   
        
    def machineList(self):
        api = cuckooapi.Api()
        result = api.machinesList()
        if result is "TO" or result is None:
            print "Error - Connection timeout"
        elif result is "SE":
            print "Error - Server Error"
        elif result is "KO":
            print "Error - Non controlled error"
        else:
            machineslist = result["machines"]
            if len(machineslist) == 0:
                print "Error - Machines list is empty"
            else:
                print "-------------------------------------------"
                for m in machineslist:
                    print "Machine ID: ", m.get("id")
                    print "Name: ", m.get("name")
                    print "Label: ", m.get("label")
                    print "Platform: ", m.get("platform")
                    print "IP: ", m.get("ip")
                    print "Status: ", m.get("status")
                    print "Status changed on: ", m.get("status_changed_on")
                    print "Locked: ", m.get("locked")
                    print "Locked changed on: ", m.get("locked_changed_on")
                    print "-------------------------------------------"

    def machineView(self,name):
        api = cuckooapi.Api()
        result = api.machinesView(name=name)
        if result is "NF":
            print "Error - Machine not found"
        elif result is "TO" or result is None:
            print "Error - Connection timeout"
        elif result is "KO":
            print "Error - Non controlled error"
        elif result is "SE":
            print "Error - Machine not found"
        elif result is "ILT":
            print "Error - Machine not found"
        else:
            print "-------------------------------------------"
            print "Machine ID: ", result["machine"].get("id")
            print "Name: ", result["machine"].get("name")
            print "Label: ", result["machine"].get("label")
            print "Platform: ", result["machine"].get("platform")
            print "IP: ", result["machine"].get("ip")
            print "Status: ", result["machine"].get("status")
            print "Status changed on: ", result["machine"].get("status_changed_on")
            print "Locked: ", result["machine"].get("locked")
            print "Locked changed on: ", result["machine"].get("locked_changed_on")
            print "-------------------------------------------"

    def isvalidMachine(self,machine):
        api = cuckooapi.Api()
        result = api.machinesList()
        if result is "TO" or result is None:
            print "Error - Connection timeout"
        elif result is "SE":
            print "Error - Server Error"
        elif result is "KO":
            print "Error - Non controlled error"
        else:
            machineslist = result["machines"]
            valid = False
            if len(machineslist) == 0:
                return valid
            else:
                for m in machineslist:
                   name = m.get("name")
                   if name == machine:
                       valid = True
                return valid
                    
    def isvalidPlatform(self,platform):
        valid = False
        if platform == "windows" or platform == "darwin" or platform == "linux":    
           valid = True
        return valid

    def isavailablePlatform(self,platform):
        api = cuckooapi.Api()
        result = api.machinesList()
        if result is "TO" or result is None:
            print "Error - Connection timeout"
        elif result is "SE":
            print "Error - Server Error"
        elif result is "KO":
            print "Error - Non controlled error"
        else:
            machineslist = result["machines"]
            valid = False
            if len(machineslist) == 0:
                return valid
            else:
                for m in machineslist:
                   name = m.get("platform")
                   if name == platform:
                       valid = True
                return valid


if __name__ == "__main__":

    usage = "usage: python %prog [options] "

    parser = optparse.OptionParser()
    parser.set_usage(usage)

    parser.add_option("-s", "--submit", dest="submit", action="store_true", help="Submit a file/directory for analysis", default=None)
    parser.add_option("-l", "--tasklist", dest="tasklist", action="store_true", help="Returns list of tasks", default=None)
    parser.add_option("-v", "--view", dest="view", action="store_true", help="Returns details on the file matching either the specified MD5 hash, SHA256 hash or ID", default=None)
    parser.add_option("--remove", dest="remove", action="store", help="Removes the given task from the database and deletes the results", default=None)
    parser.add_option("--taskview", dest="taskview", action="store", help="Returns details on the task associated with the specified ID", default=None)
    parser.add_option("--report", dest="taskreport", action="store", help="Returns the report associated with the specified task ID", default=None)
    parser.add_option("--getfile", dest="getfile", action="store", help="Returns the binary content of the file matching the specified SHA256 hash", default=None)
    parser.add_option("--machinelist", dest="machinelist", action="store_true", help="Returns a list with details on the analysis machines available to Cuckoo")
    parser.add_option("--machineview", dest="machineview", action="store", help="Returns details on the analysis machine associated with the given name", default=None)
 
    submitoptions = optparse.OptionGroup(parser, "Submit Options")
    submitoptions.add_option("--file", action="store", help="File path to submit")
    submitoptions.add_option("--dir", action="store", help="Directory path to submit")
    submitoptions.add_option("--url", action="store", help="URL to analyze")
    parser.add_option_group(submitoptions)
    
    fileoptions = optparse.OptionGroup(parser, "File/Directory Options [Optional]")
    fileoptions.add_option("--package", action="store", help="Analysis package to be used for the analysis")
    fileoptions.add_option("--timeout", action="store", help="Priority to assign to the task (1-3)")
    fileoptions.add_option("--options", action="store", help="Options to pass to the analysis package")
    fileoptions.add_option("--machine", action="store", help="Machine name to use for the analysis")
    fileoptions.add_option("--custom", action="store", help="Custom string to pass over the analysis and the processing/reporting modules")
    fileoptions.add_option("--memory", action="store_true", help="Enable the creation of a full memory dump of the analysis machine")
    fileoptions.add_option("--enforce_timeout", action="store_true", help="Enable to enforce the execution for the full timeout value")
    fileoptions.add_option("--platform", action="store", help="Name of the platform to select the analysis machine (windows/darwin/linux)")
    parser.add_option_group(fileoptions)

    viewoptions = optparse.OptionGroup(parser, "View Files Options")
    viewoptions.add_option("--md5", action="store", help="File md5", default=None)
    viewoptions.add_option("--sha256", action="store", help="File sha256", default=None)
    viewoptions.add_option("--id", action="store", help="File ID", default=None)
    parser.add_option_group(viewoptions)

    (options,args) = parser.parse_args()

    package = None
    timeout = None
    option = None
    machine = None
    platform = None
    custom = None
    memory = None
    enforce_timeout = None

    cuckoo = CuckooMain()

    if options.submit != None:
        if options.package is not None:
            package = options.package
        if options.timeout is not None:
            try:
                (options.timeout == int(options.timeout))
                timeout = options.timeout
            except ValueError:
                print "Error - Timeout is not valid integer value"
                sys.exit(1)
        if options.options is not None:
            option = options.options
        if options.machine is not None:
            if cuckoo.isvalidMachine(options.machine) is True:
                machine = options.machine
            else:
                print "Error - Machine name is not valid"
                sys.exit(1)
        if options.platform is not None:
            if cuckoo.isvalidPlatform(options.platform) is True:
                if cuckoo.isavailablePlatform(options.platform) is True:
                    platform = options.platform
                else:
                    print "Error - Platform type is not available. Try another one."
                    sys.exit(1)
            else:
                print "Error - Platform name is not valid"
                sys.exit(1)
        if options.custom is not None:
            custom = options.custom
        if options.memory is True:
            memory = options.memory
        if options.enforce_timeout is True:
            enforce_timeout = options.enforce_timeout 
        if options.file != None:
            if os.path.isfile(options.file):
                cuckoo.submitFile(file=options.file, package=package, timeout=timeout, options=option, machine=machine, platform=platform, custom=custom, memory=memory, enforce_timeout=enforce_timeout)
            else:
                print "Error - File path doesn't exist"
                sys.exit(1)     
        elif options.dir != None:
            if os.path.isdir(options.dir):
                cuckoo.submitDir(dir=options.dir, package=package, timeout=timeout, options=option, machine=machine, platform=platform, custom=custom, memory=memory, enforce_timeout=enforce_timeout)
            else:
                print "Error - Directory path doesn't exist"
                sys.exit(1)
        elif options.url != None:
            cuckoo.submitURL(url=options.url, package=package, timeout=timeout, options=option, machine=machine, platform=platform, custom=custom, memory=memory, enforce_timeout=enforce_timeout)
        else: 
            print "Review submit options"
    elif options.remove != None:
        cuckoo.taskDelete(id=options.remove)  
    elif options.view is True:
        if options.md5 is not None:
            cuckoo.taskFilesView(md5=options.md5)
        elif options.sha256 is not None:
            cuckoo.taskFilesView(sha256=options.sha256)
        elif options.id is not None:
            cuckoo.taskFilesView(id=options.id)
        else:
            print "Error - Review view file options"
    elif options.taskview is not None:
        cuckoo.taskView(id=options.taskview)
    elif options.tasklist is True:
        cuckoo.taskList()
    elif options.taskreport is not None:
        cuckoo.taskReport(id=options.taskreport)
    elif options.getfile is not None:
        cuckoo.getFile(sha256=options.getfile)
    elif options.machinelist is True:
        cuckoo.machineList()
    elif options.machineview is not None:
        cuckoo.machineView(name=options.machineview)
    else:
        parser.print_help()
        print ""
        sys.exit(1) 


