from Blending_Model import *

if __name__ == "__main__":
    pulp.pulpTestAll()
    
    # Parameters
    commodities = ['Fe', 'Al', 'Mn', 'Si']
    numStockpiles = 2
    numPlantProducts = 2
    
    # Tonnages available per stockpile for the day (TA)
    dailyAvailableTonnages = {}
    dailyAvailableTonnages[1] = 2230.0
    dailyAvailableTonnages[2] = 910.0
    
    # Daily Grades (G_x,n) (per stockpile per commodity)
    dailyGrades = {}
    dailyGrades[(1,"Fe")] = 60.55
    dailyGrades[(1,"Al")] = 0.69
    dailyGrades[(1,"Mn")] = 1.28
    dailyGrades[(1,"Si")] = 8.8
    dailyGrades[(2,"Fe")] = 53.26
    dailyGrades[(2,"Al")] = 0.6
    dailyGrades[(2,"Mn")] = 0.62
    dailyGrades[(2,"Si")] = 20.95    

    # Average Commodity 1 Grade (G_avg)
    avgMainCommGrade = 62.0    

    # Min and Max Grades (per commodity)
    minGrades = {}
    minGrades["Fe"] = 60.0
    minGrades["Al"] = 0.0
    minGrades["Mn"] = 1.0
    minGrades["Si"] = 5.0
    maxGrades = {}
    maxGrades["Fe"] = 62.0
    maxGrades["Al"] = 0.0
    maxGrades["Mn"] = 1.0
    maxGrades["Si"] = 5.0    

    # Percent Grade (G%) (per plant product)
    percentGrades = {}
    percentGrades[1] = 55.247002
    #percentGrades[1] = 55.248
    #percentGrades[1] = 64.0
    percentGrades[2] = 61.0
    
    # Percent Recovery (R%) (per plant product)
    percentRecoveries = {}
    percentRecoveries[1] = 35.0
    percentRecoveries[2] = 65.0    

    # Moistures (M%) (per plant product)
    moistures = {}
    moistures[1] = 4.0
    moistures[2] = 7.0
    
    # Price per ton (per plant product)
    stockpile1Prices = {}
    stockpile1Prices[1] = 110.0
    stockpile1Prices[2] = 95.0
    
    # Smelters: We always consider the smelter term for stockpileID=1 only
    # Smelter Min Terms (per stockpile per commodity)
    minSmelters = {}
    minSmelters["Fe"] = -3.0
    minSmelters["Al"] = 0.0
    minSmelters["Mn"] = 0.0
    minSmelters["Si"] = 0.0
    
    # Smelter MinMax Terms (per stockpile per commodity)
    minMaxSmelters = {}
    minMaxSmelters["Fe"] = -1.5
    minMaxSmelters["Al"] = 0.0
    minMaxSmelters["Mn"] = 0.0
    minMaxSmelters["Si"] = 0.0
    
    # Smelter Max Terms (per stockpile per commodity)
    maxSmelters = {}
    maxSmelters["Fe"] = 1.5
    maxSmelters["Al"] = 0.0
    maxSmelters["Mn"] = -0.2
    maxSmelters["Si"] = -0.75    

    # Increments (per commodity)
    increments = {}
    increments["Fe"] = 1.0
    increments["Al"] = 1.0
    increments["Mn"] = 100.0
    increments["Si"] = 1.0
    
    opexPT = 58.36
    FXRate = 0.8
    shippingCost = 15.63    

    blending_model = blending_model(numStockpiles, numPlantProducts, commodities, dailyAvailableTonnages,
                                    dailyGrades, avgMainCommGrade, minGrades, maxGrades, percentGrades,
                                    percentRecoveries, moistures, stockpile1Prices, minSmelters,
                                    minMaxSmelters, maxSmelters, increments, opexPT, FXRate, shippingCost)
    
    #for variable in blending_model.variables():
        #print("{} = {}".format(variable.name, variable.varValue))
    #print(LpStatus[blending_model.status])
    #print(value(blending_model.objective))

    #print("")

    varsDict = {}
    for v in blending_model.variables():
        varsDict[v.name] = v.varValue
        
    # Print Daily Available Tonnages
    for i in range(1, numStockpiles+1):
        print("Stockpile {0} tonnage available is {1}".format(i, dailyAvailableTonnages[i]))

    # Print Daily Used Tonnages
    for i in range(1, numStockpiles+1):
        print("Stockpile {0} tonnage used is {1}".format(i, varsDict["T_{0}".format(i)]))
        
    # Print Total Used Tonnage
    print("Total used tonnage is {0}".format(varsDict["sumT"]))
    
    print("")
            
    print("Optimized Grades:")
    for i in range(1, numPlantProducts+1):
        for comm in commodities:
            if varsDict["sumT"] > 0:
                print("    PP{0}, {1}: {2}%".format(i, comm, varsDict["WG_({0},_'{1}')".format(i, comm)]/varsDict["sumT"]))
            else:
                print("    PP{0}, {1}: 0.0%".format(i, comm))
            for j in range(1,4):
                if varsDict["PT_({0},_'{1}',_{2})".format(i,comm,j)] == 1.0:
                    print("    PP{0}, {1} grade in Tier {2}. (MinGrade is {3}%. MaxGrade is {4}%)".format(i,comm,j,minGrades[comm],maxGrades[comm]))
                    break
            if varsDict["sumT"] > 0:
                print("    PP{0}, {1} smelter value is {2}".format(i,comm,(varsDict["Prem_({0},_'{1}',_{2})".format(i,comm,j)] - varsDict["Pen_({0},_'{1}',_{2})".format(i,comm,j)])/varsDict["sumT"]))
            else:
                print("    PP{0}, {1} smelter value is 0.0".format(i,comm))
            print("")    
    
    print("Maximized objective function value is: {0}".format(value(blending_model.objective)))
    print("Foreign exchange rate is {0}".format(FXRate))
    print("Foreign exchange rate adjusted value is: {0}".format(value(blending_model.objective)/FXRate))
    print("Test use case evaluation complete.")
