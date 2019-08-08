#!/usr/bin/env python
"""
Jason C. Rochon
University of Illinois at Chicago

I don't know anything about Python, dog - I'm a Perl Frog.
But this is an example of a kludge to recover some data
after a horrible Microsoft Windows NTFS chkdsk [usb]: /f/x/r

This program will move and organize your recovered files by extension.

If the destination file exists:
* if size is same:
    deletes the currently recovered file (no wasted space)
* else:
    moves smaller file into a duplicate sub folder (2nd chance recovery) 
    (corruption increased file size on previous file, or current file is compressed)
* if the duplicate file is the same as both the current and previous:
    moves same size file into duplicate sub folder (exact copy, 2nd chance recovery)
    
Copyright (C) 2014  Jason C. Rochon

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os.path
import shutil
import sys

while not (len(sys.argv) == 3):
    sys.exit('Needs source and destination directories: [source] [destination]\n')

source = sys.argv[1]
destination = sys.argv[2]

if not os.path.exists(source):
    sys.exit('Source directory must exist: [source] '+ destination +'\n')

if not os.path.exists(destination):
    sys.exit('Destination directory must exist: ' + source + ' [destination]\n')


for root, dirs, files in os.walk(source, topdown=False):
    for myFile in files:
        currFile = os.path.join(root,myFile)
        extension = os.path.splitext(myFile)[1][1:].lower()
        destPath = os.path.join(destination,extension)
        destFile = os.path.join(destPath,myFile)
        dupePath = os.path.join(destPath,'dupes')
        dupeFile = os.path.join(dupePath,myFile)
        
        if not os.path.exists(destPath):
            os.mkdir(destPath)
      
        if not os.path.exists(dupePath):
            os.mkdir(dupePath)
 
        if os.path.exists(destFile):
            mySize = os.path.getsize(os.path.join(root,myFile))
            destSize = os.path.getsize(destFile)
            
            print '\nmySize: ' + str(mySize) + '\ndestSize: ' + str(destSize)
 
            if (mySize > destSize):
                print '\nremove dest file: ' + destFile
                os.remove(destFile)
                print '\nmove curr file: ' + currFile + ' to dest path: ' + destPath
                shutil.move(currFile, destPath)
            else:
                if os.path.exists(dupeFile):
                    dupeSize = os.path.getsize(dupeFile)
                    print '\ndupeSize: ' + str(dupeSize)        
                    
                    if (mySize >= dupeSize):
                        print '\nremove dupe file: ' + dupeFile
                        os.remove(dupeFile)
                        print '\nmove curr file: ' + currFile + ' to dupe path: ' + dupePath
                        shutil.move(currFile, dupePath) 
                    else:
                        print '\nremove curr file: ' + currFile
                        os.remove(currFile)
                else:
                    print '\nmove curr file: ' + currFile + ' to dupe path: ' + dupePath
                    shutil.move(currFile, dupePath)
        else:
            print '\nmove curr file: ' + currFile + ' to dest path: ' + destPath
            shutil.move(currFile, destPath)
            
            
