

def getStoppedParticleGrid() :

  lifetime = "100ps"

  nEvts = 100000

  request_stoppedparticle = {lifetime : {}}
  request_stoppedparticle_variations = {lifetime : {}}

  for mGluino in range(400,1801,200) : 

    request_stoppedparticle[lifetime][mGluino] = {}

    request_stoppedparticle[lifetime][mGluino][mGluino-100] = nEvts
    request_stoppedparticle[lifetime][mGluino][mGluino-500] = nEvts
    request_stoppedparticle[lifetime][mGluino][100] = nEvts

  # Need to find a way to add variation samples
  request_stoppedparticle_variations[lifetime]= {1000 : 
    {900 : ["spectrum","interaction"],
     100 : ["spectrum","interaction"]}
  }

  return request_stoppedparticle, request_stoppedparticle_variations
