from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from netmiko import ConnectHandler
from requests import request

# Create your views here.

app_name="first_app"

networks=[]
confs=[]


network_obj={
    "networks":networks
}

def home_page(request):
    network_obj={
    "networks":networks
}
    return render(request,"user_managment.html",context=network_obj)

def add_network(request):

    if request.POST:  
        

        if  request.POST["do"]=="add-network":
           
            network={
                "network":request.POST["network-ip"],
                "host":request.POST["address"]
              
            }
            if network not in networks:
                networks.append(network)
            
            network_obj["networks"]=networks
            create_network(request.POST["address"],request.POST["username"],request.POST["password"],request.POST["network-ip"])
        elif request.POST["do"]=="upgrade" :
            upgrade_rip(request.POST["address"],request.POST["username"],request.POST["password"])
            # user={
            #     "vlan_id":request.POST["vlan_id"],
            #     "name":request.POST["name"],
            #     "type":request.POST["type"]
            # }
            
            network_obj["networks"]=networks
            confs.append(request.POST["address"]+" has been upgraded")
            network_obj["confs"]=confs
        elif request.POST["do"]=="default" :
            default(request.POST["address"],request.POST["username"],request.POST["password"])
            confs.append(request.POST["address"]+" made as default route")
            network_obj["confs"]=confs
        elif request.POST["do"]=="config" :
             conf=config(request.POST["address"],request.POST["username"],request.POST["password"])
             network_obj["config"]=conf
             
        elif request.POST["do"]=="summary" :
            summary(request.POST["address"],request.POST["username"],request.POST["password"])
            confs.append(request.POST["address"]+" enable summarizing")
            network_obj["confs"]=confs
        return render(request,"user_managment.html",context=network_obj)





def create_network(ip,username,password,net_id):
    iosL2={
        "device_type":"cisco_ios",
        "ip":ip,
        "username":username,
        "password":password
    }
    net=ConnectHandler(**iosL2)
    return net.send_config_set(["router rip","network "+net_id])

def upgrade_rip(ip,username,password):
    iosL2={
        "device_type":"cisco_ios",
        "ip":ip,
        "username":username,
        "password":password
    }
    net=ConnectHandler(**iosL2)
    return net.send_config_set(["router rip","version 2"])

def default(ip,username,password):
    iosL2={
        "device_type":"cisco_ios",
        "ip":ip,
        "username":username,
        "password":password
    }
    net=ConnectHandler(**iosL2)
    return net.send_config_set(["router rip","default-information originate"])

def config(ip,username,password):
    iosL2={
        "device_type":"cisco_ios",
        "ip":ip,
        "username":username,
        "password":password
    }
    net=ConnectHandler(**iosL2)
    return net.send_config_set(["do termin length 0","do show run"])

def summary(ip,username,password):
    iosL2={
        "device_type":"cisco_ios",
        "ip":ip,
        "username":username,
        "password":password 
    }
    net=ConnectHandler(**iosL2)
    return net.send_config_set(["router rip","auto-summary"])






