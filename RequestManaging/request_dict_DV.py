

def getDVGrid() :

  lifetimes = ["10ps", "100ps","1ns","10ns"]
  numbermap_lowsensitivity = {1100 : 160000,
                              1500 : 50000,
                              3100 : 30000}
  numbermap_highsensitivity = {1100 : 300000,
                              1500 : 100000,
                              3100 : 30000}

  request_DV = {}

  for lifetime in lifetimes :

    request_DV[lifetime] = {}

    # Each mass will also be a sub-dictionary
    # of neutralino masses, number of events
    # Grid based around mGluino between 1 and 3 TeV
    # in 200 GeV blocks.
    for mGluino in range(1000,3001,200) :
      request_DV[lifetime][mGluino] = {}

    # Low end of sensitivity
    if "10ps" in lifetime or "10ns" in lifetime :

      # Compressed
      for mGluino in range(1000,2001,200) :
        
        # Number of events
        correctInterval = 1100
        for separation in reversed(sorted(numbermap_lowsensitivity.keys())) :
          if mGluino < separation :
            nEvts = numbermap_lowsensitivity[separation]

        # Really compressed        
        request_DV[lifetime][mGluino][mGluino - 30] = nEvts

        # Somewhat compressed
        request_DV[lifetime][mGluino][mGluino  - 100] = nEvts

      # Non-compressed
      for mGluino in range(1600, 2601, 200) :

        # Number of events
        nEvts = 0
        for separation in reversed(sorted(numbermap_lowsensitivity.keys())) :
          if mGluino < separation :
            nEvts = numbermap_lowsensitivity[separation]

        request_DV[lifetime][mGluino][100] = nEvts
        
    # Medium sensitivity
    if "1ns" in lifetime :

      # Compressed
      for mGluino in range(1000, 2401,200) :

        # Number of events
        nEvts = 0
        for separation in reversed(sorted(numbermap_lowsensitivity.keys())) :
          if mGluino < separation :
            nEvts = numbermap_lowsensitivity[separation]

        # Really compressed        
        request_DV[lifetime][mGluino][mGluino - 30] = nEvts

        # Somewhat compressed
        request_DV[lifetime][mGluino][mGluino  - 100] = nEvts

      # Non-compressed
      for mGluino in range(1600, 3001, 200) :      

        # Number of events
        nEvts = 0
        for separation in reversed(sorted(numbermap_lowsensitivity.keys())) :
          if mGluino < separation :
            nEvts = numbermap_lowsensitivity[separation]

        request_DV[lifetime][mGluino][100] = nEvts

    # High sensitivity
    if "100ps" in lifetime :

      # Compressed
      for mGluino in range(1000, 2401,200) :

        # Number of events
        nEvts = 0
        for separation in reversed(sorted(numbermap_highsensitivity.keys())) :
          if mGluino < separation :
            nEvts = numbermap_highsensitivity[separation]

        # Really compressed        
        request_DV[lifetime][mGluino][mGluino - 10] = nEvts

        # Somewhat compressed
        request_DV[lifetime][mGluino][mGluino  - 30] = nEvts

      # Less compressed to non-compressed
      for mGluino in range(1600, 3001, 200) :      

        # Number of events
        nEvts = 0
        for separation in reversed(sorted(numbermap_highsensitivity.keys())) :
          if mGluino < separation :
            nEvts = numbermap_highsensitivity[separation]

        # Still compressed, ish
        # This one doesn't have to go as far
        if mGluino < 2401 :
          request_DV[lifetime][mGluino][mGluino - 100] = nEvts

        # Filling diagonals
        request_DV[lifetime][mGluino][mGluino - 200] = nEvts
        request_DV[lifetime][mGluino][mGluino - 500] = nEvts
        request_DV[lifetime][mGluino][mGluino - 1000] = nEvts

        # And light neutralino
        request_DV[lifetime][mGluino][100] = nEvts

  return request_DV
