from math import fmod, degrees,pi

def norm_(deg):
    deg =fmod(deg,360)
    if deg<0:deg=deg+360
    return deg

def norm_r(rad):
    π2=2*pi
    rad =fmod(rad,π2)
    rad=round(rad,8)
    if rad<0: rad += π2
    return rad

def rd(r,d=1):
    return round(degrees(r),d)

def r(dig,d=4):
    return round(dig,d)

def a1(*arr0,d=3,s=""):
    arr=[]
    for i in range(len(arr0)):
        if type(arr0[i]) == float:
            arr.append(round(arr0[i],d))
        elif str(type(arr0[i]))=="<class 'numpy.float64'>":
            arr.append(round(arr0[i],d))
        elif str(type(arr0[i]))=="<class 'numpy.ndarray'>":
            arr2= [round(el,d) if str(type(el))=="<class 'numpy.float64'>" else el for el in arr0[i]]
            arr.append(arr2)          
        elif type(arr0[i])== list:
            arr2= [round(el,d) if type(el) is float or str(type(el))=="<class 'numpy.float64'>" else el for el in arr0[i]]
            arr.append(arr2)
        else:
            arr.append(arr0[i])
    for el in arr:
        print(el,end=" ")
    print(s)



