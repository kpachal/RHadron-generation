import ROOT
import request_dict_DV
import request_dict_dEdx

request_DV = request_dict_DV.getDVGrid()
request_dEdx = request_dict_dEdx.getdEdxGrid()
print "hello! DV wants:"
print request_DV
print "dEdx wants:"
print request_dEdx