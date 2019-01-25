import os

# Want detailed scan of each thing, rather than all combinations.
# Take central value as "crossing point" and scan the other axis.
grid = {
  "mass_gluino" : [1000,1500,2000,2500,3000],
  "mass_neutralino" : [100,300,500,700,900],
  "mass_spectrum" : ["mass0","mass3","mass5","mass8"],
  "gluinoball_frac" : [5,10,20],
}

# Generate combinations
points = []
for scan_axis in grid.keys() :

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

    points.append(point_dict)

# Loop over each point to make JOs and launch job
for point in points :
  print point

# Make output directory


# Make job options file


# Make batch script

# Run generation