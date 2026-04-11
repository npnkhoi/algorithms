
"""
Using regular expression to extract the last three digits of the user IDs from a document. The user IDs are in the format of [letter1][number1][letter2][number2]_[digit][digit][digit]. For example, a6y7_000, e2z9_230, n7u8_998, etc. Your program should take the input .txt file name as the command line argument and print the list of the last three digits of the user IDs. 

Run your program using the following command line:
python hw1_p1.py input.txt

An example input file can be found here.
For this example, your program should prinP1.2_input.txtt:
000
998

An example python regex program can be found here. 

When making the submission, name your file as hw1_p1.py. We will have more test cases other than this example; please try to test your program with more examples thoroughly. 

If you want to use other programming languages other than python, it’s acceptable as long as you use regular expressions to solve this problem. If you use other programming languages, please also submit a readme file to indicate how to run your program. 

Note: If you do not use regular expressions for this problem, you will receive a score of zero. 

"""

import re
import sys

if __name__ == "__main__":
    fn = sys.argv[1]
    with open(fn) as f:
        inp = f.read()
    
    pattern = r"((\w\d){2})\_(\d{3})"
    res = re.findall(pattern, inp)

    for x in res:
        print(x[2])
