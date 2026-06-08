import json
from app import app, db
from models import Problem

PROBLEMS = [
    {
        'title':       'Two Sum',
        'difficulty':  'easy',
        'category':    'arrays',
        'description': '''Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- Only one valid answer exists.''',
        'examples': [
            {'input': 'nums = [2,7,11,15], target = 9', 'output': '[0,1]', 'explanation': 'nums[0] + nums[1] = 2 + 7 = 9'},
            {'input': 'nums = [3,2,4], target = 6',     'output': '[1,2]', 'explanation': 'nums[1] + nums[2] = 2 + 4 = 6'},
        ],
        'test_cases': [
            {'input': {'nums': [2,7,11,15], 'target': 9},  'expected': [0,1]},
            {'input': {'nums': [3,2,4],     'target': 6},  'expected': [1,2]},
            {'input': {'nums': [3,3],       'target': 6},  'expected': [0,1]},
            {'input': {'nums': [1,2,3,4],   'target': 7},  'expected': [2,3]},
        ]
    },
    {
        'title':       'Reverse a String',
        'difficulty':  'easy',
        'category':    'strings',
        'description': '''Write a function that reverses a string. The input string is given as an array of characters `s`.

You must do this by modifying the input array in-place with O(1) extra memory.

Constraints:
- 1 <= s.length <= 10^5
- s[i] is a printable ASCII character.''',
        'examples': [
            {'input': 's = ["h","e","l","l","o"]', 'output': '["o","l","l","e","h"]', 'explanation': 'Reversed in place'},
            {'input': 's = ["H","a","n","n","a","h"]', 'output': '["h","a","n","n","a","H"]', 'explanation': 'Reversed in place'},
        ],
        'test_cases': [
            {'input': {'s': ['h','e','l','l','o']},            'expected': ['o','l','l','e','h']},
            {'input': {'s': ['H','a','n','n','a','h']},        'expected': ['h','a','n','n','a','H']},
            {'input': {'s': ['a']},                            'expected': ['a']},
            {'input': {'s': ['a','b']},                        'expected': ['b','a']},
        ]
    },
    {
        'title':       'Valid Parentheses',
        'difficulty':  'easy',
        'category':    'stacks',
        'description': '''Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
- Open brackets must be closed by the same type of brackets.
- Open brackets must be closed in the correct order.
- Every close bracket has a corresponding open bracket of the same type.

Constraints:
- 1 <= s.length <= 10^4
- s consists of parentheses only.''',
        'examples': [
            {'input': 's = "()"',     'output': 'true',  'explanation': 'Simple matching pair'},
            {'input': 's = "()[]{}"', 'output': 'true',  'explanation': 'Multiple pairs'},
            {'input': 's = "(]"',     'output': 'false', 'explanation': 'Mismatched brackets'},
        ],
        'test_cases': [
            {'input': {'s': '()'},     'expected': True},
            {'input': {'s': '()[]{}'}, 'expected': True},
            {'input': {'s': '(]'},     'expected': False},
            {'input': {'s': '([)]'},   'expected': False},
            {'input': {'s': '{[]}'},   'expected': True},
        ]
    },
    {
        'title':       'Maximum Subarray',
        'difficulty':  'medium',
        'category':    'dynamic programming',
        'description': '''Given an integer array `nums`, find the subarray with the largest sum and return its sum.

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

Follow up: Can you solve this in O(n) time?''',
        'examples': [
            {'input': 'nums = [-2,1,-3,4,-1,2,1,-5,4]', 'output': '6',  'explanation': 'Subarray [4,-1,2,1] has the largest sum 6'},
            {'input': 'nums = [1]',                      'output': '1',  'explanation': 'Single element'},
            {'input': 'nums = [5,4,-1,7,8]',             'output': '23', 'explanation': 'Whole array is max subarray'},
        ],
        'test_cases': [
            {'input': {'nums': [-2,1,-3,4,-1,2,1,-5,4]}, 'expected': 6},
            {'input': {'nums': [1]},                      'expected': 1},
            {'input': {'nums': [5,4,-1,7,8]},             'expected': 23},
            {'input': {'nums': [-1,-2,-3]},               'expected': -1},
        ]
    },
    {
        'title':       'Climbing Stairs',
        'difficulty':  'easy',
        'category':    'dynamic programming',
        'description': '''You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Constraints:
- 1 <= n <= 45''',
        'examples': [
            {'input': 'n = 2', 'output': '2', 'explanation': '1+1 or 2'},
            {'input': 'n = 3', 'output': '3', 'explanation': '1+1+1, 1+2, or 2+1'},
        ],
        'test_cases': [
            {'input': {'n': 1},  'expected': 1},
            {'input': {'n': 2},  'expected': 2},
            {'input': {'n': 3},  'expected': 3},
            {'input': {'n': 5},  'expected': 8},
            {'input': {'n': 10}, 'expected': 89},
        ]
    },
    {
        'title':       'Binary Search',
        'difficulty':  'easy',
        'category':    'binary search',
        'description': '''Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search target in nums.

If target exists, return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

Constraints:
- 1 <= nums.length <= 10^4
- All integers in nums are unique.
- nums is sorted in ascending order.''',
        'examples': [
            {'input': 'nums = [-1,0,3,5,9,12], target = 9', 'output': '4', 'explanation': '9 exists at index 4'},
            {'input': 'nums = [-1,0,3,5,9,12], target = 2', 'output': '-1', 'explanation': '2 does not exist'},
        ],
        'test_cases': [
            {'input': {'nums': [-1,0,3,5,9,12], 'target': 9},  'expected': 4},
            {'input': {'nums': [-1,0,3,5,9,12], 'target': 2},  'expected': -1},
            {'input': {'nums': [5],              'target': 5},  'expected': 0},
            {'input': {'nums': [1,2,3,4,5],      'target': 1},  'expected': 0},
        ]
    },
    {
        'title':       'Merge Two Sorted Lists',
        'difficulty':  'easy',
        'category':    'linked lists',
        'description': '''You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

Note: For this problem, implement the merge logic as a function that accepts two lists and returns a merged sorted list (you can use Python lists instead of actual linked list nodes).

Constraints:
- The number of nodes in both lists is in the range [0, 50].
- -100 <= Node.val <= 100
- Both list1 and list2 are sorted in non-decreasing order.''',
        'examples': [
            {'input': 'list1 = [1,2,4], list2 = [1,3,4]', 'output': '[1,1,2,3,4,4]', 'explanation': 'Merged sorted list'},
            {'input': 'list1 = [], list2 = []',           'output': '[]',             'explanation': 'Both empty'},
        ],
        'test_cases': [
            {'input': {'list1': [1,2,4],  'list2': [1,3,4]}, 'expected': [1,1,2,3,4,4]},
            {'input': {'list1': [],       'list2': []},       'expected': []},
            {'input': {'list1': [],       'list2': [0]},      'expected': [0]},
            {'input': {'list1': [1,3,5],  'list2': [2,4,6]}, 'expected': [1,2,3,4,5,6]},
        ]
    },
    {
        'title':       'Number of Islands',
        'difficulty':  'medium',
        'category':    'graphs',
        'description': '''Given an m x n 2D binary grid `grid` which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are surrounded by water.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 300
- grid[i][j] is '0' or '1'.''',
        'examples': [
            {'input': 'grid = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]', 'output': '1', 'explanation': 'One large island'},
            {'input': 'grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]', 'output': '3', 'explanation': 'Three separate islands'},
        ],
        'test_cases': [
            {'input': {'grid': [['1','1','1','1','0'],['1','1','0','1','0'],['1','1','0','0','0'],['0','0','0','0','0']]}, 'expected': 1},
            {'input': {'grid': [['1','1','0','0','0'],['1','1','0','0','0'],['0','0','1','0','0'],['0','0','0','1','1']]}, 'expected': 3},
            {'input': {'grid': [['1']]},                                                                                   'expected': 1},
            {'input': {'grid': [['0']]},                                                                                   'expected': 0},
        ]
    },
    {
        'title':       'Fibonacci Number',
        'difficulty':  'easy',
        'category':    'recursion',
        'description': '''The Fibonacci numbers, commonly denoted F(n) form a sequence such that each number is the sum of the two preceding ones, starting from 0 and 1.

F(0) = 0, F(1) = 1
F(n) = F(n-1) + F(n-2), for n > 1

Given n, calculate F(n).

Constraints:
- 0 <= n <= 30''',
        'examples': [
            {'input': 'n = 2', 'output': '1', 'explanation': 'F(2) = F(1) + F(0) = 1 + 0 = 1'},
            {'input': 'n = 4', 'output': '3', 'explanation': 'F(4) = F(3) + F(2) = 2 + 1 = 3'},
        ],
        'test_cases': [
            {'input': {'n': 0},  'expected': 0},
            {'input': {'n': 1},  'expected': 1},
            {'input': {'n': 2},  'expected': 1},
            {'input': {'n': 5},  'expected': 5},
            {'input': {'n': 10}, 'expected': 55},
        ]
    },
    {
        'title':       'Longest Common Prefix',
        'difficulty':  'easy',
        'category':    'strings',
        'description': '''Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".

Constraints:
- 1 <= strs.length <= 200
- 0 <= strs[i].length <= 200
- strs[i] consists of only lowercase English letters.''',
        'examples': [
            {'input': 'strs = ["flower","flow","flight"]', 'output': '"fl"',  'explanation': 'Common prefix is "fl"'},
            {'input': 'strs = ["dog","racecar","car"]',    'output': '""',    'explanation': 'No common prefix'},
        ],
        'test_cases': [
            {'input': {'strs': ['flower','flow','flight']}, 'expected': 'fl'},
            {'input': {'strs': ['dog','racecar','car']},    'expected': ''},
            {'input': {'strs': ['a']},                      'expected': 'a'},
            {'input': {'strs': ['ab','a']},                 'expected': 'a'},
        ]
    },
]

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()
        for p in PROBLEMS:
            prob = Problem(
                title       = p['title'],
                difficulty  = p['difficulty'],
                category    = p['category'],
                description = p['description'],
                examples    = json.dumps(p['examples']),
                test_cases  = json.dumps(p['test_cases'])
            )
            db.session.add(prob)
        db.session.commit()
        print(f'✅ Seeded {len(PROBLEMS)} problems')

if __name__ == '__main__':
    seed()