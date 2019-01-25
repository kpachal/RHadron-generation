#!/usr/bin/python

import os

# Want detailed scan of each thing, rather than all combinations.
# Take central value as "crossing point" and scan the other axis.
grid = {
  "mass_gluino" : [1000,1500,2000,2500,3000],
  "mass_neutralino" : [100,300,500,700,900],
  "mass_spectrum" : ["mass0","mass3","mass5","mass8"],
  "lifetime" : ["0p1ns","0p5ns","1ns","10ns"],
  "gluinoball_frac" : [5,10,20],
}

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

# Loop over each point to make JOs and launch job
for point in points :
  
  name_string = "{0}_{1}_{2}_{3}_gl{4}".format(point["mass_gluino"],point["mass_neutralino"],point["lifetime"],point["mass_spectrum"],point["gluinoball_frac"])
  dir_name = "Generate_"+name_string
  JO_name = "MC15.375120.MGPy8EG_A14NNPDF23LO_GG_direct_RHad_"+name_string+".py"

  # Make output directory
  if not os.path.exists(dir_name) :
    os.mkdir(dir_name)

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

  # Make batch script

  # Run generation