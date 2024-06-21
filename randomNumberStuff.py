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
    for result in results:
        result.expression = parenthesisCleanupBruteForce(result.expression)
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

def evalNoError(expression):
    try:
        res = eval(expression)
    except:
        return False
    return res


#fjern:
    #ydre parentes
    #parentes om et tal
    #hvis kun gange/division, fjern alle parenteser
    #hvis kun +-, fjern alle parenteser (altså i hele udtrykket)
    #mere generelt - for hvert udtryk med gange/division. fjern parenteser omkring det
#examples 
    # ((4)-3)
    # (((4)+3)-5)
    # (3)
    # (((5)+3)-4)
    # (5)
    # (((4)+5)-3)
    # (((4)*(3))-5)
    # (((3))+5)
    # ((4)+5)
def parenthesisCleanup(expression):
    print("initial expression",expression)
    expressionCopy = expression
    opGroup1 = ["+","-"]
    opGroup2 = ["*","/"]
    #attempt to remove outer parenthesis
    if expression[0] == "(" and expression[-1] == ")":
        newExpression = expression[1:-1]
        if evalNoError(newExpression) == evalNoError(expression):
            expression = newExpression
    #removes full expression if it is only +/- operators or only multiply/division operators (except if it is like (-3))
    if not any(op in expression for op in opGroup1) or not any(op in expression for op in opGroup2):
        #will be true if we read the start parenthesis in (-x)
        readingNegation = False
        newExpression = ""
        for i,char in enumerate(expression):
            if readingNegation:
                if char == ")":
                    readingNegation = False
                continue
            if char == "(":
                # print("expression to check",expression)
                if expression[i+1] == "-" and expression[i+2].isnumeric():
                    newExpression += expression[i:i+4]
                    readingNegation = True
            elif char != ")":
                newExpression += char
        expression = newExpression
        expressionCopy = expression
    parenthesisStart = False
    parenthesisStartLocation = -1
    subExpression = ""
    for i,char in enumerate(expression):            
        if char == "(":
            subExpression = ""
            parenthesisStart = True
            parenthesisStartLocation = i
            subExpression += char
            continue
        if parenthesisStart:
            subExpression += char
        if char == ")" and parenthesisStart:
            parenthesisStart = False
            # if len(subExpression) == 0:
            #     print("wtf: ",expression, i)
                # raise Exception("should not be possible")
            if len(subExpression) == 1:
                #remove at current location and 2 before
                expression = expression[:parenthesisStartLocation] + subExpression[1:-1] + expression[i+1:]          
            elif not any(op in subExpression for op in opGroup1):
                # print("subexpression", subExpression)
                # print("sub2: ",subExpression[1:-1])
                # print("before: ",expression)
                expression = expression[:parenthesisStartLocation] + subExpression[1:-1] + expression[i+1:]
                # print("after: ",expression)
            subExpression = ""
            if expressionCopy != expression:
                break
    if expressionCopy == expression:
        return expression
    return parenthesisCleanup(expression)
            
#make a parenthesis shortener that tries to remove each pair of parenthesis and checks with eval if it is possible
def parenthesisCleanupBruteForce(expression):
    for i,char in enumerate(expression):
        if char == "(":
            for j in range(i+1,len(expression)):
                if expression[j] == ")":
                    newExpression = expression[:i] + expression[i+1:j] + expression[j+1:]
                    if evalNoError(newExpression) == evalNoError(expression):
                        return parenthesisCleanupBruteForce(newExpression)
    return expression

#     print(parenthesisCleanup(test))     
# print(parenthesisCleanup("(3*9-6)-4"))
# print(parenthesisCleanupBruteForce("((6+9)/3)*4"))


#stuff that could be shortened more - with parenthesisCleanup :
    #(3*9-6)-4 = 3*9-6-4
    #((6+9)/3)*4 = (6+9)/3*4
    #3*9-(6-4) = 3*9-6+4
    #((3+6)/9)+4 = (3+6)/9+4

# results = getResults([3,4,6,9])
# printResults(results,verbose=True)
# pickXBestNumbersInRange(4,1,10)

