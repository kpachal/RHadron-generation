import ROOT
from art.morisot import Morisot

import request_dict_DV
import request_dict_dEdx
import request_dict_stopped_particle

# Get requests
request_DV = request_dict_DV.getDVGrid()
request_dEdx = request_dict_dEdx.getdEdxGrid()
request_stoppedparticle,request_stoppedparticle_variations = request_dict_stopped_particle.getStoppedParticleGrid()

print request_dEdx["1ns"]

# Initialize painter
myPainter = Morisot()
myPainter.setColourPalette("notSynthwave")
myPainter.setLabelType(4) # Sets label type i.e. Internal, Work in progress etc.
                          # See below for label explanation

requests = {"DV" : request_DV,
            "dEdx" : request_dEdx,
            "Stopped particle" : request_stoppedparticle}

print request_stoppedparticle

all_lifetimes = list(set(request_DV.keys() + request_dEdx.keys() + request_stoppedparticle.keys()))

# Make a plot per lifetime.
# Also, determine maximum number of events being requested at each point.
# If max number comes from stopped particle, shout....
for lifetime in all_lifetimes :

  print "Starting lifetime",lifetime

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

      for mNeutrino in mass_grid[mGluino].keys() :

        index = thisgraph.GetN()
        thisgraph.SetPoint(index,mGluino, mNeutrino)
        thisgraph.SetPointError(index,0,mass_grid[mGluino][mNeutrino])

    print "Adding graph for request",request
    graphs.append(thisgraph)

  if not "stable" in lifetime :
    myPainter.drawSignalGrid(graphs,"plots/grid_{0}".format(lifetime),request_list,"m_{G} [GeV]","automatic","automatic","m_{#chi} [GeV]",0,"automatic")
  else :
    myPainter.drawSignalGrid(graphs,"plots/grid_{0}".format(lifetime),request_list,"m_{G} [GeV]","automatic","automatic","m_{#chi} [GeV]","automatic","automatic",addDiagonal=False)


