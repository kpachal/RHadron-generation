#!/usr/bin/env python

import ROOT
from ROOT import *
import xAODRootAccess.GenerateDVIterators  

import os,sys
import glob

# User settings
# No point scanning items which I can't measure changing:
# those are really just for Atsushi
inputfile_form = "/afs/cern.ch/work/k/kpachal/RHadronGeneration/EVNTtoTruth/EVNTtoTruth_*500_1ns*/DAOD_TRUTH1.*.root"

verbose = False

## Larry magic
ROOT.gROOT.Macro( '$ROOTCOREDIR/scripts/load_packages.C' )
## Magic end

## This dict defines the mapping from index to PDGID for my R-hadrons
RHad_map = {
  1000993 : 1,  # Gluino R-glueball
  1009113 : 2,  # Gluino q-qbar R-mesons
  1009223 : 3,
  1009333 : 4, 
  1009443 : 5,
  1009553 : 6,
  1009213 : 7,  # Light-flavor Gluino R-mesons
  1009313 : 8,  # Strange Gluino R-mesons
  1009323 : 9,
  1009413 : 10, # Charm Gluino R-mesons
  1009423 : 11,
  1009433 : 12,
  1009513 : 13, # Bottom Gluino R-mesons
  1009523 : 14,
  1009533 : 15,
  1009543 : 16,
  1093214 : 17, # Light-flavor singlet Gluino R-baryons
  1094214 : 18, # Charm singlet Gluino R-baryons
  1094314 : 19,
  1094324 : 20,
  1095214 : 21, # Bottom singlet Gluino R-baryons
  1095314 : 22,
  1095324 : 23,
  1091114 : 24, # Light flavor Gluino R-baryons
  1092114 : 25,
  1092214 : 26,
  1092224 : 27,
  1093114 : 28, # Strange Gluino R-baryons
  1093224 : 29,
  1093314 : 30,
  1093324 : 31,
  1093334 : 32,
  1094114 : 33, # Charm Gluino R-baryons
  1094224 : 34,
  1094334 : 35,
  1095114 : 36, # Bottom Gluino R-baryons
  1095224 : 37,
  1095334 : 38,
  1000512 : 39, # Sbottom R-mesons
  1000522 : 40,
  1000532 : 41,
  1000542 : 42,
  1000552 : 43,
  1005113 : 44, # Sbottom R-baryons
  1005211 : 45,
  1005213 : 46,
  1005223 : 47,
  1005311 : 48,
  1005313 : 49,
  1005321 : 50,
  1005323 : 51,
  1005333 : 52,
  1000612 : 53, # Stop R-mesons
  1000622 : 54,
  1000632 : 55,
  1000642 : 56,
  1000652 : 57,
  1006113 : 58, # Stop R-baryons
  1006211 : 59,
  1006213 : 60,
  1006223 : 61,
  1006311 : 62,
  1006313 : 63,
  1006321 : 64,
  1006323 : 65,
  1006333 : 66
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
print "Got file list",file_list
for inputfile in file_list :

  t = readXAODFile(inputfile)

  outputFile = TFile("outputFiles/"+inputfile.replace(".root","_output.root").split("/")[-1],"RECREATE")
  h_mgluino = TH1D("h_mgluino","h_mgluino", 250 , 1000. ,3500.)
  h_mRHads = TH2D("h_mRHads","h_mRHads", len(RHad_map.keys()), 1., len(RHad_map.keys())+1, 2500*4 , 1000. ,3500.)
  h_nRHads = TH1D("h_nRHads","h_nRHads",5,-0.5,4.5)
  h_statusRHads = TH1D("h_statusRHads","h_statusRHads",5,-0.5,4.5)

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
