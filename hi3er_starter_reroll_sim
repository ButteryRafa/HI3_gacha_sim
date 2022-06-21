import random
import numpy as np
from datetime import datetime
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
        result = random.choices(["S-rank Valkyrie", "A-rank Valkyrie"], weights=[srankRate, arankRate], k=1)
    else:
        # Regular pull
        result = random.choices(rates["Name"], weights=rates["Rate"], k=1)

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
    
random.seed(datetime.now())
# Usage: python HI3gacha_sim.py [<number of pulls>]
# Defaults to a resolvePull
starter = False
pullcnt = 10
maxpulls = -1
if len(sys.argv) > 1:
    try:
        pullcnt = int(sys.argv[1])
    except:
        pullcnt = 10
    if len(sys.argv) > 2:
        starter = True
        try:
            num_runs = int(sys.argv[2])
        except:
            num_runs = 10000

print("Will do", pullcnt, "pulls in the", end=' ')
if starter:
    print("starter supply")
else:
    print("dorm supply")

result = [0]*pullcnt
print(result)

# Rates and Pool for Dorm Supply
if starter:
    rates = np.genfromtxt("StarterRates.csv", delimiter=',', dtype=None, names=True, encoding=None)
    valkPool = np.genfromtxt("StarterCharacterPool.csv", delimiter=',', dtype=None, names=True, encoding=None)
else:
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
senti_res = []
hofs_res = []
if not starter:
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

else:
    for i in range(num_runs):
        senti_cnt = 0
        hofs_cnt = 0
        for j in range(pullcnt):
        #while b"Frag" not in _result:
            # Pull
            _result, softten, pity = singlePull(rates, arankRate, srankRate, softten, pity)
            if "S-rank" not in _result:
                continue

            # Assign the pull a value
            res = resolvePull(_result, bRankPool, aRankPool, sRankPool)
    
            # Clear ten-pull pity when a S or A rank Valk is pulled    
            if "Sentience" in res["Name"]:
                print("Run:", i, "Pull:", j, "Found Senti!")
                senti_cnt = senti_cnt + 1
            elif "Flamescion" in res["Name"]:
                print("Run:", i, "Pull:", j, "Found HoFs")
                hofs_cnt = hofs_cnt + 1
        senti_res.append(senti_cnt)
        hofs_res.append(hofs_cnt)

if not starter:
    print(result)
else:
    print(senti_res)
    print(hofs_res)
    
sen_len = len(senti_res)

for i in range(1, max(senti_res)+1):
    senti_filtered = [1 for x in senti_res if x >= i]
    sen_fil = len(senti_filtered)
    print("Rate of finding at least", i, "Senti in", pullcnt, "pulls is", sen_fil/sen_len, ",", sen_fil, "out of", sen_len)

hfs_len = len(hofs_res)

for i in range(1, max(hofs_res)+1):
    hofs_filtered = [1 for x in hofs_res if x >= i]
    hfs_fil = len(hofs_filtered)
    print("Rate of finding at least", i, "HoFs in", pullcnt, "pulls is", hfs_fil/hfs_len, ",", hfs_fil, "out of", sen_len)

senti_bool = [1 if x > 0 else 0 for x in senti_res]
hofs_bool  = [1 if x > 0 else 0 for x in hofs_res]
s_res = [sum(i) for i in zip(senti_res, hofs_res)]

s_bool  = [1 if x > 1 else 0 for x in s_res]
s_fil = sum(s_bool)
s_len = len(s_bool)

print("Rate of finding both Senti and HoFs in", pullcnt, "pulls is", s_fil/s_len, ",", s_fil, "out of", s_len)

for r in rates:
    print(r["Name"], r["Rate"])
