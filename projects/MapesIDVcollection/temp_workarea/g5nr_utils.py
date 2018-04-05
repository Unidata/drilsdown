class getG5NRImage:
    g5nr_variables=("aerosols","carbon","cloudsir","cloudsvis","cyclones")
    g5nr_variables+=("storms","temperature","tropical","water","winds")
    current_variable=None
    def __init__(self,centerlon=None,centerlat=None,deltalon=5,deltalat=5,yyyymmdd=20050601,timedeltaday=0,cycle=False,**kwargs):
        from urllib import urlopen
        from PIL import Image
        import ssl
        try:
            #check if year month day are passed as keyword arguments
            year=str(kwargs['year'])
            month=format(kwargs['month'],"02")
            day=format(kwargs['day'],"02")
        except KeyError:
            year=str(yyyymmdd)[0:4]
            month=str(yyyymmdd)[4:6]
            day=str(yyyymmdd)[6:8]
            
        try:
            #check if keyword argument is present
            self.cropLeftLon=kwargs['cropLeftLon']
            self.cropRightLon=kwargs['cropRightLon']
            self.cropTopLat=kwargs['cropTopLat']
            self.cropBottomLat=kwargs['cropBottomLat']
        except KeyError:
            try:
                #if centerlat,lon values are legal
                self.cropLeftLon=centerlon-deltalon
                self.cropRightLon=centerlon+deltalon
                self.cropTopLat=centerlat+deltalat
                self.cropBottomLat=centerlat-deltalat
            except TypeError:
                #None case where we want whole image
                self.cropLeftLon=0
                self.cropRightLon=360
                self.cropTopLat=90
                self.cropBottomLat=-90

        if 'variable' in kwargs:
            self.__set_variable_props(variable)
            
        self.cycle = cycle
        self.yyyymmdd=[year+month+format(int(day)+i,"02") for i in range(-1*abs(timedeltaday),abs(timedeltaday)+1)]
 


            
        #self.image=self.__getImage(self.urls[0])
        self.urlindex=0
        #self.url=self.urls[self.urlindex]
        self.image=None
        self.format='png'
        self.context = ssl._create_unverified_context()
    def __set_variable_props(self,variable):
        assert variable in self.g5nr_variables,"variable not found use one of : "+self.g5nr_variables

        self.current_variable=variable
        #below is necessary beacuse aerosol and carbon images start at different longitudes
        if self.current_variable=="aerosols" or self.current_variable=="carbon":
            self.origLeftLon=-180.0
            self.origRightLon=180.0
            self.origTopLat=90.0
            self.origBottomLat=-90.0
          
            self.cropLeftLon=cropLeftLon-180.0
            self.cropRightLon=cropRightLon-180.0                
        else:
            self.origLeftLon=-17.5
            self.origRightLon=342.5
            self.origTopLat=90
            self.origBottomLat=-90
        self.urls=[self.__getURL(date) for date in self.yyyymmdd]
            
    def __getURL(self,yyyymmdd):
        baseurl="https://g5nr.nccs.nasa.gov/static/naturerun/fimages"
        d="/"
        
        stringList=[baseurl,self.current_variable.upper(),"Y"+yyyymmdd[0:4],"M"+yyyymmdd[4:6],"D"+yyyymmdd[6:8]]
        stringList+=[self.current_variable.lower()+"_globe_c1440_NR_BETA9-SNAP_"+yyyymmdd+"_0000z.png"]
        url=d.join(stringList)
        return url
    @staticmethod
    def getURL(variable,yyyymmdd):
        baseurl="https://g5nr.nccs.nasa.gov/static/naturerun/fimages"
        d="/"
        
        stringList=[baseurl,variable.upper(),"Y"+yyyymmdd[0:4],"M"+yyyymmdd[4:6],"D"+yyyymmdd[6:8]]
        stringList+=[variable.lower()+"_globe_c1440_NR_BETA9-SNAP_"+yyyymmdd+"_0000z.png"]
        url=d.join(stringList)
        return url   
    def __getImage(self,url):
        from geoimage import GeoLocateImage

        geoimageobj=GeoLocateImage(url,self.origLeftLon,self.origRightLon,self.origTopLat,self.origBottomLat,context=self.context)
        return geoimageobj.crop_at_llbox(self.cropLeftLon,self.cropRightLon,self.cropTopLat,self.cropBottomLat)
    def __iter__(self):
        return self
    def next(self):
        try:
            
            if self.urlindex<=len(self.urls)-1:
                self.image=self.__getImage(self.urls[self.urlindex])
                self.url=self.urls[self.urlindex]
                self.date=self.yyyymmdd[self.urlindex]
                self.urlindex+=1
                return self.image
            elif self.cycle:
                print('Warning Back to first image')
                self.urlindex=0
                self.image=self.__getImage(self.urls[self.urlindex])
                self.url=self.urls[self.urlindex]
                self.date=self.yyyymmdd[self.urlindex]
                return self.image
            else:
                raise StopIteration('End of loop: use cycle = True if you want to want to loop')
        except:
            raise 
    def save(self,filename=None):
        if filename==None:
            filename="./"+self.current_variable+"_"+str(self.cropLeftLon)+"_"+str(self.cropRightLon)
            filename+="_"+str(self.cropTopLat)+"_"+str(self.cropBottomLat)
            filename+="_"+self.yyyymmdd[self.urlindex]+".png"
        try:
            self.image.save(filename)
        except IOError:
            raise IOError('Bad filename provided '+filename) 
    def save_animation(self,filename=None,duration=1000):
        from PIL import __version__ as version
        assert float(version[0:3])>=3.4,"Saving animation works only with pillow library version >= 3.4"
        if filename==None:
            filename="./"+self.current_variable+"_"+str(self.cropLeftLon)+"_"+str(self.cropRightLon)
            filename+="_"+str(self.cropTopLat)+"_"+str(self.cropBottomLat)
            filename+="_"+self.yyyymmdd[self.urlindex]+".gif"
        temp_urlindex=self.urlindex
        self.urlindex=0
        print("saving to file : "+filename)
        try:
            images=[i for i in self]
            assert len(images)>1,"Only one time step available, use save method"
            images[0].save(filename,append_images=images[1:],save_all=True,duration=duration)
            self.urlindex=temp_urlindex
        except IOError:
            self.urlindex=temp_urlindex
            raise IOError('Bad filename provided '+filename)
        except:
            raise
    #def __repr__(self):
    #    if self.image==None:
    #        self.next()
    #        return "hey"+"\n"+self._repr_png_()
    #    else:
    #        return self._repr_png()
    
#    def _repr_png_(self):
#        from io import BytesIO
#        b = BytesIO()
#        if self.image==None:
#            self.next() #it updates the images
#        self.image.save(b, 'PNG')
#        return b.getvalue()
    def __getitem__(self,variable):
        self.__set_variable_props(variable)
        self.image=self.__getImage(self.urls[self.urlindex])
        return self