import ROOT
from art.morisot import Morisot

# Turn off giant printouts
verbose = True
# 1 = Andrea's request
# 2 = setting all points <=1 TeV, at 100 GeV spacing and lifetimes including 1, to 90k
# 3 = setting all points <=1 TeV, at 100 GeV spacing and lifetimes including 1, to 160k
ambitionLevel = 3

import request_dict_DV
import request_dict_dEdx
import request_dict_stopped_particle

# Get requests
request_DV = request_dict_DV.getDVGrid()
request_dEdx = request_dict_dEdx.getdEdxGrid(ambitionLevel)
request_stoppedparticle,request_stoppedparticle_variations = request_dict_stopped_particle.getStoppedParticleGrid()

# Initialize painter
myPainter = Morisot()
myPainter.setColourPalette("notSynthwave")
myPainter.setLabelType(4) # Sets label type i.e. Internal, Work in progress etc.
                          # See below for label explanation

requests = {"DV" : request_DV,
            "dEdx" : request_dEdx,
            "Stopped particle" : request_stoppedparticle}

all_lifetimes = list(set(request_DV.keys() + request_dEdx.keys() + request_stoppedparticle.keys()))

# Make a plot per lifetime.
# Also, determine maximum number of events being requested at each point.
# If max number comes from stopped particle, shout....

# These will store sizes of event requests at each point,
# assuming analyses share wherever possible.
n_EVNT = {}
n_FullSim = {}
n_specialSim = {}
dict_list = [n_EVNT,n_FullSim,n_specialSim]

for lifetime in all_lifetimes :

  print "Starting lifetime",lifetime
  for mydict in dict_list :
    mydict[lifetime] = {}

  graphs = []

  request_list = requests.keys()
  for request in request_list :

    thisgraph = ROOT.TGraphErrors()

    request_content = requests[request]
    if not lifetime in request_content.keys() :
      graphs.append(thisgraph)
      continue

    mass_grid = request_content[lifetime]

    for mGluino in mass_grid.keys() :

      for mydict in dict_list :
        if not mGluino in mydict[lifetime].keys() :
          mydict[lifetime][mGluino] = {}

      for mNeutrino in mass_grid[mGluino].keys() :

        # Fill graphs

        index = thisgraph.GetN()
        thisgraph.SetPoint(index,mGluino, mNeutrino)
        thisgraph.SetPointError(index,0,mass_grid[mGluino][mNeutrino])

        # Store or update number of events

        # Want all of them for EVNT
        if not mNeutrino in n_EVNT[lifetime][mGluino].keys() :
          n_EVNT[lifetime][mGluino][mNeutrino] = mass_grid[mGluino][mNeutrino]
        else :
          if mass_grid[mGluino][mNeutrino] > n_EVNT[lifetime][mGluino][mNeutrino] :
            n_EVNT[lifetime][mGluino][mNeutrino] = mass_grid[mGluino][mNeutrino]

        # Want non-stopped-particle for Fullsim
        if not "Stopped" in request :
          if not mNeutrino in n_FullSim[lifetime][mGluino].keys() :
            n_FullSim[lifetime][mGluino][mNeutrino] = mass_grid[mGluino][mNeutrino]
          elif mass_grid[mGluino][mNeutrino] > n_FullSim[lifetime][mGluino][mNeutrino] :
            n_FullSim[lifetime][mGluino][mNeutrino] = mass_grid[mGluino][mNeutrino]

        # Want stopped particle only for special reconstruction
        else :
          if not mNeutrino in n_specialSim[lifetime][mGluino].keys() :
            n_specialSim[lifetime][mGluino][mNeutrino] = mass_grid[mGluino][mNeutrino]
          elif mass_grid[mGluino][mNeutrino] > n_specialSim[lifetime][mGluino][mNeutrino] :
            n_specialSim[lifetime][mGluino][mNeutrino] = mass_grid[mGluino][mNeutrino]

    print "Adding graph for request",request
    graphs.append(thisgraph)

  if not "stable" in lifetime :
    myPainter.drawSignalGrid(graphs,"plots/grid_{0}".format(lifetime),request_list,"m_{G} [GeV]","automatic","automatic","m_{#chi} [GeV]",0,"automatic")
  else :
    myPainter.drawSignalGrid(graphs,"plots/grid_{0}".format(lifetime),request_list,"m_{G} [GeV]","automatic","automatic","m_{#chi} [GeV]","automatic","automatic",addDiagonal=False)

# Now summarise number of events at each lifetime. 
# Print things to check them by eye.
total_EVNT = 0
total_FullSim = 0
total_SpecialReco = 0
for lifetime in all_lifetimes :

  if verbose :
    print "For lifetime",lifetime
    print "mGluino, mNeutrino, number of EVNT:"

  for mGluino in sorted(n_EVNT[lifetime].keys()) :
    for mNeutrino in sorted(n_EVNT[lifetime][mGluino].keys()) :
      thisEVNT = n_EVNT[lifetime][mGluino][mNeutrino]
      if verbose : print "\t",mGluino,"\t",mNeutrino,"\t",thisEVNT
      total_EVNT = total_EVNT+thisEVNT

  if verbose : print "number of FullSim:"

  for mGluino in sorted(n_FullSim[lifetime].keys()) :
    for mNeutrino in sorted(n_FullSim[lifetime][mGluino].keys()) :
      thisFS = n_FullSim[lifetime][mGluino][mNeutrino]
      if verbose : print "\t",mGluino,"\t",mNeutrino,"\t",thisFS
      total_FullSim = total_FullSim+thisFS

  if verbose : print "Number of special reco for Stopped Particle:"

  for mGluino in sorted(n_specialSim[lifetime].keys()) :
    for mNeutrino in sorted(n_specialSim[lifetime][mGluino].keys()) :
      this_special = n_specialSim[lifetime][mGluino][mNeutrino]
      if verbose : print "\t",mGluino,"\t",mNeutrino,"\t",this_special
      total_SpecialReco = total_SpecialReco+this_special

print "\nTotals:"
print "\tEVNT:",total_EVNT,"=",round(float(total_EVNT)/1000000.0,2),"million"
print "\tFullSim:",total_FullSim,"=",round(float(total_FullSim)/1000000.0,2),"million"
print "\tSpecial for Stopped Particle:",total_SpecialReco,"=",round(float(total_SpecialReco)/1000000.0,2),"million"
