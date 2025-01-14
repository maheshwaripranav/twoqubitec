# Implement the fault-tolerant error correction of [[7,1,3]] code using only two ancilla qubit. 

from utility import *
import matplotlib.pyplot as plt

# Perform weight-1 Pauli correction according to the syndromes of six stabilizers.
def correctErrorsUsingSyndromes(errors, syndromes): 
  xsyndrome = (syndromes[0]<<2) + (syndromes[1]<<1) + syndromes[2]
  if xsyndrome:
    errors.z ^= 1<<(xsyndrome-1)
  zsyndrome = (syndromes[3]<<2) + (syndromes[4]<<1) + syndromes[5]
  if zsyndrome:
    errors.x ^= 1<<(zsyndrome-1)

# Extract the syndromes of X stabilizers using one qubit a time.
# For CSS codes we sometimes only have to measure X or Z stabilizers alone.
def extractXSyndromes(errors, errorRates): 
  syndromes = [0 for i in range(6)]
  prepX(7, errors, errorRates)
  cnot(7, 6, errors, errorRates)
  cnot(7, 5, errors, errorRates)
  cnot(7, 4, errors, errorRates)
  cnot(7, 3, errors, errorRates)
  syndromes[0] = measX(7, errors, errorRates)
  prepX(7, errors, errorRates)
  cnot(7, 6, errors, errorRates)
  cnot(7, 5, errors, errorRates)
  cnot(7, 2, errors, errorRates)
  cnot(7, 1, errors, errorRates)
  syndromes[1] = measX(7, errors, errorRates)
  prepX(7, errors, errorRates)
  cnot(7, 6, errors, errorRates)
  cnot(7, 4, errors, errorRates)
  cnot(7, 2, errors, errorRates)
  cnot(7, 0, errors, errorRates)
  syndromes[2] = measX(7, errors, errorRates)
  return syndromes

# Extract the syndromes of Z stabilizers using one qubit a time.
def extractZSyndromes(errors, errorRates): 
  syndromes = [0 for i in range(6)]
  prepZ(7, errors, errorRates)
  cnot(6, 7, errors, errorRates)
  cnot(5, 7, errors, errorRates)
  cnot(4, 7, errors, errorRates)
  cnot(3, 7, errors, errorRates)
  syndromes[3] = measZ(7, errors, errorRates)
  prepZ(7, errors, errorRates)
  cnot(6, 7, errors, errorRates)
  cnot(5, 7, errors, errorRates)
  cnot(2, 7, errors, errorRates)
  cnot(1, 7, errors, errorRates)
  syndromes[4] = measZ(7, errors, errorRates)
  prepZ(7, errors, errorRates)
  cnot(6, 7, errors, errorRates)
  cnot(4, 7, errors, errorRates)
  cnot(2, 7, errors, errorRates)
  cnot(0, 7, errors, errorRates)
  syndromes[5] = measZ(7, errors, errorRates)
  return syndromes

def extractSyndromes(errors, errorRates):
  xsyn = extractXSyndromes(errors, errorRates)
  zsyn = extractZSyndromes(errors, errorRates)
  return [xsyn[i]+zsyn[i] for i in range(6)]

# Implement the error correction procedure in Section III in the paper. For example, the circuit for measurement of IIIZZZZ follows FIG.3 (b).
def correctErrors(errors, errorRates, verbose=False):
  if verbose: print("starting syndrome0")
  prepX(7, errors, errorRates)
  prepZ(8, errors, errorRates)
  cnot(7, 3, errors, errorRates)
  cnot(7, 8, errors, errorRates)
  cnot(7, 4, errors, errorRates)
  cnot(7, 5, errors, errorRates)
  cnot(7, 8, errors, errorRates)
  cnot(7, 6, errors, errorRates)
  syndrome0 = measX(7, errors, errorRates)
  flag0 = measZ(8, errors, errorRates)
  if flag0:
    if verbose: print("flag0")
    syndromes = extractZSyndromes(errors, errorRates)
    if verbose: print("corrX:", syndromes)
    if syndromes == [0,0,0,1,1,1]:
      errors.x ^= 1<<6
    elif syndromes == [0,0,0,0,0,1]:
      errors.x ^= (1<<6) ^ (1<<5)
    elif syndromes == [0,0,0,1,0,0]:
      errors.x ^= 1<<3
    syndromes = extractXSyndromes(errors, errorRates)
    if verbose: print("Z:", syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return
  elif syndrome0:
    if verbose: print("syndrome0")
    syndromes = extractSyndromes(errors, errorRates)
    if verbose: print(syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return

  if verbose: print("starting syndrome1")
  prepX(7, errors, errorRates)
  prepZ(8, errors, errorRates)
  cnot(7, 1, errors, errorRates)
  cnot(7, 8, errors, errorRates)
  cnot(7, 2, errors, errorRates)
  cnot(7, 5, errors, errorRates)
  cnot(7, 8, errors, errorRates)
  cnot(7, 6, errors, errorRates)
  syndrome1 = measX(7, errors, errorRates)
  flag1 = measZ(8, errors, errorRates)
  if flag1:
    if verbose: print("flag1")
    syndromes = extractZSyndromes(errors, errorRates)
    if verbose: print("corrX:", syndromes)
    if syndromes == [0,0,0,1,1,1]:
      errors.x ^= 1<<6
    elif syndromes == [0,0,0,0,0,1]:
      errors.x ^= (1<<6) ^ (1<<5)
    elif syndromes == [0,0,0,0,1,0]:
      errors.x ^= 1<<1
    syndromes = extractXSyndromes(errors, errorRates)
    if verbose: print("Z:", syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return
  elif syndrome1:
    if verbose: print("syndrome1")
    syndromes = extractSyndromes(errors, errorRates)
    if verbose: print(syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return
  
  if verbose: print("starting syndrome2")
  prepX(7, errors, errorRates)
  prepZ(8, errors, errorRates)
  cnot(7, 0, errors, errorRates)
  cnot(7, 8, errors, errorRates)
  cnot(7, 2, errors, errorRates)
  cnot(7, 4, errors, errorRates)
  cnot(7, 8, errors, errorRates)
  cnot(7, 6, errors, errorRates)
  syndrome2 = measX(7, errors, errorRates)
  flag2 = measZ(8, errors, errorRates)
  if flag2:
    if verbose: print("flag2")
    syndromes = extractZSyndromes(errors, errorRates)
    if verbose: print("corrX:", syndromes)
    if syndromes == [0,0,0,1,1,1]:
      errors.x ^= 1<<6
    elif syndromes == [0,0,0,0,1,0]:
      errors.x ^= (1<<6) ^ (1<<4)
    elif syndromes == [0,0,0,0,0,1]:
      errors.x ^= 1<<0
    syndromes = extractXSyndromes(errors, errorRates)
    if verbose: print("Z:", syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return
  elif syndrome2:
    if verbose: print("syndrome2")
    syndromes = extractSyndromes(errors, errorRates)
    if verbose: print(syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return

  if verbose: print("starting syndrome3")
  prepZ(7, errors, errorRates)
  prepX(8, errors, errorRates)
  cnot(3, 7, errors, errorRates)
  cnot(8, 7, errors, errorRates)
  cnot(4, 7, errors, errorRates)
  cnot(5, 7, errors, errorRates)
  cnot(8, 7, errors, errorRates)
  cnot(6, 7, errors, errorRates)
  syndrome3 = measZ(7, errors, errorRates)
  flag3 = measX(8, errors, errorRates)
  if flag3:
    if verbose: print("flag3")
    syndromes = extractXSyndromes(errors, errorRates)
    if verbose: print("corrZ:", syndromes)
    if syndromes == [1,1,1,0,0,0]:
      errors.z ^= 1<<6
    elif syndromes == [0,0,1,0,0,0]:
      errors.z ^= (1<<6) ^ (1<<5)
    elif syndromes == [1,0,0,0,0,0]:
      errors.z ^= 1<<3
    syndromes = extractZSyndromes(errors, errorRates)
    if verbose: print("X:", syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return
  elif syndrome3:
    if verbose: print("syndrome3")
    syndromes = extractSyndromes(errors, errorRates)
    if verbose: print(syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return

  if verbose: print("starting syndrome4")
  prepZ(7, errors, errorRates)
  prepX(8, errors, errorRates)
  cnot(1, 7, errors, errorRates)
  cnot(8, 7, errors, errorRates)
  cnot(2, 7, errors, errorRates)
  cnot(5, 7, errors, errorRates)
  cnot(8, 7, errors, errorRates)
  cnot(6, 7, errors, errorRates)
  syndrome4 = measZ(7, errors, errorRates)
  flag4 = measX(8, errors, errorRates)
  if flag4:
    if verbose: print("flag4")
    syndromes = extractXSyndromes(errors, errorRates)
    if verbose: print("corrZ:", syndromes)
    if syndromes == [1,1,1,0,0,0]:
      errors.z ^= 1<<6
    elif syndromes == [0,0,1,0,0,0]:
      errors.z ^= (1<<6) ^ (1<<5)
    elif syndromes == [0,1,0,0,0,0]:
      errors.z ^= 1<<1
    syndromes = extractZSyndromes(errors, errorRates)
    if verbose: print("X:", syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return
  elif syndrome4:
    if verbose: print("syndrome4")
    syndromes = extractSyndromes(errors, errorRates)
    if verbose: print(syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return

  if verbose: print("starting syndrome5")
  prepZ(7, errors, errorRates)
  prepX(8, errors, errorRates)
  cnot(0, 7, errors, errorRates)
  cnot(8, 7, errors, errorRates)
  cnot(2, 7, errors, errorRates)
  cnot(4, 7, errors, errorRates)
  cnot(8, 7, errors, errorRates)
  cnot(6, 7, errors, errorRates)
  syndrome5 = measZ(7, errors, errorRates)
  flag5 = measX(8, errors, errorRates)
  if flag5:
    if verbose: print("flag5")
    syndromes = extractXSyndromes(errors, errorRates)
    if verbose: print("corrZ:", syndromes)
    if syndromes == [1,1,1,0,0,0]:
      errors.z ^= 1<<6
    elif syndromes == [0,1,0,0,0,0]:
      errors.z ^= (1<<6) ^ (1<<4)
    elif syndromes == [0,0,1,0,0,0]:
      errors.z ^= 1<<0
    syndromes = extractZSyndromes(errors, errorRates)
    if verbose: print("X:", syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return
  elif syndrome5:
    if verbose: print("syndrome5")
    syndromes = extractSyndromes(errors, errorRates)
    if verbose: print(syndromes)
    correctErrorsUsingSyndromes(errors, syndromes)
    return

# Find least weight representation modulo stabilizers.
def weight(errors):
  return bin((errors.x | errors.z) & ((1 << 7) - 1)).count("1")

def reduceError(errors): 
  stabilizers = \
  [[(1<<6)+(1<<5)+(1<<4)+(1<<3),0], \
  [(1<<6)+(1<<5)+(1<<2)+(1<<1),0], \
  [(1<<6)+(1<<4)+(1<<2)+(1<<0),0], \
  [0,(1<<6)+(1<<5)+(1<<4)+(1<<3)], \
  [0,(1<<6)+(1<<5)+(1<<2)+(1<<1)], \
  [0,(1<<6)+(1<<4)+(1<<2)+(1<<0)], \
  ]
  bestErrors = Errors(errors.x, errors.z)
  bestWeight = weight(bestErrors)
  trialErrors = Errors(0, 0)
  for k in range(1, 1<<(len(stabilizers))):
    trialErrors.x = errors.x
    trialErrors.z = errors.z
    for digit in range(len(stabilizers)):
      if (k>>digit)&1: 
        print(bin(trialErrors.x), bin(trialErrors.z))
        print(k, digit)
        trialErrors.x ^= stabilizers[digit][0]
        trialErrors.z ^= stabilizers[digit][1]
        print(bin(trialErrors.x), bin(trialErrors.z))
    if weight(trialErrors) < bestWeight: 
      bestErrors.x = trialErrors.x
      bestErrors.z = trialErrors.z
      bestWeight = weight(bestErrors)
  return bestErrors

# Run consecutive trials of error correction with physical error rate of gamma, and count the number of failures, i.e., when the trialing error is not correctable by perfect error correction.
# The logical error rate is calculated as the ratio of failures over trials. 
def simulateErrorCorrection(gamma, trials, verbose=False): 
  errors = Errors(0, 0)
  errorsCopy = Errors(0, 0)
  
  errorRates0 = ErrorRates(0, 0, 0)
  errorRates = ErrorRates((4/15.)*gamma, gamma, (4/15.)*gamma)
  
  failures = 0
  for k in range(trials): 
    correctErrors(errors, errorRates, verbose)
    errorsCopy.x = errors.x
    errorsCopy.z = errors.z
    # print('first step completed')
    # print(f'Errors are {bin(errors.x)}, {bin(errors.z)}')
    correctErrors(errorsCopy, errorRates0, verbose)
    # print(f'Errors are {bin(errorsCopy.x)}, {bin(errorsCopy.z)}')
    # print('second step completed')
    errorsCopy = reduceError(errorsCopy)
    # print(f'Reduced Errors are {bin(errorsCopy.x)}, {bin(errorsCopy.z)}')
    if (errorsCopy.x & ((1<<7)-1)) or (errorsCopy.z & ((1<<7)-1)): 
      failures += 1
      errors.x = 0
      errors.z = 0
    # print(f'{k+1} rounds completed.')
  # print(failures)
  return failures/trials

# Wrapper function for the plot. More trials are needed for small gammas due to the confidence interval.
# gammas = [10**(i/10.-4) for i in range(21)]
# for i in range(10):
#   print("gamma=10^(%d/10-4), trials=10^7"% i)
#   simulateErrorCorrection(gammas[i], 10**7)
# for i in range(11):
#   print("gamma=10^(%d/10-4), trials=10^6"% (i+10))
#   simulateErrorCorrection(gammas[i+10], 10**6)


gammas = [0.1]#, 0.05]#, 0.01, 0.007, 0.003, 0.001]#, 0.0007, 0.0003, 0.0001]
deltas = []
print('Gammas \t Logical')
for g in gammas:
  failure_rate = simulateErrorCorrection(g, 1, verbose=False)
  deltas.append(failure_rate)
  print(f'{g} \t {failure_rate}')
plt.xscale('log')
plt.yscale('log')
plt.plot(gammas, deltas)
plt.plot(gammas, gammas)