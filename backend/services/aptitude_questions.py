"""
Aptitude & Situational Questions for Interview Practice

Includes:
1. Quantitative Aptitude (Math, Numbers, Percentages)
2. Logical Reasoning (Patterns, Sequences, Puzzles)
3. Situational Judgment (Case-based workplace scenarios)
4. Analytical Reasoning (Data interpretation)
"""

from typing import Dict, List, Optional
import random


# Quantitative Aptitude Questions
APTITUDE_QUESTIONS = {
    "quantitative": [
        {
            "id": "apt_q1",
            "title": "Profit & Loss Calculation",
            "category": "Quantitative",
            "difficulty": "Easy",
            "question": """A shopkeeper buys an article for ₹500 and sells it for ₹600. What is the profit percentage?""",
            "options": [
                "A) 15%",
                "B) 20%",
                "C) 25%",
                "D) 10%"
            ],
            "correct_answer": "B",
            "explanation": """Profit = Selling Price - Cost Price = ₹600 - ₹500 = ₹100
Profit % = (Profit / Cost Price) × 100 = (100/500) × 100 = 20%""",
            "topic": "Profit & Loss"
        },
        {
            "id": "apt_q2",
            "title": "Time & Work Problem",
            "category": "Quantitative",
            "difficulty": "Medium",
            "question": """A can complete a work in 12 days and B can complete the same work in 18 days. If they work together, in how many days will they complete the work?""",
            "options": [
                "A) 7.2 days",
                "B) 6.5 days",
                "C) 8 days",
                "D) 5 days"
            ],
            "correct_answer": "A",
            "explanation": """A's 1 day work = 1/12
B's 1 day work = 1/18
Together in 1 day = 1/12 + 1/18 = (3+2)/36 = 5/36
Total days = 36/5 = 7.2 days""",
            "topic": "Time & Work"
        },
        {
            "id": "apt_q3",
            "title": "Speed, Time & Distance",
            "category": "Quantitative",
            "difficulty": "Medium",
            "question": """A train travels 360 km in 4 hours. How much time will it take to travel 540 km at the same speed?""",
            "options": [
                "A) 5 hours",
                "B) 6 hours",
                "C) 7 hours",
                "D) 8 hours"
            ],
            "correct_answer": "B",
            "explanation": """Speed = Distance/Time = 360/4 = 90 km/hr
Time for 540 km = 540/90 = 6 hours""",
            "topic": "Speed & Distance"
        },
        {
            "id": "apt_q4",
            "title": "Percentage Calculation",
            "category": "Quantitative",
            "difficulty": "Easy",
            "question": """If a number is increased by 25% and then decreased by 20%, what is the net change?""",
            "options": [
                "A) No change",
                "B) 5% increase",
                "C) 5% decrease",
                "D) 10% increase"
            ],
            "correct_answer": "A",
            "explanation": """Let original = 100
After 25% increase = 125
After 20% decrease = 125 × 0.8 = 100
Net change = 0% (No change)""",
            "topic": "Percentages"
        },
        {
            "id": "apt_q5",
            "title": "Ratio & Proportion",
            "category": "Quantitative",
            "difficulty": "Medium",
            "question": """The ratio of ages of A and B is 3:5. After 5 years, their ratio becomes 4:6. What is A's current age?""",
            "options": [
                "A) 12 years",
                "B) 15 years",
                "C) 18 years",
                "D) 20 years"
            ],
            "correct_answer": "B",
            "explanation": """Let A = 3x, B = 5x
After 5 years: (3x+5)/(5x+5) = 4/6 = 2/3
3(3x+5) = 2(5x+5)
9x + 15 = 10x + 10
x = 5
A's age = 3 × 5 = 15 years""",
            "topic": "Ratio & Proportion"
        },
        {
            "id": "apt_q6",
            "title": "Simple Interest",
            "category": "Quantitative",
            "difficulty": "Easy",
            "question": """Find the simple interest on ₹5000 at 8% per annum for 3 years.""",
            "options": [
                "A) ₹1000",
                "B) ₹1200",
                "C) ₹1500",
                "D) ₹800"
            ],
            "correct_answer": "B",
            "explanation": """SI = (P × R × T) / 100
SI = (5000 × 8 × 3) / 100 = ₹1200""",
            "topic": "Interest"
        },
        {
            "id": "apt_q7",
            "title": "Average Calculation",
            "category": "Quantitative",
            "difficulty": "Easy",
            "question": """The average of 5 numbers is 20. If one number is excluded, the average becomes 18. What is the excluded number?""",
            "options": [
                "A) 25",
                "B) 28",
                "C) 30",
                "D) 32"
            ],
            "correct_answer": "B",
            "explanation": """Sum of 5 numbers = 5 × 20 = 100
Sum of 4 numbers = 4 × 18 = 72
Excluded number = 100 - 72 = 28""",
            "topic": "Averages"
        },
        {
            "id": "apt_q8",
            "title": "Compound Interest",
            "category": "Quantitative",
            "difficulty": "Hard",
            "question": """What is the compound interest on ₹10,000 at 10% per annum for 2 years, compounded annually?""",
            "options": [
                "A) ₹2000",
                "B) ₹2100",
                "C) ₹2200",
                "D) ₹1900"
            ],
            "correct_answer": "B",
            "explanation": """A = P(1 + R/100)^n
A = 10000(1 + 10/100)² = 10000 × 1.21 = ₹12100
CI = A - P = 12100 - 10000 = ₹2100""",
            "topic": "Interest"
        },
        {
            "id": "apt_q9",
            "title": "Mixture Problem",
            "category": "Quantitative",
            "difficulty": "Medium",
            "question": """A container has 60 liters of milk. 6 liters of milk is taken out and replaced with water. This process is repeated once more. What is the amount of milk left?""",
            "options": [
                "A) 48.6 liters",
                "B) 48 liters",
                "C) 50 liters",
                "D) 45 liters"
            ],
            "correct_answer": "A",
            "explanation": """After first replacement: Milk = 60 - 6 = 54 liters
After second replacement: Milk = 54 × (54/60) = 54 × 0.9 = 48.6 liters
Formula: Final = Initial × (1 - replaced/total)^n = 60 × (1 - 6/60)² = 60 × 0.81 = 48.6""",
            "topic": "Mixtures"
        },
        {
            "id": "apt_q10",
            "title": "Partnership Problem",
            "category": "Quantitative",
            "difficulty": "Medium",
            "question": """A and B start a business with ₹50,000 and ₹30,000 respectively. After 6 months, C joins with ₹40,000. At the end of the year, total profit is ₹37,500. What is C's share?""",
            "options": [
                "A) ₹7,500",
                "B) ₹10,000",
                "C) ₹12,500",
                "D) ₹15,000"
            ],
            "correct_answer": "A",
            "explanation": """Ratio of investments (considering time):
A = 50,000 × 12 = 6,00,000
B = 30,000 × 12 = 3,60,000
C = 40,000 × 6 = 2,40,000
Ratio = 600:360:240 = 5:3:2
C's share = (2/10) × 37,500 = ₹7,500""",
            "topic": "Partnership"
        },
        {
            "id": "apt_q11",
            "title": "Pipes & Cisterns",
            "category": "Quantitative",
            "difficulty": "Medium",
            "question": """Pipe A can fill a tank in 12 hours, Pipe B in 15 hours. Pipe C can empty it in 20 hours. If all three are opened, how long to fill the tank?""",
            "options": [
                "A) 8 hours",
                "B) 10 hours",
                "C) 12 hours",
                "D) 15 hours"
            ],
            "correct_answer": "B",
            "explanation": """Work done per hour:
A fills = 1/12
B fills = 1/15
C empties = 1/20
Net = 1/12 + 1/15 - 1/20 = (5 + 4 - 3)/60 = 6/60 = 1/10
Time to fill = 10 hours""",
            "topic": "Pipes & Cisterns"
        },
        {
            "id": "apt_q12",
            "title": "Permutation",
            "category": "Quantitative",
            "difficulty": "Hard",
            "question": """In how many ways can the letters of 'LEADER' be arranged?""",
            "options": [
                "A) 720",
                "B) 360",
                "C) 180",
                "D) 240"
            ],
            "correct_answer": "B",
            "explanation": """LEADER has 6 letters with E appearing twice.
Total arrangements = 6!/2! = 720/2 = 360""",
            "topic": "Permutation & Combination"
        },
        {
            "id": "apt_q13",
            "title": "Probability",
            "category": "Quantitative",
            "difficulty": "Medium",
            "question": """Two dice are thrown. What is the probability of getting a sum of 7?""",
            "options": [
                "A) 1/6",
                "B) 5/36",
                "C) 7/36",
                "D) 1/9"
            ],
            "correct_answer": "A",
            "explanation": """Total outcomes = 6 × 6 = 36
Favorable outcomes for sum 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6
Probability = 6/36 = 1/6""",
            "topic": "Probability"
        },
        {
            "id": "apt_q14",
            "title": "Boats & Streams",
            "category": "Quantitative",
            "difficulty": "Medium",
            "question": """A boat goes 24 km upstream in 6 hours and 24 km downstream in 4 hours. Find the speed of the stream.""",
            "options": [
                "A) 1 km/hr",
                "B) 2 km/hr",
                "C) 1.5 km/hr",
                "D) 2.5 km/hr"
            ],
            "correct_answer": "A",
            "explanation": """Upstream speed = 24/6 = 4 km/hr
Downstream speed = 24/4 = 6 km/hr
Speed of stream = (Downstream - Upstream)/2 = (6-4)/2 = 1 km/hr""",
            "topic": "Boats & Streams"
        },
        {
            "id": "apt_q15",
            "title": "LCM & HCF",
            "category": "Quantitative",
            "difficulty": "Easy",
            "question": """The LCM of two numbers is 180 and their HCF is 6. If one number is 36, find the other.""",
            "options": [
                "A) 25",
                "B) 30",
                "C) 35",
                "D) 40"
            ],
            "correct_answer": "B",
            "explanation": """Product of numbers = LCM × HCF
36 × Other = 180 × 6 = 1080
Other number = 1080/36 = 30""",
            "topic": "LCM & HCF"
        },
        {
            "id": "apt_q16",
            "title": "Age Problem",
            "category": "Quantitative",
            "difficulty": "Easy",
            "question": """Father's age is 3 times his son's age. 10 years ago, father was 5 times as old as his son. What is the father's current age?""",
            "options": [
                "A) 45 years",
                "B) 60 years",
                "C) 50 years",
                "D) 55 years"
            ],
            "correct_answer": "B",
            "explanation": """Let son's age = x, Father's age = 3x
10 years ago: (3x-10) = 5(x-10)
3x - 10 = 5x - 50
40 = 2x → x = 20
Father's age = 3 × 20 = 60 years""",
            "topic": "Age Problems"
        },
    ],
    "logical": [
        {
            "id": "apt_l1",
            "title": "Number Series",
            "category": "Logical Reasoning",
            "difficulty": "Easy",
            "question": """Find the next number in the series: 2, 6, 12, 20, 30, ?""",
            "options": [
                "A) 40",
                "B) 42",
                "C) 44",
                "D) 38"
            ],
            "correct_answer": "B",
            "explanation": """Pattern: Differences are 4, 6, 8, 10, 12...
2 → 6 (+4)
6 → 12 (+6)
12 → 20 (+8)
20 → 30 (+10)
30 → 42 (+12)
Answer: 42""",
            "topic": "Number Series"
        },
        {
            "id": "apt_l2",
            "title": "Letter Series",
            "category": "Logical Reasoning",
            "difficulty": "Medium",
            "question": """Find the next letter in the series: A, C, F, J, O, ?""",
            "options": [
                "A) T",
                "B) U",
                "C) V",
                "D) S"
            ],
            "correct_answer": "B",
            "explanation": """Pattern: +2, +3, +4, +5, +6
A → C (+2)
C → F (+3)
F → J (+4)
J → O (+5)
O → U (+6)
Answer: U""",
            "topic": "Letter Series"
        },
        {
            "id": "apt_l3",
            "title": "Blood Relations",
            "category": "Logical Reasoning",
            "difficulty": "Medium",
            "question": """Pointing to a photograph, Rahul says, "She is the daughter of my grandfather's only son." How is the person in the photograph related to Rahul?""",
            "options": [
                "A) Daughter",
                "B) Sister",
                "C) Mother",
                "D) Aunt"
            ],
            "correct_answer": "B",
            "explanation": """Grandfather's only son = Rahul's father
Daughter of Rahul's father = Rahul's sister
Answer: Sister""",
            "topic": "Blood Relations"
        },
        {
            "id": "apt_l4",
            "title": "Direction Sense",
            "category": "Logical Reasoning",
            "difficulty": "Easy",
            "question": """A man walks 5 km North, then 3 km East, then 5 km South. How far is he from the starting point?""",
            "options": [
                "A) 3 km",
                "B) 5 km",
                "C) 8 km",
                "D) 13 km"
            ],
            "correct_answer": "A",
            "explanation": """North 5 km + South 5 km = 0 (back to same line)
Only East 3 km remains.
Distance from start = 3 km""",
            "topic": "Direction Sense"
        },
        {
            "id": "apt_l5",
            "title": "Coding-Decoding",
            "category": "Logical Reasoning",
            "difficulty": "Medium",
            "question": """If COMPUTER is coded as RFUVQNPC, how is LAPTOP coded?""",
            "options": [
                "A) QPUQBM",
                "B) MBQUPQ",
                "C) QPUBML",
                "D) POTPAL"
            ],
            "correct_answer": "B",
            "explanation": """Pattern: Reverse the word, then +1 to each letter
COMPUTER → RETUPMOC → +1 → RFUVQNPC
LAPTOP → POTPAL → +1 → QPUQBM... wait let me recalculate.
Actually: Each letter +1, then reverse.
L+1=M, A+1=B, P+1=Q, T+1=U, O+1=P, P+1=Q
MBQUPQ reversed = QPUQBM
Answer: MBQUPQ (not reversed)""",
            "topic": "Coding-Decoding"
        },
        {
            "id": "apt_l6",
            "title": "Syllogism",
            "category": "Logical Reasoning",
            "difficulty": "Medium",
            "question": """Statements:
All cats are dogs.
All dogs are animals.

Conclusions:
I. All cats are animals.
II. All animals are cats.

Which conclusion follows?""",
            "options": [
                "A) Only I follows",
                "B) Only II follows",
                "C) Both I and II follow",
                "D) Neither follows"
            ],
            "correct_answer": "A",
            "explanation": """From the statements:
Cats ⊂ Dogs ⊂ Animals
So all cats are indeed animals (I is correct)
But not all animals are cats (II is wrong)
Answer: Only I follows""",
            "topic": "Syllogism"
        },
        {
            "id": "apt_l7",
            "title": "Clock Problem",
            "category": "Logical Reasoning",
            "difficulty": "Hard",
            "question": """At what time between 3 and 4 o'clock will the hands of a clock be at right angles?""",
            "options": [
                "A) 3:32 8/11 min",
                "B) 3:30 min",
                "C) 3:35 min",
                "D) 3:28 min"
            ],
            "correct_answer": "A",
            "explanation": """At 3 o'clock, minute hand is at 12, hour hand at 3 (90° apart).
For right angle: hands need to be 90° apart.
Speed of minute hand = 6°/min
Speed of hour hand = 0.5°/min
Relative speed = 5.5°/min
At 3, they're at 90°. For next right angle:
Time = (90 + 90) / 5.5 = 180/5.5 = 32 8/11 minutes
Answer: 3:32 8/11 minutes""",
            "topic": "Clocks"
        },
        {
            "id": "apt_l8",
            "title": "Seating Arrangement",
            "category": "Logical Reasoning",
            "difficulty": "Hard",
            "question": """Six people A, B, C, D, E, F sit in a row. B sits next to D. E is not adjacent to F. A sits at one end. C is not adjacent to B. Who sits in the middle?""",
            "options": [
                "A) B and D",
                "B) C and E",
                "C) D and E",
                "D) B and C"
            ],
            "correct_answer": "A",
            "explanation": """A is at one end. B-D must be adjacent.
C is not next to B.
E is not next to F.
Possible: A _ _ B D _ or A _ _ D B _
With constraints: A F E B D C or A C D B E F
Middle positions: B and D""",
            "topic": "Seating Arrangement"
        },
        {
            "id": "apt_l9",
            "title": "Odd One Out",
            "category": "Logical Reasoning",
            "difficulty": "Easy",
            "question": """Find the odd one out: 125, 343, 512, 729, 1__(27)__""",
            "options": [
                "A) 125",
                "B) 343",
                "C) 512",
                "D) 729"
            ],
            "correct_answer": "C",
            "explanation": """125 = 5³, 343 = 7³, 729 = 9³ (all odd number cubes)
512 = 8³ (even number cube)
512 is the odd one out.""",
            "topic": "Odd One Out"
        },
        {
            "id": "apt_l10",
            "title": "Analogy",
            "category": "Logical Reasoning",
            "difficulty": "Easy",
            "question": """DOCTOR : HOSPITAL :: TEACHER : ?""",
            "options": [
                "A) College",
                "B) School",
                "C) Student",
                "D) Book"
            ],
            "correct_answer": "B",
            "explanation": """Doctor works in Hospital.
Similarly, Teacher works in School.
Answer: School""",
            "topic": "Analogy"
        },
        {
            "id": "apt_l11",
            "title": "Calendar Problem",
            "category": "Logical Reasoning",
            "difficulty": "Medium",
            "question": """If January 1, 2024 is Monday, what day is March 15, 2024?""",
            "options": [
                "A) Thursday",
                "B) Friday",
                "C) Saturday",
                "D) Wednesday"
            ],
            "correct_answer": "B",
            "explanation": """January has 31 days (31 - 1 = 30 days after Jan 1)
February 2024 has 29 days (leap year)
March 15 = 15 days
Total days = 30 + 29 + 15 = 74 days
74 ÷ 7 = 10 weeks + 4 days
Monday + 4 = Friday""",
            "topic": "Calendar"
        },
        {
            "id": "apt_l12",
            "title": "Cube & Dice",
            "category": "Logical Reasoning",
            "difficulty": "Hard",
            "question": """A cube has six faces with numbers 1-6. If 1 is opposite to 4, 2 is opposite to 5, and when 3 is on top with 1 facing you, what number is at the bottom?""",
            "options": [
                "A) 1",
                "B) 2",
                "C) 5",
                "D) 6"
            ],
            "correct_answer": "D",
            "explanation": """3 is on top, so 6 is at bottom (opposite to 3).
Given: 1 opposite 4, 2 opposite 5
So 3 must be opposite 6.
Answer: 6 is at the bottom.""",
            "topic": "Cube & Dice"
        },
        {
            "id": "apt_l13",
            "title": "Statement & Assumption",
            "category": "Logical Reasoning",
            "difficulty": "Medium",
            "question": """Statement: "All employees must carry ID cards inside the office premises."
Assumptions:
I. Some employees do not carry ID cards.
II. ID cards help in identification.

Which assumption is implicit?""",
            "options": [
                "A) Only I",
                "B) Only II",
                "C) Both I and II",
                "D) Neither"
            ],
            "correct_answer": "B",
            "explanation": """The statement implies that ID cards are useful for identification (II is implicit).
The statement doesn't assume people weren't carrying cards before - it's setting a rule (I is not necessarily implicit).
Answer: Only II""",
            "topic": "Statement & Assumption"
        },
        {
            "id": "apt_l14",
            "title": "Ranking",
            "category": "Logical Reasoning",
            "difficulty": "Easy",
            "question": """In a class of 40 students, Rahul is 15th from the top. What is his rank from the bottom?""",
            "options": [
                "A) 25th",
                "B) 26th",
                "C) 24th",
                "D) 27th"
            ],
            "correct_answer": "B",
            "explanation": """Rank from bottom = Total students - Rank from top + 1
= 40 - 15 + 1 = 26th""",
            "topic": "Ranking"
        },
        {
            "id": "apt_l15",
            "title": "Venn Diagram",
            "category": "Logical Reasoning",
            "difficulty": "Medium",
            "question": """In a survey of 100 people: 60 like tea, 50 like coffee, 30 like both. How many like neither?""",
            "options": [
                "A) 10",
                "B) 15",
                "C) 20",
                "D) 25"
            ],
            "correct_answer": "C",
            "explanation": """Using inclusion-exclusion:
Tea OR Coffee = Tea + Coffee - Both = 60 + 50 - 30 = 80
Neither = Total - (Tea OR Coffee) = 100 - 80 = 20""",
            "topic": "Venn Diagrams"
        },
    ],
    "data_interpretation": [
        {
            "id": "apt_d1",
            "title": "Bar Graph Analysis",
            "category": "Data Interpretation",
            "difficulty": "Medium",
            "question": """A company's revenue (in crores) for 5 years:
2019: 50, 2020: 45, 2021: 60, 2022: 75, 2023: 90

What is the percentage increase in revenue from 2020 to 2023?""",
            "options": [
                "A) 80%",
                "B) 100%",
                "C) 90%",
                "D) 75%"
            ],
            "correct_answer": "B",
            "explanation": """Increase = 90 - 45 = 45 crores
Percentage increase = (45/45) × 100 = 100%""",
            "topic": "Bar Graphs"
        },
        {
            "id": "apt_d2",
            "title": "Pie Chart Analysis",
            "category": "Data Interpretation",
            "difficulty": "Medium",
            "question": """In a class of 200 students, the distribution of hobbies is:
Music: 25%, Sports: 30%, Reading: 20%, Gaming: 15%, Others: 10%

How many students have Sports or Gaming as hobby?""",
            "options": [
                "A) 80",
                "B) 90",
                "C) 100",
                "D) 85"
            ],
            "correct_answer": "B",
            "explanation": """Sports + Gaming = 30% + 15% = 45%
Number of students = 45% of 200 = 90 students""",
            "topic": "Pie Charts"
        },
        {
            "id": "apt_d3",
            "title": "Table Analysis",
            "category": "Data Interpretation",
            "difficulty": "Medium",
            "question": """Sales data (in units):
Product A: Q1=100, Q2=150, Q3=120, Q4=180
Product B: Q1=80, Q2=90, Q3=110, Q4=120

What is the ratio of total sales of Product A to Product B?""",
            "options": [
                "A) 11:8",
                "B) 55:40",
                "C) 3:2",
                "D) 13:10"
            ],
            "correct_answer": "A",
            "explanation": """Product A total = 100 + 150 + 120 + 180 = 550
Product B total = 80 + 90 + 110 + 120 = 400
Ratio = 550:400 = 55:40 = 11:8""",
            "topic": "Tables"
        },
        {
            "id": "apt_d4",
            "title": "Line Graph Trend",
            "category": "Data Interpretation",
            "difficulty": "Hard",
            "question": """Temperature readings over a week (°C):
Mon: 25, Tue: 28, Wed: 30, Thu: 27, Fri: 32, Sat: 29, Sun: 31

On how many days was the temperature above the week's average?""",
            "options": [
                "A) 3 days",
                "B) 4 days",
                "C) 5 days",
                "D) 2 days"
            ],
            "correct_answer": "B",
            "explanation": """Average = (25+28+30+27+32+29+31)/7 = 202/7 ≈ 28.86°C
Days above average: Wed(30), Fri(32), Sat(29), Sun(31) = 4 days""",
            "topic": "Line Graphs"
        },
        {
            "id": "apt_d5",
            "title": "Mixed Chart Analysis",
            "category": "Data Interpretation",
            "difficulty": "Hard",
            "question": """Employee distribution in departments:
IT: 120 (40% male), HR: 60 (50% male), Finance: 80 (25% male), Marketing: 40 (60% male)

What percentage of total employees are female?""",
            "options": [
                "A) 55%",
                "B) 58%",
                "C) 60%",
                "D) 52%"
            ],
            "correct_answer": "B",
            "explanation": """Total employees = 120 + 60 + 80 + 40 = 300
Female: IT = 72, HR = 30, Finance = 60, Marketing = 16 = 178
Percentage = (178/300) × 100 = 59.33% ≈ 58%""",
            "topic": "Mixed Charts"
        },
        {
            "id": "apt_d6",
            "title": "Growth Rate",
            "category": "Data Interpretation",
            "difficulty": "Medium",
            "question": """Company profits (in lakhs): 2020: 50, 2021: 60, 2022: 78, 2023: 93.6

What is the CAGR (Compound Annual Growth Rate) approximately?""",
            "options": [
                "A) 20%",
                "B) 23%",
                "C) 25%",
                "D) 18%"
            ],
            "correct_answer": "B",
            "explanation": """CAGR = ((Final/Initial)^(1/n) - 1) × 100
= ((93.6/50)^(1/3) - 1) × 100
= (1.872^0.333 - 1) × 100
= (1.232 - 1) × 100 ≈ 23%""",
            "topic": "Growth Analysis"
        },
        {
            "id": "apt_d7",
            "title": "Comparative Analysis",
            "category": "Data Interpretation",
            "difficulty": "Easy",
            "question": """Marks of 5 students (out of 100):
Amit: 85, Priya: 92, Raj: 78, Sneha: 88, Vikram: 72

What is the median score?""",
            "options": [
                "A) 83",
                "B) 85",
                "C) 88",
                "D) 78"
            ],
            "correct_answer": "B",
            "explanation": """Arranging in order: 72, 78, 85, 88, 92
Middle value (3rd) = 85
Median = 85""",
            "topic": "Statistics"
        },
    ]
}


# Situational Judgment / Case-Based Questions
SITUATIONAL_QUESTIONS = [
    {
        "id": "sit_1",
        "title": "Deadline Conflict",
        "category": "Situational Judgment",
        "difficulty": "Medium",
        "scenario": """You are working on a critical project with a deadline tomorrow. Your manager assigns you an urgent task from a new client that also needs to be completed by tomorrow. Both tasks require at least 8 hours each, and you only have 10 hours available.""",
        "question": "What would be the BEST course of action?",
        "options": [
            "A) Work overtime to complete both tasks, even if it means working through the night",
            "B) Immediately inform your manager about the conflict and discuss prioritization or delegation options",
            "C) Focus on the original project since you committed to it first",
            "D) Complete the new client task first as it might bring more business"
        ],
        "best_answer": "B",
        "worst_answer": "A",
        "explanation": """The best approach is to communicate proactively with your manager. This allows for:
1. Proper prioritization based on business impact
2. Potential delegation of one task
3. Realistic deadline negotiation
4. No unrealistic promises to either party

Working overnight (A) leads to burnout and lower quality. Unilateral decisions (C, D) don't consider the full business context.""",
        "competencies": ["Communication", "Problem Solving", "Time Management"]
    },
    {
        "id": "sit_2",
        "title": "Team Conflict Resolution",
        "category": "Situational Judgment",
        "difficulty": "Medium",
        "scenario": """Two of your team members, Raj and Priya, have been arguing about the technical approach for a project. Raj wants to use technology A which he's experienced with, while Priya suggests technology B which is newer but better suited. Their conflict is affecting team morale and project progress.""",
        "question": "As the team lead, what should you do?",
        "options": [
            "A) Let them resolve it themselves as both are senior developers",
            "B) Make a quick decision yourself to end the conflict",
            "C) Arrange a meeting to evaluate both approaches objectively based on project requirements, then make a collaborative decision",
            "D) Escalate to your manager to avoid taking sides"
        ],
        "best_answer": "C",
        "worst_answer": "A",
        "explanation": """A structured, objective evaluation is best because:
1. Both team members feel heard
2. Decision is based on facts, not preferences
3. It models good conflict resolution
4. Team learns to evaluate options objectively

Avoiding (A) or escalating (D) shows poor leadership. Quick decisions (B) may miss important considerations.""",
        "competencies": ["Leadership", "Conflict Resolution", "Decision Making"]
    },
    {
        "id": "sit_3",
        "title": "Code Review Feedback",
        "category": "Situational Judgment",
        "difficulty": "Easy",
        "scenario": """During a code review, you notice that a senior developer has written code that works but violates the team's coding standards and contains potential security vulnerabilities.""",
        "question": "What is the most appropriate action?",
        "options": [
            "A) Approve the code anyway since they are senior and must know what they're doing",
            "B) Reject the code without explanation",
            "C) Privately message them to change the code before others notice",
            "D) Leave constructive comments in the review explaining the concerns with specific references to coding standards and security best practices"
        ],
        "best_answer": "D",
        "worst_answer": "A",
        "explanation": """Professional code reviews should be:
1. Constructive and educational
2. Based on objective standards
3. Transparent (visible to the team)
4. Respectful regardless of seniority

Option D maintains standards while being professional. Seniority (A) doesn't exempt anyone from standards. Rejection without explanation (B) isn't constructive.""",
        "competencies": ["Communication", "Technical Excellence", "Integrity"]
    },
    {
        "id": "sit_4",
        "title": "Production Bug",
        "category": "Situational Judgment",
        "difficulty": "Hard",
        "scenario": """Late Friday evening, you discover a critical bug in production that's affecting 20% of users. The bug was introduced by your code that was deployed yesterday. Your manager and most of the team have left for the weekend.""",
        "question": "What should you do FIRST?",
        "options": [
            "A) Wait until Monday to fix it properly with the full team",
            "B) Immediately alert your manager and on-call team member about the issue",
            "C) Quickly write a fix and deploy it yourself to resolve the issue",
            "D) Roll back to the previous version and go home"
        ],
        "best_answer": "B",
        "worst_answer": "A",
        "explanation": """The first step should always be communication:
1. Alert stakeholders immediately
2. On-call resources exist for such situations
3. Collaborative decisions prevent hasty mistakes
4. 20% of users affected is significant

Don't wait (A) as users are impacted. Don't deploy alone (C) without review. Rollback (D) might be needed but should be a team decision.""",
        "competencies": ["Accountability", "Communication", "Crisis Management"]
    },
    {
        "id": "sit_5",
        "title": "Credit for Work",
        "category": "Situational Judgment",
        "difficulty": "Medium",
        "scenario": """Your team lead presents a project idea to senior management that you had originally proposed in a team meeting. They receive significant praise, but don't mention your contribution.""",
        "question": "How would you handle this situation?",
        "options": [
            "A) Immediately interrupt during the presentation to clarify that it was your idea",
            "B) Complain to your colleagues about the situation",
            "C) Have a private, professional conversation with your team lead about receiving acknowledgment for your contributions",
            "D) Send an email to senior management directly, explaining that it was your idea"
        ],
        "best_answer": "C",
        "worst_answer": "A",
        "explanation": """A private, professional conversation is best because:
1. It addresses the issue directly with the person involved
2. Maintains professional relationships
3. Gives them a chance to correct the oversight
4. Avoids public confrontation

Public interruption (A) or going over their head (D) damages relationships. Complaining to others (B) doesn't solve the problem.""",
        "competencies": ["Communication", "Professionalism", "Assertiveness"]
    },
    {
        "id": "sit_6",
        "title": "Unrealistic Deadline",
        "category": "Situational Judgment",
        "difficulty": "Medium",
        "scenario": """Your manager commits to delivering a feature in 2 weeks to a client, without consulting the development team. After analysis, your team estimates it will take at least 4 weeks to complete properly.""",
        "question": "As the tech lead, what should you do?",
        "options": [
            "A) Tell the team to work overtime to meet the 2-week deadline",
            "B) Present the analysis to your manager with options: reduce scope for 2 weeks, or full scope in 4 weeks",
            "C) Start working and hope things go faster than estimated",
            "D) Tell the manager it's impossible and refuse to start"
        ],
        "best_answer": "B",
        "worst_answer": "C",
        "explanation": """Presenting options with clear trade-offs is professional because:
1. It provides data-driven alternatives
2. Respects the commitment while being realistic
3. Allows business to make informed decisions
4. Shows problem-solving mindset

Hoping for the best (C) usually fails. Refusing (D) isn't constructive. Forced overtime (A) affects quality and morale.""",
        "competencies": ["Negotiation", "Problem Solving", "Communication"]
    },
    {
        "id": "sit_7",
        "title": "Struggling Colleague",
        "category": "Situational Judgment",
        "difficulty": "Easy",
        "scenario": """A new team member is struggling with tasks and frequently asks you for help. While you want to support them, it's starting to affect your own deliverables.""",
        "question": "What's the best way to handle this?",
        "options": [
            "A) Stop helping them so you can focus on your work",
            "B) Keep helping them whenever they ask, even if your work suffers",
            "C) Set aside specific time slots for mentoring, help them become self-sufficient, and suggest additional resources",
            "D) Report them to your manager as underperforming"
        ],
        "best_answer": "C",
        "worst_answer": "D",
        "explanation": """Structured mentoring with boundaries is ideal:
1. Teaches them to be independent ("teach to fish")
2. Protects your deliverables
3. Shows teamwork and leadership
4. Provides sustainable support

Completely refusing (A) isn't collaborative. Overhelping (B) enables dependency. Reporting immediately (D) doesn't give them a chance to improve.""",
        "competencies": ["Mentoring", "Time Management", "Teamwork"]
    },
    {
        "id": "sit_8",
        "title": "Ethical Dilemma",
        "category": "Situational Judgment",
        "difficulty": "Hard",
        "scenario": """You discover that your company's mobile app is collecting user location data more frequently than disclosed in the privacy policy. This data is being used for targeted advertising without explicit user consent.""",
        "question": "What should you do?",
        "options": [
            "A) Ignore it as it's not your responsibility - you're just a developer",
            "B) Raise the concern through proper channels - first to your manager, then to compliance/legal if needed",
            "C) Post about it on social media to warn users",
            "D) Quietly fix the code to match the privacy policy without telling anyone"
        ],
        "best_answer": "B",
        "worst_answer": "A",
        "explanation": """Using proper internal channels first is appropriate because:
1. Gives the company chance to correct the issue
2. Protects users' rights properly
3. Shows integrity and responsibility
4. Follows professional and legal protocols

Ignoring (A) is unethical. Social media (C) may violate employment terms and doesn't give proper resolution. Silent fixes (D) don't address the policy issue.""",
        "competencies": ["Ethics", "Integrity", "Communication"]
    },
    {
        "id": "sit_9",
        "title": "Technology Decision",
        "category": "Situational Judgment",
        "difficulty": "Medium",
        "scenario": """Your company is about to choose between two technologies for a major project. Technology A is what the team knows well. Technology B is newer, better suited for the project, but has a learning curve. The CTO favors Technology A for faster delivery.""",
        "question": "As the senior developer, how would you contribute to this decision?",
        "options": [
            "A) Go with the CTO's decision without comment - they know best",
            "B) Prepare a detailed comparison document highlighting pros/cons, long-term maintenance costs, and present it objectively",
            "C) Insist on Technology B since it's technically superior",
            "D) Privately tell team members that the CTO is making a mistake"
        ],
        "best_answer": "B",
        "worst_answer": "D",
        "explanation": """Providing objective analysis empowers good decisions:
1. Respects hierarchy while contributing expertise
2. Documents trade-offs for everyone
3. Considers long-term implications
4. Allows informed final decision

Blind agreement (A) wastes your expertise. Insisting (C) ignores valid delivery concerns. Undermining (D) is unprofessional.""",
        "competencies": ["Technical Leadership", "Communication", "Strategic Thinking"]
    },
    {
        "id": "sit_10",
        "title": "Remote Team Challenge",
        "category": "Situational Judgment",
        "difficulty": "Medium",
        "scenario": """You're managing a distributed team across 3 time zones. One team member consistently misses meetings and delivers work late. When confronted, they mention they're dealing with personal issues but don't elaborate.""",
        "question": "How should you approach this?",
        "options": [
            "A) Issue a formal warning for performance issues",
            "B) Have a private, empathetic conversation to understand their situation and explore flexible arrangements while setting clear expectations",
            "C) Ignore their lateness since they mentioned personal issues",
            "D) Redistribute their work to other team members permanently"
        ],
        "best_answer": "B",
        "worst_answer": "A",
        "explanation": """Empathetic but structured approach works best:
1. Shows you care about the person
2. Maintains professional expectations
3. Explores solutions together
4. Documents the plan going forward

Immediate punishment (A) ignores context. Ignoring (C) affects the team unfairly. Permanent redistribution (D) is premature.""",
        "competencies": ["Empathy", "Performance Management", "Leadership"]
    },
    {
        "id": "sit_11",
        "title": "Client Pressure",
        "category": "Situational Judgment",
        "difficulty": "Hard",
        "scenario": """A major client is demanding a feature that would compromise user data security. They're threatening to cancel a ₹50 lakh contract if you don't comply. Your sales team is pressuring you to implement it.""",
        "question": "What should you do?",
        "options": [
            "A) Implement the feature since the client is paying",
            "B) Refuse outright and let sales handle the client",
            "C) Propose alternative solutions that meet the client's needs without compromising security, and escalate if needed",
            "D) Implement it but add extra logging to track any issues"
        ],
        "best_answer": "C",
        "worst_answer": "A",
        "explanation": """Security should never be compromised for revenue:
1. Propose alternatives that address the underlying need
2. Escalate to leadership with clear risk assessment
3. Document everything for compliance
4. Let leadership make final business decision

Compromising security (A, D) creates legal/reputational risk worth far more than ₹50L.""",
        "competencies": ["Ethics", "Negotiation", "Risk Management"]
    },
    {
        "id": "sit_12",
        "title": "Onboarding Failure",
        "category": "Situational Judgment",
        "difficulty": "Medium",
        "scenario": """A new employee who joined 3 months ago is still struggling to contribute. They received minimal onboarding due to team bandwidth issues. Other team members are starting to complain about carrying extra load.""",
        "question": "As their manager, how do you address this?",
        "options": [
            "A) Put them on a Performance Improvement Plan immediately",
            "B) Take responsibility for the onboarding gap, provide structured catch-up support, and set clear milestones",
            "C) Ask HR to find a better fit for them in another team",
            "D) Pair them with a senior developer permanently to supervise their work"
        ],
        "best_answer": "B",
        "worst_answer": "A",
        "explanation": """The manager should own the onboarding failure:
1. Acknowledge the process gap
2. Create a structured catch-up plan
3. Set clear, achievable milestones
4. Regular check-ins and feedback

PIP (A) is unfair when onboarding failed. Transfer (C) doesn't solve the problem. Permanent pairing (D) doesn't build independence.""",
        "competencies": ["Leadership", "Accountability", "Coaching"]
    },
    {
        "id": "sit_13",
        "title": "Feature Disagreement",
        "category": "Situational Judgment",
        "difficulty": "Medium",
        "scenario": """Product management wants to ship a feature that you believe has significant usability issues. You've raised concerns, but they're insisting because of market pressure. The feature won't cause harm but will likely frustrate users.""",
        "question": "How should you proceed?",
        "options": [
            "A) Refuse to build it until your concerns are addressed",
            "B) Build it without objection since product decisions aren't your responsibility",
            "C) Document your concerns in writing, propose A/B testing, and proceed with building while advocating for user research",
            "D) Build a better version secretly and present it later"
        ],
        "best_answer": "C",
        "worst_answer": "A",
        "explanation": """Document and advocate, but collaborate:
1. Put concerns in writing (creates record)
2. Propose data-driven validation (A/B testing)
3. Continue executing while advocating
4. Maintain professional relationship with product

Refusing (A) blocks the team. Silent compliance (B) abandons user advocacy. Secret work (D) undermines trust.""",
        "competencies": ["Collaboration", "User Advocacy", "Professionalism"]
    },
    {
        "id": "sit_14",
        "title": "Legacy System",
        "category": "Situational Judgment",
        "difficulty": "Easy",
        "scenario": """You've inherited a legacy codebase with no documentation, no tests, and spaghetti code. Management wants new features added quickly. You're the only developer who understands this system now.""",
        "question": "What's your approach?",
        "options": [
            "A) Refuse to add features until you rewrite the entire system",
            "B) Add features as fast as possible to meet deadlines, cleaning up later",
            "C) Propose a balanced approach: add features incrementally while documenting and adding tests to touched code",
            "D) Add all the features but warn management it will break eventually"
        ],
        "best_answer": "C",
        "worst_answer": "A",
        "explanation": """Boy Scout Rule - leave code better than you found it:
1. Add tests to code you modify
2. Document as you learn
3. Incremental improvements alongside features
4. Communicate technical debt to management

Blocking (A) isn't realistic. Speed without quality (B) adds debt. Just warnings (D) isn't proactive.""",
        "competencies": ["Technical Excellence", "Communication", "Pragmatism"]
    },
    {
        "id": "sit_15",
        "title": "Interview Bias",
        "category": "Situational Judgment",
        "difficulty": "Hard",
        "scenario": """During a hiring panel discussion, a senior colleague dismisses a candidate saying "they won't fit our culture" without citing specific technical or behavioral concerns. The candidate performed well technically.""",
        "question": "How should you respond?",
        "options": [
            "A) Stay quiet as the senior colleague has more experience",
            "B) Ask the colleague to elaborate on specific concerns that can be objectively evaluated",
            "C) Immediately report them to HR for bias",
            "D) Argue that the candidate should be hired regardless of culture fit"
        ],
        "best_answer": "B",
        "worst_answer": "A",
        "explanation": """Request specifics to ensure fair evaluation:
1. "Culture fit" can mask unconscious bias
2. Ask for concrete, observable concerns
3. Redirect to objective criteria
4. Everyone deserves fair evaluation

Staying silent (A) enables potential bias. Immediate reporting (C) escalates prematurely. Arguing (D) doesn't address the root issue.""",
        "competencies": ["Integrity", "Communication", "Fairness"]
    },
]


# Case Study Questions (More complex scenarios)
CASE_STUDY_QUESTIONS = [
    {
        "id": "case_1",
        "title": "System Design Decision",
        "category": "Case Study",
        "difficulty": "Hard",
        "scenario": """You're the tech lead for an e-commerce platform that handles 100,000 orders per day. The current monolithic architecture is causing deployment delays and scaling issues. Management wants a recommendation.

Current Issues:
- Deployment takes 4 hours and requires full app restart
- During sales events, the entire site slows down
- Database queries are taking longer as data grows
- Different teams step on each other's code

Options being considered:
A) Continue with monolith but add more servers
B) Complete rewrite to microservices (estimated 18 months)
C) Gradual extraction of high-impact services (start with Order & Payment)
D) Move to a serverless architecture""",
        "questions": [
            {
                "q": "Which approach would you recommend and why?",
                "key_points": [
                    "C is often the best balance - gradual migration reduces risk",
                    "Start with services causing most pain (Order, Payment)",
                    "Complete rewrite (B) is risky - 'second system syndrome'",
                    "Just adding servers (A) doesn't fix root cause",
                    "Serverless (D) might work for some components but not all"
                ]
            },
            {
                "q": "What would be your first 3 steps if you chose gradual extraction?",
                "key_points": [
                    "1. Identify bounded contexts and service boundaries",
                    "2. Set up CI/CD pipeline for independent deployments",
                    "3. Extract the highest-pain service first with proper APIs",
                    "4. Implement monitoring and observability",
                    "5. Create database-per-service strategy"
                ]
            }
        ],
        "topics": ["System Design", "Architecture", "Decision Making"]
    },
    {
        "id": "case_2",
        "title": "Product Launch Crisis",
        "category": "Case Study",
        "difficulty": "Hard",
        "scenario": """Your startup is scheduled to launch a new product in 2 days. During final testing, you discover:
1. A critical bug that causes data loss in 5% of cases
2. The payment integration fails intermittently (2% of transactions)
3. The mobile app crashes on older Android devices (affects 15% of target users)

Your CEO is under pressure from investors who expect the launch date. Marketing has already sent press releases. The team has been working overtime for weeks.""",
        "questions": [
            {
                "q": "What would you recommend to the CEO?",
                "key_points": [
                    "Data loss bug is non-negotiable - must be fixed",
                    "Delay launch by minimum time needed for critical fixes",
                    "Payment issues might be acceptable with fallback (manual processing)",
                    "Android issue could launch without older device support initially",
                    "Transparent communication with investors is better than failed launch"
                ]
            },
            {
                "q": "How would you communicate this to stakeholders?",
                "key_points": [
                    "Present data: 5% data loss = X customers affected = Y revenue loss + reputation damage",
                    "Offer options with trade-offs clearly outlined",
                    "Propose realistic new timeline",
                    "Suggest soft launch to limited users first",
                    "Have recovery plan ready"
                ]
            }
        ],
        "topics": ["Crisis Management", "Leadership", "Communication"]
    },
    {
        "id": "case_3",
        "title": "Team Scaling Challenge",
        "category": "Case Study",
        "difficulty": "Medium",
        "scenario": """Your engineering team of 5 needs to grow to 15 in 6 months to meet product roadmap. Current challenges:
- No documented coding standards
- Knowledge is siloed in individual developers
- No formal onboarding process
- CI/CD pipeline is fragile and only understood by one person

You have budget for hiring but need to ensure productivity doesn't drop during scaling.""",
        "questions": [
            {
                "q": "What infrastructure would you put in place before hiring?",
                "key_points": [
                    "Document coding standards and architecture decisions (ADRs)",
                    "Create comprehensive onboarding documentation",
                    "Set up pair programming and knowledge sharing sessions",
                    "Make CI/CD pipeline robust with documentation",
                    "Implement code review guidelines",
                    "Create mentorship program structure"
                ]
            },
            {
                "q": "How would you structure the hiring and onboarding?",
                "key_points": [
                    "Hire in cohorts (3-4 at a time) for easier onboarding",
                    "Each new hire gets a dedicated mentor/buddy",
                    "Start with experienced senior hires who can help train others",
                    "30-60-90 day plan for each new hire",
                    "Regular feedback loops and check-ins"
                ]
            }
        ],
        "topics": ["Team Building", "Leadership", "Process Improvement"]
    },
    {
        "id": "case_4",
        "title": "Technical Debt Crisis",
        "category": "Case Study",
        "difficulty": "Hard",
        "scenario": """Your 5-year-old codebase has accumulated significant technical debt:
- 40% code coverage (mostly happy path)
- Dependencies 3 major versions behind
- Security vulnerabilities reported by audit
- Average bug fix takes 2 days (was 4 hours initially)
- New developers take 3 months to become productive

Management wants 5 new features delivered this quarter. Your team of 8 engineers is already struggling with maintenance.""",
        "questions": [
            {
                "q": "How would you balance feature development with debt reduction?",
                "key_points": [
                    "Propose dedicated allocation: e.g., 70% features, 30% debt",
                    "Prioritize debt by business risk (security first)",
                    "Quantify cost of doing nothing (bugs, slowdown)",
                    "Link debt reduction to feature velocity improvement",
                    "Quick wins vs strategic improvements"
                ]
            },
            {
                "q": "How would you communicate the tech debt situation to non-technical stakeholders?",
                "key_points": [
                    "Use business language, not technical jargon",
                    "Show impact: 'bugs take 12x longer to fix than initially'",
                    "Present as investment with ROI, not 'cleanup'",
                    "Visualize with graphs: velocity decline over time",
                    "Propose measurable outcomes"
                ]
            }
        ],
        "topics": ["Technical Debt", "Communication", "Strategic Planning"]
    },
    {
        "id": "case_5",
        "title": "Startup Pivot Decision",
        "category": "Case Study",
        "difficulty": "Hard",
        "scenario": """Your B2B SaaS startup has:
- 50 paying customers, ₹80L ARR
- 18 months runway remaining
- Product-market fit is weak (high churn: 8%/month)
- Team: 12 engineers, 5 sales, 3 support

A major enterprise customer offers ₹2Cr/year if you pivot to solve their specific problem. This would mean:
- Abandoning current product direction
- Letting go of 40 existing customers
- 6-month development timeline
- Becoming essentially a single-customer company initially""",
        "questions": [
            {
                "q": "What factors would you consider in making this decision?",
                "key_points": [
                    "Current path sustainability (8% churn = unsustainable)",
                    "Enterprise customer stability and growth potential",
                    "Domain expertise applicability to other enterprises",
                    "Team capability for enterprise product",
                    "Contract terms and dependency risk",
                    "Exit opportunities in both scenarios"
                ]
            },
            {
                "q": "If you proceed with the pivot, how would you manage the transition?",
                "key_points": [
                    "Negotiate multi-year contract with enterprise",
                    "Communicate honestly with existing customers",
                    "Offer migration path or referrals",
                    "Retain key team members with new mission",
                    "Plan for expanding beyond single customer",
                    "Document learnings from v1"
                ]
            }
        ],
        "topics": ["Business Strategy", "Decision Making", "Change Management"]
    },
    {
        "id": "case_6",
        "title": "Production Incident Postmortem",
        "category": "Case Study",
        "difficulty": "Medium",
        "scenario": """A production incident caused 4-hour downtime:
- Root cause: Database migration script ran in production without staging test
- Junior developer ran the script, senior approved the PR
- No rollback plan was prepared
- Monitoring alerts were ignored for 30 minutes
- ₹25L estimated revenue loss

Management wants someone held accountable. The junior developer is worried about being fired.""",
        "questions": [
            {
                "q": "How would you conduct the postmortem?",
                "key_points": [
                    "Blameless postmortem culture",
                    "Focus on system failures, not individuals",
                    "Timeline reconstruction with all stakeholders",
                    "Identify contributing factors at each step",
                    "Generate actionable improvements",
                    "Share learnings company-wide"
                ]
            },
            {
                "q": "What process improvements would you recommend?",
                "key_points": [
                    "Mandatory staging deployment before production",
                    "Automated rollback scripts for migrations",
                    "Runbook for production deployments",
                    "Alert escalation procedures",
                    "Deployment freeze periods sensitivity",
                    "Junior-senior pairing for critical operations"
                ]
            }
        ],
        "topics": ["DevOps", "Process Improvement", "Leadership"]
    },
    {
        "id": "case_7",
        "title": "Competitive Threat",
        "category": "Case Study",
        "difficulty": "Medium",
        "scenario": """A well-funded competitor has launched a product similar to yours:
- They're offering 60% lower prices
- Their product has 80% of your features
- They have ₹500Cr in funding
- 3 of your customers are evaluating switching
- Your team is demoralized by the news

You have strong customer relationships and domain expertise they lack.""",
        "questions": [
            {
                "q": "What would be your immediate response strategy?",
                "key_points": [
                    "Reach out to at-risk customers proactively",
                    "Emphasize differentiation (support, expertise, features)",
                    "Consider loyalty pricing for key accounts",
                    "Rally team around competitive challenge",
                    "Accelerate development of differentiating features",
                    "Don't panic-discount across the board"
                ]
            },
            {
                "q": "What long-term strategy would you recommend?",
                "key_points": [
                    "Double down on customer success and relationships",
                    "Focus on features competitor can't easily copy",
                    "Build switching costs (integrations, data)",
                    "Consider moving upmarket (enterprise focus)",
                    "Community and ecosystem building",
                    "Potential partnership or acquisition conversations"
                ]
            }
        ],
        "topics": ["Competition", "Strategy", "Leadership"]
    },
    {
        "id": "case_8",
        "title": "Remote Team Performance",
        "category": "Case Study",
        "difficulty": "Medium",
        "scenario": """Post-pandemic, your company went fully remote. After 1 year:
- Productivity metrics are down 15%
- Employee satisfaction surveys show decline
- Junior developers report feeling isolated
- Cross-team collaboration has decreased
- Some senior employees want to return to office
- Others threaten to quit if forced back

Management is asking for your recommendation on workplace policy.""",
        "questions": [
            {
                "q": "How would you gather more information before making recommendations?",
                "key_points": [
                    "Survey with specific, actionable questions",
                    "1:1 interviews with representative sample",
                    "Analyze productivity by role/seniority",
                    "Benchmark against industry",
                    "Understand individual circumstances",
                    "Pilot test different arrangements"
                ]
            },
            {
                "q": "What workplace solutions would you consider?",
                "key_points": [
                    "Hybrid model with flexibility",
                    "Team-based decisions for collaboration days",
                    "Invest in remote collaboration tools",
                    "Structured mentorship for juniors",
                    "Regular in-person team events",
                    "Co-working allowances for those preferring office"
                ]
            }
        ],
        "topics": ["Remote Work", "HR", "Change Management"]
    }
]


def get_aptitude_questions(category: str = None, difficulty: str = None) -> List[Dict]:
    """Get aptitude questions, optionally filtered."""
    questions = []
    
    for cat_key, cat_questions in APTITUDE_QUESTIONS.items():
        for q in cat_questions:
            if category and q["category"].lower() != category.lower():
                continue
            if difficulty and q["difficulty"].lower() != difficulty.lower():
                continue
            questions.append(q)
    
    return questions


def get_situational_questions(difficulty: str = None) -> List[Dict]:
    """Get situational judgment questions, optionally filtered by difficulty."""
    if difficulty:
        return [q for q in SITUATIONAL_QUESTIONS if q["difficulty"].lower() == difficulty.lower()]
    return SITUATIONAL_QUESTIONS


def get_case_studies() -> List[Dict]:
    """Get all case study questions."""
    return CASE_STUDY_QUESTIONS


def check_aptitude_answer(question_id: str, answer: str) -> Dict:
    """Check if the aptitude answer is correct."""
    # Find the question
    for cat_questions in APTITUDE_QUESTIONS.values():
        for q in cat_questions:
            if q["id"] == question_id:
                is_correct = answer.upper() == q["correct_answer"].upper()
                return {
                    "correct": is_correct,
                    "correct_answer": q["correct_answer"],
                    "explanation": q["explanation"],
                    "topic": q.get("topic", "General")
                }
    
    return {"error": "Question not found"}


def check_situational_answer(question_id: str, answer: str) -> Dict:
    """Check situational judgment answer and provide feedback."""
    for q in SITUATIONAL_QUESTIONS:
        if q["id"] == question_id:
            user_answer = answer.upper()
            is_best = user_answer == q["best_answer"].upper()
            is_worst = user_answer == q["worst_answer"].upper()
            
            if is_best:
                score = 100
                feedback = "Excellent choice! This demonstrates strong professional judgment."
            elif is_worst:
                score = 0
                feedback = "This would not be the recommended approach in this situation."
            else:
                score = 50
                feedback = "This is acceptable but not the optimal response."
            
            return {
                "score": score,
                "best_answer": q["best_answer"],
                "worst_answer": q["worst_answer"],
                "explanation": q["explanation"],
                "competencies": q["competencies"],
                "feedback": feedback
            }
    
    return {"error": "Question not found"}


def get_random_aptitude_quiz(count: int = 10, categories: List[str] = None) -> List[Dict]:
    """Generate a random aptitude quiz."""
    all_questions = get_aptitude_questions()
    
    if categories:
        all_questions = [q for q in all_questions if q["category"].lower() in [c.lower() for c in categories]]
    
    if len(all_questions) <= count:
        return all_questions
    
    return random.sample(all_questions, count)


def get_random_situational_quiz(count: int = 5) -> List[Dict]:
    """Generate a random situational judgment quiz."""
    if len(SITUATIONAL_QUESTIONS) <= count:
        return SITUATIONAL_QUESTIONS
    
    return random.sample(SITUATIONAL_QUESTIONS, count)
