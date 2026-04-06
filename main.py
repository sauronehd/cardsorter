from algorithim import *

if __name__ == '__main__':

    cardsToSort = [[setList.evo,193],[setList.hnt,31],[setList.mon,165],[setList.ele,173],[setList.hnt,20],[setList.wtr,40],[setList.dyn,140],
                   [setList.evr,67],[setList.pen,193],[setList.pen,196],[setList.mst,31],[setList.mon,90],[setList.hp1,200]]

    fullSortList = []

    for set in setList:
        inSetCards =  [x for x in cardsToSort if x[0] == set]
        sortedInSet = quick_sort_in_set(inSetCards)
        if inSetCards:
            fullSortList.append(sortedInSet)

    print(fullSortList)