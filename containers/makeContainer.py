#! /usr/bin/env python

import sys, os, os.path, shutil
from pyslet.imscpv1p2 import ContentPackage, PathInPath
from pyslet.rfc2396 import URIFactory

def main():
        if len(sys.argv)!=3:
                print "Usage: makecp <resource file> <package file>"
                return
        resFile=sys.argv[1]
        pkgFile=sys.argv[2]
        pkg=ContentPackage()
        try:
                if os.path.isdir(resFile):
                        print "Resource entry point must be a file, not a directory."
                        return
                resHREF=URI.from_path(resFile)
                srcDir,srcFile=os.path.split(resFile)
                r=pkg.manifest.root.Resources.add_child(pkg.manifest.root.Resources.ResourceClass)
                r.href=str(resHREF.relative(URI.from_path(os.path.join(srcDir,'imsmanifest.xml'))))
                r.type=='webcontent'
                for dirpath,dirnames,filenames in os.walk(srcDir):
                        for f in filenames:
                                srcPath=os.path.join(dirpath,f)
                                if pkg.IgnoreFilePath(srcPath):
                                        print "Skipping: %s"%srcPath
                                        continue
                                dstPath=os.path.join(pkg.dPath,PathInPath(srcPath,srcDir))
                                # copy the file
                                dname,fName=os.path.split(dstPath)
                                if not os.path.isdir(dname):
                                        os.makedirs(dname)
                                print "Copying: %s"%srcPath
                                shutil.copy(srcPath,dstPath)
                                pkg.File(r,URI.from_path(dstPath))
                if os.path.exists(pkgFile):
                        if raw_input("Are you sure you want to overwrite %s? (y/n) "%pkgFile).lower()!='y':
                                return
                pkg.manifest.update()
                pkg.ExportToPIF(pkgFile)
        finally:
                pkg.Close()

if __name__ == "__main__":
        main()

