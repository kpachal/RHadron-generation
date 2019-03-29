import os
import ROOT
import pickle
from art.morisot import Morisot

# Turn off giant printouts
verbose = False
# 1 = Andrea's request
# 2 = setting all points <=1 TeV, at 100 GeV spacing and lifetimes including 1, to 90k
# 3 = setting all points <=1 TeV, at 100 GeV spacing and lifetimes including 1, to 160k
ambitionLevel = 3

# Request priority
priority = 2

# Release used for generation
release = "TBD"

import request_dict_DV
import request_dict_dEdx
import request_dict_stopped_particle

import cross_section_dict

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
# Print things to check them by eye, if desired.
# Also use this step to create job options for the full request.
total_EVNT = 0
total_FullSim = 0
total_SpecialReco = 0
jo_dict = {}
jo_dir = os.getcwd()+"/JOs"
jo_format = "MC15.{0}.MGPy8EG_A14NNPDF23LO_GG_direct_RH_{1}_{2}_{3}_{4}_{5}.py"
for lifetime in all_lifetimes :

  jo_dict[lifetime] = {}

  if verbose :
    print "For lifetime",lifetime
    print "mGluino, mNeutrino, number of EVNT:"

  for mGluino in sorted(n_EVNT[lifetime].keys()) :
    jo_dict[lifetime][mGluino] = {}
    for mNeutrino in sorted(n_EVNT[lifetime][mGluino].keys()) :
      thisEVNT = n_EVNT[lifetime][mGluino][mNeutrino]
      if verbose : print "\t",mGluino,"\t",mNeutrino,"\t",thisEVNT
      total_EVNT = total_EVNT+thisEVNT

      # Generate JO
      convert_lifetime_ns = lifetime
      if "ps" in lifetime :
        lifetime_ps = eval(lifetime.replace("ps",""))
        lifetime_ns = round(lifetime_ps/1000.0,2)
        convert_lifetime_ns = "{0}ns".format(lifetime_ns)
        convert_lifetime_ns = convert_lifetime_ns.replace(".","p")
      if "stable" in lifetime :
        convert_lifetime_ns = "stab"
      jo_name = jo_format.format("000001",mGluino,mNeutrino,convert_lifetime_ns,"sp5","gl10")
      jo_total = jo_dir+"/"+jo_name
      with open(jo_total, 'w') as outfile :
        outfile.write("include ( 'MC15JobOptions/MadGraphControl_SimplifiedModel_GG_direct_LongLived_RHadron.py' )\n")

      jo_dict[lifetime][mGluino][mNeutrino] = jo_name

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

# Generate special JOs for our one point with variations
for spectrum in range(1,9) :
  if spectrum == 5 : continue
  jo_name = jo_format.format("000001",1000,100,"stab","sp{0}".format(spectrum),"gl10")
  jo_total = jo_dir+"/"+jo_name
  with open(jo_total, 'w') as outfile :
    outfile.write("include ( 'MC15JobOptions/MadGraphControl_SimplifiedModel_GG_direct_LongLived_RHadron.py' )\n")
for gluinoballFrac in ["gl5","gl20"] :
  jo_name = jo_format.format("000001",1000,100,"stab","sp5",gluinoballFrac)
  jo_total = jo_dir+"/"+jo_name
  with open(jo_total, 'w') as outfile :
    outfile.write("include ( 'MC15JobOptions/MadGraphControl_SimplifiedModel_GG_direct_LongLived_RHadron.py' )\n")

# Generate a spreadsheet
# Requirements are here: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MC16SpreadSheet
description = "Long-lived gluino pair production, m_gl={0}, m_LSP={1}, lifetime={2}"
lines_FS = []
lines_EVGNOnly = []
for lifetime in all_lifetimes :
  for mGluino in jo_dict[lifetime].keys() :
    for mNeutrino in jo_dict[lifetime][mGluino].keys() :

      # Using this for list sorting as well as for naming
      useGLMass = "{0}".format(mGluino)
      if mGluino < 1000 : useGLMass = "0"+useGLMass
      useNeutMass = "{0}".format(mNeutrino)
      if mNeutrino < 1000 : useNeutMass = "0"+useNeutMass
      this_description = description.format(useGLMass,useNeutMass,lifetime)

      # Do 2 versions depending on whether this is FS or EVGN
      for sim in ["FS","EVNT"] :

        line = this_description + "\t"

        # JobOptions
        line = line + jo_dict[lifetime][mGluino][mNeutrino]+"\t"

        # CME
        line = line + "13000\t"

        # nEvents
        # TODO: Split into mc16a/mc16d/mc16e
        try : nEVNT = n_EVNT[lifetime][mGluino][mNeutrino]
        except : continue
        try : nFS = n_FullSim[lifetime][mGluino][mNeutrino]
        except : continue

        # Events, EVGEN-only
        # This is where we continue if we don't need any EVGN only events
        nEvts = 0
        if "EVNT" in sim :

          # Don't need a line if numbers are equal
          if not nEVNT > nFS :
            continue

          nEvts = nEVNT - nFS
          line = line + "{0}\t\t\t".format(nEvts)

        # Events straight to full simulation
        else :

          # A few of these points are stopped-particle only.
          if nFS==0 :
            continue

          line = line + "\t{0}\t\t".format(nFS)
          nEvts = nFS

        # Priority, then skip "Output formats"
        line = line + "{0}\t\t".format(priority)

        # Cross section (pb)
        xsec = cross_section_dict.xs[mGluino][0]
        line = line + "{0}\t".format(xsec)

        # Effective luminosity (1/fb)
        # Ignoring our filter eff of 1 and converting from pb to fb
        eff_lumi = (float(nEvts)/xsec)/1000.0
        line = line + "{0}\t".format(eff_lumi)

        # Filter efficiency (1 for us, then skip CPU time and input files)
        line = line + "1\t\t\t"

        # MC-tag: ????
        # TODO FIXME
        line = line + "\t"

        # Release
        line = line + release+"\n"

        if "FS" in sim :
          lines_FS.append(line)
        else :
          lines_EVGNOnly.append(line)

# Add special JOs to FS
# TODO

  
# Print the text file to turn into spreadsheet
with open("spreadsheets/spreadsheet.txt","w") as outfile :
  for line in sorted(lines_FS) :
    outfile.write(line)
  for line in sorted(lines_EVGNOnly) :
    outfile.write(line)

# Summarise numbers of events
print "\nTotals:"
print "\tEVNT:",total_EVNT,"=",round(float(total_EVNT)/1000000.0,2),"million"
print "\tFullSim:",total_FullSim,"=",round(float(total_FullSim)/1000000.0,2),"million"
print "\tSpecial for Stopped Particle:",total_SpecialReco,"=",round(float(total_SpecialReco)/1000000.0,2),"million"


