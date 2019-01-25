#!/usr/bin/python

import os
import subprocess

# Do everything but submit if true
isTest = False

# Want detailed scan of each thing, rather than all combinations.
# Take central value as "crossing point" and scan the other axis.
grid = {
  "mass_gluino" : [1000,1500,2000,2500,3000],
  "mass_neutralino" : [100,300,500,700,900],
  "mass_spectrum" : ["sp0","sp3","sp5","sp8"],
  "lifetime" : ["0p1ns","0p5ns","1ns","10ns"],
  "gluinoball_frac" : [5,10,20],
}

# These settings let it run on the batch
templatescript = "../batch_templates/batchScript_template_CEDAR.sh"
location_batchscripts = "batch_scripts/"
location_batchlogs = "batch_logs/"

# Make sure they exist
for thisdir in [location_batchscripts,location_batchlogs] :
  if not os.path.exists(thisdir) :
    os.mkdir(thisdir)

# Generate combinations
points = []
ordered_axes = sorted(grid.keys())
for scan_axis in ordered_axes :

  fixed_grid = {}
  for fixed_axis in grid.keys() :
    if fixed_axis == scan_axis : continue
    fixed_index = int(len(grid[fixed_axis])/2.0)
    fixed_val = grid[fixed_axis][fixed_index]
    fixed_grid[fixed_axis] = fixed_val

  for point in grid[scan_axis] :
    point_dict = {}
    point_dict[scan_axis] = point
    point_dict.update(fixed_grid)

    # Currently crossing point being added numerous times
    # but I think that's OK.

    points.append(point_dict)

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
        line = line.replace("TIMEVAL","2:00:00")
      fbatchout.write(line)

  modcommand = 'chmod 744 {0}'.format(batchtempname)
  subprocess.call(modcommand, shell=True)
  fbatchout.close()

  return batchtempname

# Remove duplicates from points
used_combos = []
for point in points :
  name_string = "{0}_{1}_{2}_{3}_gl{4}".format(point["mass_gluino"],point["mass_neutralino"],point["lifetime"],point["mass_spectrum"],point["gluinoball_frac"])
  if name_string in used_combos :
    del points[points.index(point)]
  else :
    used_combos.append(name_string)

# Loop over each point to make JOs and launch job
for point in points :
  
  name_string = "{0}_{1}_{2}_{3}_gl{4}".format(point["mass_gluino"],point["mass_neutralino"],point["lifetime"],point["mass_spectrum"],point["gluinoball_frac"])
  dir_name = "Generate_"+name_string
  JO_name = "MC15.375120.MGPy8EG_A14NNPDF23LO_GG_direct_RH_"+name_string+".py"

  # Make output directory
  if not os.path.exists(dir_name) :
    os.mkdir(dir_name)
  else :
    print "Duplicate present here!"
    print dir_name

  # Make job options file
  filename = dir_name+"/"+JO_name
  with open(filename,"w") as file :
    file.write("include ( 'MC15JobOptions/MadGraphControl_SimplifiedModel_GG_direct_LongLived_RHadron.py' )")

  # Make symbolic link in each directory so MC15JobOptions are available
  # Check for redundancy since one folder will be checked numerous times
  src = os.path.join(os.getcwd()+"/MC15JobOptions")
  dest = os.path.join(os.getcwd()+"/{0}/MC15JobOptions".format(dir_name))
  if not os.path.exists(dest) :
    os.symlink(src,dest)

  generate_command = "Generate_tf.py --ecmEnergy=13000 --firstEvent=1 --runNumber=375120 --jobConfig={0} --maxEvents=10000 --outputEVNTFile=test_evgen.EVNT.root --randomSeed=4".format(JO_name)
  run_command = """echo 'starting job.';\ncd {0};\nasetup --restore;\ncd {1};\n{2}\n""".format(os.getcwd(),dir_name,generate_command)

  # Make batch script
  script = makeBatchScript(run_command,name_string)

  # Run generation
  submitcommand = "sbatch {0}".format(script)
  print submitcommand

  if not isTest :
    subprocess.call(submitcommand, shell=True) 

  # Uncomment to do just one point
  #break 