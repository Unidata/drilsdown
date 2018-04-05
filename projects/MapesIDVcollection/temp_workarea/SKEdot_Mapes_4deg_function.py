def calc_for_timerange(*start_stop):
    import os  
    import xarray as xr
    import numpy as np
    inputPath = '/data2/niznik/dlVars_3D/'
    uInputFile = inputPath+'U_r90x45.nc4'
    vInputFile = inputPath+'V_r90x45.nc4'
    wInputFile = inputPath+'W_r90x45.nc4'
    wuwvInputFile = '/data2/suvarchal/G5NR/wv_and_wu_4deg.nc4'
    TInputFile = '/data2/suvarchal/G5NR/T_r90x45_1time.nc4'
    
    u_da=xr.open_dataset(uInputFile) 
    v_da=xr.open_dataset(vInputFile)
    w_da=xr.open_dataset(wInputFile)
    wuwv_da=xr.open_dataset(wuwvInputFile)
    T_da=xr.open_dataset(TInputFile)
    
    P=u_da.lev*100.0 #convert Pressure to Pa and is ordered top down
    dPbyg=np.gradient(P)/9.8
    dPbyg=xr.DataArray(dPbyg,coords={'lev':u_da.lev},dims=['lev'])

    rho=(1/(T_da['T'][0,:,:,:]*287.06))*P #kg/m3 #checked by plotting rho[47,:,:].plot.contourf()
    chunk=500
    start=start_stop[0][0] #-chunk
    stop=start_stop[0][1] #+chunk
    if os.path.isfile('/data2/suvarchal/G5NR/SKE_testX_'+str(format(start,'05'))+'.nc'):
        print ("exists"+str(start))
        return "file exists" 
    u = u_da['U'][start:stop,:,:,:]
    v = v_da['V'][start:stop,:,:,:]
    w = w_da['W'][start:stop,:,:,:]
    wu = wuwv_da['WU'][start:stop,:,:,:]
    wv = wuwv_da['WV'][start:stop,:,:,:]

    Eddy_Flux_Zon = (wu - u*w)*rho
    Eddy_Flux_Mer = (wv - v*w)*rho
    Eddy_Flux_Zon.name='Eddy_Flux_Zon'
    Eddy_Flux_Mer.name='Eddy_Flux_Mer'
    Eddy_Flux_Zon.attrs={'longname':'Eddy_Flux_Zonal','units':'kg m-1 s-2'}
    Eddy_Flux_Mer.attrs={'longname':'Eddy_Flux_Meridional','units':'kg m-1 s-2'}
    #make it a dataset for easy function application on all variables 
    Eddy_Flux=xr.merge([Eddy_Flux_Zon,Eddy_Flux_Mer]) 


    axisint=1 if len(np.shape(Eddy_Flux_Zon))>3 else 0
    Eddy_Flux_Tend=Eddy_Flux.apply(np.gradient,axis=axisint)
    Eddy_Flux_Tend=Eddy_Flux_Tend/dPbyg
    Eddy_Flux_Tend.rename({'Eddy_Flux_Zon':'Eddy_Tend_Zon','Eddy_Flux_Mer':'Eddy_Tend_Mer'},inplace=True)
    Eddy_Flux_Tend.Eddy_Tend_Zon.attrs={'longname':'Eddy Zonal Tendency','units':'m s-2'}
    Eddy_Flux_Tend.Eddy_Tend_Mer.attrs={'longname':'Eddy Meridional Tendency','units':'m s-2'}

    u_baro=(rho*u).sum(dim='lev')/rho.sum(dim='lev')
    v_baro=(rho*v).sum(dim='lev')/rho.sum(dim='lev')
    ushear=u-u_baro
    vshear=v-v_baro 

    SKE=(ushear*ushear+vshear*vshear)*0.5
    SKE=(SKE*rho).sum(dim='lev')/rho.sum(dim='lev')
    SKE.name='SKE'
    SKE.attrs={'long_name':'Average Shear Kinetic Energy','units':'J Kg^-1'}

    SKE2= ((ushear*ushear+vshear*vshear)*0.5*dPbyg).sum(dim='lev')
    SKE2.name='SKE2'
    SKE2.attrs={'long_name':'Vertically Integrated Shear Kinetic Energy','units':'J m-2'}

    SKEDOT=( (Eddy_Flux_Tend['Eddy_Tend_Zon']*ushear)*dPbyg + (Eddy_Flux_Tend['Eddy_Tend_Mer']*vshear)*dPbyg ).sum(dim='lev')
    SKEDOT.name='SKEDOT'
    SKEDOT.attrs={'long_name':'dp/g Integral(-d/dp([uw]-[u][w])*u_shear - d/dp([vw]-[v][w])*v_shear)','units':'W m-2'}

    KEDOT=( (Eddy_Flux_Tend['Eddy_Tend_Zon']*u)*dPbyg + (Eddy_Flux_Tend['Eddy_Tend_Mer']*v)*dPbyg ).sum(dim='lev')
    KEDOT.name='KEDOT'
    KEDOT.attrs={'long_name':'Integral(-d/dp([uw]-[u][w])*u - d/dp([vw]-[v][w])*v)','units':'W m-2'}
    xr.merge([KEDOT,SKEDOT,SKE,SKE2]).to_netcdf('/data2/suvarchal/G5NR/SKE_testX_'+str(format(start,'05'))+'.nc')
    return (start,stop)

#from multiprocessing import Pool
#p=Pool(9)    
#p.imap_unordered(calc_for_timerange,zip(range(len(u_da.time))[0::1000],range(len(u_da.time))[1000::1000]+[len(u_da.time)]))

