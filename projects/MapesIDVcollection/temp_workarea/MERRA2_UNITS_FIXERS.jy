def theta(temp):
  """Returns potential temperature with proper units that MERRA-2 misses.
  """
  temp= newUnit(temp, "temp", "K")
  return DerivedGridFactory.createPotentialTemperature(temp)

def thetae(temp,rh):
  """Returns equivalent potential temperature with proper units that MERRA-2 misses.
  """
  temp= newUnit(temp, "temp", "K")
  return DerivedGridFactory.createEquivalentPotentialTemperature(temp,rh)
