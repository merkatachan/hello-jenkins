from pulp import *

def blending_model(numStockpiles, numPlantProducts, commodities, dailyAvailableTonnages,
                   dailyGrades, avgMainCommGrade, minGrades, maxGrades, percentGrades,
                   percentRecoveries, moistures, stockpile1Prices, minSmelters,
                   minMaxSmelters, maxSmelters, increments, opexPT, FXRate, shippingCost):
    
    blending_model = LpProblem("Ore Blending Model", LpMaximize)
    
    totalAvailableTonnage = sum(dailyAvailableTonnages.values()) + 1
    
    conversions = {}
    for i in range(1, numPlantProducts+1):
        conversions[i] = percentGrades[i] / avgMainCommGrade    

    # Decision Variables: Daily Used Tonnages (per stockpile)
    dailyUsedTonnages = LpVariable.dicts("T", range(1, numStockpiles+1),
                                         lowBound=0,
                                         cat='Continuous')
    
    #blending_model += dailyUsedTonnages[2] == 0.0
    
    # Constraints
    for i in range(1, numStockpiles+1):
        blending_model += dailyUsedTonnages[i] <= dailyAvailableTonnages[i]
        
    # Aggregate Tonnage-Grade Products (1 per commodity) (i.e., Sigma t_i*g_i)
    weightedSums = {}
    for comm in commodities:
        weightedSum = 0.0
        for curr in range(1, numStockpiles+1):
            weightedSum += dailyUsedTonnages[curr]*dailyGrades[(curr,comm)]
        weightedSums[comm] = weightedSum
        
    # Converted Aggregate Tonnage-Grade Products (1 per Plant Product per Commodity)
    weightedGrades = LpVariable.dicts("WG",
                                      ((i, j) for i in range(1, numPlantProducts+1) for j in commodities),
                                      lowBound=0,
                                      cat="Continuous")
    
    for i in range(1, numPlantProducts+1):
        for comm in commodities:
            blending_model += weightedGrades[(i,comm)] == weightedSums[comm]*conversions[i]

    # Binary variable declaring which penalty tier a grade belongs in
    penaltyTiers = LpVariable.dicts("PT",
                                    ((i, j, k) for i in range(1, numPlantProducts+1) for j in commodities for k in range(1, 4)),
                                    cat="Binary")
    
    # Constraint: Sum of the three tier variables equals 1
    for i in range(1, numPlantProducts+1):
        for comm in commodities:
            blending_model += penaltyTiers[(i, comm, 1)] + penaltyTiers[(i, comm, 2)] + penaltyTiers[(i, comm, 3)] == 1
    
    # Variable V (1 per plant product per commodity per tier)
    V = LpVariable.dicts("V",
                         ((i, j, k) for i in range(1, numPlantProducts+1) for j in commodities for k in range(1, 4)),
                         lowBound=0,
                         cat="Continuous")
    
    sumT = LpVariable('sumT', lowBound=0, cat='Continuous')
    blending_model += sumT == sum(dailyUsedTonnages.values())
    
    # Constraints for each V
    for i in range(1, numPlantProducts+1):
        for comm in commodities:
            for j in range(1, 4):
                blending_model += V[(i,comm,j)] <= sumT
                blending_model += V[(i,comm,j)] <= penaltyTiers[(i,comm,j)]*totalAvailableTonnage
                blending_model += V[(i,comm,j)] >= sumT - (1-penaltyTiers[(i,comm,j)])*totalAvailableTonnage
                blending_model += V[(i,comm,j)] >= sumT - totalAvailableTonnage + totalAvailableTonnage*penaltyTiers[(i,comm,j)]
                

    # Constraints for the grades
    MG = 100.0*totalAvailableTonnage            
    for i in range(1, numPlantProducts+1):
        for comm in commodities:
            blending_model += weightedGrades[(i,comm)] >= 0.0
            blending_model += weightedGrades[(i,comm)] <= sumT*minGrades[comm] + (sumT - V[(i,comm,1)])*MG
            #blending_model += weightedGrades[(i,comm)] < sum(dailyUsedTonnages.values())*minGrades[comm] + (sum(dailyUsedTonnages.values()) - V[(i,comm,1)])*MG
            blending_model += weightedGrades[(i,comm)] >= V[(i,comm,2)]*minGrades[comm]
            #blending_model += weightedGrades[(i,comm)] < sum(dailyUsedTonnages.values())*maxGrades[comm] + (sum(dailyUsedTonnages.values()) - V[(i,comm,2)])*MG
            blending_model += weightedGrades[(i,comm)] <= sumT*maxGrades[comm] + (sumT - V[(i,comm,2)])*MG
            #blending_model += weightedGrades[(i,comm)] >= sumT*maxGrades[comm] - (sumT - V[(i,comm,3)])*MG
            blending_model += weightedGrades[(i,comm)] >= V[(i,comm,3)]*maxGrades[comm]
            
    # Penalties (1 per plant product per commodity per tier)
    penalties = LpVariable.dicts("Pen",
                         ((i, j, k) for i in range(1, numPlantProducts+1) for j in commodities for k in range(1, 4)),
                         lowBound=0.0,
                         cat="Continuous")
    
    premiums = LpVariable.dicts("Prem",
                         ((i, j, k) for i in range(1, numPlantProducts+1) for j in commodities for k in range(1, 4)),
                         lowBound=0.0,
                         cat="Continuous")
    
    # New constraint for premiums/penalties
    M = 1.0*10**10
    for i in range(1, numPlantProducts+1):
        for comm in commodities:
            # No penalties/premiums if all smelter terms are zero
            if minSmelters[comm] == minMaxSmelters[comm] == maxSmelters[comm] == 0.0:
                blending_model += premiums[(i,comm,1)] == 0.0
                blending_model += premiums[(i,comm,2)] == 0.0
                blending_model += premiums[(i,comm,3)] == 0.0
                blending_model += penalties[(i,comm,1)] == 0.0
                blending_model += penalties[(i,comm,2)] == 0.0
                blending_model += penalties[(i,comm,3)] == 0.0            
            else:
                if minMaxSmelters[comm] < 0.0:
                    additionalPen = -1*sumT*(maxGrades[comm] - minGrades[comm])*increments[comm]*minMaxSmelters[comm]
                    
                if maxSmelters[comm] > minSmelters[comm]:
                    blending_model += penalties[(i,comm,3)] == 0.0                
                    if maxSmelters[comm] == 0:
                        blending_model += premiums[(i,comm,3)] == 0.0
                    else:
                        blending_model += premiums[(i,comm,3)] <= (weightedGrades[(i,comm)] - sumT*maxGrades[comm])*increments[comm]*maxSmelters[comm] + (1-penaltyTiers[(i,comm,3)])*M
                        blending_model += premiums[(i,comm,3)] <= penaltyTiers[(i,comm,3)]*M
                    
                    blending_model += premiums[(i,comm,1)] == 0.0
                    if minSmelters[comm] == 0:
                        blending_model += penalties[(i,comm,1)] == 0.0
                    else:
                        blending_model += penalties[(i,comm,1)] >= -1*(sumT*minGrades[comm] - weightedGrades[(i,comm)])*increments[comm]*minSmelters[comm] + additionalPen - (1-penaltyTiers[(i,comm,1)])*M
                        
                    if minMaxSmelters[comm] == 0.0:
                        blending_model += premiums[(i,comm,2)] == 0.0
                        blending_model += penalties[(i,comm,2)] == 0.0
                    elif minMaxSmelters[comm] > 0.0:
                        blending_model += penalties[(i,comm,2)] == 0.0
                        blending_model += premiums[(i,comm,2)] <= (weightedGrades[(i,comm)] - sumT*minGrades[comm])*increments[comm]*minMaxSmelters[comm] + (1-penaltyTiers[(i,comm,2)])*M
                        blending_model += premiums[(i,comm,2)] <= penaltyTiers[(i,comm,2)]*M
                    else:                    
                        blending_model += premiums[(i,comm,2)] == 0.0
                        blending_model += penalties[(i,comm,2)] >= -1*(sumT*maxGrades[comm] - weightedGrades[(i,comm)])*increments[comm]*minMaxSmelters[comm] - (1-penaltyTiers[(i,comm,2)])*M
                
                else:
                    blending_model += premiums[(i,comm,1)] == 0.0
                    blending_model += penalties[(i,comm,1)] == 0.0
                    
                    blending_model += premiums[(i,comm,2)] == 0.0
                    blending_model += penalties[(i,comm,2)] == 0.0                
                    
                    blending_model += premiums[(i,comm,3)] == 0.0
                    if maxSmelters[comm] == 0:
                        blending_model += penalties[(i,comm,3)] == 0.0
                    else:
                        blending_model += penalties[(i,comm,3)] >= -1*(weightedGrades[(i,comm)] - sumT*maxGrades[comm])*increments[comm]*maxSmelters[comm] - (1-penaltyTiers[(i,comm,3)])*M

    sumPenalties = {}
    for i in range(1, numPlantProducts+1):
        sumPenalty = 0.0
        for comm in commodities:
            sumPenalty += penalties[(i,comm,1)] + penalties[(i,comm,2)] + penalties[(i,comm,3)]
        sumPenalties[i] = sumPenalty
        
    sumPremiums = {}
    for i in range(1, numPlantProducts+1):
        sumPremium = 0.0
        for comm in commodities:
            sumPremium += premiums[(i,comm,1)] + premiums[(i,comm,2)] + premiums[(i,comm,3)]
        sumPremiums[i] = sumPremium
        
    blending_model += lpSum([
        (sum(dailyUsedTonnages.values())*percentRecoveries[curr]*(100.0-moistures[curr])*(stockpile1Prices[curr] - opexPT - shippingCost) + (sumPremiums[curr]-sumPenalties[curr])*percentRecoveries[curr]*(100.0-moistures[curr]))/10000.0
        for curr in range(1,numPlantProducts+1)
    ] )
    
    blending_model.writeLP("test1.lp")
    blending_model.solve(pulp.COINMP_DLL())   

    return blending_model
