import swisseph as swe
import time
from datetime import datetime,timezone,timedelta
from pytz import timezone
from astro_calc import *
from func_tools import *

class constants:
    aspects_PM=[0,30,-30,45,-45,60,-60,90,-90,120,-120,180,150,-150,135,-135]
    aspects_PM_major=[0,60,-60,90,-90,120,-120,180]
c=constants

import math 
def cos(δ): 
    radians=math.radians(δ)
    return math.cos(radians)

def sin(δ): 
    radians=math.radians(δ)
    return math.sin(radians)

def tan(δ): 
    radians=math.radians(δ)
    return math.tan(radians)

def atan(x):
    radians=math.atan(x)    
    δ=math.degrees(radians)
    return δ

def asin(x):
    radians=math.asin(x)
    δ=math.degrees(radians)
    return δ

def acos(x):
    radians=math.acos(x)
    δ=math.degrees(radians)
    return δ

class calc_for_3D:
    def __init__(self):
        self.aspects=c.aspects_PM
        ε=23.44
        self.ε=ε
    
    def get_planets_data(self, date_utc,time_utc,latitude,longitude,trueNode=True): # equatorial
        date_=format_date_time(date_utc,time_utc)
        julday_ = swe.julday(*date_)
        s=swe.calc_ut(julday_, -1) #SE_ECL_NUT = -1   #ecliptic obliquity ε  
        ε=s[0][0]
        self.ε=ε

        if trueNode==True:
            omit_Node="mean Node"
        else:
            omit_Node="true Node"

        planets_data={}
        for i in range(12):
            pl=swe.get_planet_name(i)
            if pl==omit_Node:continue

            pl=pl.replace("true Node","Node_N")
            pl=pl.replace("mean Node","Node_N")
            planets_data[pl]={}         
            pl_pos_obj=swe.calc_ut(julday_, i)
            pl_ecl_lon = pl_pos_obj[0][0]
            pl_ecl_lat = pl_pos_obj[0][1]
            pl_speed   = pl_pos_obj[0][3]
            planets_data[pl]["ecl"]=(pl_ecl_lon,pl_ecl_lat,pl_speed)
            obj_eq=swe.calc_ut(julday_, i,2048)  #right ascension, declination, distance
            pl_RA=obj_eq[0][0]
            pl_decl=obj_eq[0][1]
            planets_data[pl]["eq"]=(pl_RA,pl_decl) 
            
            if pl=="Node_N":
                planets_data["Node_S"]={}
                pl_ecl_lon=pl_ecl_lon+180
                pl_ecl_lon=norm_(pl_ecl_lon)
                pl_RA=pl_RA+180
                pl_RA=norm_(pl_RA)
                planets_data["Node_S"]["ecl"]=(pl_ecl_lon,0,pl_speed)
                planets_data["Node_S"]["eq"]=(pl_RA,-pl_decl) 

        try:
            houses_pos=swe.houses(julday_, latitude,longitude,  b'P')
        except:
            houses_pos=swe.houses(julday_, latitude,longitude,  b'E')

        Asc=houses_pos[1][0]
        MC=houses_pos[1][1]
        ARMC=houses_pos[1][2]
        planets_data["Asc"]={}; planets_data["MC"]={}
        planets_data["Asc"]["ecl"]=(Asc,0)
        planets_data["MC"]["ecl"]=(MC,0)

        s= swe.cotrans(Asc,0,1,-ε) #ecliptic -> equator:-ε 
        Asc_RA=s[0]; Asc_decl=s[1]
        planets_data["Asc"]["eq"]=(Asc_RA,Asc_decl)
        MC_RA,MC_decl,d = swe.cotrans(MC,0,1,-ε)
        MC_AD=0
        planets_data["MC"]["eq"]=(ARMC,MC_decl)
        try:
            Asc_AD= asin(tan(Asc_decl) * tan(latitude))
        except:
            Asc_AD=0

        Dsc=norm_(Asc + 180)
        s= swe.cotrans(Dsc,0,1,-ε) 
        Dsc_RA=s[0]; Dsc_decl=s[1]
        planets_data["Dsc"]={}
        planets_data["Dsc"]["ecl"]=(Dsc,0)
        planets_data["Dsc"]["eq"]=(Dsc_RA,Dsc_decl)

        IC=MC+180
        IC=norm_(IC)
        s= swe.cotrans(IC,0,1,-ε) 
        IC_RA=s[0]; IC_decl=s[1]
        planets_data["IC"]={}
        planets_data["IC"]["ecl"]=(IC,0)
        planets_data["IC"]["eq"]=(IC_RA,IC_decl)

        #Oblique Ascension
        Asc_OA = ARMC + 90
        Asc_OA=norm_(Asc_OA)
        planets_data["Asc"]["OA"] = Asc_OA       
        planets_data["Asc"]["AD"] = Asc_AD
        planets_data["Asc"]["OA_e"]= Asc_OA
        planets_data["Asc"]["AD_e"]= Asc_AD

        planets_data["MC"]["OA"] =planets_data["MC"]["OA_e"]=0
        planets_data["MC"]["AD"] = planets_data["MC"]["AD_e"]=0     

        planets_data["Asc"]["RA_e"] = Asc_RA
        planets_data["MC"]["RA_e"] = ARMC

        Dsc_OD=ARMC - 90 # Oblique Descension
        Dsc_OD=norm_(Dsc_OD)
        planets_data["Dsc"]["OA"]= Dsc_OD
        planets_data["Dsc"]["AD"]= -Asc_AD 
        planets_data["Dsc"]["OA_e"]= Dsc_OD
        planets_data["Dsc"]["AD_e"]= -Asc_AD 
        planets_data["Dsc"]["RA_e"] = Dsc_RA    

        planets_data["IC"]["OA"] =planets_data["IC"]["OA_e"]=0
        planets_data["IC"]["AD"] = planets_data["IC"]["AD_e"]=0  
        RA_e= norm_(ARMC+180)
        planets_data["IC"]["RA_e"] = RA_e

        for pl,obj in planets_data.items():
            #if pl in ["Asc","MC","Dsc","IC"]:continue
            ecl_long=planets_data[pl]["ecl"][0]
            RA=planets_data[pl]["eq"][0]
            decl=planets_data[pl]["eq"][1]
            try: 
                AD= asin(tan(decl) * tan(latitude))
                OA = RA - AD
            except:
                AD=0
                OA=0

            planets_data[pl]["OA"] = OA
            planets_data[pl]["AD"] = round(AD,5)
            RA_,decl_,d = swe.cotrans(ecl_long,0,1,-ε)
            try: 
                AD= asin(tan(decl_) * tan(latitude))
                OA = RA - AD
            except:
                AD=0
                OA=0

            if pl not in ["Asc","Dsc","MC","IC"]:
                planets_data[pl]["OA_e"] = OA
                planets_data[pl]["AD_e"] = round(AD,5)
                planets_data[pl]["RA_e"] = RA_

            OAA=Asc_OA
            try:
                Q=self.get_Q(OAA, RA, decl, latitude)
            except:
                Q=0

            hemi_=self.get_hemi_west_east(RA, ARMC)
            if pl in ["Asc","MC","Dsc","IC"]:Q=0   
            if hemi_=="east":
                QRA = RA - Q
            if hemi_=="west":
                QRA = RA + Q
            QRA=norm_(QRA)
            planets_data[pl]["Q"]=Q
            planets_data[pl]["QRA"]=QRA

        for el in ["MC","IC"]:
            planets_data[el]["Q"]=0
            planets_data[el]["QRA"]=planets_data[el]["eq"][0]

        return planets_data

    def get_quadrant(self,RA,AD,planets,pl=""):
        RAMC=planets["MC"]["eq"][0]
        RA_rel= RA - RAMC        
        if RA_rel<0:RA_rel=RA_rel+360
        if RA_rel>=360:RA_rel=RA_rel-360

        MD=abs(RA-RAMC)
        if MD>180:MD=360-MD
        DSA=90+AD

        if MD>DSA:
            if RA_rel<180:
                quadrant=1
            else:
                quadrant=2
        else:
            if RA_rel<180:
                quadrant=4
            else:
                quadrant=3
        return quadrant

    def get_hemi_west_east(self,RA, ARMC):
        hemi_="east"
        RA_rel= RA - ARMC
        if RA_rel>=360:RA_rel=RA_rel-360
        if RA_rel<0:RA_rel=RA_rel+360
        if RA_rel>180:
            hemi_="west"
        return hemi_

    def get_Q(self,OAA,RA,declination,geo_latitude):
        ALT_MER = atan(tan(OAA-RA) / cos(geo_latitude))
        θ = acos(cos(OAA-RA) * sin(geo_latitude))
        DPV = atan(tan(geo_latitude) * sin(OAA-RA))

        R = DPV - declination
        Δ = atan(cos(θ) * tan(R))
        APH = ALT_MER - Δ
        pole = asin(cos(APH) * sin(geo_latitude))    
        Q = asin(tan(declination) * tan(pole))
        return Q


if __name__ == "__main__":
    pass


