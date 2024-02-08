from random import randint
from random import shuffle
import itertools

class Result:
    def __init__(self, nums, acc,exp):
        self.usedNums = nums
        self.acc = acc
        self.expression = exp
    def __lt__(self, other):
         return self.acc < other.acc
    def __eq__(self, other):
        if isinstance(other, int):
            return self.acc == other
        return self.acc == other.acc


def getResults(originalNumbers):
    results = []
    subExpressions = []
    for _ in range(2000):
        nums = originalNumbers.copy()
        usedNums = []
        acc = 0
        expression = ""
        while len(nums) > 0:
            #handling the the number - not sure why i have to return all values and the function doesnt change them
            (expression,subExpressions,nums,usedNums,acc) = addNumber(expression,subExpressions,nums,usedNums,acc)
            if len(nums) == 0:
                break
            #handling the operator
            result = addOperator(expression)
            if result == False: #if no operator should be added, and that expression is finished
                break
            else:
                expression = result
                
        if not any(subExpression.expression==expression for subExpression in subExpressions):
            subExpressions.append(Result(usedNums, acc, expression))
        if not any(result.acc==acc for result in results):
            results.append(Result(usedNums, int(acc), expression))
    return results
    
def addOperator(expression):
    i = randint(-1,3)
    if i == -1:
        return False #stop
    elif i == 0:
        expression += "+"
    elif i == 1:
        expression += "-"
    elif i == 2:
        expression += "*"
    elif i == 3:
        expression += "/"
    return expression

def addNumber(expression,subExpressions,nums,usedNums,acc):
    if subExpressions == []:
        i = randint(0, len(nums)-1)
    else:
        i = randint(-1, len(nums)-1)
            
    if i == -1: #add subexpression rather than a number
        shuffle(subExpressions)
        performedOperation = False
        for subExpression in subExpressions:
            if not any(x in subExpression.usedNums for x in usedNums):
                res = performOperation(expression,acc,subExpression.acc)
                if res != False: #if it is possible to perform the operation
                    acc = res
                    expression = "(" + expression + subExpression.expression + ")"
                    usedNums.extend(subExpression.usedNums)
                    nums = [x for x in nums if x not in subExpression.usedNums]
                    performedOperation = True
                    break
        #if it was not possible to perform any operations with a subexpression
        if not performedOperation:
            expression = expression[:-1]
    else: #add number corresponding to index in list
        num = nums[i]
        res = performOperation(expression,acc,num)
        if res == False: #if it is not possible to perform the operation
            expression = expression[:-1]
        else:
            acc = res    
            num = nums.pop(i)
            usedNums.append(num)
            expression = "(" + expression + str(num) + ")"   
    return (expression,subExpressions,nums,usedNums,acc)
    
def performOperation(expression,acc,num):
    if expression == "" or expression[-1] == "+":
        acc += num
    elif expression[-1] == "-":
        if acc - num < 0:
            return False
        acc -= num
    elif expression[-1] == "*":
        acc *= num
    elif expression[-1] == "/":
        if num == 0 or (acc / num % 1 != 0):
            return False
        acc /= num
    return acc
      
      
def printResults(results,verbose=False):
    if results == []:
        print("No results")
        return
    i = 1
    while True:
        if i in results:
            if verbose:
                print(results[results.index(i)].expression,end=" = ")
            print(i)
        else:
            return
        i += 1

def getMaxNumFromResult(results):
    maxNum = 0
    while True:
        maxNum += 1
        if maxNum not in results:
            return maxNum - 1

def pickXBestNumbersInRange(numOfNumbers, lowestNum,highestNum):
    numberCollections = list(itertools.combinations(range(lowestNum,highestNum+1),numOfNumbers))
    currentHighestNum = 0
    currentHighestNumNumbers = []
    currentHighestNumResults = None
    for numbers in numberCollections:
        results = getResults(list(numbers))
        highestNumForResults = getMaxNumFromResult(results)
        if highestNumForResults > currentHighestNum:
            currentHighestNum = highestNumForResults
            currentHighestNumNumbers = numbers
            currentHighestNumResults = results
    print(f"the best {numOfNumbers} numbers between {lowestNum} and {highestNum} (inclusive) is {currentHighestNumNumbers}")
    print(f"here the highest reachable numbers is {currentHighestNum}")
    print("the calculations for it are:")
    printResults(currentHighestNumResults,verbose=True)
    

# results = getResults([3,4,5])
# printResults(results,verbose=True)
pickXBestNumbersInRange(4,1,10)