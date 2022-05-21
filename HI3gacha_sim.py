import random
import numpy as np
import sys

def singlePull(rates, arankRate, srankRate, softten, pity):
    # Pull
    if   pity == 99:
        print("\tHit full pity")
        result = ["S-rank Valkyrie"]
    elif softten == 9:
        # Guarantee A rank or higher after missing one for 9 pulls
        # Assumes A and S rank rates are same as before but weighted out of arankRate + srankRate instead of out of 100
        print("\tHit the ten-pull gaurantee")
        result = random.choices(["S-rank Valkyrie", "A-rank Valkyrie"], cum_weights=[srankRate, arankRate], k=1)
    else:
        # Regular pull
        result = random.choices(rates["Name"], cum_weights=rates["Rate"], k=1)

    softten = softten + 1
    pity = pity + 1

    return result[0], softten, pity
    
def resolvePull(pull, bRankPool, aRankPool, sRankPool):
    frag = "frag" in pull

    if "Valk" in pull:
        if   "S-rank" in pull:
            pull = random.choice(sRankPool)
        elif "A-rank" in pull:
            pull = random.choice(aRankPool)
        elif "B-rank" in pull:
            pull = random.choice(bRankPool)

    if frag:
        pull["Name"] = pull["Name"] + " frag"
        print("\t\t\tFragment")

    return pull

# Usage: python HI3gacha_sim.py [<number of pulls>]
# Defaults to a ten-pull
if len(sys.argv) > 1:
    try:
        pullcnt = int(sys.argv[1])
    except:
        pullcnt = 10
else:
    pullcnt = 10

print("Will do", pullcnt, "pulls in the Dorm Supply")

result = [0]*pullcnt
print(result)

# Rates and Pool for Dorm Supply
rates = np.genfromtxt("DormRates.csv", delimiter=',', dtype=None, names=True, encoding=None)
valkPool = np.genfromtxt("DormCharacterPool.csv", delimiter=',', dtype=None, names=True, encoding=None)

for r in rates:
    print(r["Name"], r["Rate"])
#print(rates["Name"])
#print(rates["Rate"])
print(sum(rates["Rate"]))

srankRate = 0
arankRate = 0

#print("Finding Srank rate")
# S rank rate
for r in rates:
    #print(r)
    if r["Name"] == 'S-rank Valkyrie':
        srankRate = r["Rate"]
        #print("Found Srank rate")
        break

#print("Finding Arank rate")
# A rank rate
for r in rates:
    #print(r)
    if r["Name"] == "A-rank Valkyrie":
        arankRate = r["Rate"]
        #print("Found Arank rate")
        break

# Set default if rates not found and warn user
if srankRate == 0:
    print("Warning: unable to find S rank rate, using 1.5")
    srankRate = 1.5
if arankRate == 0:
    print("Warning: unable to find A rank rate, using 13.5")
    arankRate == 13.5

print("Rates: A rank", arankRate, "; S rank", srankRate)

bRankPool = [x for x in valkPool if x["Rank"] == "B Rank"]
aRankPool = [x for x in valkPool if x["Rank"] == "A Rank"]
sRankPool = [x for x in valkPool if x["Rank"] == "S Rank"]

softten = 0
pity = 0
i = 0
ind = 0
_result = "test"
for i in range(pullcnt):
#while b"Frag" not in _result:
    # Pull
    _result, softten, pity = singlePull(rates, arankRate, srankRate, softten, pity)
    print(ind, "Pulled", _result, end='')

    # Assign the pull a value
    result[i] = resolvePull(_result, bRankPool, aRankPool, sRankPool)
    print(", resolved to", result[i])
    
    # Clear ten-pull pity when a S or A rank Valk is pulled    
    if _result == 'A-rank Valkyrie':
        print("\tten-pull cleared")
        softten = 0
    elif _result == 'S-rank Valkyrie':
        print("\tpity reset")
        softten = 0
        pity = 0
        
    ind = ind + 1

print(result)

for r in rates:
    print(r["Name"], r["Rate"])
