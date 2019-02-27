import os
import glob
import subprocess
from pbs_handler import PBSHandler
from condor_handler import CondorHandler

# Do everything but submit if true
isTest = False

# Batch controls
useBatch = True
# Currently supported: condor, pbs
batch_type = "condor"

# Use if you want only a subset of the files
tag = ""

# Getting EVNT files
source_dir = os.path.abspath(os.path.join(os.getcwd()+"/../Generate/"))
print source_dir
evnt_files = glob.glob(source_dir+"/Generate_*{0}*/*.EVNT.root".format(tag))

# Create batch handler
location_batchscripts = os.getcwd()+"/batch_scripts/"
location_batchlogs = os.getcwd()+"/batch_logs/"
if batch_type == "condor" :
  batchmanager = CondorHandler(location_batchlogs, location_batchscripts)
elif batch_type == "pbs" :
  batchmanager = PBSHandler(location_batchlogs, location_batchscripts) 

# Make sure they exist
for thisdir in [location_batchscripts,location_batchlogs] :
  if not os.path.exists(thisdir) :
    os.mkdir(thisdir)

# Want to run a derivation job for each of the 
# existing points, and give output TRUTH files meaningful names
for evnt_file in evnt_files :

  name_string = evnt_file.split("/")[-2].replace("Generate_","")
  print name_string

  # Want an output dir for this
  out_dir = os.getcwd()+"/EVNTtoTruth_{0}".format(name_string)
  if not os.path.exists(out_dir) :
    os.mkdir(out_dir)

  out_file = "{0}.pool.root".format(name_string)

  reco_command = "Reco_tf.py --inputEVNTFile {0} --outputDAODFile {1} --reductionConf TRUTH1".format(evnt_file,out_file)
  run_command = """echo 'starting job.';\ncd {0};\nasetup --restore;\ncd {1};\n{2}\n""".format(os.getcwd(),out_dir,reco_command)

  if isTest :
    print reco_command
    continue

  if useBatch :

    # Make and send
    batchmanager.send_job(run_command,name_string)

  else :
    subprocess.call(reco_command, shell=True) 

  # Uncomment to do just one point
  #break 

