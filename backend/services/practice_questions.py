from typing import Dict, List, Optional
import re

# LeetCode-style practice questions bank
PRACTICE_QUESTIONS = {
    "easy": [
        {
            "id": 1,
            "title": "Two Sum",
            "difficulty": "Easy",
            "description": """Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

**Example 1:**
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

**Example 2:**
```
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

**Example 3:**
```
Input: nums = [3,3], target = 6
Output: [0,1]
```""",
            "starter_code": """def twoSum(nums, target):
    # Write your solution here
    pass

# Test your solution
print(twoSum([2,7,11,15], 9))  # Expected: [0, 1]
print(twoSum([3,2,4], 6))      # Expected: [1, 2]
print(twoSum([3,3], 6))        # Expected: [0, 1]""",
            "solution": """def twoSum(nums, target):
    # Use a hash map to store complements
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []

# Time Complexity: O(n)
# Space Complexity: O(n)""",
            "hints": [
                "Think about what value you need to find for each number",
                "Can you use a hash map to store numbers you've seen?",
                "For each number, check if (target - number) exists in the map"
            ],
            "test_cases": [
                {"input": {"nums": [2,7,11,15], "target": 9}, "expected": [0, 1]},
                {"input": {"nums": [3,2,4], "target": 6}, "expected": [1, 2]},
                {"input": {"nums": [3,3], "target": 6}, "expected": [0, 1]}
            ],
            "topics": ["Array", "Hash Table"]
        },
        {
            "id": 2,
            "title": "Palindrome Number",
            "difficulty": "Easy",
            "description": """Given an integer `x`, return `true` if `x` is a palindrome, and `false` otherwise.

An integer is a palindrome when it reads the same backward as forward.

**Example 1:**
```
Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.
```

**Example 2:**
```
Input: x = -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
```

**Example 3:**
```
Input: x = 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
```""",
            "starter_code": """def isPalindrome(x):
    # Write your solution here
    pass

# Test your solution
print(isPalindrome(121))   # Expected: True
print(isPalindrome(-121))  # Expected: False
print(isPalindrome(10))    # Expected: False""",
            "solution": """def isPalindrome(x):
    # Negative numbers are not palindromes
    if x < 0:
        return False
    
    # Convert to string and compare with reverse
    return str(x) == str(x)[::-1]

# Alternative solution without string conversion:
def isPalindromeNumeric(x):
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    
    reversed_half = 0
    while x > reversed_half:
        reversed_half = reversed_half * 10 + x % 10
        x //= 10
    
    return x == reversed_half or x == reversed_half // 10

# Time Complexity: O(log n)
# Space Complexity: O(1)""",
            "hints": [
                "Negative numbers cannot be palindromes",
                "You can convert to string and compare with its reverse",
                "Or reverse half of the number and compare"
            ],
            "test_cases": [
                {"input": {"x": 121}, "expected": True},
                {"input": {"x": -121}, "expected": False},
                {"input": {"x": 10}, "expected": False},
                {"input": {"x": 12321}, "expected": True}
            ],
            "topics": ["Math"]
        },
        {
            "id": 3,
            "title": "Valid Parentheses",
            "difficulty": "Easy",
            "description": """Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

**Example 1:**
```
Input: s = "()"
Output: true
```

**Example 2:**
```
Input: s = "()[]{}"
Output: true
```

**Example 3:**
```
Input: s = "(]"
Output: false
```""",
            "starter_code": """def isValid(s):
    # Write your solution here
    pass

# Test your solution
print(isValid("()"))      # Expected: True
print(isValid("()[]{}"))  # Expected: True
print(isValid("(]"))      # Expected: False""",
            "solution": """def isValid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            # It's a closing bracket
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            # It's an opening bracket
            stack.append(char)
    
    return len(stack) == 0

# Time Complexity: O(n)
# Space Complexity: O(n)""",
            "hints": [
                "Use a stack data structure",
                "Push opening brackets onto the stack",
                "For closing brackets, check if it matches the top of stack"
            ],
            "test_cases": [
                {"input": {"s": "()"}, "expected": True},
                {"input": {"s": "()[]{}"}, "expected": True},
                {"input": {"s": "(]"}, "expected": False},
                {"input": {"s": "([)]"}, "expected": False},
                {"input": {"s": "{[]}"}, "expected": True}
            ],
            "topics": ["String", "Stack"]
        },
        {
            "id": 4,
            "title": "Reverse String",
            "difficulty": "Easy",
            "description": """Write a function that reverses a string. The input string is given as an array of characters `s`.

You must do this by modifying the input array in-place with O(1) extra memory.

**Example 1:**
```
Input: s = ["h","e","l","l","o"]
Output: ["o","l","l","e","h"]
```

**Example 2:**
```
Input: s = ["H","a","n","n","a","h"]
Output: ["h","a","n","n","a","H"]
```""",
            "starter_code": """def reverseString(s):
    # Write your solution here - modify s in-place
    pass

# Test your solution
s1 = ["h","e","l","l","o"]
reverseString(s1)
print(s1)  # Expected: ["o","l","l","e","h"]

s2 = ["H","a","n","n","a","h"]
reverseString(s2)
print(s2)  # Expected: ["h","a","n","n","a","H"]""",
            "solution": """def reverseString(s):
    # Two pointer approach
    left, right = 0, len(s) - 1
    
    while left < right:
        # Swap characters
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    
    # No return needed - modified in-place

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Use two pointers - one at start, one at end",
                "Swap characters at both pointers",
                "Move pointers towards the center"
            ],
            "test_cases": [
                {"input": {"s": ["h","e","l","l","o"]}, "expected": ["o","l","l","e","h"]},
                {"input": {"s": ["H","a","n","n","a","h"]}, "expected": ["h","a","n","n","a","H"]}
            ],
            "topics": ["Two Pointers", "String"]
        },
        {
            "id": 5,
            "title": "FizzBuzz",
            "difficulty": "Easy",
            "description": """Given an integer `n`, return a string array `answer` (1-indexed) where:

- `answer[i] == "FizzBuzz"` if `i` is divisible by 3 and 5.
- `answer[i] == "Fizz"` if `i` is divisible by 3.
- `answer[i] == "Buzz"` if `i` is divisible by 5.
- `answer[i] == i` (as a string) if none of the above conditions are true.

**Example 1:**
```
Input: n = 3
Output: ["1","2","Fizz"]
```

**Example 2:**
```
Input: n = 5
Output: ["1","2","Fizz","4","Buzz"]
```

**Example 3:**
```
Input: n = 15
Output: ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]
```""",
            "starter_code": """def fizzBuzz(n):
    # Write your solution here
    pass

# Test your solution
print(fizzBuzz(3))   # Expected: ["1","2","Fizz"]
print(fizzBuzz(5))   # Expected: ["1","2","Fizz","4","Buzz"]
print(fizzBuzz(15))  # Expected: ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]""",
            "solution": """def fizzBuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result

# Time Complexity: O(n)
# Space Complexity: O(n) for the output""",
            "hints": [
                "Check divisibility by 15 first (both 3 and 5)",
                "Then check divisibility by 3 and 5 separately",
                "Use modulo operator % to check divisibility"
            ],
            "test_cases": [
                {"input": {"n": 3}, "expected": ["1","2","Fizz"]},
                {"input": {"n": 5}, "expected": ["1","2","Fizz","4","Buzz"]},
                {"input": {"n": 15}, "expected": ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]}
            ],
            "topics": ["Math", "String"]
        },
        # STRING QUESTIONS
        {
            "id": 13,
            "title": "Valid Anagram",
            "difficulty": "Easy",
            "description": """Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

An anagram is a word formed by rearranging the letters of another word, using all the original letters exactly once.

**Example 1:**
```
Input: s = "anagram", t = "nagaram"
Output: true
```

**Example 2:**
```
Input: s = "rat", t = "car"
Output: false
```""",
            "starter_code": """def isAnagram(s, t):
    # Write your solution here
    pass

# Test your solution
print(isAnagram("anagram", "nagaram"))  # Expected: True
print(isAnagram("rat", "car"))          # Expected: False""",
            "solution": """def isAnagram(s, t):
    if len(s) != len(t):
        return False
    
    # Count characters in both strings
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1
    for c in t:
        count[c] = count.get(c, 0) - 1
    
    return all(v == 0 for v in count.values())

# Alternative: return sorted(s) == sorted(t)
# Time Complexity: O(n)
# Space Complexity: O(1) - at most 26 characters""",
            "hints": [
                "Anagrams have the same characters with same frequencies",
                "Use a hash map to count character frequencies",
                "Or simply sort both strings and compare"
            ],
            "test_cases": [
                {"input": {"s": "anagram", "t": "nagaram"}, "expected": True},
                {"input": {"s": "rat", "t": "car"}, "expected": False},
                {"input": {"s": "a", "t": "a"}, "expected": True}
            ],
            "topics": ["String", "Hash Table", "Sorting"]
        },
        {
            "id": 14,
            "title": "Longest Common Prefix",
            "difficulty": "Easy",
            "description": """Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string `""`.

**Example 1:**
```
Input: strs = ["flower","flow","flight"]
Output: "fl"
```

**Example 2:**
```
Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.
```""",
            "starter_code": """def longestCommonPrefix(strs):
    # Write your solution here
    pass

# Test your solution
print(longestCommonPrefix(["flower","flow","flight"]))  # Expected: "fl"
print(longestCommonPrefix(["dog","racecar","car"]))     # Expected: \"\"""",
            "solution": """def longestCommonPrefix(strs):
    if not strs:
        return ""
    
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    
    return prefix

# Time Complexity: O(S) where S is sum of all characters
# Space Complexity: O(1)""",
            "hints": [
                "Start with the first string as the prefix",
                "Compare with each subsequent string",
                "Shorten the prefix until it matches"
            ],
            "test_cases": [
                {"input": {"strs": ["flower","flow","flight"]}, "expected": "fl"},
                {"input": {"strs": ["dog","racecar","car"]}, "expected": ""},
                {"input": {"strs": ["a"]}, "expected": "a"}
            ],
            "topics": ["String"]
        },
        {
            "id": 15,
            "title": "First Unique Character in a String",
            "difficulty": "Easy",
            "description": """Given a string `s`, find the first non-repeating character in it and return its index. If it does not exist, return `-1`.

**Example 1:**
```
Input: s = "leetcode"
Output: 0
Explanation: 'l' is the first character that appears only once.
```

**Example 2:**
```
Input: s = "loveleetcode"
Output: 2
Explanation: 'v' is the first character that appears only once.
```

**Example 3:**
```
Input: s = "aabb"
Output: -1
```""",
            "starter_code": """def firstUniqChar(s):
    # Write your solution here
    pass

# Test your solution
print(firstUniqChar("leetcode"))      # Expected: 0
print(firstUniqChar("loveleetcode"))  # Expected: 2
print(firstUniqChar("aabb"))          # Expected: -1""",
            "solution": """def firstUniqChar(s):
    # Count frequency of each character
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1
    
    # Find first character with count 1
    for i, c in enumerate(s):
        if count[c] == 1:
            return i
    
    return -1

# Time Complexity: O(n)
# Space Complexity: O(1) - at most 26 characters""",
            "hints": [
                "Count the frequency of each character first",
                "Then iterate through the string to find first unique",
                "Use a hash map for O(1) lookups"
            ],
            "test_cases": [
                {"input": {"s": "leetcode"}, "expected": 0},
                {"input": {"s": "loveleetcode"}, "expected": 2},
                {"input": {"s": "aabb"}, "expected": -1}
            ],
            "topics": ["String", "Hash Table"]
        },
        {
            "id": 16,
            "title": "String to Integer (atoi)",
            "difficulty": "Easy",
            "description": """Implement the `myAtoi(string s)` function, which converts a string to a 32-bit signed integer.

The algorithm:
1. Skip leading whitespace
2. Check for '+' or '-' sign
3. Read digits until non-digit or end
4. Clamp to 32-bit signed integer range [-2^31, 2^31 - 1]

**Example 1:**
```
Input: s = "42"
Output: 42
```

**Example 2:**
```
Input: s = "   -42"
Output: -42
```

**Example 3:**
```
Input: s = "4193 with words"
Output: 4193
```""",
            "starter_code": """def myAtoi(s):
    # Write your solution here
    pass

# Test your solution
print(myAtoi("42"))              # Expected: 42
print(myAtoi("   -42"))          # Expected: -42
print(myAtoi("4193 with words")) # Expected: 4193""",
            "solution": """def myAtoi(s):
    s = s.strip()
    if not s:
        return 0
    
    sign = 1
    i = 0
    
    if s[0] == '-':
        sign = -1
        i = 1
    elif s[0] == '+':
        i = 1
    
    result = 0
    while i < len(s) and s[i].isdigit():
        result = result * 10 + int(s[i])
        i += 1
    
    result *= sign
    
    # Clamp to 32-bit range
    INT_MIN, INT_MAX = -2**31, 2**31 - 1
    return max(INT_MIN, min(INT_MAX, result))

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Handle edge cases: whitespace, signs, non-digits",
                "Process digits one by one: result = result * 10 + digit",
                "Don't forget to clamp to 32-bit integer range"
            ],
            "test_cases": [
                {"input": {"s": "42"}, "expected": 42},
                {"input": {"s": "   -42"}, "expected": -42},
                {"input": {"s": "4193 with words"}, "expected": 4193}
            ],
            "topics": ["String"]
        },
        {
            "id": 17,
            "title": "Count and Say",
            "difficulty": "Easy",
            "description": """The count-and-say sequence is a sequence of digit strings defined by the recursive formula:
- countAndSay(1) = "1"
- countAndSay(n) is the way you would "say" the digit string from countAndSay(n-1)

To "say" a digit string, split it into groups of consecutive same digits, then for each group say the count followed by the digit.

**Example 1:**
```
Input: n = 1
Output: "1"
```

**Example 2:**
```
Input: n = 4
Output: "1211"
Explanation:
countAndSay(1) = "1"
countAndSay(2) = say "1" = "11" (one 1)
countAndSay(3) = say "11" = "21" (two 1s)
countAndSay(4) = say "21" = "1211" (one 2, one 1)
```""",
            "starter_code": """def countAndSay(n):
    # Write your solution here
    pass

# Test your solution
print(countAndSay(1))  # Expected: "1"
print(countAndSay(4))  # Expected: "1211"
print(countAndSay(5))  # Expected: "111221\"""",
            "solution": """def countAndSay(n):
    if n == 1:
        return "1"
    
    prev = countAndSay(n - 1)
    result = ""
    i = 0
    
    while i < len(prev):
        char = prev[i]
        count = 0
        while i < len(prev) and prev[i] == char:
            count += 1
            i += 1
        result += str(count) + char
    
    return result

# Time Complexity: O(2^n) - string can double in size
# Space Complexity: O(2^n)""",
            "hints": [
                "Build each term from the previous one",
                "Group consecutive same digits together",
                "For each group, append count + digit to result"
            ],
            "test_cases": [
                {"input": {"n": 1}, "expected": "1"},
                {"input": {"n": 4}, "expected": "1211"},
                {"input": {"n": 5}, "expected": "111221"}
            ],
            "topics": ["String"]
        },
        {
            "id": 18,
            "title": "Implement strStr()",
            "difficulty": "Easy",
            "description": """Given two strings `haystack` and `needle`, return the index of the first occurrence of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`.

**Example 1:**
```
Input: haystack = "sadbutsad", needle = "sad"
Output: 0
Explanation: "sad" occurs at index 0 and 6. The first occurrence is at index 0.
```

**Example 2:**
```
Input: haystack = "leetcode", needle = "leeto"
Output: -1
Explanation: "leeto" did not occur in "leetcode".
```""",
            "starter_code": """def strStr(haystack, needle):
    # Write your solution here
    pass

# Test your solution
print(strStr("sadbutsad", "sad"))  # Expected: 0
print(strStr("leetcode", "leeto")) # Expected: -1""",
            "solution": """def strStr(haystack, needle):
    if not needle:
        return 0
    
    n, m = len(haystack), len(needle)
    
    for i in range(n - m + 1):
        if haystack[i:i+m] == needle:
            return i
    
    return -1

# Time Complexity: O((n-m) * m)
# Space Complexity: O(1)""",
            "hints": [
                "Slide a window of needle's length over haystack",
                "Compare the window with needle at each position",
                "Return the index when a match is found"
            ],
            "test_cases": [
                {"input": {"haystack": "sadbutsad", "needle": "sad"}, "expected": 0},
                {"input": {"haystack": "leetcode", "needle": "leeto"}, "expected": -1},
                {"input": {"haystack": "hello", "needle": "ll"}, "expected": 2}
            ],
            "topics": ["String", "Two Pointers"]
        },
        # ARRAY QUESTIONS
        {
            "id": 19,
            "title": "Remove Duplicates from Sorted Array",
            "difficulty": "Easy",
            "description": """Given an integer array `nums` sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. Return the number of unique elements.

**Example 1:**
```
Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]
Explanation: Your function should return k = 2, with the first two elements being 1 and 2.
```

**Example 2:**
```
Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
```""",
            "starter_code": """def removeDuplicates(nums):
    # Write your solution here
    pass

# Test your solution
nums1 = [1,1,2]
print(removeDuplicates(nums1), nums1[:2])  # Expected: 2, [1, 2]""",
            "solution": """def removeDuplicates(nums):
    if not nums:
        return 0
    
    # Two pointer approach
    write = 1
    
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    
    return write

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Use two pointers: read and write",
                "Read pointer scans the array",
                "Write pointer places unique elements"
            ],
            "test_cases": [
                {"input": {"nums": [1,1,2]}, "expected": 2},
                {"input": {"nums": [0,0,1,1,1,2,2,3,3,4]}, "expected": 5}
            ],
            "topics": ["Array", "Two Pointers"]
        },
        {
            "id": 20,
            "title": "Best Time to Buy and Sell Stock",
            "difficulty": "Easy",
            "description": """You are given an array `prices` where `prices[i]` is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy and a single day to sell in the future.

Return the maximum profit you can achieve. If no profit is possible, return 0.

**Example 1:**
```
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
```

**Example 2:**
```
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: No profit is possible.
```""",
            "starter_code": """def maxProfit(prices):
    # Write your solution here
    pass

# Test your solution
print(maxProfit([7,1,5,3,6,4]))  # Expected: 5
print(maxProfit([7,6,4,3,1]))    # Expected: 0""",
            "solution": """def maxProfit(prices):
    if not prices:
        return 0
    
    min_price = prices[0]
    max_profit = 0
    
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    
    return max_profit

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Track the minimum price seen so far",
                "At each point, calculate potential profit",
                "Keep track of maximum profit"
            ],
            "test_cases": [
                {"input": {"prices": [7,1,5,3,6,4]}, "expected": 5},
                {"input": {"prices": [7,6,4,3,1]}, "expected": 0}
            ],
            "topics": ["Array", "Dynamic Programming"]
        },
        {
            "id": 21,
            "title": "Contains Duplicate",
            "difficulty": "Easy",
            "description": """Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.

**Example 1:**
```
Input: nums = [1,2,3,1]
Output: true
```

**Example 2:**
```
Input: nums = [1,2,3,4]
Output: false
```

**Example 3:**
```
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true
```""",
            "starter_code": """def containsDuplicate(nums):
    # Write your solution here
    pass

# Test your solution
print(containsDuplicate([1,2,3,1]))  # Expected: True
print(containsDuplicate([1,2,3,4]))  # Expected: False""",
            "solution": """def containsDuplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# Alternative: return len(nums) != len(set(nums))
# Time Complexity: O(n)
# Space Complexity: O(n)""",
            "hints": [
                "Use a set to track seen numbers",
                "If a number is already in the set, return True",
                "Or compare length of array to length of set"
            ],
            "test_cases": [
                {"input": {"nums": [1,2,3,1]}, "expected": True},
                {"input": {"nums": [1,2,3,4]}, "expected": False},
                {"input": {"nums": [1,1,1,3,3,4,3,2,4,2]}, "expected": True}
            ],
            "topics": ["Array", "Hash Table"]
        },
        {
            "id": 22,
            "title": "Product of Array Except Self",
            "difficulty": "Easy",
            "description": """Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`.

You must not use division and solve it in O(n) time.

**Example 1:**
```
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
```

**Example 2:**
```
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
```""",
            "starter_code": """def productExceptSelf(nums):
    # Write your solution here
    pass

# Test your solution
print(productExceptSelf([1,2,3,4]))      # Expected: [24,12,8,6]
print(productExceptSelf([-1,1,0,-3,3]))  # Expected: [0,0,9,0,0]""",
            "solution": """def productExceptSelf(nums):
    n = len(nums)
    result = [1] * n
    
    # Left pass: result[i] = product of all elements to the left
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]
    
    # Right pass: multiply by product of all elements to the right
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result

# Time Complexity: O(n)
# Space Complexity: O(1) excluding output array""",
            "hints": [
                "For each element, you need left product and right product",
                "First pass: calculate prefix products",
                "Second pass: multiply by suffix products"
            ],
            "test_cases": [
                {"input": {"nums": [1,2,3,4]}, "expected": [24,12,8,6]},
                {"input": {"nums": [-1,1,0,-3,3]}, "expected": [0,0,9,0,0]}
            ],
            "topics": ["Array", "Prefix Sum"]
        },
        {
            "id": 23,
            "title": "Maximum Subarray",
            "difficulty": "Easy",
            "description": """Given an integer array `nums`, find the subarray with the largest sum, and return its sum.

**Example 1:**
```
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.
```

**Example 2:**
```
Input: nums = [1]
Output: 1
```

**Example 3:**
```
Input: nums = [5,4,-1,7,8]
Output: 23
```""",
            "starter_code": """def maxSubArray(nums):
    # Write your solution here
    pass

# Test your solution
print(maxSubArray([-2,1,-3,4,-1,2,1,-5,4]))  # Expected: 6
print(maxSubArray([5,4,-1,7,8]))              # Expected: 23""",
            "solution": """def maxSubArray(nums):
    # Kadane's algorithm
    max_sum = nums[0]
    current_sum = nums[0]
    
    for num in nums[1:]:
        # Either extend current subarray or start new
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Use Kadane's algorithm",
                "At each position, decide: extend current subarray or start new",
                "Track the maximum sum seen so far"
            ],
            "test_cases": [
                {"input": {"nums": [-2,1,-3,4,-1,2,1,-5,4]}, "expected": 6},
                {"input": {"nums": [1]}, "expected": 1},
                {"input": {"nums": [5,4,-1,7,8]}, "expected": 23}
            ],
            "topics": ["Array", "Dynamic Programming", "Divide and Conquer"]
        },
        {
            "id": 24,
            "title": "Move Zeroes",
            "difficulty": "Easy",
            "description": """Given an integer array `nums`, move all `0`'s to the end of it while maintaining the relative order of the non-zero elements.

You must do this in-place without making a copy of the array.

**Example 1:**
```
Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]
```

**Example 2:**
```
Input: nums = [0]
Output: [0]
```""",
            "starter_code": """def moveZeroes(nums):
    # Write your solution here - modify nums in-place
    pass

# Test your solution
nums = [0,1,0,3,12]
moveZeroes(nums)
print(nums)  # Expected: [1,3,12,0,0]""",
            "solution": """def moveZeroes(nums):
    # Two pointer approach
    write = 0
    
    # Move non-zero elements to front
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write] = nums[read]
            write += 1
    
    # Fill remaining with zeros
    while write < len(nums):
        nums[write] = 0
        write += 1

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Use two pointers: write and read",
                "Copy non-zero elements to the write position",
                "Fill remaining positions with zeros"
            ],
            "test_cases": [
                {"input": {"nums": [0,1,0,3,12]}, "expected": [1,3,12,0,0]},
                {"input": {"nums": [0]}, "expected": [0]}
            ],
            "topics": ["Array", "Two Pointers"]
        },
        # MATH QUESTIONS
        {
            "id": 25,
            "title": "Power of Two",
            "difficulty": "Easy",
            "description": """Given an integer `n`, return `true` if it is a power of two. Otherwise, return `false`.

An integer `n` is a power of two if there exists an integer `x` such that `n == 2^x`.

**Example 1:**
```
Input: n = 1
Output: true (2^0 = 1)
```

**Example 2:**
```
Input: n = 16
Output: true (2^4 = 16)
```

**Example 3:**
```
Input: n = 3
Output: false
```""",
            "starter_code": """def isPowerOfTwo(n):
    # Write your solution here
    pass

# Test your solution
print(isPowerOfTwo(1))   # Expected: True
print(isPowerOfTwo(16))  # Expected: True
print(isPowerOfTwo(3))   # Expected: False""",
            "solution": """def isPowerOfTwo(n):
    if n <= 0:
        return False
    
    # Power of 2 has exactly one bit set
    # n & (n-1) clears the lowest set bit
    return (n & (n - 1)) == 0

# Alternative: return n > 0 and bin(n).count('1') == 1
# Time Complexity: O(1)
# Space Complexity: O(1)""",
            "hints": [
                "Powers of 2 in binary have exactly one '1' bit",
                "Use bit manipulation: n & (n-1) clears lowest set bit",
                "If result is 0, it's a power of 2"
            ],
            "test_cases": [
                {"input": {"n": 1}, "expected": True},
                {"input": {"n": 16}, "expected": True},
                {"input": {"n": 3}, "expected": False}
            ],
            "topics": ["Math", "Bit Manipulation"]
        },
        {
            "id": 26,
            "title": "Add Digits",
            "difficulty": "Easy",
            "description": """Given an integer `num`, repeatedly add all its digits until the result has only one digit, and return it.

**Example 1:**
```
Input: num = 38
Output: 2
Explanation: 3 + 8 = 11, 1 + 1 = 2. Since 2 has only one digit, return it.
```

**Example 2:**
```
Input: num = 0
Output: 0
```""",
            "starter_code": """def addDigits(num):
    # Write your solution here
    pass

# Test your solution
print(addDigits(38))  # Expected: 2
print(addDigits(0))   # Expected: 0""",
            "solution": """def addDigits(num):
    # Using digital root formula
    if num == 0:
        return 0
    return 1 + (num - 1) % 9

# Iterative solution:
def addDigitsIterative(num):
    while num >= 10:
        total = 0
        while num:
            total += num % 10
            num //= 10
        num = total
    return num

# Time Complexity: O(1) for formula, O(log n) for iterative
# Space Complexity: O(1)""",
            "hints": [
                "You could iteratively sum digits until single digit",
                "Or use the digital root formula: 1 + (num - 1) % 9",
                "This is based on number theory (congruence)"
            ],
            "test_cases": [
                {"input": {"num": 38}, "expected": 2},
                {"input": {"num": 0}, "expected": 0},
                {"input": {"num": 123}, "expected": 6}
            ],
            "topics": ["Math"]
        },
        {
            "id": 27,
            "title": "Count Primes",
            "difficulty": "Easy",
            "description": """Given an integer `n`, return the number of prime numbers that are strictly less than `n`.

**Example 1:**
```
Input: n = 10
Output: 4
Explanation: There are 4 primes less than 10: 2, 3, 5, 7.
```

**Example 2:**
```
Input: n = 0
Output: 0
```

**Example 3:**
```
Input: n = 1
Output: 0
```""",
            "starter_code": """def countPrimes(n):
    # Write your solution here
    pass

# Test your solution
print(countPrimes(10))  # Expected: 4
print(countPrimes(0))   # Expected: 0
print(countPrimes(1))   # Expected: 0""",
            "solution": """def countPrimes(n):
    if n < 2:
        return 0
    
    # Sieve of Eratosthenes
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            # Mark multiples as not prime
            for j in range(i * i, n, i):
                is_prime[j] = False
    
    return sum(is_prime)

# Time Complexity: O(n log log n)
# Space Complexity: O(n)""",
            "hints": [
                "Use Sieve of Eratosthenes algorithm",
                "Mark all multiples of each prime as not prime",
                "Start marking from i*i since smaller multiples are already marked"
            ],
            "test_cases": [
                {"input": {"n": 10}, "expected": 4},
                {"input": {"n": 0}, "expected": 0},
                {"input": {"n": 1}, "expected": 0}
            ],
            "topics": ["Math", "Array"]
        },
        {
            "id": 28,
            "title": "Roman to Integer",
            "difficulty": "Easy",
            "description": """Convert a Roman numeral string `s` to an integer.

Roman numerals: I=1, V=5, X=10, L=50, C=100, D=500, M=1000

Subtraction rules: I before V/X, X before L/C, C before D/M.

**Example 1:**
```
Input: s = "III"
Output: 3
```

**Example 2:**
```
Input: s = "LVIII"
Output: 58 (L=50, V=5, III=3)
```

**Example 3:**
```
Input: s = "MCMXCIV"
Output: 1994 (M=1000, CM=900, XC=90, IV=4)
```""",
            "starter_code": """def romanToInt(s):
    # Write your solution here
    pass

# Test your solution
print(romanToInt("III"))      # Expected: 3
print(romanToInt("LVIII"))    # Expected: 58
print(romanToInt("MCMXCIV"))  # Expected: 1994""",
            "solution": """def romanToInt(s):
    values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }
    
    total = 0
    prev = 0
    
    for char in s:
        curr = values[char]
        if curr > prev:
            # Subtraction case: subtract what we added before
            total += curr - 2 * prev
        else:
            total += curr
        prev = curr
    
    return total

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Normally, add the value of each symbol",
                "If a smaller value comes before larger, subtract it",
                "Process left to right, comparing with previous value"
            ],
            "test_cases": [
                {"input": {"s": "III"}, "expected": 3},
                {"input": {"s": "LVIII"}, "expected": 58},
                {"input": {"s": "MCMXCIV"}, "expected": 1994}
            ],
            "topics": ["Math", "String"]
        },
        {
            "id": 29,
            "title": "Reverse Integer",
            "difficulty": "Easy",
            "description": """Given a signed 32-bit integer `x`, return `x` with its digits reversed. If reversing causes the value to go outside the 32-bit signed integer range [-2^31, 2^31 - 1], return 0.

**Example 1:**
```
Input: x = 123
Output: 321
```

**Example 2:**
```
Input: x = -123
Output: -321
```

**Example 3:**
```
Input: x = 120
Output: 21
```""",
            "starter_code": """def reverse(x):
    # Write your solution here
    pass

# Test your solution
print(reverse(123))   # Expected: 321
print(reverse(-123))  # Expected: -321
print(reverse(120))   # Expected: 21""",
            "solution": """def reverse(x):
    INT_MIN, INT_MAX = -2**31, 2**31 - 1
    
    sign = -1 if x < 0 else 1
    x = abs(x)
    
    result = 0
    while x:
        result = result * 10 + x % 10
        x //= 10
    
    result *= sign
    
    if result < INT_MIN or result > INT_MAX:
        return 0
    
    return result

# Time Complexity: O(log x)
# Space Complexity: O(1)""",
            "hints": [
                "Extract digits from right using modulo 10",
                "Build reversed number by multiplying by 10 and adding",
                "Don't forget to handle negative numbers and overflow"
            ],
            "test_cases": [
                {"input": {"x": 123}, "expected": 321},
                {"input": {"x": -123}, "expected": -321},
                {"input": {"x": 120}, "expected": 21}
            ],
            "topics": ["Math"]
        },
        {
            "id": 30,
            "title": "Excel Sheet Column Number",
            "difficulty": "Easy",
            "description": """Given a string `columnTitle` representing the Excel column title, return its corresponding column number.

```
A -> 1, B -> 2, ..., Z -> 26
AA -> 27, AB -> 28, ...
```

**Example 1:**
```
Input: columnTitle = "A"
Output: 1
```

**Example 2:**
```
Input: columnTitle = "AB"
Output: 28
```

**Example 3:**
```
Input: columnTitle = "ZY"
Output: 701
```""",
            "starter_code": """def titleToNumber(columnTitle):
    # Write your solution here
    pass

# Test your solution
print(titleToNumber("A"))   # Expected: 1
print(titleToNumber("AB"))  # Expected: 28
print(titleToNumber("ZY"))  # Expected: 701""",
            "solution": """def titleToNumber(columnTitle):
    result = 0
    for char in columnTitle:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Think of it as base-26 number system",
                "A=1, B=2, ..., Z=26",
                "Multiply by 26 for each position shift"
            ],
            "test_cases": [
                {"input": {"columnTitle": "A"}, "expected": 1},
                {"input": {"columnTitle": "AB"}, "expected": 28},
                {"input": {"columnTitle": "ZY"}, "expected": 701}
            ],
            "topics": ["Math", "String"]
        },
        # STACK QUESTIONS
        {
            "id": 31,
            "title": "Min Stack",
            "difficulty": "Easy",
            "description": """Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:
- MinStack() initializes the stack object
- push(val) pushes element val onto the stack
- pop() removes the element on top
- top() gets the top element
- getMin() retrieves the minimum element

**Example:**
```
Input: ["MinStack","push","push","push","getMin","pop","top","getMin"]
       [[],[-2],[0],[-3],[],[],[],[]]
Output: [null,null,null,null,-3,null,0,-2]
```""",
            "starter_code": """class MinStack:
    def __init__(self):
        # Initialize your data structure here
        pass

    def push(self, val):
        pass

    def pop(self):
        pass

    def top(self):
        pass

    def getMin(self):
        pass

# Test your solution
minStack = MinStack()
minStack.push(-2)
minStack.push(0)
minStack.push(-3)
print(minStack.getMin())  # Expected: -3
minStack.pop()
print(minStack.top())     # Expected: 0
print(minStack.getMin())  # Expected: -2""",
            "solution": """class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self):
        if self.stack[-1] == self.min_stack[-1]:
            self.min_stack.pop()
        self.stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]

# Time Complexity: O(1) for all operations
# Space Complexity: O(n)""",
            "hints": [
                "Use an auxiliary stack to track minimums",
                "Push to min_stack when new value <= current min",
                "Pop from min_stack when popped value equals current min"
            ],
            "test_cases": [],
            "topics": ["Stack", "Design"]
        },
        {
            "id": 32,
            "title": "Evaluate Reverse Polish Notation",
            "difficulty": "Easy",
            "description": """Evaluate the value of an arithmetic expression in Reverse Polish Notation (postfix notation).

Valid operators are +, -, *, /. Each operand may be an integer or another expression.

Division truncates toward zero.

**Example 1:**
```
Input: tokens = ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) * 3) = 9
```

**Example 2:**
```
Input: tokens = ["4","13","5","/","+"]
Output: 6
Explanation: (4 + (13 / 5)) = 6
```""",
            "starter_code": """def evalRPN(tokens):
    # Write your solution here
    pass

# Test your solution
print(evalRPN(["2","1","+","3","*"]))     # Expected: 9
print(evalRPN(["4","13","5","/","+"]))    # Expected: 6""",
            "solution": """def evalRPN(tokens):
    stack = []
    operators = {'+', '-', '*', '/'}
    
    for token in tokens:
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:
                stack.append(int(a / b))  # Truncate toward zero
        else:
            stack.append(int(token))
    
    return stack[0]

# Time Complexity: O(n)
# Space Complexity: O(n)""",
            "hints": [
                "Use a stack to store operands",
                "When you see an operator, pop two operands",
                "Apply the operator and push the result back"
            ],
            "test_cases": [
                {"input": {"tokens": ["2","1","+","3","*"]}, "expected": 9},
                {"input": {"tokens": ["4","13","5","/","+"]}, "expected": 6}
            ],
            "topics": ["Stack", "Math"]
        },
        {
            "id": 33,
            "title": "Daily Temperatures",
            "difficulty": "Easy",
            "description": """Given an array of integers `temperatures` representing daily temperatures, return an array `answer` where `answer[i]` is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day with warmer temperature, set `answer[i] = 0`.

**Example 1:**
```
Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]
```

**Example 2:**
```
Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]
```""",
            "starter_code": """def dailyTemperatures(temperatures):
    # Write your solution here
    pass

# Test your solution
print(dailyTemperatures([73,74,75,71,69,72,76,73]))  # Expected: [1,1,4,2,1,1,0,0]
print(dailyTemperatures([30,40,50,60]))               # Expected: [1,1,1,0]""",
            "solution": """def dailyTemperatures(temperatures):
    n = len(temperatures)
    answer = [0] * n
    stack = []  # Store indices
    
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev_idx = stack.pop()
            answer[prev_idx] = i - prev_idx
        stack.append(i)
    
    return answer

# Time Complexity: O(n)
# Space Complexity: O(n)""",
            "hints": [
                "Use a monotonic decreasing stack of indices",
                "When you find a warmer day, pop and calculate days waited",
                "Remaining indices in stack have no warmer future day"
            ],
            "test_cases": [
                {"input": {"temperatures": [73,74,75,71,69,72,76,73]}, "expected": [1,1,4,2,1,1,0,0]},
                {"input": {"temperatures": [30,40,50,60]}, "expected": [1,1,1,0]}
            ],
            "topics": ["Stack", "Array", "Monotonic Stack"]
        },
        # LINKED LIST QUESTIONS
        {
            "id": 34,
            "title": "Reverse Linked List",
            "difficulty": "Easy",
            "description": """Given the head of a singly linked list, reverse the list, and return the reversed list.

**Example 1:**
```
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]
```

**Example 2:**
```
Input: head = [1,2]
Output: [2,1]
```

**Example 3:**
```
Input: head = []
Output: []
```""",
            "starter_code": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head):
    # Write your solution here
    pass

# Helper to create list from array
def create_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

# Helper to print list
def print_list(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    print(result)

# Test
print_list(reverseList(create_list([1,2,3,4,5])))  # Expected: [5,4,3,2,1]""",
            "solution": """def reverseList(head):
    prev = None
    current = head
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    return prev

# Recursive solution:
def reverseListRecursive(head):
    if not head or not head.next:
        return head
    
    new_head = reverseListRecursive(head.next)
    head.next.next = head
    head.next = None
    
    return new_head

# Time Complexity: O(n)
# Space Complexity: O(1) iterative, O(n) recursive""",
            "hints": [
                "Use three pointers: prev, current, next",
                "Save the next node before changing pointers",
                "Move all pointers forward after reversing link"
            ],
            "test_cases": [],
            "topics": ["Linked List", "Recursion"]
        },
        {
            "id": 35,
            "title": "Merge Two Sorted Lists",
            "difficulty": "Easy",
            "description": """Merge two sorted linked lists and return it as a sorted list. The list should be made by splicing together the nodes of the first two lists.

**Example 1:**
```
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
```

**Example 2:**
```
Input: list1 = [], list2 = []
Output: []
```

**Example 3:**
```
Input: list1 = [], list2 = [0]
Output: [0]
```""",
            "starter_code": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(list1, list2):
    # Write your solution here
    pass

# Test your solution (create test lists similarly to previous question)""",
            "solution": """def mergeTwoLists(list1, list2):
    dummy = ListNode()
    current = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    # Attach remaining nodes
    current.next = list1 or list2
    
    return dummy.next

# Time Complexity: O(n + m)
# Space Complexity: O(1)""",
            "hints": [
                "Use a dummy node to simplify edge cases",
                "Compare heads of both lists, pick smaller",
                "Attach remaining list at the end"
            ],
            "test_cases": [],
            "topics": ["Linked List", "Recursion"]
        },
        {
            "id": 36,
            "title": "Linked List Cycle",
            "difficulty": "Easy",
            "description": """Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

A cycle exists if some node can be reached again by continuously following the next pointer.

Return `true` if there is a cycle, otherwise return `false`.

**Example 1:**
```
Input: head = [3,2,0,-4], pos = 1 (tail connects to index 1)
Output: true
```

**Example 2:**
```
Input: head = [1,2], pos = 0 (tail connects to index 0)
Output: true
```

**Example 3:**
```
Input: head = [1], pos = -1 (no cycle)
Output: false
```""",
            "starter_code": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def hasCycle(head):
    # Write your solution here
    pass""",
            "solution": """def hasCycle(head):
    # Floyd's Cycle Detection (Tortoise and Hare)
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    
    return False

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Use Floyd's Cycle Detection algorithm",
                "Use two pointers: slow moves 1 step, fast moves 2 steps",
                "If they meet, there's a cycle"
            ],
            "test_cases": [],
            "topics": ["Linked List", "Two Pointers"]
        },
        {
            "id": 37,
            "title": "Remove Nth Node From End of List",
            "difficulty": "Easy",
            "description": """Given the head of a linked list, remove the nth node from the end of the list and return its head.

**Example 1:**
```
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
```

**Example 2:**
```
Input: head = [1], n = 1
Output: []
```

**Example 3:**
```
Input: head = [1,2], n = 1
Output: [1]
```""",
            "starter_code": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def removeNthFromEnd(head, n):
    # Write your solution here
    pass""",
            "solution": """def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    
    # Move fast n+1 steps ahead
    for _ in range(n + 1):
        fast = fast.next
    
    # Move both until fast reaches end
    while fast:
        slow = slow.next
        fast = fast.next
    
    # Remove the nth node
    slow.next = slow.next.next
    
    return dummy.next

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Use two pointers with n nodes gap between them",
                "When fast reaches end, slow is at the node before target",
                "Use a dummy node to handle edge cases"
            ],
            "test_cases": [],
            "topics": ["Linked List", "Two Pointers"]
        },
        {
            "id": 38,
            "title": "Middle of the Linked List",
            "difficulty": "Easy",
            "description": """Given the head of a singly linked list, return the middle node of the linked list.

If there are two middle nodes, return the second middle node.

**Example 1:**
```
Input: head = [1,2,3,4,5]
Output: [3,4,5] (middle node with value 3)
```

**Example 2:**
```
Input: head = [1,2,3,4,5,6]
Output: [4,5,6] (middle node with value 4)
```""",
            "starter_code": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def middleNode(head):
    # Write your solution here
    pass""",
            "solution": """def middleNode(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Use slow and fast pointers",
                "Slow moves 1 step, fast moves 2 steps",
                "When fast reaches end, slow is at middle"
            ],
            "test_cases": [],
            "topics": ["Linked List", "Two Pointers"]
        },
        # TREE QUESTIONS
        {
            "id": 39,
            "title": "Maximum Depth of Binary Tree",
            "difficulty": "Easy",
            "description": """Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

**Example 1:**
```
Input: root = [3,9,20,null,null,15,7]
Output: 3
```

**Example 2:**
```
Input: root = [1,null,2]
Output: 2
```""",
            "starter_code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxDepth(root):
    # Write your solution here
    pass""",
            "solution": """def maxDepth(root):
    if not root:
        return 0
    
    return 1 + max(maxDepth(root.left), maxDepth(root.right))

# Iterative BFS solution:
def maxDepthBFS(root):
    if not root:
        return 0
    
    from collections import deque
    queue = deque([root])
    depth = 0
    
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return depth

# Time Complexity: O(n)
# Space Complexity: O(h) where h is height""",
            "hints": [
                "Use recursion: depth = 1 + max(left depth, right depth)",
                "Base case: empty tree has depth 0",
                "Or use BFS and count levels"
            ],
            "test_cases": [],
            "topics": ["Tree", "DFS", "BFS", "Recursion"]
        },
        {
            "id": 40,
            "title": "Invert Binary Tree",
            "difficulty": "Easy",
            "description": """Given the root of a binary tree, invert the tree, and return its root.

**Example 1:**
```
Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]
```

**Example 2:**
```
Input: root = [2,1,3]
Output: [2,3,1]
```

**Example 3:**
```
Input: root = []
Output: []
```""",
            "starter_code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invertTree(root):
    # Write your solution here
    pass""",
            "solution": """def invertTree(root):
    if not root:
        return None
    
    # Swap children
    root.left, root.right = root.right, root.left
    
    # Recursively invert subtrees
    invertTree(root.left)
    invertTree(root.right)
    
    return root

# Time Complexity: O(n)
# Space Complexity: O(h) for recursion stack""",
            "hints": [
                "Swap left and right children of each node",
                "Recursively apply to all nodes",
                "Base case: null node returns null"
            ],
            "test_cases": [],
            "topics": ["Tree", "DFS", "BFS", "Recursion"]
        },
        {
            "id": 41,
            "title": "Same Tree",
            "difficulty": "Easy",
            "description": """Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

**Example 1:**
```
Input: p = [1,2,3], q = [1,2,3]
Output: true
```

**Example 2:**
```
Input: p = [1,2], q = [1,null,2]
Output: false
```

**Example 3:**
```
Input: p = [1,2,1], q = [1,1,2]
Output: false
```""",
            "starter_code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isSameTree(p, q):
    # Write your solution here
    pass""",
            "solution": """def isSameTree(p, q):
    # Both null
    if not p and not q:
        return True
    
    # One null, one not null
    if not p or not q:
        return False
    
    # Both non-null: check value and children
    return (p.val == q.val and 
            isSameTree(p.left, q.left) and 
            isSameTree(p.right, q.right))

# Time Complexity: O(n)
# Space Complexity: O(h) for recursion stack""",
            "hints": [
                "Check if both are null (same)",
                "Check if one is null (different)",
                "Compare values and recursively check children"
            ],
            "test_cases": [],
            "topics": ["Tree", "DFS", "BFS", "Recursion"]
        },
        {
            "id": 42,
            "title": "Symmetric Tree",
            "difficulty": "Easy",
            "description": """Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).

**Example 1:**
```
Input: root = [1,2,2,3,4,4,3]
Output: true
```

**Example 2:**
```
Input: root = [1,2,2,null,3,null,3]
Output: false
```""",
            "starter_code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isSymmetric(root):
    # Write your solution here
    pass""",
            "solution": """def isSymmetric(root):
    def isMirror(left, right):
        if not left and not right:
            return True
        if not left or not right:
            return False
        return (left.val == right.val and
                isMirror(left.left, right.right) and
                isMirror(left.right, right.left))
    
    return isMirror(root, root)

# Time Complexity: O(n)
# Space Complexity: O(h) for recursion stack""",
            "hints": [
                "A tree is symmetric if left subtree mirrors right subtree",
                "Mirror means: left.left = right.right, left.right = right.left",
                "Use a helper function to compare two subtrees"
            ],
            "test_cases": [],
            "topics": ["Tree", "DFS", "BFS", "Recursion"]
        },
        {
            "id": 43,
            "title": "Binary Tree Level Order Traversal",
            "difficulty": "Easy",
            "description": """Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

**Example 1:**
```
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]
```

**Example 2:**
```
Input: root = [1]
Output: [[1]]
```

**Example 3:**
```
Input: root = []
Output: []
```""",
            "starter_code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def levelOrder(root):
    # Write your solution here
    pass""",
            "solution": """def levelOrder(root):
    if not root:
        return []
    
    from collections import deque
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    
    return result

# Time Complexity: O(n)
# Space Complexity: O(n)""",
            "hints": [
                "Use BFS with a queue",
                "Process all nodes at current level before moving to next",
                "Track level size to know when level ends"
            ],
            "test_cases": [],
            "topics": ["Tree", "BFS"]
        },
        {
            "id": 44,
            "title": "Validate Binary Search Tree",
            "difficulty": "Easy",
            "description": """Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

**Example 1:**
```
Input: root = [2,1,3]
Output: true
```

**Example 2:**
```
Input: root = [5,1,4,null,null,3,6]
Output: false (4 is in right subtree of 5 but 4 < 5)
```""",
            "starter_code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isValidBST(root):
    # Write your solution here
    pass""",
            "solution": """def isValidBST(root):
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))

# Time Complexity: O(n)
# Space Complexity: O(h) for recursion stack""",
            "hints": [
                "Each node must be within a valid range",
                "Pass min and max bounds down the recursion",
                "Left child must be less than node, right must be greater"
            ],
            "test_cases": [],
            "topics": ["Tree", "DFS", "BST"]
        }
    ],
    "medium": [
        {
            "id": 6,
            "title": "Longest Substring Without Repeating Characters",
            "difficulty": "Medium",
            "description": """Given a string `s`, find the length of the longest substring without repeating characters.

**Example 1:**
```
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
```

**Example 2:**
```
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
```

**Example 3:**
```
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
```""",
            "starter_code": """def lengthOfLongestSubstring(s):
    # Write your solution here
    pass

# Test your solution
print(lengthOfLongestSubstring("abcabcbb"))  # Expected: 3
print(lengthOfLongestSubstring("bbbbb"))     # Expected: 1
print(lengthOfLongestSubstring("pwwkew"))    # Expected: 3""",
            "solution": """def lengthOfLongestSubstring(s):
    char_index = {}  # Store last index of each character
    max_length = 0
    start = 0  # Start of current window
    
    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            # Move start past the duplicate
            start = char_index[char] + 1
        
        char_index[char] = end
        max_length = max(max_length, end - start + 1)
    
    return max_length

# Time Complexity: O(n)
# Space Complexity: O(min(m, n)) where m is the charset size""",
            "hints": [
                "Use sliding window technique",
                "Keep track of character positions with a hash map",
                "When you find a duplicate, move the window start"
            ],
            "test_cases": [
                {"input": {"s": "abcabcbb"}, "expected": 3},
                {"input": {"s": "bbbbb"}, "expected": 1},
                {"input": {"s": "pwwkew"}, "expected": 3},
                {"input": {"s": ""}, "expected": 0}
            ],
            "topics": ["Hash Table", "String", "Sliding Window"]
        },
        {
            "id": 7,
            "title": "Container With Most Water",
            "difficulty": "Medium",
            "description": """You are given an integer array `height` of length `n`. There are `n` vertical lines where the two endpoints of the ith line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

**Example 1:**
```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The max area is between index 1 (height=8) and index 8 (height=7).
             Area = min(8,7) * (8-1) = 7 * 7 = 49
```

**Example 2:**
```
Input: height = [1,1]
Output: 1
```""",
            "starter_code": """def maxArea(height):
    # Write your solution here
    pass

# Test your solution
print(maxArea([1,8,6,2,5,4,8,3,7]))  # Expected: 49
print(maxArea([1,1]))                # Expected: 1""",
            "solution": """def maxArea(height):
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        # Calculate current area
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        
        # Move the pointer with smaller height
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Use two pointers at the start and end",
                "The area depends on the minimum height and width",
                "Move the pointer with the smaller height towards center"
            ],
            "test_cases": [
                {"input": {"height": [1,8,6,2,5,4,8,3,7]}, "expected": 49},
                {"input": {"height": [1,1]}, "expected": 1},
                {"input": {"height": [4,3,2,1,4]}, "expected": 16}
            ],
            "topics": ["Array", "Two Pointers", "Greedy"]
        },
        {
            "id": 8,
            "title": "3Sum",
            "difficulty": "Medium",
            "description": """Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.

**Example 1:**
```
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
```

**Example 2:**
```
Input: nums = [0,1,1]
Output: []
```

**Example 3:**
```
Input: nums = [0,0,0]
Output: [[0,0,0]]
```""",
            "starter_code": """def threeSum(nums):
    # Write your solution here
    pass

# Test your solution
print(threeSum([-1,0,1,2,-1,-4]))  # Expected: [[-1,-1,2],[-1,0,1]]
print(threeSum([0,1,1]))           # Expected: []
print(threeSum([0,0,0]))           # Expected: [[0,0,0]]""",
            "solution": """def threeSum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Two pointer approach for remaining elements
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
    
    return result

# Time Complexity: O(n²)
# Space Complexity: O(log n) for sorting""",
            "hints": [
                "Sort the array first to avoid duplicates easily",
                "Fix one element and use two pointers for the other two",
                "Skip duplicate elements to avoid duplicate triplets"
            ],
            "test_cases": [
                {"input": {"nums": [-1,0,1,2,-1,-4]}, "expected": [[-1,-1,2],[-1,0,1]]},
                {"input": {"nums": [0,1,1]}, "expected": []},
                {"input": {"nums": [0,0,0]}, "expected": [[0,0,0]]}
            ],
            "topics": ["Array", "Two Pointers", "Sorting"]
        },
        {
            "id": 9,
            "title": "Binary Search",
            "difficulty": "Medium",
            "description": """Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in nums. If target exists, then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

**Example 1:**
```
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4
```

**Example 2:**
```
Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1
```""",
            "starter_code": """def search(nums, target):
    # Write your solution here
    pass

# Test your solution
print(search([-1,0,3,5,9,12], 9))   # Expected: 4
print(search([-1,0,3,5,9,12], 2))   # Expected: -1""",
            "solution": """def search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Time Complexity: O(log n)
# Space Complexity: O(1)""",
            "hints": [
                "Use binary search - divide the search space in half each time",
                "Compare the middle element with target",
                "Adjust left or right boundary based on comparison"
            ],
            "test_cases": [
                {"input": {"nums": [-1,0,3,5,9,12], "target": 9}, "expected": 4},
                {"input": {"nums": [-1,0,3,5,9,12], "target": 2}, "expected": -1},
                {"input": {"nums": [5], "target": 5}, "expected": 0}
            ],
            "topics": ["Array", "Binary Search"]
        },
        {
            "id": 10,
            "title": "Merge Intervals",
            "difficulty": "Medium",
            "description": """Given an array of `intervals` where `intervals[i] = [starti, endi]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

**Example 1:**
```
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
```

**Example 2:**
```
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.
```""",
            "starter_code": """def merge(intervals):
    # Write your solution here
    pass

# Test your solution
print(merge([[1,3],[2,6],[8,10],[15,18]]))  # Expected: [[1,6],[8,10],[15,18]]
print(merge([[1,4],[4,5]]))                  # Expected: [[1,5]]""",
            "solution": """def merge(intervals):
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last = merged[-1]
        
        if current[0] <= last[1]:
            # Overlapping - extend the end
            last[1] = max(last[1], current[1])
        else:
            # Non-overlapping - add new interval
            merged.append(current)
    
    return merged

# Time Complexity: O(n log n) for sorting
# Space Complexity: O(n) for output""",
            "hints": [
                "Sort intervals by their start time first",
                "Compare each interval with the last merged interval",
                "If they overlap, extend the end time; otherwise add new interval"
            ],
            "test_cases": [
                {"input": {"intervals": [[1,3],[2,6],[8,10],[15,18]]}, "expected": [[1,6],[8,10],[15,18]]},
                {"input": {"intervals": [[1,4],[4,5]]}, "expected": [[1,5]]},
                {"input": {"intervals": [[1,4],[0,4]]}, "expected": [[0,4]]}
            ],
            "topics": ["Array", "Sorting"]
        },
        # MORE STRING QUESTIONS - MEDIUM
        {
            "id": 45,
            "title": "Longest Palindromic Substring",
            "difficulty": "Medium",
            "description": """Given a string `s`, return the longest palindromic substring in `s`.

**Example 1:**
```
Input: s = "babad"
Output: "bab" (or "aba")
```

**Example 2:**
```
Input: s = "cbbd"
Output: "bb"
```""",
            "starter_code": """def longestPalindrome(s):
    # Write your solution here
    pass

# Test your solution
print(longestPalindrome("babad"))  # Expected: "bab" or "aba"
print(longestPalindrome("cbbd"))   # Expected: "bb\"""",
            "solution": """def longestPalindrome(s):
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]
    
    result = ""
    for i in range(len(s)):
        # Odd length palindromes
        odd = expand(i, i)
        if len(odd) > len(result):
            result = odd
        
        # Even length palindromes
        even = expand(i, i + 1)
        if len(even) > len(result):
            result = even
    
    return result

# Time Complexity: O(n²)
# Space Complexity: O(1)""",
            "hints": [
                "Expand around center technique",
                "For each position, try both odd and even length",
                "Track the longest palindrome found"
            ],
            "test_cases": [
                {"input": {"s": "babad"}, "expected": "bab"},
                {"input": {"s": "cbbd"}, "expected": "bb"}
            ],
            "topics": ["String", "Dynamic Programming"]
        },
        {
            "id": 46,
            "title": "Group Anagrams",
            "difficulty": "Medium",
            "description": """Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

**Example 1:**
```
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
```

**Example 2:**
```
Input: strs = [""]
Output: [[""]]
```

**Example 3:**
```
Input: strs = ["a"]
Output: [["a"]]
```""",
            "starter_code": """def groupAnagrams(strs):
    # Write your solution here
    pass

# Test your solution
print(groupAnagrams(["eat","tea","tan","ate","nat","bat"]))""",
            "solution": """def groupAnagrams(strs):
    from collections import defaultdict
    
    groups = defaultdict(list)
    
    for s in strs:
        # Use sorted string as key
        key = tuple(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())

# Alternative: Use character count tuple as key
def groupAnagramsCount(strs):
    from collections import defaultdict
    groups = defaultdict(list)
    
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(s)
    
    return list(groups.values())

# Time Complexity: O(n * k log k) or O(n * k) with count method
# Space Complexity: O(n * k)""",
            "hints": [
                "Anagrams have the same sorted characters",
                "Use sorted string as a hash map key",
                "Or use character frequency tuple as key"
            ],
            "test_cases": [
                {"input": {"strs": ["eat","tea","tan","ate","nat","bat"]}, "expected": [["bat"],["nat","tan"],["ate","eat","tea"]]}
            ],
            "topics": ["String", "Hash Table", "Sorting"]
        },
        {
            "id": 47,
            "title": "Palindromic Substrings",
            "difficulty": "Medium",
            "description": """Given a string `s`, return the number of palindromic substrings in it.

A substring is a contiguous sequence of characters within the string.

**Example 1:**
```
Input: s = "abc"
Output: 3
Explanation: "a", "b", "c" are palindromic.
```

**Example 2:**
```
Input: s = "aaa"
Output: 6
Explanation: "a", "a", "a", "aa", "aa", "aaa" are palindromic.
```""",
            "starter_code": """def countSubstrings(s):
    # Write your solution here
    pass

# Test your solution
print(countSubstrings("abc"))  # Expected: 3
print(countSubstrings("aaa"))  # Expected: 6""",
            "solution": """def countSubstrings(s):
    count = 0
    
    def expand(left, right):
        nonlocal count
        while left >= 0 and right < len(s) and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    
    for i in range(len(s)):
        expand(i, i)      # Odd length
        expand(i, i + 1)  # Even length
    
    return count

# Time Complexity: O(n²)
# Space Complexity: O(1)""",
            "hints": [
                "Use expand around center technique",
                "Count palindromes of odd and even length",
                "Each single character is a palindrome"
            ],
            "test_cases": [
                {"input": {"s": "abc"}, "expected": 3},
                {"input": {"s": "aaa"}, "expected": 6}
            ],
            "topics": ["String", "Dynamic Programming"]
        },
        {
            "id": 48,
            "title": "Decode Ways",
            "difficulty": "Medium",
            "description": """A message containing letters A-Z can be encoded: 'A' -> "1", 'B' -> "2", ..., 'Z' -> "26".

Given a string `s` containing only digits, return the number of ways to decode it.

**Example 1:**
```
Input: s = "12"
Output: 2
Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).
```

**Example 2:**
```
Input: s = "226"
Output: 3
Explanation: "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).
```

**Example 3:**
```
Input: s = "06"
Output: 0
Explanation: "06" cannot be mapped (leading zero is invalid).
```""",
            "starter_code": """def numDecodings(s):
    # Write your solution here
    pass

# Test your solution
print(numDecodings("12"))   # Expected: 2
print(numDecodings("226"))  # Expected: 3
print(numDecodings("06"))   # Expected: 0""",
            "solution": """def numDecodings(s):
    if not s or s[0] == '0':
        return 0
    
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    
    for i in range(2, n + 1):
        # Single digit decode
        if s[i-1] != '0':
            dp[i] += dp[i-1]
        
        # Two digit decode
        two_digit = int(s[i-2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i-2]
    
    return dp[n]

# Time Complexity: O(n)
# Space Complexity: O(n), can be O(1) with two variables""",
            "hints": [
                "Use dynamic programming",
                "dp[i] = ways to decode first i characters",
                "Consider both single digit and two digit decodings"
            ],
            "test_cases": [
                {"input": {"s": "12"}, "expected": 2},
                {"input": {"s": "226"}, "expected": 3},
                {"input": {"s": "06"}, "expected": 0}
            ],
            "topics": ["String", "Dynamic Programming"]
        },
        {
            "id": 49,
            "title": "Letter Combinations of a Phone Number",
            "difficulty": "Medium",
            "description": """Given a string containing digits from 2-9, return all possible letter combinations that the number could represent.

```
2 -> abc, 3 -> def, 4 -> ghi, 5 -> jkl
6 -> mno, 7 -> pqrs, 8 -> tuv, 9 -> wxyz
```

**Example 1:**
```
Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

**Example 2:**
```
Input: digits = ""
Output: []
```""",
            "starter_code": """def letterCombinations(digits):
    # Write your solution here
    pass

# Test your solution
print(letterCombinations("23"))  # Expected: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
print(letterCombinations(""))    # Expected: []""",
            "solution": """def letterCombinations(digits):
    if not digits:
        return []
    
    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    
    result = []
    
    def backtrack(index, path):
        if index == len(digits):
            result.append(path)
            return
        
        for letter in phone[digits[index]]:
            backtrack(index + 1, path + letter)
    
    backtrack(0, "")
    return result

# Time Complexity: O(4^n) where n is length of digits
# Space Complexity: O(n) for recursion depth""",
            "hints": [
                "Use backtracking to generate all combinations",
                "Map each digit to its letters",
                "For each digit, try all possible letters"
            ],
            "test_cases": [
                {"input": {"digits": "23"}, "expected": ["ad","ae","af","bd","be","bf","cd","ce","cf"]},
                {"input": {"digits": ""}, "expected": []}
            ],
            "topics": ["String", "Backtracking"]
        },
        # DYNAMIC PROGRAMMING QUESTIONS
        {
            "id": 50,
            "title": "Climbing Stairs",
            "difficulty": "Medium",
            "description": """You are climbing a staircase. It takes `n` steps to reach the top. Each time you can climb 1 or 2 steps.

In how many distinct ways can you climb to the top?

**Example 1:**
```
Input: n = 2
Output: 2
Explanation: 1+1 or 2
```

**Example 2:**
```
Input: n = 3
Output: 3
Explanation: 1+1+1, 1+2, or 2+1
```""",
            "starter_code": """def climbStairs(n):
    # Write your solution here
    pass

# Test your solution
print(climbStairs(2))  # Expected: 2
print(climbStairs(3))  # Expected: 3
print(climbStairs(5))  # Expected: 8""",
            "solution": """def climbStairs(n):
    if n <= 2:
        return n
    
    prev2, prev1 = 1, 2
    
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "This is the Fibonacci sequence!",
                "ways(n) = ways(n-1) + ways(n-2)",
                "Use space-optimized DP with two variables"
            ],
            "test_cases": [
                {"input": {"n": 2}, "expected": 2},
                {"input": {"n": 3}, "expected": 3},
                {"input": {"n": 5}, "expected": 8}
            ],
            "topics": ["Dynamic Programming", "Math"]
        },
        {
            "id": 51,
            "title": "House Robber",
            "difficulty": "Medium",
            "description": """You are a robber planning to rob houses along a street. Each house has a certain amount of money. Adjacent houses have security systems connected - if two adjacent houses are broken into, the police will be alerted.

Given an array `nums` representing the amount at each house, return the maximum amount you can rob without alerting the police.

**Example 1:**
```
Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 ($1) + house 3 ($3) = $4.
```

**Example 2:**
```
Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 ($2) + house 3 ($9) + house 5 ($1) = $12.
```""",
            "starter_code": """def rob(nums):
    # Write your solution here
    pass

# Test your solution
print(rob([1,2,3,1]))    # Expected: 4
print(rob([2,7,9,3,1]))  # Expected: 12""",
            "solution": """def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    prev2, prev1 = 0, 0
    
    for num in nums:
        current = max(prev1, prev2 + num)
        prev2 = prev1
        prev1 = current
    
    return prev1

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "At each house, decide: rob it or skip it",
                "rob[i] = max(rob[i-1], rob[i-2] + nums[i])",
                "Use two variables to track the last two values"
            ],
            "test_cases": [
                {"input": {"nums": [1,2,3,1]}, "expected": 4},
                {"input": {"nums": [2,7,9,3,1]}, "expected": 12}
            ],
            "topics": ["Dynamic Programming"]
        },
        {
            "id": 52,
            "title": "Coin Change",
            "difficulty": "Medium",
            "description": """You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return the fewest number of coins needed to make up that amount. If that amount cannot be made up, return -1.

**Example 1:**
```
Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1
```

**Example 2:**
```
Input: coins = [2], amount = 3
Output: -1
```

**Example 3:**
```
Input: coins = [1], amount = 0
Output: 0
```""",
            "starter_code": """def coinChange(coins, amount):
    # Write your solution here
    pass

# Test your solution
print(coinChange([1,2,5], 11))  # Expected: 3
print(coinChange([2], 3))       # Expected: -1
print(coinChange([1], 0))       # Expected: 0""",
            "solution": """def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

# Time Complexity: O(amount * len(coins))
# Space Complexity: O(amount)""",
            "hints": [
                "Use bottom-up dynamic programming",
                "dp[i] = minimum coins to make amount i",
                "For each coin, update dp[x] = min(dp[x], dp[x-coin] + 1)"
            ],
            "test_cases": [
                {"input": {"coins": [1,2,5], "amount": 11}, "expected": 3},
                {"input": {"coins": [2], "amount": 3}, "expected": -1},
                {"input": {"coins": [1], "amount": 0}, "expected": 0}
            ],
            "topics": ["Dynamic Programming", "BFS"]
        },
        {
            "id": 53,
            "title": "Longest Increasing Subsequence",
            "difficulty": "Medium",
            "description": """Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

**Example 1:**
```
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: [2,3,7,101] is the longest increasing subsequence.
```

**Example 2:**
```
Input: nums = [0,1,0,3,2,3]
Output: 4
```

**Example 3:**
```
Input: nums = [7,7,7,7,7,7,7]
Output: 1
```""",
            "starter_code": """def lengthOfLIS(nums):
    # Write your solution here
    pass

# Test your solution
print(lengthOfLIS([10,9,2,5,3,7,101,18]))  # Expected: 4
print(lengthOfLIS([0,1,0,3,2,3]))          # Expected: 4""",
            "solution": """def lengthOfLIS(nums):
    # O(n log n) solution using binary search
    from bisect import bisect_left
    
    sub = []
    for num in nums:
        pos = bisect_left(sub, num)
        if pos == len(sub):
            sub.append(num)
        else:
            sub[pos] = num
    
    return len(sub)

# O(n²) DP solution:
def lengthOfLIS_DP(nums):
    n = len(nums)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

# Time Complexity: O(n log n) with binary search, O(n²) with DP
# Space Complexity: O(n)""",
            "hints": [
                "DP approach: dp[i] = length of LIS ending at index i",
                "For O(n log n): maintain a sorted subsequence",
                "Use binary search to find position to replace or append"
            ],
            "test_cases": [
                {"input": {"nums": [10,9,2,5,3,7,101,18]}, "expected": 4},
                {"input": {"nums": [0,1,0,3,2,3]}, "expected": 4},
                {"input": {"nums": [7,7,7,7,7,7,7]}, "expected": 1}
            ],
            "topics": ["Dynamic Programming", "Binary Search"]
        },
        {
            "id": 54,
            "title": "Unique Paths",
            "difficulty": "Medium",
            "description": """A robot is located at the top-left corner of a `m x n` grid. The robot can only move either down or right at any point.

The robot is trying to reach the bottom-right corner. How many possible unique paths are there?

**Example 1:**
```
Input: m = 3, n = 7
Output: 28
```

**Example 2:**
```
Input: m = 3, n = 2
Output: 3
Explanation: Right-Right-Down, Right-Down-Right, Down-Right-Right
```""",
            "starter_code": """def uniquePaths(m, n):
    # Write your solution here
    pass

# Test your solution
print(uniquePaths(3, 7))  # Expected: 28
print(uniquePaths(3, 2))  # Expected: 3""",
            "solution": """def uniquePaths(m, n):
    # Space-optimized DP
    dp = [1] * n
    
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    
    return dp[n-1]

# Or use combinatorics: C(m+n-2, m-1)
def uniquePathsMath(m, n):
    from math import factorial
    return factorial(m + n - 2) // (factorial(m - 1) * factorial(n - 1))

# Time Complexity: O(m*n)
# Space Complexity: O(n)""",
            "hints": [
                "paths[i][j] = paths[i-1][j] + paths[i][j-1]",
                "First row and column have only 1 path each",
                "Or use combinatorics: choose m-1 downs from m+n-2 moves"
            ],
            "test_cases": [
                {"input": {"m": 3, "n": 7}, "expected": 28},
                {"input": {"m": 3, "n": 2}, "expected": 3}
            ],
            "topics": ["Dynamic Programming", "Math", "Combinatorics"]
        },
        {
            "id": 55,
            "title": "Word Break",
            "difficulty": "Medium",
            "description": """Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.

**Example 1:**
```
Input: s = "leetcode", wordDict = ["leet","code"]
Output: true
Explanation: "leetcode" can be segmented as "leet code".
```

**Example 2:**
```
Input: s = "applepenapple", wordDict = ["apple","pen"]
Output: true
Explanation: "applepenapple" can be segmented as "apple pen apple".
```

**Example 3:**
```
Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: false
```""",
            "starter_code": """def wordBreak(s, wordDict):
    # Write your solution here
    pass

# Test your solution
print(wordBreak("leetcode", ["leet","code"]))        # Expected: True
print(wordBreak("applepenapple", ["apple","pen"]))   # Expected: True
print(wordBreak("catsandog", ["cats","dog","sand","and","cat"]))  # Expected: False""",
            "solution": """def wordBreak(s, wordDict):
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True  # Empty string can be segmented
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    
    return dp[n]

# Time Complexity: O(n² * k) where k is max word length
# Space Complexity: O(n)""",
            "hints": [
                "Use DP: dp[i] = can s[0:i] be segmented?",
                "dp[i] is True if dp[j] is True and s[j:i] is a word",
                "Use a set for O(1) word lookups"
            ],
            "test_cases": [
                {"input": {"s": "leetcode", "wordDict": ["leet","code"]}, "expected": True},
                {"input": {"s": "applepenapple", "wordDict": ["apple","pen"]}, "expected": True},
                {"input": {"s": "catsandog", "wordDict": ["cats","dog","sand","and","cat"]}, "expected": False}
            ],
            "topics": ["String", "Dynamic Programming", "Hash Table"]
        },
        # GRAPH QUESTIONS
        {
            "id": 56,
            "title": "Number of Islands",
            "difficulty": "Medium",
            "description": """Given an `m x n` 2D binary grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.

**Example 1:**
```
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1
```

**Example 2:**
```
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3
```""",
            "starter_code": """def numIslands(grid):
    # Write your solution here
    pass

# Test your solution
grid1 = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]
print(numIslands(grid1))  # Expected: 1""",
            "solution": """def numIslands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        grid[r][c] = '0'  # Mark as visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    
    return count

# Time Complexity: O(m * n)
# Space Complexity: O(m * n) for recursion stack""",
            "hints": [
                "Use DFS or BFS to traverse connected land cells",
                "Mark visited cells to avoid counting twice",
                "Each DFS/BFS starting point is a new island"
            ],
            "test_cases": [
                {"input": {"grid": [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]}, "expected": 1}
            ],
            "topics": ["Graph", "DFS", "BFS", "Matrix"]
        },
        {
            "id": 57,
            "title": "Clone Graph",
            "difficulty": "Medium",
            "description": """Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.

Each node contains a value and a list of its neighbors.

**Example 1:**
```
Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: [[2,4],[1,3],[2,4],[1,3]]
```""",
            "starter_code": """class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node):
    # Write your solution here
    pass""",
            "solution": """def cloneGraph(node):
    if not node:
        return None
    
    cloned = {}
    
    def dfs(node):
        if node in cloned:
            return cloned[node]
        
        clone = Node(node.val)
        cloned[node] = clone
        
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)

# Time Complexity: O(V + E)
# Space Complexity: O(V)""",
            "hints": [
                "Use a hash map to map old nodes to new nodes",
                "Use DFS or BFS to traverse the graph",
                "Clone each node and recursively clone neighbors"
            ],
            "test_cases": [],
            "topics": ["Graph", "DFS", "BFS", "Hash Table"]
        },
        {
            "id": 58,
            "title": "Course Schedule",
            "difficulty": "Medium",
            "description": """There are a total of `numCourses` courses you have to take, labeled from 0 to numCourses - 1. Some courses may have prerequisites.

Given the total number of courses and a list of prerequisite pairs, is it possible to finish all courses?

**Example 1:**
```
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: To take course 1, you should have finished course 0. So it is possible.
```

**Example 2:**
```
Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There is a cycle between courses 0 and 1.
```""",
            "starter_code": """def canFinish(numCourses, prerequisites):
    # Write your solution here
    pass

# Test your solution
print(canFinish(2, [[1,0]]))          # Expected: True
print(canFinish(2, [[1,0],[0,1]]))    # Expected: False""",
            "solution": """def canFinish(numCourses, prerequisites):
    from collections import defaultdict
    
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    
    # 0: unvisited, 1: visiting, 2: visited
    state = [0] * numCourses
    
    def hasCycle(course):
        if state[course] == 1:
            return True  # Cycle detected
        if state[course] == 2:
            return False  # Already processed
        
        state[course] = 1
        for prereq in graph[course]:
            if hasCycle(prereq):
                return True
        state[course] = 2
        return False
    
    for course in range(numCourses):
        if hasCycle(course):
            return False
    
    return True

# Time Complexity: O(V + E)
# Space Complexity: O(V + E)""",
            "hints": [
                "This is a cycle detection problem in a directed graph",
                "Use DFS with three states: unvisited, visiting, visited",
                "If we visit a 'visiting' node, there's a cycle"
            ],
            "test_cases": [
                {"input": {"numCourses": 2, "prerequisites": [[1,0]]}, "expected": True},
                {"input": {"numCourses": 2, "prerequisites": [[1,0],[0,1]]}, "expected": False}
            ],
            "topics": ["Graph", "DFS", "BFS", "Topological Sort"]
        },
        # BACKTRACKING QUESTIONS
        {
            "id": 59,
            "title": "Subsets",
            "difficulty": "Medium",
            "description": """Given an integer array `nums` of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.

**Example 1:**
```
Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

**Example 2:**
```
Input: nums = [0]
Output: [[],[0]]
```""",
            "starter_code": """def subsets(nums):
    # Write your solution here
    pass

# Test your solution
print(subsets([1,2,3]))  # Expected: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]""",
            "solution": """def subsets(nums):
    result = []
    
    def backtrack(start, path):
        result.append(path[:])
        
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result

# Iterative solution:
def subsetsIterative(nums):
    result = [[]]
    for num in nums:
        result += [subset + [num] for subset in result]
    return result

# Time Complexity: O(n * 2^n)
# Space Complexity: O(n)""",
            "hints": [
                "Use backtracking to generate all combinations",
                "At each position, choose to include or exclude the element",
                "Or iteratively add each number to all existing subsets"
            ],
            "test_cases": [
                {"input": {"nums": [1,2,3]}, "expected": [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]}
            ],
            "topics": ["Backtracking", "Bit Manipulation"]
        },
        {
            "id": 60,
            "title": "Permutations",
            "difficulty": "Medium",
            "description": """Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.

**Example 1:**
```
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**Example 2:**
```
Input: nums = [0,1]
Output: [[0,1],[1,0]]
```

**Example 3:**
```
Input: nums = [1]
Output: [[1]]
```""",
            "starter_code": """def permute(nums):
    # Write your solution here
    pass

# Test your solution
print(permute([1,2,3]))  # Expected: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]""",
            "solution": """def permute(nums):
    result = []
    
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        
        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()
    
    backtrack([], nums)
    return result

# Time Complexity: O(n * n!)
# Space Complexity: O(n)""",
            "hints": [
                "Use backtracking to try each element at each position",
                "Track which elements are remaining to be used",
                "Base case: when all elements are used"
            ],
            "test_cases": [
                {"input": {"nums": [1,2,3]}, "expected": [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]}
            ],
            "topics": ["Backtracking"]
        },
        {
            "id": 61,
            "title": "Combination Sum",
            "difficulty": "Medium",
            "description": """Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of candidates where the chosen numbers sum to target.

You may use the same number an unlimited number of times. The combinations may be returned in any order.

**Example 1:**
```
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
```

**Example 2:**
```
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]
```""",
            "starter_code": """def combinationSum(candidates, target):
    # Write your solution here
    pass

# Test your solution
print(combinationSum([2,3,6,7], 7))  # Expected: [[2,2,3],[7]]
print(combinationSum([2,3,5], 8))    # Expected: [[2,2,2,2],[2,3,3],[3,5]]""",
            "solution": """def combinationSum(candidates, target):
    result = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # Can reuse same element
            path.pop()
    
    backtrack(0, [], target)
    return result

# Time Complexity: O(n^(target/min))
# Space Complexity: O(target/min) for recursion depth""",
            "hints": [
                "Use backtracking with ability to reuse elements",
                "Pass start index to avoid duplicates",
                "Stop when remaining sum is 0 or negative"
            ],
            "test_cases": [
                {"input": {"candidates": [2,3,6,7], "target": 7}, "expected": [[2,2,3],[7]]},
                {"input": {"candidates": [2,3,5], "target": 8}, "expected": [[2,2,2,2],[2,3,3],[3,5]]}
            ],
            "topics": ["Backtracking"]
        },
        # SLIDING WINDOW QUESTIONS
        {
            "id": 62,
            "title": "Minimum Window Substring",
            "difficulty": "Medium",
            "description": """Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return "".

**Example 1:**
```
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
```

**Example 2:**
```
Input: s = "a", t = "a"
Output: "a"
```

**Example 3:**
```
Input: s = "a", t = "aa"
Output: ""
```""",
            "starter_code": """def minWindow(s, t):
    # Write your solution here
    pass

# Test your solution
print(minWindow("ADOBECODEBANC", "ABC"))  # Expected: "BANC"
print(minWindow("a", "a"))                 # Expected: "a"
print(minWindow("a", "aa"))                # Expected: \"\"""",
            "solution": """def minWindow(s, t):
    from collections import Counter
    
    if not s or not t:
        return ""
    
    t_count = Counter(t)
    required = len(t_count)
    
    left = formed = 0
    window_counts = {}
    ans = float('inf'), None, None
    
    for right, char in enumerate(s):
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1
        
        while formed == required:
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)
            
            char = s[left]
            window_counts[char] -= 1
            if char in t_count and window_counts[char] < t_count[char]:
                formed -= 1
            left += 1
    
    return "" if ans[0] == float('inf') else s[ans[1]:ans[2] + 1]

# Time Complexity: O(|S| + |T|)
# Space Complexity: O(|S| + |T|)""",
            "hints": [
                "Use sliding window with two pointers",
                "Track character counts with hash maps",
                "Expand right to include all chars, contract left to minimize"
            ],
            "test_cases": [
                {"input": {"s": "ADOBECODEBANC", "t": "ABC"}, "expected": "BANC"},
                {"input": {"s": "a", "t": "a"}, "expected": "a"}
            ],
            "topics": ["String", "Hash Table", "Sliding Window"]
        },
        {
            "id": 63,
            "title": "Sliding Window Maximum",
            "difficulty": "Medium",
            "description": """You are given an array of integers `nums`, there is a sliding window of size `k` which moves from the very left to the very right. You can only see the `k` numbers in the window. Return the max in each window position.

**Example 1:**
```
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]
Explanation: 
Window [1,3,-1] max = 3
Window [3,-1,-3] max = 3, etc.
```

**Example 2:**
```
Input: nums = [1], k = 1
Output: [1]
```""",
            "starter_code": """def maxSlidingWindow(nums, k):
    # Write your solution here
    pass

# Test your solution
print(maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3))  # Expected: [3,3,5,5,6,7]""",
            "solution": """def maxSlidingWindow(nums, k):
    from collections import deque
    
    dq = deque()  # Store indices
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements (they can't be max)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Time Complexity: O(n)
# Space Complexity: O(k)""",
            "hints": [
                "Use a monotonic deque to track potential maximums",
                "Keep indices in decreasing order of their values",
                "Front of deque is always the current window maximum"
            ],
            "test_cases": [
                {"input": {"nums": [1,3,-1,-3,5,3,6,7], "k": 3}, "expected": [3,3,5,5,6,7]}
            ],
            "topics": ["Array", "Sliding Window", "Monotonic Queue"]
        }
    ],
    "hard": [
        {
            "id": 11,
            "title": "Median of Two Sorted Arrays",
            "difficulty": "Hard",
            "description": """Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

**Example 1:**
```
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
```

**Example 2:**
```
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
```""",
            "starter_code": """def findMedianSortedArrays(nums1, nums2):
    # Write your solution here
    pass

# Test your solution
print(findMedianSortedArrays([1,3], [2]))     # Expected: 2.0
print(findMedianSortedArrays([1,2], [3,4]))   # Expected: 2.5""",
            "solution": """def findMedianSortedArrays(nums1, nums2):
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    
    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1
        
        maxLeft1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        minRight1 = float('inf') if partition1 == m else nums1[partition1]
        
        maxLeft2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        minRight2 = float('inf') if partition2 == n else nums2[partition2]
        
        if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:
            # Found the correct partition
            if (m + n) % 2 == 0:
                return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2
            else:
                return float(max(maxLeft1, maxLeft2))
        elif maxLeft1 > minRight2:
            right = partition1 - 1
        else:
            left = partition1 + 1
    
    return 0.0

# Time Complexity: O(log(min(m, n)))
# Space Complexity: O(1)""",
            "hints": [
                "Use binary search on the smaller array",
                "Partition both arrays such that left elements <= right elements",
                "The median is derived from elements around the partition"
            ],
            "test_cases": [
                {"input": {"nums1": [1,3], "nums2": [2]}, "expected": 2.0},
                {"input": {"nums1": [1,2], "nums2": [3,4]}, "expected": 2.5},
                {"input": {"nums1": [], "nums2": [1]}, "expected": 1.0}
            ],
            "topics": ["Array", "Binary Search", "Divide and Conquer"]
        },
        {
            "id": 12,
            "title": "Trapping Rain Water",
            "difficulty": "Hard",
            "description": """Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

**Example 1:**
```
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The elevation map [0,1,0,2,1,0,1,3,2,1,2,1] can trap 6 units of rain water.
```

**Example 2:**
```
Input: height = [4,2,0,3,2,5]
Output: 9
```""",
            "starter_code": """def trap(height):
    # Write your solution here
    pass

# Test your solution
print(trap([0,1,0,2,1,0,1,3,2,1,2,1]))  # Expected: 6
print(trap([4,2,0,3,2,5]))              # Expected: 9""",
            "solution": """def trap(height):
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water

# Time Complexity: O(n)
# Space Complexity: O(1)""",
            "hints": [
                "Water at each position = min(max_left, max_right) - height",
                "Use two pointers from both ends",
                "Track the maximum height seen from each side"
            ],
            "test_cases": [
                {"input": {"height": [0,1,0,2,1,0,1,3,2,1,2,1]}, "expected": 6},
                {"input": {"height": [4,2,0,3,2,5]}, "expected": 9},
                {"input": {"height": [1,2,1]}, "expected": 0}
            ],
            "topics": ["Array", "Two Pointers", "Stack", "Dynamic Programming"]
        },
        # MORE HARD QUESTIONS - STRING
        {
            "id": 64,
            "title": "Longest Valid Parentheses",
            "difficulty": "Hard",
            "description": """Given a string containing just '(' and ')', return the length of the longest valid (well-formed) parentheses substring.

**Example 1:**
```
Input: s = "(()"
Output: 2
Explanation: The longest valid parentheses substring is "()".
```

**Example 2:**
```
Input: s = ")()())"
Output: 4
Explanation: The longest valid parentheses substring is "()()".
```

**Example 3:**
```
Input: s = ""
Output: 0
```""",
            "starter_code": """def longestValidParentheses(s):
    # Write your solution here
    pass

# Test your solution
print(longestValidParentheses("(()"))     # Expected: 2
print(longestValidParentheses(")()())"))  # Expected: 4""",
            "solution": """def longestValidParentheses(s):
    stack = [-1]
    max_length = 0
    
    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                max_length = max(max_length, i - stack[-1])
    
    return max_length

# Time Complexity: O(n)
# Space Complexity: O(n)""",
            "hints": [
                "Use a stack to track indices of '(' characters",
                "Initialize stack with -1 as base index",
                "When closing a valid substring, calculate length from stack top"
            ],
            "test_cases": [
                {"input": {"s": "(()"}, "expected": 2},
                {"input": {"s": ")()())"}, "expected": 4},
                {"input": {"s": ""}, "expected": 0}
            ],
            "topics": ["String", "Stack", "Dynamic Programming"]
        },
        {
            "id": 65,
            "title": "Regular Expression Matching",
            "difficulty": "Hard",
            "description": """Given an input string `s` and a pattern `p`, implement regular expression matching with support for '.' and '*' where:
- '.' Matches any single character.
- '*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).

**Example 1:**
```
Input: s = "aa", p = "a"
Output: false
```

**Example 2:**
```
Input: s = "aa", p = "a*"
Output: true
```

**Example 3:**
```
Input: s = "ab", p = ".*"
Output: true
```""",
            "starter_code": """def isMatch(s, p):
    # Write your solution here
    pass

# Test your solution
print(isMatch("aa", "a"))    # Expected: False
print(isMatch("aa", "a*"))   # Expected: True
print(isMatch("ab", ".*"))   # Expected: True""",
            "solution": """def isMatch(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    # Handle patterns like a*, a*b*, etc.
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                # Zero occurrences of preceding element
                dp[i][j] = dp[i][j-2]
                # One or more occurrences
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]
    
    return dp[m][n]

# Time Complexity: O(m * n)
# Space Complexity: O(m * n)""",
            "hints": [
                "Use dynamic programming with 2D table",
                "Handle '*' cases: zero matches or one+ matches",
                "dp[i][j] = does s[0:i] match p[0:j]?"
            ],
            "test_cases": [
                {"input": {"s": "aa", "p": "a"}, "expected": False},
                {"input": {"s": "aa", "p": "a*"}, "expected": True},
                {"input": {"s": "ab", "p": ".*"}, "expected": True}
            ],
            "topics": ["String", "Dynamic Programming", "Recursion"]
        },
        {
            "id": 66,
            "title": "Wildcard Matching",
            "difficulty": "Hard",
            "description": """Given an input string `s` and a pattern `p`, implement wildcard pattern matching with support for '?' and '*' where:
- '?' Matches any single character.
- '*' Matches any sequence of characters (including empty).

**Example 1:**
```
Input: s = "aa", p = "a"
Output: false
```

**Example 2:**
```
Input: s = "aa", p = "*"
Output: true
```

**Example 3:**
```
Input: s = "cb", p = "?a"
Output: false
```""",
            "starter_code": """def isMatchWildcard(s, p):
    # Write your solution here
    pass

# Test your solution
print(isMatchWildcard("aa", "a"))   # Expected: False
print(isMatchWildcard("aa", "*"))   # Expected: True
print(isMatchWildcard("cb", "?a"))  # Expected: False""",
            "solution": """def isMatchWildcard(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    # Handle leading stars in pattern
    for j in range(1, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-1]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[i][j] = dp[i-1][j] or dp[i][j-1]
            elif p[j-1] == '?' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]
    
    return dp[m][n]

# Time Complexity: O(m * n)
# Space Complexity: O(m * n)""",
            "hints": [
                "Use dynamic programming similar to regex matching",
                "'*' can match empty (dp[i][j-1]) or any char (dp[i-1][j])",
                "'?' must match exactly one character"
            ],
            "test_cases": [
                {"input": {"s": "aa", "p": "a"}, "expected": False},
                {"input": {"s": "aa", "p": "*"}, "expected": True},
                {"input": {"s": "cb", "p": "?a"}, "expected": False}
            ],
            "topics": ["String", "Dynamic Programming", "Greedy"]
        },
        # HARD DP QUESTIONS
        {
            "id": 67,
            "title": "Edit Distance",
            "difficulty": "Hard",
            "description": """Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`.

You have three operations: Insert, Delete, Replace a character.

**Example 1:**
```
Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation: 
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')
```

**Example 2:**
```
Input: word1 = "intention", word2 = "execution"
Output: 5
```""",
            "starter_code": """def minDistance(word1, word2):
    # Write your solution here
    pass

# Test your solution
print(minDistance("horse", "ros"))          # Expected: 3
print(minDistance("intention", "execution"))  # Expected: 5""",
            "solution": """def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # Delete
                    dp[i][j-1],    # Insert
                    dp[i-1][j-1]   # Replace
                )
    
    return dp[m][n]

# Time Complexity: O(m * n)
# Space Complexity: O(m * n)""",
            "hints": [
                "Use dynamic programming with 2D table",
                "dp[i][j] = min operations to convert word1[0:i] to word2[0:j]",
                "Consider all three operations at each cell"
            ],
            "test_cases": [
                {"input": {"word1": "horse", "word2": "ros"}, "expected": 3},
                {"input": {"word1": "intention", "word2": "execution"}, "expected": 5}
            ],
            "topics": ["String", "Dynamic Programming"]
        },
        {
            "id": 68,
            "title": "Burst Balloons",
            "difficulty": "Hard",
            "description": """You are given `n` balloons indexed from 0 to n-1. Each balloon is painted with a number on it represented by array `nums`. 

You are asked to burst all the balloons. If you burst the ith balloon, you will get `nums[i-1] * nums[i] * nums[i+1]` coins. If i-1 or i+1 goes out of bounds, treat it as if there is a balloon with a 1 painted on it.

Return the maximum coins you can collect.

**Example 1:**
```
Input: nums = [3,1,5,8]
Output: 167
Explanation:
nums = [3,1,5,8] --> [3,5,8] --> [3,8] --> [8] --> []
coins =  3*1*5    +   3*5*8   +  1*3*8  + 1*8*1 = 167
```

**Example 2:**
```
Input: nums = [1,5]
Output: 10
```""",
            "starter_code": """def maxCoins(nums):
    # Write your solution here
    pass

# Test your solution
print(maxCoins([3,1,5,8]))  # Expected: 167
print(maxCoins([1,5]))      # Expected: 10""",
            "solution": """def maxCoins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    
    for length in range(2, n):
        for left in range(n - length):
            right = left + length
            for k in range(left + 1, right):
                # k is the last balloon to burst in range (left, right)
                coins = nums[left] * nums[k] * nums[right]
                dp[left][right] = max(
                    dp[left][right],
                    dp[left][k] + coins + dp[k][right]
                )
    
    return dp[0][n-1]

# Time Complexity: O(n³)
# Space Complexity: O(n²)""",
            "hints": [
                "Think about which balloon to burst LAST instead of first",
                "Add virtual balloons with value 1 at boundaries",
                "dp[i][j] = max coins from bursting all balloons between i and j"
            ],
            "test_cases": [
                {"input": {"nums": [3,1,5,8]}, "expected": 167},
                {"input": {"nums": [1,5]}, "expected": 10}
            ],
            "topics": ["Dynamic Programming"]
        },
        {
            "id": 69,
            "title": "Longest Increasing Path in a Matrix",
            "difficulty": "Hard",
            "description": """Given an `m x n` integers matrix, return the length of the longest increasing path in matrix.

From each cell, you can move in four directions: left, right, up, or down. You may not move diagonally or outside the boundary.

**Example 1:**
```
Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
Output: 4
Explanation: The longest increasing path is [1, 2, 6, 9].
```

**Example 2:**
```
Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
Output: 4
Explanation: The longest increasing path is [3, 4, 5, 6].
```""",
            "starter_code": """def longestIncreasingPath(matrix):
    # Write your solution here
    pass

# Test your solution
print(longestIncreasingPath([[9,9,4],[6,6,8],[2,1,1]]))  # Expected: 4
print(longestIncreasingPath([[3,4,5],[3,2,6],[2,2,1]]))  # Expected: 4""",
            "solution": """def longestIncreasingPath(matrix):
    if not matrix:
        return 0
    
    m, n = len(matrix), len(matrix[0])
    memo = [[0] * n for _ in range(m)]
    
    def dfs(i, j):
        if memo[i][j]:
            return memo[i][j]
        
        path = 1
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                path = max(path, 1 + dfs(ni, nj))
        
        memo[i][j] = path
        return path
    
    return max(dfs(i, j) for i in range(m) for j in range(n))

# Time Complexity: O(m * n)
# Space Complexity: O(m * n)""",
            "hints": [
                "Use DFS with memoization",
                "memo[i][j] = longest path starting from (i, j)",
                "Only move to larger values (ensures no cycles)"
            ],
            "test_cases": [
                {"input": {"matrix": [[9,9,4],[6,6,8],[2,1,1]]}, "expected": 4},
                {"input": {"matrix": [[3,4,5],[3,2,6],[2,2,1]]}, "expected": 4}
            ],
            "topics": ["Dynamic Programming", "DFS", "Matrix", "Memoization"]
        },
        # HARD GRAPH QUESTIONS
        {
            "id": 70,
            "title": "Word Ladder",
            "difficulty": "Hard",
            "description": """A transformation sequence from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence where:
- Every adjacent pair of words differs by a single letter.
- Every word in the sequence is in wordList. Note that beginWord does not need to be in wordList.

Return the number of words in the shortest transformation sequence, or 0 if no such sequence exists.

**Example 1:**
```
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
Explanation: "hit" -> "hot" -> "dot" -> "dog" -> "cog"
```

**Example 2:**
```
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
Output: 0
```""",
            "starter_code": """def ladderLength(beginWord, endWord, wordList):
    # Write your solution here
    pass

# Test your solution
print(ladderLength("hit", "cog", ["hot","dot","dog","lot","log","cog"]))  # Expected: 5""",
            "solution": """def ladderLength(beginWord, endWord, wordList):
    from collections import deque
    
    word_set = set(wordList)
    if endWord not in word_set:
        return 0
    
    queue = deque([(beginWord, 1)])
    
    while queue:
        word, length = queue.popleft()
        
        if word == endWord:
            return length
        
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                if new_word in word_set:
                    word_set.remove(new_word)
                    queue.append((new_word, length + 1))
    
    return 0

# Time Complexity: O(M² * N) where M is word length, N is wordList size
# Space Complexity: O(M * N)""",
            "hints": [
                "Use BFS to find shortest path",
                "Generate all possible one-letter transformations",
                "Remove visited words to avoid cycles"
            ],
            "test_cases": [
                {"input": {"beginWord": "hit", "endWord": "cog", "wordList": ["hot","dot","dog","lot","log","cog"]}, "expected": 5}
            ],
            "topics": ["BFS", "Hash Table", "String"]
        },
        {
            "id": 71,
            "title": "Alien Dictionary",
            "difficulty": "Hard",
            "description": """There is a new alien language that uses the English alphabet. However, the order of the letters is unknown to you.

You are given a list of strings `words` from the alien language's dictionary, where the strings are sorted lexicographically by the rules of this new language.

Return a string of the unique letters in the new alien language sorted in lexicographically increasing order by the new language's rules. If there is no solution, return "".

**Example 1:**
```
Input: words = ["wrt","wrf","er","ett","rftt"]
Output: "wertf"
```

**Example 2:**
```
Input: words = ["z","x"]
Output: "zx"
```

**Example 3:**
```
Input: words = ["z","x","z"]
Output: ""
Explanation: The order is invalid, so return "".
```""",
            "starter_code": """def alienOrder(words):
    # Write your solution here
    pass

# Test your solution
print(alienOrder(["wrt","wrf","er","ett","rftt"]))  # Expected: "wertf\"""",
            "solution": """def alienOrder(words):
    from collections import defaultdict, deque
    
    # Build adjacency list and in-degree count
    graph = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}
    
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        
        # Check for invalid case: prefix comes after word
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in graph[w1[j]]:
                    graph[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break
    
    # Topological sort
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []
    
    while queue:
        char = queue.popleft()
        result.append(char)
        for neighbor in graph[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return ''.join(result) if len(result) == len(in_degree) else ""

# Time Complexity: O(C) where C is total characters in all words
# Space Complexity: O(1) or O(U) where U is unique characters""",
            "hints": [
                "Build a directed graph from adjacent word comparisons",
                "Use topological sort to determine order",
                "Check for cycles (invalid ordering)"
            ],
            "test_cases": [
                {"input": {"words": ["wrt","wrf","er","ett","rftt"]}, "expected": "wertf"},
                {"input": {"words": ["z","x"]}, "expected": "zx"}
            ],
            "topics": ["Graph", "Topological Sort", "BFS"]
        },
        {
            "id": 72,
            "title": "N-Queens",
            "difficulty": "Hard",
            "description": """The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.

Given an integer `n`, return all distinct solutions to the n-queens puzzle.

Each solution contains a distinct board configuration where 'Q' indicates a queen and '.' indicates an empty space.

**Example 1:**
```
Input: n = 4
Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
```

**Example 2:**
```
Input: n = 1
Output: [["Q"]]
```""",
            "starter_code": """def solveNQueens(n):
    # Write your solution here
    pass

# Test your solution
print(solveNQueens(4))  # Expected: 2 solutions""",
            "solution": """def solveNQueens(n):
    result = []
    board = [['.'] * n for _ in range(n)]
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col
    
    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            backtrack(row + 1)
            
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    backtrack(0)
    return result

# Time Complexity: O(N!)
# Space Complexity: O(N)""",
            "hints": [
                "Use backtracking to place queens row by row",
                "Track attacked columns and diagonals with sets",
                "Diagonals can be identified by row-col and row+col"
            ],
            "test_cases": [
                {"input": {"n": 1}, "expected": [["Q"]]}
            ],
            "topics": ["Backtracking", "Array"]
        },
        {
            "id": 73,
            "title": "Sudoku Solver",
            "difficulty": "Hard",
            "description": """Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:
1. Each of the digits 1-9 must occur exactly once in each row.
2. Each of the digits 1-9 must occur exactly once in each column.
3. Each of the digits 1-9 must occur exactly once in each of the 9 3x3 sub-boxes.

The '.' character indicates empty cells.

**Example:**
```
Input: board = [["5","3",".",".","7",".",".",".","."],
                ["6",".",".","1","9","5",".",".","."],
                [".","9","8",".",".",".",".","6","."],
                ["8",".",".",".","6",".",".",".","3"],
                ["4",".",".","8",".","3",".",".","1"],
                ["7",".",".",".","2",".",".",".","6"],
                [".","6",".",".",".",".","2","8","."],
                [".",".",".","4","1","9",".",".","5"],
                [".",".",".",".","8",".",".","7","9"]]
Output: (solved board)
```""",
            "starter_code": """def solveSudoku(board):
    # Write your solution here - modify board in-place
    pass""",
            "solution": """def solveSudoku(board):
    def isValid(row, col, num):
        # Check row
        if num in board[row]:
            return False
        # Check column
        if num in [board[r][col] for r in range(9)]:
            return False
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False
        return True
    
    def solve():
        for row in range(9):
            for col in range(9):
                if board[row][col] == '.':
                    for num in '123456789':
                        if isValid(row, col, num):
                            board[row][col] = num
                            if solve():
                                return True
                            board[row][col] = '.'
                    return False
        return True
    
    solve()

# Time Complexity: O(9^(empty cells))
# Space Complexity: O(81) for recursion stack""",
            "hints": [
                "Use backtracking to try each number 1-9 in empty cells",
                "Check validity against row, column, and 3x3 box",
                "Backtrack when no valid number can be placed"
            ],
            "test_cases": [],
            "topics": ["Backtracking", "Array", "Matrix"]
        },
        {
            "id": 74,
            "title": "Merge k Sorted Lists",
            "difficulty": "Hard",
            "description": """You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

**Example 1:**
```
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
```

**Example 2:**
```
Input: lists = []
Output: []
```

**Example 3:**
```
Input: lists = [[]]
Output: []
```""",
            "starter_code": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists):
    # Write your solution here
    pass""",
            "solution": """def mergeKLists(lists):
    import heapq
    
    # Handle empty and equal comparison issues
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))
    
    dummy = ListNode()
    current = dummy
    
    while heap:
        val, i, node = heapq.heappop(heap)
        current.next = node
        current = current.next
        
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next

# Time Complexity: O(N log k) where N is total nodes, k is number of lists
# Space Complexity: O(k) for the heap""",
            "hints": [
                "Use a min-heap to efficiently find the smallest element",
                "Add the heads of all lists to the heap",
                "Pop minimum, add next node from that list to heap"
            ],
            "test_cases": [],
            "topics": ["Linked List", "Heap", "Divide and Conquer"]
        },
        {
            "id": 75,
            "title": "Serialize and Deserialize Binary Tree",
            "difficulty": "Hard",
            "description": """Design an algorithm to serialize and deserialize a binary tree. Serialization is converting a tree to a string so that it can be stored. Deserialization is reconstructing the tree from the string.

**Example 1:**
```
Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]
```

**Example 2:**
```
Input: root = []
Output: []
```""",
            "starter_code": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    def serialize(self, root):
        # Write your solution here
        pass

    def deserialize(self, data):
        # Write your solution here
        pass""",
            "solution": """class Codec:
    def serialize(self, root):
        def dfs(node):
            if not node:
                return ['null']
            return [str(node.val)] + dfs(node.left) + dfs(node.right)
        
        return ','.join(dfs(root))

    def deserialize(self, data):
        vals = iter(data.split(','))
        
        def dfs():
            val = next(vals)
            if val == 'null':
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node
        
        return dfs()

# Time Complexity: O(n)
# Space Complexity: O(n)""",
            "hints": [
                "Use preorder traversal for serialization",
                "Include null markers for missing children",
                "Use an iterator for deserialization"
            ],
            "test_cases": [],
            "topics": ["Tree", "DFS", "Design", "String"]
        }
    ]
}


def get_all_questions() -> List[Dict]:
    """Get all practice questions."""
    all_questions = []
    for difficulty in ["easy", "medium", "hard"]:
        for q in PRACTICE_QUESTIONS[difficulty]:
            all_questions.append({
                "id": q["id"],
                "title": q["title"],
                "difficulty": q["difficulty"],
                "topics": q["topics"]
            })
    return all_questions


def get_question_by_id(question_id: int) -> Optional[Dict]:
    """Get a specific question by ID."""
    for difficulty in ["easy", "medium", "hard"]:
        for q in PRACTICE_QUESTIONS[difficulty]:
            if q["id"] == question_id:
                return q
    return None


def get_questions_by_difficulty(difficulty: str) -> List[Dict]:
    """Get questions by difficulty level."""
    return PRACTICE_QUESTIONS.get(difficulty.lower(), [])


def get_hint(question_id: int, hint_index: int) -> Optional[str]:
    """Get a specific hint for a question."""
    question = get_question_by_id(question_id)
    if question and 0 <= hint_index < len(question["hints"]):
        return question["hints"][hint_index]
    return None


def check_solution(question_id: int, user_output: str) -> Dict:
    """
    Basic solution checker - compares user output format.
    In a real implementation, this would execute the code safely.
    """
    question = get_question_by_id(question_id)
    if not question:
        return {"correct": False, "message": "Question not found"}
    
    # For now, return the solution with explanation
    return {
        "correct": False,  # Would need code execution to verify
        "solution": question["solution"],
        "hints": question["hints"],
        "test_cases": question["test_cases"]
    }
