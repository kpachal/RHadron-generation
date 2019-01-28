# Need output EVNT files to carry information in their names
# so that I can give them to Atsushi.

import os
import glob

from shutil import copyfile

consolidated = "AllEVNTFiles/"
if not os.path.exists(consolidated) :
  os.mkdir(consolidated)

files = glob.glob("Generate_*/*EVNT*.root")
for file in files :
  name_string = file.split("/")[-2].replace("Generate_","")
  newname = consolidated+"/{0}.EVNT.root".format(name_string)

  print "Making file",newname
  copyfile(file,newname)

print "Done."