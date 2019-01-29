#!/usr/bin/env python

import ROOT
from ROOT import *
import xAODRootAccess.GenerateDVIterators  

import os,sys
import glob

# User settings
# No point scanning items which I can't measure changing:
# those are really just for Atsushi
inputfile_form = "/home/kpachal/RHadronGeneration/EVNTtoTruth/EVNTtoTruth_*500_1ns*/DAOD_TRUTH1.*.root"

verbose = False

## Larry magic
ROOT.gROOT.Macro( '$ROOTCOREDIR/scripts/load_packages.C' )
## Magic end

## This dict defines the mapping from index to PDGID for my R-hadrons
RHad_map = {
  1000993 : 1, # Gluinoballs
  1009113 : 2,
  1009213 : 3,
  1009223 : 4,
  1009313 : 5,
  1009323 : 6, 
  1009333 : 7,
  1009413 : 8,
  1009423 : 9,
  1009433 : 10,
  1009443 : 11,
  1009513 : 12,
  1009523 : 13,
  1009533 : 14,
  1009543 : 15,  
  1009553 : 16,    
  1091114 : 17, 
  1092114 : 18,
  1092214 : 19,
  1092224 : 20,
  1093114 : 21,
  1093214 : 22,
  1093224 : 23,
  1093314 : 24,
  1093324 : 25,
  1093334 : 26,
  1094114 : 27,
  1094214 : 28,
  1094224 : 29,
  1094314 : 30,
  1094324 : 31,
  1094334 : 32,
  1095114 : 33,
  1095214 : 34,
  1095224 : 35,
  1095314 : 36,
  1095324 : 37,
  1095334 : 38
}

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

def findGluinosAndRHads(truthparticles) :

  gluinos = []
  RHads = []
  for iparticle,particle in enumerate(truthparticles):

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

  return gluinos,RHads    

file_list = glob.glob(inputfile_form)
for inputfile in file_list :

  t = readXAODFile(inputfile)

  outputFile = TFile("outputFiles/"+inputfile.replace(".root","_output.root").split("/")[-1],"RECREATE")
  h_mgluino = TH1D("h_mgluino","h_mgluino", 250 , 1000. ,3500.)
  h_mRHads = TH2D("h_mRHads","h_mRHads", 38, 1., 39, 2500*4 , 1000. ,3500.)
  h_nRHads = TH1D("h_nRHads","h_nRHads",5,0,5)
  h_statusRHads = TH1D("h_statusRHads","h_statusRHads",5,0,5)

  for entry in xrange( t.GetEntries() ):
    t.GetEntry( entry )

    if verbose :
      print "#"*100+"\n"+"#"*100
      print "Run: %d Event: %d -----------------------------------"%(t.EventInfo.runNumber(), t.EventInfo.eventNumber() )

    # Collect links to gluinos and R-hadrons.
    gluinos, RHads = findGluinosAndRHads(t.TruthParticles)

    # Now I have useful event contents. Get relevant quantities and fill my hists.
    if verbose : print "Gluinos:"
    for gluino in gluinos :
      if verbose : print gluino.pdgId(),gluino.m(),getPt(gluino)
      h_mgluino.Fill(gluino.m()/1000.0)

    if verbose : print "R-hadrons:"
    h_nRHads.Fill(len(RHads))
    for rHad in RHads :
      if verbose : print rHad.pdgId(),rHad.m(),getPt(rHad)
      h_mRHads.Fill(RHad_map[rHad.absPdgId()],rHad.m()/1000.0)
      h_statusRHads.Fill(rHad.status())

  outputFile.cd()
  h_mgluino.Write()
  h_mRHads.Write()
  h_nRHads.Write()
  h_statusRHads.Write()

  outputFile.Close()
  print "Created file",outputFile
