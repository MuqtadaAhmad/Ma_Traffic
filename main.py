import requests
import customtkinter as ctk
import tkintermapview as tkmp
import threading
import socket
from scapy.all import *
from urllib.parse import urlparse
#get positions of each routers
class TraficData():
    def ipaddres(self,ipAddress):
        url="https://api.ip2location.io/"
        hander={"User-Agent": "mymap/1.0"}
        parms={  #the input
        "ip": ipAddress,
        #our key that allaws to us to get respons
        "key":"5255E6A7400CEFAD1FB2990DD4FC6472",
        #the form of data respons
        "format" : "json"
    }
        respons=requests.get(url,headers=hander,params=parms)
        if respons.__bool__():
            print('ok')
            data=respons.json()
            lat=data.get("latitude")
            lon=data.get("longitude")
            flag=data.get("flag")
            ip=data.get('ip')
            country_name=data.get("country_name")
            city_name=data.get("city_name")
            _as=data.get("as")
            data={"lat":lat,"lon":lon,"flag":flag,"ip":ip,"country_name":country_name,"city_name":city_name,"as":_as}
        return data
            

    #make ping on the Routeres
class Routing():
    ips=[]
    def treaceroute(self,target_url,max_hops=30):
        #clean url
        parsedURL=urlparse(target_url)
        domanName=parsedURL.netloc
        target_ip=socket.gethostbyname(domanName)
        for ttl in range(1,max_hops+1):
            #create packet
            packet=IP(dst=target_ip,ttl=ttl) / ICMP()
            #send the packet (make pink)
            reply=sr1(packet,verbose=0,timeout=2)
            if reply is None:
                print("There is no ip")
                break
            else:
                reply_ip=reply.src
                if reply.type==11:
                    print(f"{ttl:<5} {reply_ip:<20} router")
                    Routing.ips.append(reply_ip)
                    
                elif reply.type==0:
                    print(f"{ttl:<5} {reply_ip:<20} ** tarhet router ** ")
                    #store IPs 
                    Routing.ips.append(reply_ip)

                    break
                else:
                    print(f"{ttl:<5} {reply_ip:<20} UNknown")
    def Distint(self,destance):
        #a=sin^2(df(lat)/2)+cos(lat1)*cos(lat2)*sin^(df(lon/2))
        #c=2*arctan 2(squar(a).squar(1-a))
        #d=R.c
        R=r=637.0  #=>قطر الارض 
        distint=0
        for i in range(0,len(destance)-1):
            lat1,lat2=math.radians(destance[i][0]),math.radians(destance[i+1][0])
            dfLat=math.radians(destance[i][0]-destance[i+1][0])
            dfLon=math.radians(destance[i][1]-destance[i+1][1])
            #Haversine rule
            a=math.sin(dfLat/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin(dfLon/2)**2
            c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
            d=R*c
            
            distint+=d
        return distint
    
class DFrame(ctk.CTkFrame):
    trash=[]
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        
        self.ips=ctk.CTkScrollableFrame(self,width=200)
        self.isp=ctk.CTkScrollableFrame(self,width=400)
        self.cuntryAndDis=ctk.CTkScrollableFrame(self,width=400)
        self.labIp=ctk.CTkLabel(self,text="IP",font=('arial',15,'bold'))
        self.labLockation=ctk.CTkLabel(self,text="City/Country",font=('arial',15,'bold'))
        self.labAS=ctk.CTkLabel(self,text="ISP",font=('arial',15,'bold'))
        #self.trash.append(self.ips)
        #self.trash.append(self.ips)
        #self.trash.append(self.cuntryAndDis)

       
        #======
        self.labIp.place(x=100,y=0)
        self.ips.pack(side='left')
        self.labLockation.place(x=400,y=0)
        self.cuntryAndDis.pack(side='left',padx=1)
        self.labAS.place(x=850,y=0)
       
        self.isp.pack(side='left',padx=1)
    def add_ip_info(self,ips):
        self.trash.clear
        for i in ips:
            if i["lat"]==None:

               lip=ctk.CTkLabel(self.ips,text=i['ip'],font=('arial',10,'bold'),text_color='Red')
               lip.pack(anchor='w')
               
               self.trash.append(lip)
               lcAd=ctk.CTkLabel(self.cuntryAndDis,text=i["country_name"]+"/"+i["city_name"],font=('arial',10,'bold'))
               lcAd.pack(anchor="w")
               self.trash.append(lcAd)

               lisp=ctk.CTkLabel(self.isp,text=i["as"],font=('arial',10,'bold'))
               lisp.pack(anchor="w")
               self.trash.append(lisp)

            else:
                lip=ctk.CTkLabel(self.ips,text=i['ip'],font=('arial',10,'bold'))
                lip.pack(anchor='w')
                self.trash.append(lip)

                lcAd=ctk.CTkLabel(self.cuntryAndDis,text=i["country_name"]+"/"+i["city_name"],font=('arial',10,'bold'))
                lcAd.pack(anchor="w")
                self.trash.append(lcAd)

                lisp=ctk.CTkLabel(self.isp,text=i["as"],font=('arial',10,'bold'))
                lisp.pack(anchor="w")
                self.trash.append(lisp)


    
        



    




class APP(ctk.CTk):
    poisen=False
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("taraficMap")
        self.elemint()
        self.elemint_palce()
        self.marks=[]
    hid=False
    coulecter=[]
       

        
        #thred=threading.Thread(target=self.droingDestens)
        #thred.start()
    
    def elemint(self):
        self.mapFrame=ctk.CTkFrame(self,fg_color='white')
        
        self.map=tkmp.TkinterMapView(self.mapFrame,height=500,width=800)
        self.map.set_position(0,0)     

        self.entery=ctk.CTkEntry(self,height=50,width=200)
        self.button=ctk.CTkButton(self,height=30,width=50,text="start",command=self.tread_1)
        self.frameButton=ctk.CTkButton(self,text='Details',command=self.detels)
        self.dFrame=DFrame(self.mapFrame,width=400)

        
        self.map.set_zoom(1000)
    def elemint_palce(self):  
        self.map.set_tile_server("https://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        self.entery.pack()
        self.button.pack(side='top',pady=20)
        self.frameButton.pack()
        self.map.set_position(33.3406 ,44.4009)

        self.map.set_zoom(5) 
        self.mapFrame.pack(pady=20,fill='both',expand=True)
        self.map.pack(fill='both',expand=True)
        
    def droingDestens(self):
        if APP.poisen:
           self.marks.clear()
           self.map.delete_all_path()
           self.map.delete_all_marker()
           Routing.ips.clear()
           APP.poisen=False
        if DFrame.trash:
            for t in DFrame.trash:
                t.destroy()
        
            DFrame.trash.clear()
        privetIP=[]
        privetIP.clear()
        APP.coulecter.clear()
           
           
        print("when true",self.marks)
          
           
           
        way=self.entery.get()
        if way != None:
       # mark_1=self.map.set_marker(33.3406 ,44.4009,text="start")
          routing=Routing()
          routing.treaceroute(way)
          td=TraficData()
   
          print(Routing.ips)
          
        for index,i in enumerate(Routing.ips):
            data=td.ipaddres(i)
            APP.coulecter.append(data)
            x,y=data["lat"],data["lon"]
            print(f"ip: {i}  x: {x} y: {y}")
            pos=(x,y)
            if x !=None and y!=None:
               if index==0:
                   lable="start"
                   self.map.set_marker(x,y,text=lable)
               elif index == len(Routing.ips)-1:
                   lable="End"
                   self.map.set_marker(x,y,text=lable)
                   if pos in self.marks:
                     self.map.set_marker(x,y,text=f"")
               else:
                   if pos in self.marks:
                    self.map.set_marker(x,y,text=f"")
                   else:
                       self.map.set_marker(x,y,text=f"{index}")
               self.marks.append((x,y))
            else:
                privetIP.append(i)
        self.dFrame.add_ip_info(APP.coulecter)
        distint= routing.Distint(self.marks)
         
        print(f'd=: {distint}')
        print("befor clear",self.marks)
        if APP.poisen==False:
            APP.poisen=True
            if len(self.marks)>=2:
              path=self.map.set_path(self.marks,width=2,color='red')
            else:
              print("cann't Located becuse thers no distint")
           
    #Threading for drowing map
    def tread_1(self):
        thread=threading.Thread(target=self.droingDestens,daemon=True)
        thread.start()
    #hide button
    def detels(self):
        if APP.hid:
            self.dFrame.place_forget()
            APP.hid=False
        else:
          self.dFrame.place(relx=0.0,rely=0.0,anchor='nw')
          self.dFrame.lift()
          APP.hid=True

        
    

    
              
             

                

            
              

            
       
        
        
       # 
       # print(f'x: {type(x)}: {x} y: {type(y)}: {y}')
       # mark_2=self.map.set_marker(float(x),float(y),text="end")
       # self.path=self.map.set_path([mark_1.position,mark_2.position],color="red",width=2)

        
    
        

if __name__=='__main__':
    app=APP()
    app.mainloop()
        
