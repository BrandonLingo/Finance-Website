def removeDuplicates(self, nums):
    hashset = set()
    for i in nums:
        hashset.add(i)
        
    return len(hashset)
  
print(removeDuplicates(nums = [1,1,2]))