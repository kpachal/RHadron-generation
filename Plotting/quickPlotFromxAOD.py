#!/usr/bin/env python

import ROOT
from ROOT import *


import os,sys

ROOT.gROOT.Macro( '$ROOTCOREDIR/scripts/load_packages.C' )

f = TFile(sys.argv[1])
print f


t = ROOT.xAOD.MakeTransientTree( f )
import xAODRootAccess.GenerateDVIterators


outputFile = TFile("outputFiles/"+sys.argv[1].replace(".root","_output.root").split("/")[-1],"RECREATE")
c = TCanvas("c","c",600,600)
h_mgammagamma = TH1D("h_mgammagamma","h_mgammagamma", 100 , 0e3 ,2.5e3)
h_mres = TH1D("h_mres","h_mres", 100 , 0e3 ,2.0e3)

auxDataCode = """
bool auxdataConstBool( const SG::AuxElement& el, const std::string& name ) {
   return el.auxdata< char >( name );
}
"""

ROOT.gInterpreter.Declare(auxDataCode)

def getPt(momentum):
	try:
		return momentum.Pt()
	except:
		return momentum.p4().Pt()

t.Print()

for entry in xrange( t.GetEntries() ):
	t.GetEntry( entry )

	printDebug = True if entry < 5 else False

	if entry % 1000 == 0:
		print entry

	print "#"*100
	print "#"*100

	print "Run: %d Event: %d -----------------------------------"%(t.EventInfo.runNumber(), t.EventInfo.eventNumber() )

	for iparticle,particle in enumerate(t.TruthParticles):
		# print dir(particle)

		if particle.absPdgId()<999999:
			continue

		if particle.hasDecayVtx() and particle.decayVtx().nOutgoingParticles()>1:
			# do stuff or not or whatever

			print "_"*50
			print "pdgID: %d, mass %.3f, bc %d, nCh %d, status %d"%(particle.pdgId(), particle.m(), particle.barcode(),particle.nChildren(),particle.status())
			tmpVtx = particle.decayVtx()
			print "x,y,z,r = %.2f %.2f %.2f %.2f"%(tmpVtx.x(),tmpVtx.y(),tmpVtx.z(),tmpVtx.perp())
			print "outgoing particles: %d"%particle.decayVtx().nOutgoingParticles()
			links = tmpVtx.outgoingParticleLinks()
			for iChild in xrange(particle.decayVtx().nOutgoingParticles()):
				link = links.at(iChild)
				try:
					# print link
					print link.status(), link.pdgId(), "%.0f"%(getPt(link)/1000.)
				except:
					pass


outputFile.cd()
h_mgammagamma.Write()

outputFile.Close()
