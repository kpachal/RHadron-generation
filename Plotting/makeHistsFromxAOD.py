#!/usr/bin/env python

import ROOT
from ROOT import *
import xAODRootAccess.GenerateDVIterators  

import os,sys

# User settings
inputfile = "/home/kpachal/RHadronGeneration/EVNTtoTruth/EVNTtoTruth_2000_500_1ns_mass5_gl5_byhand/DAOD_TRUTH1.2000_500_1ns_mass5_gl5.pool.root"

## Larry magic
ROOT.gROOT.Macro( '$ROOTCOREDIR/scripts/load_packages.C' )
## Magic end

def readXAODFile(filename) :

  file = TFile(filename)
  t = ROOT.xAOD.MakeTransientTree( file )

  auxDataCode = """
  bool auxdataConstBool( const SG::AuxElement& el, const std::string& name ) {
     return el.auxdata< char >( name );
  }
  """
  ROOT.gInterpreter.Declare(auxDataCode)

  return t

def getPt(momentum):
	try:
		return momentum.Pt()
	except:
		return momentum.p4().Pt()

t = readXAODFile(inputfile)

outputFile = TFile("outputFiles/"+inputfile.replace(".root","_output.root").split("/")[-1],"RECREATE")
h_mgammagamma = TH1D("h_mgammagamma","h_mgammagamma", 100 , 0e3 ,2.5e3)
h_mres = TH1D("h_mres","h_mres", 100 , 0e3 ,2.0e3)


t.Print()

for entry in xrange( t.GetEntries() ):
	t.GetEntry( entry )

	if entry % 1000 == 0:
		print entry

	print "#"*100
	print "#"*100

	print "Run: %d Event: %d -----------------------------------"%(t.EventInfo.runNumber(), t.EventInfo.eventNumber() )

  # Collect links to gluinos and R-hadrons.
	gluinos = []
	RHads = []
	for iparticle,particle in enumerate(t.TruthParticles):

    # Interested in SUSY particles only
		if particle.absPdgId()<999999:
			continue

    # Find stable R-hadrons
    # They're the SUSY particles that don't decay in these events.
		if not particle.hasDecayVtx() :
			RHads.append(particle)

		# Find my gluinos: want the ones which decay to an r-hadron
		if particle.hasDecayVtx() and particle.absPdgId()==1000021 :

			tmpVtx = particle.decayVtx()
			links = tmpVtx.outgoingParticleLinks()

      # Check if its children include a different SUSY particle.
      # If it's the same, continue
			for iChild in xrange(particle.decayVtx().nOutgoingParticles()):
				link = links.at(iChild)
        # check I can access the link
				try:
					link.pdgId()
				except:
					pass

				# Is child the same particle?
				if (link.pdgId()==particle.pdgId()) : continue
					
				# Is child an interesting particle?
				if (link.absPdgId()<999999) : continue
					
				else :
					gluinos.append(particle)
					continue						

	# Keep to do only one event
	#break

	# Now I have useful event contents. Get relevant quantities and fill my hists.
	print "Gluinos:"
	for gluino in gluinos :
		print gluino.pdgId(),gluino.m(),getPt(gluino)

	print "R-hadrons:"
	for rHad in RHads :
		print rHad.pdgId(),rHad.m(),getPt(rHad)

outputFile.cd()
h_mgammagamma.Write()

outputFile.Close()
