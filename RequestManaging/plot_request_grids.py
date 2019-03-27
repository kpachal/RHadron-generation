import ROOT
import request_dict_DV
import request_dict_dEdx
import request_dict_stopped_particle

request_DV = request_dict_DV.getDVGrid()
request_dEdx = request_dict_dEdx.getdEdxGrid()
request_stoppedparticle,request_stoppedparticle_variations = request_dict_stopped_particle.getStoppedParticleGrid()
print "hello! DV wants:"
print request_DV
print "dEdx wants:"
print request_dEdx
print "stopped particle wants:"
print request_stoppedparticle