from art.morisot import Morisot
import glob
import ROOT

# Initialize painter
myPainter = Morisot()
myPainter.setColourPalette("notSynthwave")
myPainter.setLabelType(4) # Sets label type i.e. Internal, Work in progress etc.
                          # See below for label explanation

# 0 Just ATLAS    
# 1 "Preliminary"
# 2 "Internal"
# 3 "Simulation Preliminary"
# 4 "Simulation Internal"
# 5 "Simulation"
# 6 "Work in Progress"                          

## Axis to plot: gluino mass.
files = glob.glob("outputFiles/DAOD_TRUTH1.*_500_1ns_sp5_gl10.pool_output.root")
print "Files for scanning gluino mass:",files
gmass_hists = {}
for file in files :
  mass_nominal = file.split(".")[-3].split("_")[0]
  openfile = ROOT.TFile.Open(file,"READ")
  print "Got hist from file with nominal mass",mass_nominal
  hist = openfile.Get("h_mgluino")
  hist.SetDirectory(0)
  # For plotting convenience....
  hist.Scale(1.0/1000.0)
  gmass_hists[mass_nominal] = hist

print gmass_hists

mass_list = sorted(gmass_hists.keys())
hist_list = [gmass_hists[i] for i in mass_list]
name_list = ["m_{0} = {1}".format("g",i) for i in mass_list]
myPainter.drawManyOverlaidHistograms(hist_list,name_list,"m_{gluino} [GeV]","Events/1000","plots/gluino_mass","automatic","automatic",0,35,extraLegendLines=["Nominal values"],doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None")

## Axis to plot: mass spectrum
files = glob.glob("outputFiles/DAOD_TRUTH1.2000_500_1ns_*_gl10.pool_output.root")
print "Files for scanning mass spectrum:",files
spectrum_hists = {}
ROOT.gStyle.SetPalette(ROOT.kBird)
for file in files :
  spectrum_nominal = file.split(".")[-3].split("_")[3]
  openfile = ROOT.TFile.Open(file,"READ")
  print "Got hist from file with nominal mass spectrum",spectrum_nominal
  hist = openfile.Get("h_mRHads")
  hist.SetDirectory(0)

  # Draw this hist alone
  myPainter.draw2DHist(hist,"plots/test_"+spectrum_nominal,"R-Hadron ID [A.U.]",0,40,"R-Hadron mass [GeV]",1985,2050,"Events",luminosity=-1,CME=-1,doRectangular=False)

## Axis to plot: gluinoball fraction
files = glob.glob("outputFiles/DAOD_TRUTH1.2000_500_1ns_sp5_*.pool_output.root")
print "Files for scanning gluinoball fraction:",files



