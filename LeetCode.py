def threeSum(self, nums: list[int]) -> list[list[int]]:
    longueurNum = len(nums)
    compilation = {}
    for i in range(longueurNum-1):
        if not (nums[i] in compilation):
            compilation[nums[i]] = i
        for j in range(i + 1, longueurNum):
            if not (nums[j] in compilation):
                compilation[nums[j]] = j
            somme : int = nums[i] + nums[j]
            if not (somme in compilation):
                compilation[somme] = [i,j]
                



    return []

print(threeSum("",[-1,0,1,2,-1,-4]))