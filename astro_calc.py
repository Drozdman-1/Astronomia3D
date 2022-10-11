import time
from datetime import datetime,timezone,timedelta
from pytz import timezone
import swisseph as swe
import json 
import os

#House_sys="P";  # Placidus P ; Koch K;Porphyrius O ; Regiomontanus R; E Equal
#House_sys = House_sys.encode('ASCII')
House_sys=b"P" #byte string
#House_sys=b"E"

swe.set_ephe_path('ephe')

zodiac = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
weekdays=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def get_chart_data(date_utc,time_utc,latitude,longitude,House_sys=b"P",trueNode=True):
    print("|get_chart_data=",date_utc,time_utc,latitude,longitude,"trueNode",trueNode,"House_sys=",House_sys)
    date_=format_date_time(date_utc,time_utc) 
    latitude=float(latitude);longitude=float(longitude)
    date_julian_day = swe.julday(*date_) 
    planets_pos,houses_pos= get_planets(date_julian_day,latitude,longitude,House_sys,trueNode=trueNode)
    planets_obj=get_planets_obj(planets_pos)
    houses_obj=get_houses_obj(houses_pos)
    houses_obj["Asc"]=planets_obj["Asc"]
    houses_obj["MC"]=planets_obj["MC"]
    houses_obj["ARMC"]=planets_obj["ARMC"]
    del planets_obj["ARMC"]
    return planets_obj, houses_obj

def get_planets(julday_,latitude,longitude,House_sys,trueNode=True):
    planets_pos={}
    for i in range(12):
        pl_pos_obj=swe.calc_ut(julday_, i) 
        pl=swe.get_planet_name(i)
        pl_pos=pl_pos_obj[0][0]
        pl_speed=pl_pos_obj[0][3]        
        planets_pos[pl]=(pl_pos,pl_speed)

    if trueNode==True:
        planets_pos= add_Nodes(planets_pos,"true Node")  #MEAN_NODE = 10 TRUE_NODE = 11
    else:
        planets_pos= add_Nodes(planets_pos,"mean Node")
    try:
        houses_pos=swe.houses(julday_, latitude,longitude, House_sys)
    except:
        houses_pos=swe.houses(julday_, latitude,longitude,  b'E')

    Asc=houses_pos[1][0]
    MC=houses_pos[1][1]
    ARMC=houses_pos[1][2]
    planets_pos["Asc"]=(Asc,0)
    planets_pos["MC"]=(MC,0)
    planets_pos["ARMC"]=(ARMC,0)
    houses_pos=houses_pos[0]
    return (planets_pos, houses_pos)

def get_planets_obj(planets_pos):
    planets_obj={}
    for pl in planets_pos:
        ω=planets_pos[pl][0]
        s,dec= divmod(ω,30)
        sign =zodiac[int(s)]
        deg=dec_to_deg(dec)
        planets_obj[pl]=(sign,dec,deg,ω,planets_pos[pl][1])
    return  planets_obj 

def get_houses_obj(houses_pos):
    houses_obj={}
    for i in range(len(houses_pos)):
        ω=houses_pos[i]     
        s,dec= divmod(ω,30)
        sign =zodiac[int(s)]
        deg=dec_to_deg(dec)
        h_='house'+ str(i+1)
        houses_obj[h_]=(sign,dec,deg,ω)
    return  houses_obj 

def format_date_time(date_,time_):
    arr=str(date_).split("-")
    arr= [int(el) for el in arr] 
    year=arr[2]; month=arr[1]; day=arr[0];
    date_arr=[year,month,day]
    arr=str(time_).split(":")
    arr= [int(el) for el in arr]    
    hour=arr[0];minute= arr[1]; second=arr[2]
    time_dec=hour + minute/60 + second/3600 
    date_arr.append(time_dec)
    return date_arr

def format_date_timestamp(timestamp):
    obj_UTC = time.gmtime(timestamp)
    date_arr= [obj_UTC[i] for i in range(len(obj_UTC)) if i<3 ]
    hour=obj_UTC[3];minute= obj_UTC[4]; second=obj_UTC[5]
    time_dec=hour + minute/60 + second/3600 
    date_arr.append(time_dec)
    return date_arr


def dec_to_deg(dec):
    dec_sign=bool(dec>0) - bool(dec<0)
    dec=abs(dec)
    if dec>360: dec-=360
    d,m = divmod(dec*60,60)
    m,s = divmod(m*60,60)    
    s = str(round(d)) + "°" + str(round(m)) + "ʹ"+ str(round(s)) + 'ʺ'
    s = "-" + s if dec_sign==-1 else s
    return s


def degrees_to_decimal(deg):
    import re
    r_ = re.search(r"(-)?(\d+)(?:°|d)(\d*(?:\.\d*)?)(?:'|m)?(\d*)(\d*(?:\.\d*)?)?", deg)
    sign = r_.group(1) 
    d = r_.group(2) 
    m = r_.group(3) 
    s = r_.group(4)  
    if sign==None:
        r_2 = re.search(r"N|S|W|E", deg, re.IGNORECASE)
        if r_2!=None:
            if r_2.group(0).upper() in ["S","W"]:
                sign="-"
    d = float(int(d))
    m = float(float(m)) if m!="" else 0
    s = float(float(s)) if s!="" else 0
    ω = d + m/60 + s/3600
    if sign=="-":ω= "-" + str(ω) 
    return ω


def add_Nodes(planets,node_):
    node=planets[node_]
    planets["Node_N"]=node
    s = node[0] + 180
    if s>360:s=s-360
    planets["Node_S"]=(s,node[1])
    del planets["mean Node"]
    del planets["true Node"]
    return planets

#============================================

def get_time_now(seconds=None,tz_=None):
    if seconds==None:
        seconds = time.time()
    if tz_!=None:
        tz_=timezone(tz_)
    
    if os.name=="nt" and seconds<0: # fix Windows bug
        dt_UTC_=datetime.utcfromtimestamp(0) + timedelta(seconds=int(seconds))
        if tz_==None:
            dt_local_=datetime.fromtimestamp(0) + timedelta(seconds=int(seconds))
        else:
            dt_local_=datetime.fromtimestamp(0,tz_) + timedelta(seconds=int(seconds))

        dt_UTC = dt_UTC_.strftime("%d-%m-%Y %H:%M:%S")#.lstrip("0").replace(".0", ".").replace(" 0", " ") 
        dt_loc2 = dt_local_.strftime("%d %b %Y").lstrip("0")
        dt_local = dt_local_.strftime("%d-%m-%Y %H:%M:%S").lstrip("0").replace("-0", "-").replace(" 0", " ") 

    else:
        dt_UTC_=datetime.utcfromtimestamp(seconds)
        dt_UTC=dt_UTC_.strftime("%d-%m-%Y %H:%M:%S")#.lstrip("0").replace(".0", ".").replace(" 0", " ") 
        if tz_==None:
            dt_local_=datetime.fromtimestamp(seconds)
        else:
            dt_local_=datetime.fromtimestamp(seconds,tz_)

        dt_local=dt_local_.strftime("%d-%m-%Y %H:%M:%S").lstrip("0").replace("-0", "-").replace(" 0", " ") 
        dt_loc2 =dt_local_.strftime("%d %b %Y").lstrip("0")

        #dt_local=datetime.fromtimestamp(seconds).strftime("%d-%m-%Y %H:%M:%S").lstrip("0").replace("-0", "-").replace(" 0", " ") 
        #dt_loc2 =datetime.fromtimestamp(seconds).strftime("%d %b %Y").lstrip("0")
    weekday_loc=dt_local_.weekday()
    weekday_loc=weekdays[weekday_loc]
    weekday_UTC=dt_UTC_.weekday()
    weekday_UTC=weekdays[weekday_UTC]        
    t_obj={"date_utc" : dt_UTC.split(" ")[0],"time_utc" : dt_UTC.split(" ")[1], "date_loc" : dt_local.split(" ")[0],"time_loc" : dt_local.split(" ")[1], "date_loc2" :dt_loc2, "timestamp": seconds,"weekday_UTC":weekday_UTC,"weekday_loc":weekday_loc}
    return t_obj


def add_days(timestamp, seconds=0, minutes=0, hours=0, days=0, years=0, tz_=None):
    seconds_add = seconds
    seconds_add += minutes * 60 
    seconds_add += hours * 60*60
    seconds_add += days * 24*60*60
    seconds_add += years * 365*24*60*60
    seconds_new = timestamp + seconds_add

    if tz_!=None:
        from pytz import timezone
        tz_=timezone(tz_)

    if os.name=="nt" and seconds_new<0: # fix Windows bug
        dt_UTC_new_=datetime.utcfromtimestamp(0) + timedelta(seconds=int(seconds_new)) 
        dt_local_new_=datetime.fromtimestamp(0,tz_) + timedelta(seconds=int(seconds_new))
        dt_loc_new2 = dt_local_new_.strftime("%d %b %Y").lstrip("0")
        dt_UTC_new = dt_UTC_new_.strftime("%d-%m-%Y %H:%M:%S")#.lstrip("0").replace(".0", ".").replace(" 0", " ") 
        dt_local_new = dt_local_new_.strftime("%d-%m-%Y %H:%M:%S").lstrip("0").replace("-0", "-").replace(" 0", " ") 
    else:
        dt_UTC_new_=datetime.utcfromtimestamp(seconds_new)
        dt_UTC_new=dt_UTC_new_.strftime("%d-%m-%Y %H:%M:%S")#.lstrip("0").replace(".0", ".").replace(" 0", " ") 
        dt_local_new_=datetime.fromtimestamp(seconds_new,tz_)
        dt_local_new=dt_local_new_.strftime("%d-%m-%Y %H:%M:%S").lstrip("0").replace("-0", "-").replace(" 0", " ") 
        dt_loc_new2 =dt_local_new_.strftime("%d %b %Y").lstrip("0")


    weekday_loc=dt_local_new_.weekday()
    weekday_loc=weekdays[weekday_loc]
    weekday_UTC=dt_UTC_new_.weekday()
    weekday_UTC=weekdays[weekday_UTC]        

    t_obj={"date_utc" : dt_UTC_new.split(" ")[0],"time_utc" : dt_UTC_new.split(" ")[1], "date_loc" : dt_local_new.split(" ")[0],"time_loc" : dt_local_new.split(" ")[1], "date_loc2" :dt_loc_new2, "timestamp": seconds_new,"weekday_UTC":weekday_UTC,"weekday_loc":weekday_loc}

    return t_obj


def get_time_progression(seconds_natal,seconds_now,tz_=None ,reverse=False):
    minute = 60
    hour = 60*60
    day = 24*60*60 #86400
    #year = 365.25*24*60*60 #31557600
    year= 365*24*60*60 + 5*60*60 + 48*60 + 46 #31556880 = #365 days, 5 hours, 48 minutes, 46 seconds= 365.2422 days
    delta= seconds_now - seconds_natal

    if delta<0:return None

    y_l,r = divmod(delta,year); d_l,r1 = divmod(r,day)
    ratio=r/year
    y_dec=round(delta/year,3)
    sec_add= y_l * day + ratio * day
    seconds_prog=seconds_natal+sec_add  

    d,r2 = divmod(sec_add,day);
    h,r3 = divmod(r2,hour);
    m,r4 = divmod(r3,minute);

    if reverse==True:
        seconds_prog=seconds_natal-sec_add

    if tz_!=None:
        from pytz import timezone
        tz_=timezone(tz_)

    if os.name=="nt" and seconds_prog<0: # fix Windows bug
        dt_UTC_prog_=datetime.utcfromtimestamp(0) + timedelta(seconds=int(seconds_prog)) 
        dt_UTC_prog = dt_UTC_prog_.strftime("%d-%m-%Y %H:%M:%S")#.lstrip("0").replace(".0", ".").replace(" 0", " ")
        if tz_==None:
            dt_local_prog_=datetime.fromtimestamp(0) + timedelta(seconds=int(seconds_prog))
        else:
            dt_local_prog_=datetime.fromtimestamp(0,tz_) + timedelta(seconds=int(seconds_prog))
        dt_local_prog = dt_local_prog_.strftime("%d-%m-%Y %H:%M:%S").lstrip("0").replace("-0", "-").replace(" 0", " ") 
        dt_loc_prog2 = dt_local_prog_.strftime("%d %b %Y").lstrip("0")        

        dt_UTC_now_=datetime.utcfromtimestamp(0) + timedelta(seconds=int(seconds_now)) 
        dt_UTC_now = dt_UTC_now_.strftime("%d-%m-%Y %H:%M:%S")#.lstrip("0").replace(".0", ".").replace(" 0", " ")  
        if tz_==None:
            dt_local_now_=datetime.fromtimestamp(0) + timedelta(seconds=int(seconds_now))
        else:
            dt_local_now_=datetime.fromtimestamp(0,tz_) + timedelta(seconds=int(seconds_now))
        dt_loc_now2 = dt_local_now_.strftime("%d %b %Y").lstrip("0")        
        dt_local_now = dt_local_now_.strftime("%d-%m-%Y %H:%M:%S").lstrip("0").replace("-0", "-").replace(" 0", " ") 
    else:
        dt_UTC_prog_=datetime.utcfromtimestamp(seconds_prog) 
        dt_UTC_prog=dt_UTC_prog_.strftime("%d-%m-%Y %H:%M:%S")#.lstrip("0").replace(".0", ".").replace(" 0", " ")
        if tz_==None:
            dt_local_prog_=datetime.fromtimestamp(seconds_prog)
        else:
            dt_local_prog_=datetime.fromtimestamp(seconds_prog,tz_)
        #dt_local_prog_=datetime.fromtimestamp(seconds_prog)
        dt_local_prog=dt_local_prog_.strftime("%d-%m-%Y %H:%M:%S").lstrip("0").replace("-0", "-").replace(" 0", " ") 
        dt_loc_prog2 =dt_local_prog_.strftime("%d %b %Y").lstrip("0")

        dt_UTC_now_=datetime.utcfromtimestamp(seconds_now)
        dt_UTC_now=dt_UTC_now_.strftime("%d-%m-%Y %H:%M:%S")#.lstrip("0").replace(".0", ".").replace(" 0", " ") 
        if tz_==None:
            dt_local_now_=datetime.fromtimestamp(seconds_now)
        else:
            dt_local_now_=datetime.fromtimestamp(seconds_now,tz_)        
        dt_local_now=dt_local_now_.strftime("%d-%m-%Y %H:%M:%S").lstrip("0").replace("-0", "-").replace(" 0", " ") 
        dt_loc_now2 =dt_local_now_.strftime("%d %b %Y").lstrip("0")    

    weekday_loc=dt_local_now_.weekday()
    weekday_loc=weekdays[weekday_loc]
    weekday_UTC=dt_UTC_now_.weekday()
    weekday_UTC=weekdays[weekday_UTC]        

    s=[d,h,m,y_l,d_l]
    s=[int(el) for el in s]
    text2="progressed d={},h={},m={}`n for year={},day={}".format(*s)
    text="year={}, day={}".format(int(y_l),int(d_l))
    t_obj_prog={"timestamp": seconds_prog,"date_utc_prog" : dt_UTC_prog.split(" ")[0],"time_utc_prog" : dt_UTC_prog.split(" ")[1], "date_loc_prog" :dt_local_prog.split(" ")[0], "time_loc_prog" :dt_local_prog.split(" ")[1], "date_loc_prog2" :dt_loc_prog2, "date_loc_now" : dt_local_now.split(" ")[0],"time_loc_now" : dt_local_now.split(" ")[1], "date_loc_now2" :dt_loc_now2, "date_utc_now" : dt_UTC_now.split(" ")[0],"time_utc_now" : dt_UTC_now.split(" ")[1],"text":text,"text2":text2,"weekday_UTC":weekday_UTC,"weekday_loc":weekday_loc}
    return t_obj_prog


def quick_date(seconds=None,tz_=None,short=True):
    if seconds==None:
        import time
        seconds = time.time()
    if tz_!=None:
        from pytz import timezone
        tz_=timezone(tz_)

    if os.name=="nt" and seconds<0: # fix Windows bug
        dt_UTC_=datetime.utcfromtimestamp(0) + timedelta(seconds=int(seconds))
        if tz_==None:
            dt_local_=datetime.fromtimestamp(0) + timedelta(seconds=int(seconds))
        else:
            dt_local_=datetime.fromtimestamp(0,tz_) + timedelta(seconds=int(seconds))

        dt_UTC = dt_UTC_.strftime("%d-%m-%Y %H:%M:%S")#.lstrip("0").replace(".0", ".").replace(" 0", " ") 
        dt_loc2 = dt_local_.strftime("%d %b %Y").lstrip("0")
        dt_local = dt_local_.strftime("%d-%m-%Y %H:%M:%S").lstrip("0").replace("-0", "-").replace(" 0", " ") 
        if short==True:
            dt_UTC = dt_UTC_.strftime("%d-%m-%Y %H:%M").lstrip("0").replace("-0", "-")
            dt_local = dt_local_.strftime("%d-%m-%Y %H:%M").lstrip("0").replace("-0", "-")

    else:
        dt_UTC_=datetime.utcfromtimestamp(seconds)
        dt_UTC=dt_UTC_.strftime("%d-%m-%Y %H:%M:%S")#.lstrip("0").replace(".0", ".").replace(" 0", " ") 
        if tz_==None:
            dt_local_=datetime.fromtimestamp(seconds)
        else:
            dt_local_=datetime.fromtimestamp(seconds,tz_)

        dt_local=dt_local_.strftime("%d-%m-%Y %H:%M:%S").lstrip("0").replace("-0", "-").replace(" 0", " ") 
        dt_loc2 =dt_local_.strftime("%d %b %Y").lstrip("0")
        if short==True:
            dt_UTC = dt_UTC_.strftime("%d-%m-%Y %H:%M").lstrip("0").replace("-0", "-")
            dt_local = dt_local_.strftime("%d-%m-%Y %H:%M").lstrip("0").replace("-0", "-")
    date= dt_UTC if tz_==None else dt_local
    return date
        

if __name__ == "__main__":   
    date_utc="15-3-1971"
    time_utc="17:00:00"
    latitude = 49.7235
    longitude = 20.3993
    timestamp_natal=37904400
        
    planets_pos,houses_pos=get_chart_data(date_utc,time_utc,latitude,longitude)
    #print("planets_pos",planets_pos)
    #print("houses_pos",houses_pos)

    '''
    zone = 'America/New_York'
    zone = 'Europe/Warsaw'
    print(quick_date(timestamp_natal,tz_=zone))
    
    '''



