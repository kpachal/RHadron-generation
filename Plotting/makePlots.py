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

# Dir in which to look for files
file_dir = "outputFiles"                     

## Axis to plot: gluino mass.
files = glob.glob(file_dir+"/DAOD_TRUTH1.*_500_1ns_sp5_gl10.pool_output.root")
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
  openfile.Close()

mass_list = sorted(gmass_hists.keys())
hist_list = [gmass_hists[i] for i in mass_list]
name_list = ["m_{0} = {1}".format("g",i) for i in mass_list]
myPainter.drawManyOverlaidHistograms(hist_list,name_list,"m_{gluino} [GeV]","Events/1000","plots/gluino_mass","automatic","automatic",0,35,extraLegendLines=["Nominal values"],doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None")

## Axis to plot: mass spectrum
files = glob.glob(file_dir+"/DAOD_TRUTH1.2000_500_1ns_*_gl10.pool_output.root")
print "Files for scanning mass spectrum:",files
validation_hists = {}
ROOT.gStyle.SetPalette(ROOT.kBird)
for file in files :
  spectrum_nominal = file.split(".")[-3].split("_")[3]
  openfile = ROOT.TFile.Open(file,"READ")
  print "Got hist from file with nominal mass spectrum",spectrum_nominal
  hist = openfile.Get("h_mRHads")
  hist.SetDirectory(0)
  hist_nRHads = openfile.Get("h_nRHads")
  hist_nRHads.SetDirectory(0)
  hist_nRHads.Scale(1.0/1000.0)
  hist_statusRHads = openfile.Get("h_statusRHads")
  hist_statusRHads.SetDirectory(0) 
  hist_statusRHads.Scale(1.0/1000.0) 
  openfile.Close()
  validation_hists[spectrum_nominal] = {"nRHads" : hist_nRHads, "statusRHads" : hist_statusRHads}  

  # Find peak of gluinoball bin.
  maxVal = -1
  maxBin = -1
  for ybin in range(hist.GetNbinsY()) :
    if hist.GetBinContent(1,ybin) > maxVal :
      maxVal = hist.GetBinContent(1,ybin)
      maxBin = ybin
  print "Maximum was found in bin with center",hist.GetYaxis().GetBinCenter(maxBin)
  print "and low edge, high edge",hist.GetYaxis().GetBinLowEdge(maxBin),hist.GetYaxis().GetBinLowEdge(maxBin+1)

  # Draw this hist alone
  myPainter.draw2DHist(hist,"plots/test_"+spectrum_nominal,"R-Hadron ID [A.U.]",0,40,"R-Hadron mass [GeV]",1999,2010,"Events",luminosity=-1,CME=-1,doRectangular=False)

spectrum_list = sorted(validation_hists.keys())
hist_list_nRHads = [validation_hists[i]["nRHads"] for i in spectrum_list]
hist_list_statusRHads = [validation_hists[i]["statusRHads"] for i in spectrum_list]
name_list = ["Spectrum # {0}".format(i.replace("sp","")) for i in spectrum_list]
myPainter.drawManyOverlaidHistograms(hist_list_nRHads,name_list,"Number of R-Hadrons","Events/1000","plots/n_RHadrons",0,5,"automatic","automatic",extraLegendLines=["Mass spectra"],doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None")
myPainter.drawManyOverlaidHistograms(hist_list_statusRHads,name_list,"Status of R-Hadrons","Events/1000","plots/status_RHadrons",0,5,"automatic","automatic",extraLegendLines=["Mass spectra"],doLogX=False,doLogY=False,doLegendLow=False,doATLASLabel="None")

## Axis to plot: gluinoball fraction
files = glob.glob(file_dir+"/DAOD_TRUTH1.2000_500_1ns_sp5_*.pool_output.root")
print "Files for scanning gluinoball fraction:",files
glueball_hists = {}
for file in files :
  glfrac_nominal = file.split(".")[-3].split("_")[4]
  if "gl5" in glfrac_nominal : glfrac_nominal = "gl05"
  openfile = ROOT.TFile.Open(file,"READ")
  hist = openfile.Get("h_mRHads")  
  hist.SetDirectory(0)
  openfile.Close()
  glueball_hists[glfrac_nominal] = hist

frac_list = sorted(glueball_hists.keys())
name_list = ["f_{0} = {1}".format("g",frac.replace("gl","")) for frac in frac_list]
graph_list = []
for frac in frac_list :
  hist = glueball_hists[frac]
  hist_1D = hist.ProjectionX()
  gluinoball_frac = hist_1D.GetBinContent(1) # Gluinoball bin
  gluinoball_frac = gluinoball_frac/hist_1D.Integral()
  print "Got frac",gluinoball_frac
  graph = ROOT.TGraph()
  graph.SetPoint(0,1,gluinoball_frac)
  graph_list.append(graph)

myPainter.drawSeveralObservedLimits(graph_list,name_list,"plots/gluinoball_frac","","Fraction",[],[],0,1.1,0,0.3,["Nominal fraction"])


