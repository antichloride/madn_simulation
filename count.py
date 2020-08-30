blue = 0
green = 0
red = 0
tot = 0.0
with open("res.txt","r") as f:
    for line in f.read().splitlines():
        if line=="blue": blue+=1
        if line=="red":red+=1
        if line=="green":green+=1
        tot+=1

print("Blue={}%, Red={}%, Green={}%, Total = {}".format(blue/tot,red/tot,green/tot,tot))
