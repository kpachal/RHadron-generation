import os
import glob
import subprocess

# Do everything but submit if true
isTest = False

# Use if you want only a subset of the files
tag = "byhand"

# Getting EVNT files
source_dir = os.path.abspath(os.path.join(os.getcwd()+"/../Generate/"))
print source_dir
evnt_files = glob.glob(source_dir+"/Generate_*{0}*/*.EVNT.root".format(tag))

# These settings let it run on the batch
templatescript = "../batch_templates/batchScript_template_CEDAR.sh"
location_batchscripts = "batch_scripts/"
location_batchlogs = "batch_logs/"

# Make sure they exist
for thisdir in [location_batchscripts,location_batchlogs] :
  if not os.path.exists(thisdir) :
    os.mkdir(thisdir)

# This will be used for batch submission
def makeBatchScript(batchcommand,stringForNaming) :

  # open modified batch script (fbatchout) for writing
  batchtempname = '{0}/run_{1}.sh'.format(location_batchscripts,stringForNaming)
  fbatchout = open(batchtempname, 'w')

  with open(templatescript, 'r') as fin:
    for line in fin :
      if "ALRB_CONT_RUNPAYLOAD" in line :
        line = 'export ALRB_CONT_RUNPAYLOAD="""{0}"""'.format(batchcommand)
      if "TIMEVAL" in line :
        line = line.replace("TIMEVAL","4:00:00")
      fbatchout.write(line)

  modcommand = 'chmod 744 {0}'.format(batchtempname)
  subprocess.call(modcommand, shell=True)
  fbatchout.close()

  return batchtempname

# Want to run a derivation job for each of the 
# existing points, and give output TRUTH files meaningful names
for evnt_file in evnt_files :

  name_string = evnt_file.split("/")[-2].replace("Generate_","")
  print name_string

  # Want an output dir for this
  out_dir = os.getcwd()+"/EVNTtoTruth_{0}".format(name_string)
  if not os.path.exists(out_dir) :
    os.mkdir(out_dir)

  out_file = "{0}.pool.root"

  reco_command = "Reco_tf.py --inputEVNTFile {0} --outputDAODFile {1} --reductionConf TRUTH1".format(evnt_file,out_file)
  run_command = """echo 'starting job.';\ncd {0};\nasetup --restore;\ncd {1};\n{2}\n""".format(os.getcwd(),out_dir,reco_command)

  # Make batch script
  script = makeBatchScript(run_command,name_string)

  # Run derivations
  submitcommand = "sbatch {0}".format(script)
  print submitcommand

  if not isTest :
    subprocess.call(submitcommand, shell=True) 

  # Uncomment to do just one point
  break 

