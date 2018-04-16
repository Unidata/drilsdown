
# coding: utf-8

# In[1]:

import netCDF4
import numpy as np
import sys

#inputPath = '/home/niznik/niznik-data2/dlVars_3D/'
inputPath = '/data2/niznik/dlVars_3D/'

resTag = ''

uInputFile = inputPath+'U_r90x45'+resTag+'.nc4'
vInputFile = inputPath+'V_r90x45'+resTag+'.nc4'
wInputFile = inputPath+'W_r90x45'+resTag+'.nc4'
wuInputFile = './wv_and_wu_4deg.nc4'
wvInputFile = './wv_and_wu_4deg.nc4'

uCDFIn = netCDF4.Dataset(uInputFile,'r')
vCDFIn = netCDF4.Dataset(vInputFile,'r')
wCDFIn = netCDF4.Dataset(wInputFile,'r')
wuCDFIn = netCDF4.Dataset(wuInputFile,'r')
wvCDFIn = netCDF4.Dataset(wvInputFile,'r')

lons = uCDFIn.variables['lon'][:]
lats = uCDFIn.variables['lat'][:]
levs = uCDFIn.variables['lev'][:]*100. # Pa
times = uCDFIn.variables['time'][:]

lev100  = np.where(levs == 10000. )[0][0]
lev1000 = np.where(levs == 100000.)[0][0]


# In[2]:

# set up for the 3D dp and density arrays
dp = np.gradient(levs)
dp3d = np.zeros( (np.size(levs), np.size(lats), np.size(lons)), dtype='f')
p3d  = np.zeros( (np.size(levs), np.size(lats), np.size(lons)), dtype='f')
for ilat in range(len(lats)):
    for ilon in range(len(lons)):
        p3d[:,ilat,ilon] = levs
        dp3d [:,ilat,ilon] = dp

# Grab a density array, T from 1 time level 
TInputFile = './T_r90x45_1time.nc4' # just 1  time level since it is just for a density, good enough
TCDFIn = netCDF4.Dataset(TInputFile,'r')
T = TCDFIn.variables['T'][0,:,:,:]
rho = p3d /T /287. # Make sure T is in Kelvin, p in Pa

# replace missing values with a zonal mean
latpsection = np.mean(rho,axis=2)
for ilon in range(len(lons)):
    rho[:,:,ilon] = latpsection

#check on T and density
#plt.plot(rho[:,40,40], -levs, rho[:,0,0], -levs)
#plt.contourf(latpsection); plt.colorbar()


# In[3]:

# Loop over times
for tt in range(1): #len(times)):
    timeVar = uCDFIn.variables['time'][tt]

    print 'Started time '+str(tt)+' of 18624... ' + str(timeVar)

#Load the chunked variables for this time level
    u = uCDFIn.variables['U'][tt,:,:,:]
    v = vCDFIn.variables['V'][tt,:,:,:]
    w = wCDFIn.variables['W'][tt,:,:,:]
    wu = wuCDFIn.variables['WU'][tt,:,:,:]
    wv = wvCDFIn.variables['WV'][tt,:,:,:]

# BEM: For clarity, let's compute flux, then EMT (eddy momentum tendency, i.e. flux convergence),
# then its dot product with u_shear, then the vertical integral of that.

    Eddy_Flux_Zon = rho * (wu - u*w)
    Eddy_Flux_Mer = rho * (wv - v*w)

    Eddy_Tend_Zon = 9.8 * np.gradient(Eddy_Flux_Zon, axis=0) / dp3d
    Eddy_Tend_Mer = 9.8 * np.gradient(Eddy_Flux_Mer, axis=0) / dp3d

# need to isolate the shear component of u (subtract off a barotropic mean)
# ** whole atmosphere, or troposphere only? ** Whole, for now

    ushear      = np.copy(u)
    ushear_trop = np.copy(u)
    ubaro      = np.nanmean( rho * u , axis=0) /                  np.nanmean(rho, axis=0)
    ubaro_trop = np.nanmean((rho * u)[lev100:lev1000,:,:], axis=0) /                  np.nanmean((rho * 1)[lev100:lev1000,:,:], axis=0)

    vshear      = np.copy(v)
    vshear_trop = np.copy(v)
    vbaro      = np.nanmean( rho * v , axis=0) /                  np.nanmean(rho, axis=0)
    vbaro_trop = np.nanmean((rho * v)[lev100:lev1000,:,:], axis=0) /                  np.nanmean((rho * 1)[lev100:lev1000,:,:], axis=0)

    for ilev in range(len(levs)):
        ushear[ilev,:,:] -= ubaro
        vshear[ilev,:,:] -= vbaro
        ushear_trop[ilev, :, :] -= ubaro_trop
        vshear_trop[ilev, :, :] -= vbaro_trop
    

    SKE        = np.nansum(rho*(ushear*ushear+vshear*vshear)/2,axis=0)/np.nansum(rho,axis=0)
    # Integrate column over mass (dp/g)
    SKEdot_Zon = np.nansum(  dp3d/9.8 * Eddy_Tend_Zon *ushear , axis=0)
    SKEdot_Mer = np.nansum(  dp3d/9.8 * Eddy_Tend_Mer *vshear , axis=0)
    
    SKEdot_trop_Zon = np.nansum( (dp3d/9.8 * Eddy_Tend_Zon *ushear)[lev100:lev1000,:,:] , axis=0)
    SKEdot_trop_Mer = np.nansum( (dp3d/9.8 * Eddy_Tend_Mer *vshear)[lev100:lev1000,:,:] , axis=0)
    
    KEdot_Zon  = np.nansum( dp3d/9.8 * Eddy_Tend_Zon *u ,      axis=0)
    KEdot_Mer  = np.nansum( dp3d/9.8 * Eddy_Tend_Mer *v ,      axis=0)

    SKEdot = SKEdot_Zon + SKEdot_Mer # W m-2 = kg s-3 = kg m2s-2 s-1 m-2
    SKEdot_trop = SKEdot_trop_Zon + SKEdot_trop_Mer # W m-2 = kg s-3 = kg m2s-2 s-1 m-2
    KEdot   = KEdot_Zon +  KEdot_Mer # W m-2 

# OUTPUT FILE
#    cdfOut.close() # in case an old one was open
    ttf="""%05d"""%(tt)
    outputFilepath = 'SKEDot_90x45_'+str(ttf)+'_test_nansum.nc4'
    cdfOut = netCDF4.Dataset(outputFilepath,'w')

# Fill the file
    lonDim = cdfOut.createDimension('lon',len(lons))
    latDim = cdfOut.createDimension('lat',len(lats))
    levDim = cdfOut.createDimension('lev',len(levs))
    timeDim = cdfOut.createDimension('time',1)

    lonVar = cdfOut.createVariable('lon','f4',('lon',))
    latVar = cdfOut.createVariable('lat','f4',('lat',))
    levVar = cdfOut.createVariable('lev','f4',('lev',))
    timeVar = cdfOut.createVariable('time','i4',('time',))

    lonVar[:] = lons[:]
    latVar[:] = lats[:]
    levVar[:] = levs[:]

    setattr(lonVar,'long_name','longitude')
    setattr(lonVar,'units','degrees_east')

    setattr(latVar,'long_name','latitude')
    setattr(latVar,'units','degrees_north')

    setattr(levVar,'long_name','pressure')
    setattr(levVar,'units','hPa')

    setattr(timeVar,'long_name','time')
    setattr(timeVar,'units','minutes since 2005-05-16 00:30:00')

# Results
# output variables we need to compute: KE tendencies: shear only & total, zonal only & 2D
    SKE_Var = cdfOut.createVariable('SKE','f4',('time','lat','lon',))
    setattr(SKE_Var,'long_name','SKE')
    setattr(SKE_Var,'units','J Kg^-1')
    SKE_Var[:] = SKE[:]

    SKEDot_Var = cdfOut.createVariable('SKEDOT','f4',('time','lat','lon',))
    setattr(SKEDot_Var,'long_name','dp/g Integral(-d/dp([uw]-[u][w])*u_shear - d/dp([vw]-[v][w])*v_shear)')
    setattr(SKEDot_Var,'units','W m-2')
    SKEDot_Var[:] = SKEdot[:]

    SKEDot_ZonVar = cdfOut.createVariable('SKEDOT_ZON','f4',('time','lat','lon',))
    setattr(SKEDot_ZonVar,'long_name','dp/g Integral(-d/dp([uw]-[u][w])*u_shear)')
    setattr(SKEDot_ZonVar,'units','W m-2')
    SKEDot_ZonVar[:] = SKEdot_Zon[:]

    SKEDot_trop_Var = cdfOut.createVariable('SKEDOT_troposphere','f4',('time','lat','lon',))
    setattr(SKEDot_trop_Var,'long_name','1000-100hPa dp/g Integral(-d/dp([uw]-[u][w])*u_shear - d/dp([vw]-[v][w])*v_shear)')
    setattr(SKEDot_trop_Var,'units','W m-2')
    SKEDot_trop_Var[:] = SKEdot_trop[:]

    SKEDot_trop_ZonVar = cdfOut.createVariable('SKEDOT_troposphere_ZON','f4',('time','lat','lon',))
    setattr(SKEDot_trop_ZonVar,'long_name','1000-100hPa dp/g Integral(-d/dp([uw]-[u][w])*u_shear)')
    setattr(SKEDot_trop_ZonVar,'units','W m-2')
    SKEDot_trop_ZonVar[:] = SKEdot_trop_Zon[:]

    KEDot_Var = cdfOut.createVariable('KEDOT','f4',('time','lat','lon',))
    setattr(KEDot_Var,'long_name','Integral(-d/dp([uw]-[u][w])*u - d/dp([vw]-[v][w])*v)')
    setattr(KEDot_Var,'units','W m-2')
    KEDot_Var[:] = KEdot[:]

    KEDot_ZonVar = cdfOut.createVariable('KEDOT_ZON','f4',('time','lat','lon',))
    setattr(KEDot_ZonVar,'long_name','Integral(-d/dp([uw]-[u][w])*u)')
    setattr(KEDot_ZonVar,'units','W m-2')
    KEDot_ZonVar[:] = KEdot_Zon[:]
    
    cdfOut.close()
# Fill the file
    outputFilepath = 'Eddy_Tend_90x45_'+str(ttf)+'_test_nansum.nc4'
    timeVar = uCDFIn.variables['time'][tt]
    cdfOut2 = netCDF4.Dataset(outputFilepath,'w')
    lonDim = cdfOut2.createDimension('lon',len(lons))
    latDim = cdfOut2.createDimension('lat',len(lats))
    levDim = cdfOut2.createDimension('lev',len(levs))
    timeDim = cdfOut2.createDimension('time',1)

    lonVar = cdfOut2.createVariable('lon','f4',('lon',))
    latVar = cdfOut2.createVariable('lat','f4',('lat',))
    levVar = cdfOut2.createVariable('lev','f4',('lev',))
    timeVar = cdfOut2.createVariable('time','i4',('time',))
    

    lonVar[:] = lons[:]
    latVar[:] = lats[:]
    levVar[:] = levs[:]

    setattr(lonVar,'long_name','longitude')
    setattr(lonVar,'units','degrees_east')

    setattr(latVar,'long_name','latitude')
    setattr(latVar,'units','degrees_north')

    setattr(levVar,'long_name','pressure')
    setattr(levVar,'units','hPa')

    setattr(timeVar,'long_name','time')
    setattr(timeVar,'units','minutes since 2005-05-16 00:30:00')
    timeVar = uCDFIn.variables['time'][tt]
    
    

    Eddy_Flux_ZonVar = cdfOut2.createVariable('Eddy_Flux_Zon','f4',('time','lev','lat','lon',))
    setattr(Eddy_Flux_ZonVar,'long_name','Zonal Eddy Flux')
    setattr(Eddy_Flux_ZonVar,'units','W m-2')
    Eddy_Flux_ZonVar[:] = Eddy_Flux_Zon[:]
    
    Eddy_Flux_MerVar = cdfOut2.createVariable('Eddy_Flux_Mer','f4',('time','lev','lat','lon',))
    setattr(Eddy_Flux_MerVar,'long_name','Meridional Eddy Flux')
    setattr(Eddy_Flux_MerVar,'units','W m-2')
    Eddy_Flux_MerVar[:] = Eddy_Flux_Mer[:]
    
    Eddy_Tend_ZonVar = cdfOut2.createVariable('Eddy_Tend_Zon','f4',('time','lev','lat','lon',))
    setattr(Eddy_Tend_ZonVar,'long_name','Zonal Eddy Tendency')
    setattr(Eddy_Tend_ZonVar,'units','m s^-2')
    Eddy_Tend_ZonVar[:] = Eddy_Tend_Zon[:]
    
    Eddy_Tend_MerVar = cdfOut2.createVariable('Eddy_Tend_Mer','f4',('time','lev','lat','lon',))
    setattr(Eddy_Tend_MerVar,'long_name','Meridional Eddy Tendency')
    setattr(Eddy_Tend_MerVar,'units','m s^-2')
    Eddy_Tend_MerVar[:] = Eddy_Tend_Mer[:]
    cdfOut2.close()

    exit

# In[4]:

uCDFIn.close()
vCDFIn.close()
wCDFIn.close()
wuCDFIn.close()
wvCDFIn.close()
