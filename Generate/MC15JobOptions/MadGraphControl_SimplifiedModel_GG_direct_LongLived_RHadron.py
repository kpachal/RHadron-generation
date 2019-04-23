include ( 'MC15JobOptions/MadGraphControl_SimplifiedModelPreInclude.py' )

infoStrings = runArgs.jobConfig[0].split("/")[-1].split(".")[2].split("_")

masses['1000021'] = float(infoStrings[5])
masses['1000022'] = float(infoStrings[6].split('.py')[0])
if "stab" in infoStrings[7] :
  lifetime = -1
else :
  lifetime = float(infoStrings[7].replace("ns","").split('.py')[0].replace('p','.') ) #in ns
spectrum = int(infoStrings[8].split('.py')[0].replace('sp',''))
if '_gl' in runArgs.jobConfig[0]:
    gluinoballProb = float(infoStrings[-1].split('.')[0].replace("gl",""))*0.01
else:
    gluinoballProb = -1


if masses['1000022']<0.5: masses['1000022']=0.5

gentype   = str(infoStrings[2])
decaytype = str(infoStrings[3])
process   = '''
generate p p > go go $ susysq susysq~ @1
add process p p > go go j $ susysq susysq~ @2
add process p p > go go j j $ susysq susysq~ @3
'''
njets = 2
evt_multiplier = 6
evgenLog.info('Registered generation of gluino grid '+str(runArgs.runNumber))

evgenConfig.contact  = [ "lawrence.lee.jr@cern.ch" ]
evgenConfig.keywords += ['simplifiedModel','gluino','longLived']
evgenConfig.description = 'Gluino-gluino production, glu->qq+LSP in simplified model, m_glu = %d GeV, m_N1 = %d GeV. Gluino lifetime of %f, including RHadron setup. gluino-ball probability: %f, '%(masses['1000021'],masses['1000022'],lifetime,gluinoballProb)

include ( 'MC15JobOptions/MadGraphControl_SimplifiedModelPostInclude.py' )

if njets>0:
    genSeq.Pythia8.Commands += ["Merging:Process = pp>{go,1000021}{go,1000021}"]

genSeq.Pythia8.Commands += ["Init:showChangedSettings = on"]
genSeq.Pythia8.Commands += ["Rhadrons:allow = on"]
genSeq.Pythia8.Commands += ["RHadrons:allowDecay = off"]
# Check if we are explicitly setting the gluinoball fraction; if not use the default value
if gluinoballProb!=-1:
    genSeq.Pythia8.Commands += ["RHadrons:probGluinoball = %f"%gluinoballProb]
else:
    genSeq.Pythia8.Commands += ["RHadrons:probGluinoball = 0.1"]
genSeq.Pythia8.Commands += ["Next:showScaleAndVertex = on"]
genSeq.Pythia8.Commands += ["Check:nErrList = 2"]

# Make sure that the RHadrons are allowed by TestHepMC
if 'testSeq' in dir():
    extra_pdgids_f = open('extra_pdgids.txt','w')
    from RHadrons.RHadronMasses import offset_options
    # Just allow all of them to have an anti-particle.  It's more future-proof.
    for a in offset_options:
        extra_pdgids_f.write(str(a)+'\n')
        extra_pdgids_f.write('-'+str(a)+'\n')
    extra_pdgids_f.close()
    testSeq.TestHepMC.G4ExtraWhiteFile='extra_pdgids.txt'

evgenConfig.specialConfig = "LIFETIME={lifetime};preInclude=SimulationJobOptions/preInclude.RHadronsPythia8.py".format(lifetime=lifetime)

# Set up R-hadron masses in Pythia8
import os
if os.access('param_card.dat',os.R_OK):
    from RHadrons.RHadronMasses import get_Pythia8_commands
    genSeq.Pythia8.Commands += get_Pythia8_commands('param_card.dat',spectrum)
# Otherwise this is going to be done a different way by the simulation pre-include

