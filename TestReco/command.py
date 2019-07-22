import subprocess

command = "Reco_tf.py"

# Build command
add_ons = ['--AMITag=r11505',
'--asetup="RDOtoRDOTrigger:Athena,21.0.20"',
'--autoConfiguration=everything',
'--conditionsTag "default:OFLCOND-MC16-SDR-16"',
'--digiSteeringConf="StandardSignalOnlyTruth"',
'--geometryVersion="default:ATLAS-R2-2016-01-00-01"',
'--numberOfCavernBkg=0',
'--numberOfHighPtMinBias=0.116075313',
'--numberOfLowPtMinBias=44.3839246425',
'--pileupFinalBunch=6',
'''--postExec=\'\'\'"all:CfgMgr.MessageSvc().setError+=[\\"HepMcParticleLink\\"]" "ESDtoAOD:fixedAttrib=[s if \\"CONTAINER_SPLITLEVEL = '99'\\" not in s else \\"\\" for s in svcMgr.AthenaPoolCnvSvc.PoolAttributes];svcMgr.AthenaPoolCnvSvc.PoolAttributes=fixedAttrib" "ESDtoAOD:CILMergeAOD.removeItem(\\"xAOD::CaloClusterAuxContainer\#CaloCalTopoClustersAux.LATERAL.LONGITUDINAL.SECOND_R.SECOND_LAMBDA.CENTER_MAG.CENTER_LAMBDA.FIRST_ENG_DENS.ENG_FRAC_MAX.ISOLATION.ENG_BAD_CELLS.N_BAD_CELLS.BADLARQ_FRAC.ENG_BAD_HV_CELLS.N_BAD_HV_CELLS.ENG_POS.SIGNIFICANCE.CELL_SIGNIFICANCE.CELL_SIG_SAMPLING.AVG_LAR_Q.AVG_TILE_Q.EM_PROBABILITY.PTD.BadChannelList\\");CILMergeAOD.add(\\"xAOD::CaloClusterAuxContainer\#CaloCalTopoClustersAux.N_BAD_CELLS.ENG_BAD_CELLS.BADLARQ_FRAC.AVG_TILE_Q.AVG_LAR_Q.CENTER_MAG.ENG_POS.CENTER_LAMBDA.SECOND_LAMBDA.SECOND_R.ISOLATION.EM_PROBABILITY\\");StreamAOD.ItemList=CILMergeAOD()" "RDOtoRDOTrigger:conddb.addOverride(\\"/CALO/Ofl/Noise/PileUpNoiseLumi\\",\\"CALOOflNoisePileUpNoiseLumi-mc15-mu30-dt25ns\\")"\'\'\' ''',
'--postInclude "default:PyJobTransforms/UseFrontier.py"',
'''--preExec=\'\'\'"all:rec.Commissioning.set_Value_and_Lock(True);from AthenaCommon.BeamFlags import jobproperties;jobproperties.Beam.numberOfCollisions.set_Value_and_Lock(20.0);from LArROD.LArRODFlags import larRODFlags;larRODFlags.NumberOfCollisions.set_Value_and_Lock(20);larRODFlags.nSamples.set_Value_and_Lock(4);larRODFlags.doOFCPileupOptimization.set_Value_and_Lock(True);larRODFlags.firstSample.set_Value_and_Lock(0);larRODFlags.useHighestGainAutoCorr.set_Value_and_Lock(True)" "all:from TriggerJobOpts.TriggerFlags import TriggerFlags as TF;TF.run2Config='2016'" "all:from BTagging.BTaggingFlags import BTaggingFlags;BTaggingFlags.btaggingAODList=[\\"xAOD::BTaggingContainer#BTagging_AntiKt4EMTopo\\",\\"xAOD::BTaggingAuxContainer#BTagging_AntiKt4EMTopoAux.\\",\\"xAOD::BTagVertexContainer#BTagging_AntiKt4EMTopoJFVtx\\",\\"xAOD::BTagVertexAuxContainer#BTagging_AntiKt4EMTopoJFVtxAux.\\",\\"xAOD::VertexContainer#BTagging_AntiKt4EMTopoSecVtx\\",\\"xAOD::VertexAuxContainer#BTagging_AntiKt4EMTopoSecVtxAux.-vxTrackAtVertex\\"];" "RAWtoESD:from InDetRecExample.InDetJobProperties import InDetFlags; InDetFlags.cutLevel.set_Value_and_Lock(14); from JetRec import JetRecUtils;f=lambda s:[\\"xAOD::JetContainer#AntiKt4%sJets\\"%(s,),\\"xAOD::JetAuxContainer#AntiKt4%sJetsAux.\\"%(s,),\\"xAOD::EventShape#Kt4%sEventShape\\"%(s,),\\"xAOD::EventShapeAuxInfo#Kt4%sEventShapeAux.\\"%(s,),\\"xAOD::EventShape#Kt4%sOriginEventShape\\"%(s,),\\"xAOD::EventShapeAuxInfo#Kt4%sOriginEventShapeAux.\\"%(s,)]; JetRecUtils.retrieveAODList = lambda : f(\\"EMPFlow\\")+f(\\"LCTopo\\")+f(\\"EMTopo\\")+[\\"xAOD::EventShape#NeutralParticleFlowIsoCentralEventShape\\",\\"xAOD::EventShapeAuxInfo#NeutralParticleFlowIsoCentralEventShapeAux.\\", \\"xAOD::EventShape#NeutralParticleFlowIsoForwardEventShape\\",\\"xAOD::EventShapeAuxInfo#NeutralParticleFlowIsoForwardEventShapeAux.\\", \\"xAOD::EventShape#ParticleFlowIsoCentralEventShape\\",\\"xAOD::EventShapeAuxInfo#ParticleFlowIsoCentralEventShapeAux.\\", \\"xAOD::EventShape#ParticleFlowIsoForwardEventShape\\",\\"xAOD::EventShapeAuxInfo#ParticleFlowIsoForwardEventShapeAux.\\", \\"xAOD::EventShape#TopoClusterIsoCentralEventShape\\",\\"xAOD::EventShapeAuxInfo#TopoClusterIsoCentralEventShapeAux.\\", \\"xAOD::EventShape#TopoClusterIsoForwardEventShape\\",\\"xAOD::EventShapeAuxInfo#TopoClusterIsoForwardEventShapeAux.\\",\\"xAOD::CaloClusterContainer#EMOriginTopoClusters\\",\\"xAOD::ShallowAuxContainer#EMOriginTopoClustersAux.\\",\\"xAOD::CaloClusterContainer#LCOriginTopoClusters\\",\\"xAOD::ShallowAuxContainer#LCOriginTopoClustersAux.\\"]; from eflowRec.eflowRecFlags import jobproperties; jobproperties.eflowRecFlags.useAODReductionClusterMomentList.set_Value_and_Lock(True); from TriggerJobOpts.TriggerFlags import TriggerFlags;TriggerFlags.AODEDMSet.set_Value_and_Lock(\\"AODSLIM\\");" "ESDtoAOD:from ParticleBuilderOptions.AODFlags import AODFlags; AODFlags.ThinGeantTruth.set_Value_and_Lock(True); AODFlags.ThinNegativeEnergyCaloClusters.set_Value_and_Lock(True); AODFlags.ThinNegativeEnergyNeutralPFOs.set_Value_and_Lock(True); from JetRec import JetRecUtils; aodlist = JetRecUtils.retrieveAODList(); JetRecUtils.retrieveAODList = lambda : [item for item in aodlist if not \\"OriginTopoClusters\\" in item];"\'\'\' ''',
'--preInclude="HITtoRDO:Digitization/ForceUseOfPileUpTools.py,SimulationJobOptions/preInclude.PileUpBunchTrainsMC15_2015_25ns_Config1.py,RunDependentSimData/configLumi_run284500_mc16a.py"',
#'--runNumber=449539',
'--steering="doRDO_TRIG"',
'--triggerConfig="RDOtoRDOTrigger=MCRECO:DBF:TRIGGERDBMC:2136,35,160"',
'--inputHITSFile=../mc16_13TeV.449539.MGPy8EG_A14NNPDF23LO_GG_direct_RH_2400_100_0p01ns_sp5_gl10.simul.HITS.e7601_e5984_s3468/HITS.18581455._000027.pool.root.1',
'--outputAODFile=AOD.test.root',
#'--maxEvents=100',
#'--jobNumber=0',
]

for item in add_ons :
  command = command + " " + item

print command
