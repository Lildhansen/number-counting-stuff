from random import randint
from random import shuffle

#still some errors, but works pretty well
#parenteser når vi har subexpressions er fucked

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


def main(a,b,c,d):
    results = []
    subExpressions = []
    for i in range(1000):
        nums = [a,b,c,d]
        usedNums = []
        acc = 0
        expression = ""
        while len(nums) > 0:
            res = False
            #the number
            if subExpressions == []:
                i = randint(0, len(nums)-1)
            else:
                i = randint(-1, len(nums)-1)
                 
            if i == -1:
                shuffle(subExpressions)
                for subExpression in subExpressions:
                    if not any(x in subExpression.usedNums for x in usedNums):
                        res = performOperation(expression,acc,subExpression.acc)
                        if res != False: #if it is possible to perform the operation
                            acc = res
                            expression = "(" + expression + subExpression.expression + ")"
                            usedNums.extend(subExpression.usedNums)
                            nums = [x for x in nums if x not in subExpression.usedNums]
                            break
                #if it was not possible to perform any operations with a subexpression
                expression = expression[:-1]
            else:
                num = nums[i]
                res = performOperation(expression,acc,num)
                if res == False: #if it is not possible to perform the operation
                    expression = expression[:-1]
                else:
                    acc = res    
                    num = nums.pop(i)
                    usedNums.append(num)
                    expression = "(" + expression + str(num) + ")"
            if len(nums) == 0:
                break
            #the operator
            i = randint(-1,3)
            if i == -1:
                break #stop
            elif i == 0:
                expression += "+"
            elif i == 1:
                expression += "-"
            elif i == 2:
                expression += "*"
            elif i == 3:
                expression += "/"
        addSubExpression = True
        for subExpression in subExpressions:
            if expression == subExpression.expression:
                addSubExpression = False
                break
        if addSubExpression:
            subExpressions.append(Result(usedNums, acc, expression))
        if not any(result.acc==acc for result in results):
            results.append(Result(usedNums, int(acc), expression))
    results.sort()
    return results

        
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
        

        
        # print(result.acc)
        # print(result.expression)
results = main(3,6,10,12)
printResults(results,verbose=True)