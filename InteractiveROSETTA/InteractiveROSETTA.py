#!/usr/bin/python
# ================================================================================================================
# DSSP License Agreement (http://swift.cmbi.ru.nl/gv/dssp)
#
# Boost Software License - Version 1.0 - August 17th, 2003 Permission is hereby granted, free of charge, 
# to any person or organization obtaining a copy of the software and accompanying documentation covered 
# by this license (the "Software") to use, reproduce, display, distribute, execute, and transmit the 
# Software, and to prepare derivative works of the Software, and to permit third-parties to whom the 
# Software is furnished to do so, all subject to the following: 
#
# The copyright notices in the Software and this entire statement, including the above license grant, this 
# restriction and the following disclaimer, must be included in all copies of the Software, in whole or 
# in part, and all derivative works of the Software, unless such copies or derivative works are solely in 
# the form of machine-executable object code generated by a source language processor. 
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. 
# IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR 
# OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ================================================================================================================
# MUSCLE Public Domain Notice (http://www.drive5.com/muscle/manual/license.html)
#
# The MUSCLE software, including object and source code and documentation, is hereby donated to the public domain. 
#
# Disclaimer of warranty
# THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT 
# LIMITATION IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# ================================================================================================================
# BioPython License (http://biopython.org/DIST/LICENSE)
#
# Permission to use, copy, modify, and distribute this software and its
# documentation with or without modifications and for any purpose and
# without fee is hereby granted, provided that any copyright notices
# appear in all copies and that both those copyright notices and this
# permission notice appear in supporting documentation, and that the
# names of the contributors or copyright holders not be used in
# advertising or publicity pertaining to distribution of the software
# without specific prior permission.

# THE CONTRIBUTORS AND COPYRIGHT HOLDERS OF THIS SOFTWARE DISCLAIM ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL THE
# CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY SPECIAL, INDIRECT
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
# OR PERFORMANCE OF THIS SOFTWARE.
# ================================================================================================================
# wxPython License (http://www.wxwidgets.org/about/licence)
#
# WXWINDOWS LIBRARY LICENCE 
# TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 
#
# This library is free software; you can redistribute it and/or modify it under the terms of the GNU Library General 
# Public Licence as published by the Free Software Foundation; either version 2 of the Licence, or (at your option) 
# any later version. 
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Library General Public Licence for more details. 
#
# You should have received a copy of the GNU Library General Public Licence along with this software, usually in a file named 
# COPYING.LIB. If not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA. 
# 
# EXCEPTION NOTICE 
#
# 1. As a special exception, the copyright holders of this library give permission for additional uses of the text contained 
# in this release of the library as licenced under the wxWindows Library Licence, applying either version 3 of the Licence, 
# or (at your option) any later version of the Licence as published by the copyright holders of version 3 of the Licence document. 
#
# 2. The exception is that you may use, copy, link, modify and distribute under the user's own terms, binary object code 
# versions of works based on the Library. 
#
# 3. If you copy code from files distributed under the terms of the GNU General Public Licence or the GNU Library General 
# Public Licence into a copy of this library, as this licence permits, the exception does not apply to the code that you add 
# in this way. To avoid misleading anyone as to the status of such modified files, you must delete this exception notice from 
# such code and/or adjust the licensing conditions notice accordingly. 
#
# 4. If you write modifications of your own for this library, it is your choice whether to permit this exception to apply to 
# your modifications. If you do not wish that, you must delete the exception notice from such code and/or adjust the licensing 
# conditions notice accordingly.
# ================================================================================================================
# Open Source Software Used
#
# PyMOL (Open Source Version Used)
# OpenBabel

def cleanUp():
    # Delete any input/output files from a last run because if these are still hanging around from
    # last time they can really screw things up
    goToSandbox()
    # Remove the input files
    tempfiles = glob.glob("*input")
    for tempfile in tempfiles:
        os.remove(tempfile)
    # Remove the output files
    tempfiles = glob.glob("*output")
    for tempfile in tempfiles:
        os.remove(tempfile)
    tempfiles = glob.glob("*temp")
    for tempfile in tempfiles:
        try:
            os.remove(tempfile)
        except:
            pass
    # Remove the sandbox PDBs
    tempfiles = glob.glob("*.pdb")
    for tempfile in tempfiles:
        os.remove(tempfile)
    # Remove the progress files
    tempfiles = glob.glob("*progress")
    for tempfile in tempfiles:
        os.remove(tempfile)
    # Remove the sandbox archives
    tempfiles = glob.glob("*.ensb")
    for tempfile in tempfiles:
        os.remove(tempfile)

def importModules(wxpython=False):
    # This is a function for finding and importing modules
    # Sometimes the extra Python packages get installed in weird places, most especially on OSX
    # For Windows, everything is packaged into that Python install so we shouldn't have problems on Windows
    # First let's find out if PYROSETTA_DATABASE is set, and figure out what it should be if not
    if (not(wxpython)):
        try:
            # Is PYROSETTA_DATABASE defined?
            # If not, then we don't know where PyRosetta is and have to look for it
            s = os.environ["PYROSETTA_DATABASE"]
            if (len(s) == 0):
                raise Exception
        except:
            # Let's find it
            # Did we find it already and save it?
            if (platform.system() == "Windows"):
                cfgfile = os.path.expanduser("~") + "/InteractiveROSETTA/seqwindow.cfg"
            else:
                cfgfile = os.path.expanduser("~") + "/.InteractiveROSETTA/seqwindow.cfg"
            try:
                f = open(cfgfile.strip(), "r")
                rosettadir = "Not Found"
                rosettadb = "Not Found"
                for aline in f:
                    if ("[ROSETTAPATH]" in aline):
                        rosettapath = aline.split("\t")[1].strip()
                    if ("[ROSETTADB]" in aline):
                        rosettadb = aline.split("\t")[1].strip()
                f.close()
                if (rosettapath == "Not Found"):
                    # It wasn't saved there
                    raise Exception
                else:
                    # Let's try this saved path
                    # On Windows you have to cd to where the folder is to import, because appending to the
                    # path does not appear to work
                    sys.path.append(rosettapath)
                    if (platform.system() == "Windows"):
                        olddir = os.getcwd()
                        os.chdir(rosettapath)
                    os.environ["PYROSETTA_DATABASE"] = rosettadb
                    if (platform.system() == "Windows"):
                        olddir = os.getcwd()
                        os.chdir(olddir)
            except:
                # We didn't save it or the saved location was bad
                # The error may have been the Rosetta import, which means the file needs to be closed
                try:
                    f.close()
                except:
                    pass
                # Tell the user we're busy looking for PyRosetta
                import wx
                busyDlg = wx.BusyInfo("Searching for PyRosetta installation, please be patient...")
                # Okay, we still didn't get it, so let's traverse the filesystem looking for it...
                foundIt = False
                if (platform.system() == "Windows"):
                    roots = ["C:\\"]
                elif (platform.system() == "Darwin"):
                    # To avoid long searches on Mac
                    roots = ["/Users", "/Applications", "/"]
                else:
                    roots = ["/"]
                for root in roots:
                    for dpath, dnames, fnames in os.walk(root):
                        try:
                            if (platform.system() == "Windows"):
                                # On Windows, we expect the PyRosetta folder to have either rosetta.pyd
                                # or rosetta.dll in the folder
                                try:
                                    indx = fnames.index("rosetta.pyd") # 64bit
                                except:
                                    indx = fnames.index("rosetta.dll") # 32bit
                            else:
                                # On Mac/Linux, there should be a libmini file in the folder
                                # On Mac, it's libmini.dylib, on Linux it's libmini.so
                                indx = dnames.index("rosetta")
                                files = glob.glob(dpath + "/rosetta/*libmini*")
                                if (len(files) == 0):
                                    raise Exception
                        except:
                            continue
                        # If we got this far, then we found a candidate PyRosetta folder
                        # Is the database in this folder also?
                        # It is either called "database" or "rosetta_database"
                        foundIt = True
                        rosettapath = dpath
                        for dname in dnames:
                            if ("database" in dname):
                                rosettadb = dpath + "/" + dname
                                break
                        break
                    if (foundIt):
                        break
                busyDlg = None
                if (foundIt):
                    # Let's try to import what we found
                    # Remember on Windows we have to cd
                    sys.path.append(rosettapath)
                    if (platform.system() == "Windows"):
                        olddir = os.getcwd()
                        os.chdir(rosettapath)
                    os.environ["PYROSETTA_DATABASE"] = rosettadb
                    try:
                        # Now let's save these paths so the next time this gets started we don't have to traverse the filesystem again
                        data = []
                        f = open(cfgfile, "r")
                        for aline in f:
                            if (not("[ROSETTAPATH]" in aline) and not("[ROSETTADB]") in aline):
                                data.append(aline.strip())
                        f.close()
                        f = open(cfgfile, "w")
                        for aline in data:
                            f.write(aline + "\n")
                        f.write("[ROSETTAPATH]\t" + rosettapath.strip() + "\n")
                        f.write("[ROSETTADB]\t" + rosettadb.strip() + "\n")
                        f.close()
                        if (platform.system() == "Windows"):
                            olddir = os.getcwd()
                            os.chdir(olddir)
                    except:
                        # Can't find it, it's probably not installed or it's in a hidden location
                        print "PyRosetta cannot be found on your system!"
                        print "Until you install PyRosetta, you may only use InteractiveROSETTA to visualize structures in PyMOL"
                        exit()
    # Attempt to locate other packages that may not be on the PYTHONPATH
    if (platform.system() == "Windows"):
        # We want to import wxPython a bit earlier than the others, to display graphics for the license agreement
        # On Windows, everything should already be in the Python package, so don't try to find anything
        # If there are issues, the user should reinstall InteractiveROSETTA
        if (wxpython):
            import wx
        else:
            import numpy
            import pymol
            import psutil
            #import requests
            import poster
            import Bio
            import openbabel
    else:
        if (platform.system() == "Darwin"):
            # These are the standard locations for some of these things, hopefully we'll get these right away
            # These are the paths that are used in the bash installer
            sys.path.append("/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages")
            sys.path.append("/usr/local/Cellar/open-babel/HEAD/lib/python2.7/site-packages")
        # Again, here's the option for either importing wx only, or all the modules
        if (wxpython):
            modules = ["wx"]
        else:
            modules = ["numpy", "pymol", "psutil", "poster", "Bio", "openbabel"]
        notfound = []
        # Try to import each of the modules and keep track of which ones throw an error
        for module in modules:
            try:
                mod = __import__(module)
            except:
                notfound.append(module)
        # For everything that is not found, let's first see if we've saved a location and try to import from there
        cwd = os.getcwd()
        goToSandbox()
        for module in notfound:
            keyword = "[" + module.upper() + "PATH]"
            f = open("seqwindow.cfg", "r")
            path = "N/A"
            for aline in f:
                if (keyword in aline):
                    path = aline.split("\t")[1].strip()
                    break
            f.close()
            # Add the saved location to the path
            sys.path.append(path)
            # Try to import again
            try:
                if (path == "N/A"):
                    raise Exception
                mod = __import__(module)
            except:
                # This still didn't work, so now we have to search for it
                print "Could not import " + module + "...  Searching for it..."
                root = "/usr/local"
                foundIt = False
                for dpath, dnames, fnames in os.walk(root):
                    # We're looking for a directory that is the name of the module, on some path that
                    # includes python
                    for dname in dnames:
                        if ((module in dname and os.path.isfile(dpath + "/" + dname + "/__init__.py")) or module + ".py" in fnames):
                            if ("python3" in dpath):
                                # Sometimes there are duplicates for python3, and trying to import them ruins everything
                                break
                            sys.path.append(dpath)
                            print "Trying " + dpath.strip() + "..."
                            try:
                                # Try to import it again
                                mod = __import__(str(module))
                                # Now let's save these paths so the next time this gets started we don't have to traverse the filesystem again
                                data = []
                                f = open("seqwindow.cfg", "r")
                                for aline in f:
                                    if (not(keyword in aline)):
                                        data.append(aline.strip())
                                f.close()
                                f = open("seqwindow.cfg", "w")
                                for aline in data:
                                    f.write(aline + "\n")
                                f.write(keyword + "\t" + dpath.strip() + "\n")
                                f.close()
                                print "Found " + module + " at " + dpath.strip() + "!"
                                foundIt = True
                            except:
                                pass
                            break
                    if (foundIt):
                        break
                if (not(foundIt)):
                    # Explain how to install the packages that are missing
                    print module + " cannot be found on your system!"
                    if (module == "Bio"):
                        print "Install it by executing \"sudo easy_install biopython\" in a terminal."
                    elif (module == "openbabel" and platform.system() == "Darwin"):
                        print "Install it by executing \"brew install mcs07/cheminformatics/open-babel --HEAD --with-python\" in a terminal."
                    elif (module == "openbabel" and platform.system() == "Linux"):
                        print "Install it by executing either \"sudo apt-get install python-openbabel\" or \"sudo yum install openbabel python-openbabel\" in a terminal."
                    elif (module == "wx" and platform.system() == "Darwin"):
                        print "Download and install wxPython from here: http://www.wxpython.org/download.php, wxPython3.0-osx-cocoa-py2.7"
                    elif (module == "wx" and platform.system() == "Linux"):
                        print "Install it by executing either \"sudo apt-get install python-wxgtk2.8\" or \"sudo yum install wxPython\" in a terminal."
                    else:
                        print "Install it by executing \"sudo easy_install " + module + "\" in a terminal."
                    exit()
        if (wxpython):
            import wx
        else:
            import numpy
            import pymol
            import psutil
            #import requests
            import poster
            import Bio
            import openbabel
        os.chdir(cwd)

if (__name__ == "__main__"):
    import os
    import os.path
    import shutil
    import sys
    import platform
    import __main__
    import time
    import glob
    from threading import Thread
    import multiprocessing
    from scripts.tools import goToSandbox
    import wx
    import wx.grid
    import wx.lib.scrolledpanel
    import wx.lib.dialogs
    
    # If PDBs are passed as arguments, load them automatically in PyMOL
    # On Windows, we'll assume that there is only one PDB file, since this is probably happening
    # due to a double-click on a pdbfile
    if (platform.system() == "Windows"):
        args = ["python"]
        argument = ""
        if (len(sys.argv) >= 2):
            for arg in sys.argv[1:]:
                argument += arg.strip() + " "
            args.append(argument.strip())
    else:
        args = sys.argv[:]
    pdbargs = []
    if (len(args) >= 2):
        for arg in args[1:]:
            if (arg.strip().startswith("\"") and arg.strip().endswith("\"")):
                arg = arg.strip()[1:len(arg.strip())-1]
            if (not(arg.endswith(".pdb"))):
                continue
            absolute = False
            if (platform.system() == "Windows"):
                if (len(arg.strip()) >= 3 and arg.strip()[1:3] == ":\\"):
                    absolute = True
            else:
                if (arg.strip()[0] == "/"):
                    absolute = True
            if (absolute):
                pdbargs.append(arg.strip())
            else:
                if (platform.system() == "Windows"):
                    pdbargs.append(os.getcwd() + "\\" + arg.strip())
                else:
                    pdbargs.append(os.getcwd() + "/" + arg.strip())
    
    if (platform.system() == "Windows"):
        import ctypes
        FILE_ATTRIBUTE_HIDDEN = 0x02
    
    # Change the directory to the one the InteractiveROSETTA.py script is in
    # It can be annoying because on Windows directories are delimited by \ instead of /
    homedir = os.path.expanduser("~")
    if (platform.system() == "Windows"):
        # Create the sandbox if this is the first time running
        if (not(os.path.exists(homedir + "\\InteractiveROSETTA"))):
            os.makedirs(homedir + "\\InteractiveROSETTA")
            # Create the main config file
            f = open(homedir + "\\InteractiveROSETTA\\seqwindow.cfg", "w")
            f.close()
            # Make this folder hidden
            try:
                ret = ctypes.windll.kernel32.SetFileAttributesW(unicode(homedir) + u"\\InteractiveROSETTA", FILE_ATTRIBUTE_HIDDEN)
            except:
                print "Failed to hide the sandbox folder"
    else:
        # Create the sandbox if this is the first time running
        if (not(os.path.exists(homedir + "/.InteractiveROSETTA"))):
            # Create the main config file
            os.makedirs(homedir + "/.InteractiveROSETTA")
            f = open(homedir + "/.InteractiveROSETTA/seqwindow.cfg", "w")
            f.close()
    
    # Figure out the location of this script by reading sys.argv[0]
    scriptdir = os.getcwd()
    if (platform.system() == "Windows"):
        indx = sys.argv[0].rfind("\\")
    else:
        indx = sys.argv[0].rfind("/")
    if (indx >= 0):
        tempdir = sys.argv[0][0:indx]
    else:
        tempdir = ""
    # Again, this gets annoying because root is C: on Windows, not /
    if (platform.system() == "Windows" and len(tempdir) > 1 and (tempdir[0:2] == "C:" or tempdir[0] == "\\")):
        scriptdir = tempdir
    elif ((platform.system() == "Darwin" or platform.system() == "Linux") and len(tempdir) > 0 and tempdir[0] == "/"):
        scriptdir = tempdir
    elif (platform.system() == "Windows"):
        scriptdir = scriptdir + "\\" + tempdir
    else:
        scriptdir = scriptdir + "/" + tempdir
    # Change to this directory so we can import everything in the scripts directory later on
    os.chdir(scriptdir)
    # Better yet, let's just add those locations to the PYTHONPATH now
    sys.path.append(scriptdir + "/scripts")
    # Get the template module
    try:
        if (platform.system() == "Windows"):
            shutil.rmtree(homedir + "/InteractiveROSETTA/modules/template")
        else:
            shutil.rmtree(homedir + "/.InteractiveROSETTA/modules/template")
    except:
        pass
    try:
        olddir = os.getcwd()
        if (platform.system() == "Windows"):
            os.chdir(homedir + "/InteractiveROSETTA/modules")
        else:
            os.chdir(homedir + "/.InteractiveROSETTA/modules")
        shutil.copytree(scriptdir + "/data/template", "template")
        os.chdir(olddir)
    except:
        os.chdir(scriptdir)
    
    # Start wxPython in case we're accepting the license
    importModules(wxpython=True)
    app = wx.App()
    # Check to see if the License has been accepted
    f = open("InteractiveROSETTA.py", "r")
    license_accepted = 0
    for aline in f:
        # When the license gets accepted, the following string gets added to the end of this file
        # It needs to appear 3 times because the first two will be this next line, and the line that
        # actually writes it to this script, the 3rd is the line written after accepting
        if ("### LICENSE ACCEPTED ###" in aline):
            license_accepted = license_accepted + 1
    f.close()
    if (license_accepted < 3 and platform.system() != "Windows"): # Windows users accept the license through the installer
        # Make sure we are root on OSX/Linux
        # On Windows, the batch script that starts InteractiveROSETTA makes sure they are the Admin
        if (platform.system() != "Windows" and os.getuid() != 0 and not(os.access("InteractiveROSETTA.py", os.W_OK))):
            print "You have not accepted the license agreement yet."
            print "Please run InteractiveROSETTA as root to accept it."
            dlg2 = wx.MessageDialog(None, "You have not accepted the license agreement yet.\nPlease run InteractiveROSETTA as root to accept it.\nOpen a terminal and run InteractiveROSETTA as root: sudo python /usr/local/InteractiveROSETTA/InteractiveROSETTA.py", "Run as Root to Accept License", wx.OK | wx.ICON_EXCLAMATION | wx.CENTRE)
            dlg2.ShowModal()
            exit()
        # Get the license text from the LICENSE file
        if (platform.system() == "Windows"):
            f = open("LICENSE.txt", "r")
        else:
            f = open("LICENSE", "r")
        licensetext = ""
        # Print it to stdout
        for aline in f:
            licensetext = licensetext + aline.strip() + "\n"
            print aline.strip()
        f.close()
        print ""
        # And display it in a wx text dialog
        dlg1 = wx.lib.dialogs.ScrolledMessageDialog(None, licensetext, "InteractiveROSETTA License")
        dlg1.ShowModal()
        dlg1.Destroy()
        # Ask for the user to accept
        dlg = wx.MessageDialog(None, "Do you accept the license agreement?", "InteractiveROSETTA License", wx.YES_NO | wx.ICON_QUESTION | wx.CENTRE)
        print "Do you accept the license agreement? (Yes/No)"
        if (dlg.ShowModal() == wx.ID_YES):
            try:
                # Append the flag to the end of this file
                f = open("InteractiveROSETTA.py", "a")
                f.write("### LICENSE ACCEPTED ###")
                f.close()
                dlg2 = wx.MessageDialog(None, "License agreement accepted!\nRerun InteractiveROSETTA to begin using it!", "InteractiveROSETTA License Accepted", wx.OK | wx.ICON_EXCLAMATION | wx.CENTRE)
                dlg2.ShowModal()
                print "\nLicense agreement accepted!\nRerun InteractiveROSETTA to begin using it!"
            except:
                # The script is in a global place and was not run with root/Administrator privileges
                print "We were unable to acknowledge the license acceptance."
                if (platform.system() == "Windows"):
                    print "Did you run this program as the Administrator?"
                    print "Right click on \"InteractiveROSETTA.bat\" and click \"Run as Administrator\""
                    dlg2 = wx.MessageDialog(None, "We were unable to acknowledge the license acceptance.\n\nDid you run this program as the Administrator?\nRight click on the shortcut and select \"Run as Administrator\"", "InteractiveROSETTA License Error", wx.OK | wx.ICON_EXCLAMATION | wx.CENTRE)
                    dlg2.ShowModal()
                elif (platform.system() == "Darwin"):
                    print "Did you run this program as root?"
                    print "Open a terminal and run InteractiveROSETTA as root: sudo /Applications/InteractiveROSETTA.app/Contents/MacOS/InteractiveROSETTA"
                    dlg2 = wx.MessageDialog(None, "We were unable to acknowledge the license acceptance.\n\nDid you run this program as root?\nOpen a terminal and run InteractiveROSETTA as root: sudo /Applications/InteractiveROSETTA.app/Contents/MacOS/InteractiveROSETTA", "InteractiveROSETTA License Error", wx.OK | wx.ICON_EXCLAMATION | wx.CENTRE)
                    dlg2.ShowModal()
                else:
                    print "Did you run this program as root?"
                    print "Open a terminal and run InteractiveROSETTA as root: sudo python /usr/local/InteractiveROSETTA/InteractiveROSETTA.py"
                    dlg2 = wx.MessageDialog(None, "We were unable to acknowledge the license acceptance.\n\nDid you run this program as root?\nOpen a terminal and run InteractiveROSETTA as root: sudo python /usr/local/InteractiveROSETTA/InteractiveROSETTA.py", "InteractiveROSETTA License Error", wx.OK | wx.ICON_EXCLAMATION | wx.CENTRE)
                    dlg2.ShowModal()
            # Now unpack that molfile stuff, since we already have root privileges if they were needed
            # to accept the license
            try:
                if (platform.system() == "Windows"):
                    # This finds the molfile2params stuff in the PyRosetta folder on Windows
                    # On Mac/Linux, all you have to do is move and untar a tgz archive
                    # Since Windows cannot do this without 3rd party software, I wrote a Python script to do it
                    import molfile
                    molfile.unpackMolfile()
            except:
                print "We are detecting an error with unpacking molfile2params"
                print "Check the scripts directory and make sure there is a folder called \"rosetta_py\" in it"
                print "If not, run molfile.bat as the Administrator"
                p = input("Press any key to exit: ")
            exit()
        else:
            exit()
    
    # Display splash screen
    if (platform.system() == "Windows"):
        splashImage = wx.Bitmap("images\\splash.png", wx.BITMAP_TYPE_PNG)
    else:
        splashImage = wx.Bitmap("images/splash.png", wx.BITMAP_TYPE_PNG)
    splash = wx.SplashScreen(splashImage, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_NO_TIMEOUT, 10000, None, style=wx.FRAME_NO_TASKBAR)
    wx.Yield()
    
    # Start PyMOL
    # Depending on the computer, the windows may have sizes and positions that are slightly off, so when
    # the user resizes/repositions them, their settings get saved and loaded by default the next time
    # this program is run
    # Import PyMOL with the saved window settings
    screenW = wx.GetDisplaySize()[0]
    screenH = wx.GetDisplaySize()[1]
    # These defaults get the sizes mostly right
    pymolw = screenW - 370
    pymolh = screenH - 340
    pymolx = 370
    pymoly = 0
    try:
        # Read the saved offsets and modify the coordinates/sizes as needed
        # Offsets should be saved instead of absolute sizes so we can attempt to scale the windows
        # if the screen resolution changes (i.e. for projectors and the like)
        if (platform.system() == "Windows"):
            f = open(homedir + "\\InteractiveROSETTA\\seqwindow.cfg", "r")
        else:
            f = open(homedir + "/.InteractiveROSETTA/seqwindow.cfg", "r")
        for aline in f:
            if (aline.find("[OFFSET X]") >= 0):
                pymolx = pymolx + int(aline.split()[len(aline.split())-1])
            elif (aline.find("[OFFSET PHEIGHT]") >= 0):
                pymolh = pymolh + int(aline.split()[len(aline.split())-1])
            elif (aline.find("[OFFSET PWIDTH]") >= 0):
                pymolw = pymolw + int(aline.split()[len(aline.split())-1])
        f.close()
    except:
        pass
    # Don't use the settings if the Windows are too big
    if (pymolx > screenW - 100):
        pymolx = 370
    if (pymoly > screenH - 100):
        pymoly = screenH - 340
    pymolx = str(pymolx)
    pymoly = str(pymoly)
    pymolw = str(pymolw)
    pymolh = str(pymolh)

    # This line starts PyMOL
    # It would be nice if I could disable right-clicking in the PyMOL window to prevent unexpected behavior
    __main__.pymol_argv = ["pymol", "-qhxi", "-W", pymolw, "-H", pymolh, "-X", pymolx, "-Y", pymoly]
    # Import the rest of our modules
    importModules()
    from scripts.sequence import SequenceWin
    from scripts.protocols import *
    from scripts.tools import startNewLog
    import pymol
    
    if (platform.system() == "Windows"):
        # To get the OpenBabel path for the Residue/Ligand creator
        # These are the data files for OpenBabel, since I didn't want the user to have to install OpenBabel
        # Python OpenBabel comes with the package in Windows
        # On Mac/Linux, it's easy to install OpenBabel so these files get saved to the user's home directory
        sys.path.append(scriptdir + "\\data\\OpenBabel")

    # Check to see if an instance of InteractiveROSETTA is already running
    # If it is, then abort because we should only have one instance (GUI+daemon) running at a time
    # On Windows, the batch launcher script should also prevent this from happening
    count = 0
    for proc in psutil.process_iter():
        try:
            if (len(proc.cmdline()) >= 2 and proc.cmdline()[0].find("python") >= 0 and proc.cmdline()[1].find("InteractiveROSETTA.py") >= 0):
                count = count + 1
        except:
            # In Windows it will crash if you try to read process information for the Administrator
            # Doesn't matter though since InteractiveROSETTA is run by a non-Administrator
            # But we need to catch these errors since we don't know which processes will be admin ones
            # as we check them all
            pass
    if (count != 1 and False):
        # Already running, terminate
        exit()

    cwd = homedir
    # Create some more sandbox locations if they don't already exist
    # We need a params folder for the custom params files
    # We also need to grab the HOH params file since water is so common a HETATM
    if (platform.system() == "Windows"):
        if (not(os.path.exists(homedir + "\\InteractiveROSETTA\\params"))):
            os.makedirs(homedir + "\\InteractiveROSETTA\\params")
        # We only need to do waters on Windows because PyRosetta automatically gets the metals
        # on Windows
        water = os.environ["PYROSETTA_DATABASE"] + "\\chemical\\residue_type_sets\\fa_standard\\residue_types\\water\\HOH.params"
        if (not(os.path.isfile(homedir + "\\InteractiveROSETTA\\params\\HOH.fa.params"))):
            f = open(water, "r")
            f2 = open(homedir + "\\InteractiveROSETTA\\params\\HOH.fa.params", "w")
            for aline in f:
                f2.write(aline.strip() + "\n")
            f2.close()
            f.close()
    else:
        if (not(os.path.exists(homedir + "/.InteractiveROSETTA/params"))):
            os.makedirs(homedir + "/.InteractiveROSETTA/params")
        # Now let's take the metal ions and waters that Rosetta already provides, just because
        # these HETATMS are so common
        water = os.environ["PYROSETTA_DATABASE"] + "/chemical/residue_type_sets/fa_standard/residue_types/water/HOH.params"
        if (not(os.path.isfile(homedir + "/.InteractiveROSETTA/params/HOH.fa.params"))):
            f = open(water, "r")
            f2 = open(homedir + "/.InteractiveROSETTA/params/HOH.fa.params", "w")
            for aline in f:
                f2.write(aline.strip() + "\n")
            f2.close()
            f.close()
    # We also need a data directory
    # The data directory has a file called "residues.pdb" that contains one of each amino acid type
    # for easily building structures by grabbing the amino acid structures we want
    # bigPDB.pdb is included for legacy reasons
    if (platform.system() == "Windows"):
        if (not(os.path.exists(homedir + "\\InteractiveROSETTA\\data"))):
            os.makedirs(homedir + "\\InteractiveROSETTA\\data")
        if (not(os.path.exists(homedir + "\\InteractiveROSETTA\\modules"))):
            os.makedirs(homedir + "\\InteractiveROSETTA\\modules")
        # Copy over the residue factory PDB
        if (not(os.path.isfile(homedir + "\\InteractiveROSETTA\\data\\residues.pdb"))):
            f = open("data\\residues.pdb", "r")
            f2 = open(homedir + "\\InteractiveROSETTA\\data\\residues.pdb", "w")
            for aline in f:
                f2.write(aline)
            f.close()
            f2.close()
        if (not(os.path.isfile(homedir + "\\InteractiveROSETTA\\data\\bigPDB.pdb"))):
            # Copy over the initializer PDB
            f = open("data\\bigPDB.pdb", "r")
            f2 = open(homedir + "\\InteractiveROSETTA\\data\\bigPDB.pdb", "w")
            for aline in f:
                f2.write(aline)
            f.close()
            f2.close()
    else:
        if (not(os.path.exists(homedir + "/.InteractiveROSETTA/data"))):
            os.makedirs(homedir + "/.InteractiveROSETTA/data")
        if (not(os.path.exists(homedir + "/.InteractiveROSETTA/modules"))):
            os.makedirs(homedir + "/.InteractiveROSETTA/modules")
        # Copy over the residue factory PDB
        if (not(os.path.isfile(homedir + "/.InteractiveROSETTA/data/residues.pdb"))):
            f = open("data/residues.pdb", "r")
            f2 = open(homedir + "/.InteractiveROSETTA/data/residues.pdb", "w")
            for aline in f:
                f2.write(aline)
            f.close()
            f2.close()
        if (not(os.path.isfile(homedir + "/.InteractiveROSETTA/data/bigPDB.pdb"))):
            # Copy over the initializer PDB
            f = open("data/bigPDB.pdb", "r")
            f2 = open(homedir + "/.InteractiveROSETTA/data/bigPDB.pdb", "w")
            for aline in f:
                f2.write(aline)
            f.close()
            f2.close()
    frozen = False
    poses = []
    sequences = []
    IDs = []
    
    # Grab the params files in the user's personal directory
    olddir = os.getcwd()
    #initRosetta()
    cleanUp()
    # Start a new log for this session
    startNewLog()
    os.chdir(olddir)
    
    # Start all of the windows
    SequenceFrame = SequenceWin(screenW, screenH, cwd, frozen, poses, sequences, IDs, scriptdir)
    ProtocolsFrame = ProtocolsWin(screenW, screenH, scriptdir)
    pymol.finish_launching()
    pymol.cmd.set("label_size", 28)
    pymol.cmd.set("label_position", (0, 0, 5))
    # Start the PyMOL PyRosetta server
    if (os.path.isfile(os.environ["PYROSETTA_DATABASE"] + "/../PyMOLPyRosettaServer2.py")):
        pymol.cmd.do("run " + os.environ["PYROSETTA_DATABASE"] + "/../PyMOLPyRosettaServer2.py")
    elif (os.path.isfile(os.environ["PYROSETTA_DATABASE"] + "/../PyMOLPyRosettaServer.py")):
        pymol.cmd.do("run " + os.environ["PYROSETTA_DATABASE"] + "/../PyMOLPyRosettaServer.py")

    # Make all of these windows aware of PyMOL
    SequenceFrame.setPyMOL(pymol)
    ProtocolsFrame.Selection.setPyMOL(pymol)
    ProtocolsFrame.Protocols.setPyMOL(pymol)
    ProtocolsFrame.setSeqWin(SequenceFrame)
    SequenceFrame.setProtWin(ProtocolsFrame)
    try:
        splash.Destroy()
    except:
        pass
    # Load the PDBs given at the command line
    for pdb in pdbargs:
        try:
            # In case something bad happens...
            SequenceFrame.PyMOLPDBLoad(1, pdb, "Show")
        except:
            pass
    app.MainLoop()
