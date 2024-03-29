

def getdEdxGrid(ambitionLevel) :

  lifetimes = ["300ps","1ns","3ns","10ns","30ns","stable"]

  nEvts = 30000

  highestMasses = {"300ps" : 1801, 
                   "1ns" : 2001,
                   "3ns" : 2601,
                   "10ns" : 3001,
                   "30ns" : 3001,
                   "stable" : 3001}

  request_dEdx = {}

  for lifetime in lifetimes :

    request_dEdx[lifetime] = {}

    # Each mass will also be a sub-dictionary
    # of neutralino masses, number of events

    # Grid is every 50 up to 700...
    for mGluino in range(400,701,50) :

      request_dEdx[lifetime][mGluino] = {}

      # For low masses, only for "important" lifetimes and masses, bump up the request size
      # if you are feeling ambitious.
      useEvents = nEvts
      if not "3" in lifetime and mGluino % 100 == 0 :
        if ambitionLevel==2 :
          if mGluino < 1001 : useEvents = 90000
          elif mGluino < 1401 : useEvents = 50000
        elif ambitionLevel==3 :
          if mGluino < 1001 : useEvents = 160000
          elif mGluino < 1401 : useEvents = 50000

      # Only keep every 100 for compressed spectra
      # and for intermediate lifetimes
      if mGluino % 50 == 0 and mGluino % 100 != 0 : 

        if not "3" in lifetime : 
          request_dEdx[lifetime][mGluino][100] = useEvents

      # Else keep compressed spectra also
      else :
        request_dEdx[lifetime][mGluino][100] = useEvents

        # Don't need compressed scenarios for stable lifetimes
        if not "stable" in lifetime :
          request_dEdx[lifetime][mGluino][mGluino-30] = useEvents

      # If we didn't fill anything for this lifetime/mass, don't keep it
      if not request_dEdx[lifetime][mGluino] :
        del request_dEdx[lifetime][mGluino]

    # From 800 up, only look at every 200 GeV
    for mGluino in range(800,3001,200) :

      # For low masses, only for "important" lifetimes and masses, bump up the request size
      # if you are feeling ambitious.
      useEvents = nEvts
      if not "3" in lifetime and mGluino % 100 == 0 :
        if ambitionLevel==2 :
          if mGluino < 1001 : useEvents = 90000
          elif mGluino < 1401 : useEvents = 50000
        elif ambitionLevel==3 :
          if mGluino < 1001 : useEvents = 160000
          elif mGluino < 1401 : useEvents = 50000

      request_dEdx[lifetime][mGluino] = {}

      # Keep up to highest mass in dict
      if mGluino < highestMasses[lifetime] :
        request_dEdx[lifetime][mGluino][100] = useEvents

        # ... unless compressed, which stops even sooner.
        # And again, don't need compressed for stable lifetimes.
        if mGluino < 2401 and not "stable" in lifetime :
          request_dEdx[lifetime][mGluino][mGluino-30] = useEvents

      # If we didn't fill anything for this lifetime/mass, don't keep it
      if not request_dEdx[lifetime][mGluino] :
        del request_dEdx[lifetime][mGluino]          

  return request_dEdx
