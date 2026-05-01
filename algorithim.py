from enum import Enum
import typing

setList=["wtr","arc","cru","mon",
         "ele","evr","upr","1hp","dyn","out",
         "dtd","evo","hvy","mst","ros","hnt","sea","sup","pen"]

def findSimilarSet(target):
    setScores =[]
    for s in setList:
        score = 0
        for i in range(len(s)):
            if target[i] == s[i]:
                score += 1
        setScores.append([s,score])

    return setScores

