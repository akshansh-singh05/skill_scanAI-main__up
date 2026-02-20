"""
Company-Specific Interview Modes

Each company has a distinct interview style and focus areas.
This module provides question templates and configurations for different companies.
"""

from typing import Dict, List, Any

# Company configurations with interview styles
COMPANY_MODES = {
    "google": {
        "name": "Google",
        "logo": "🔍",
        "color": "#4285F4",
        "tagline": "Think Big, Code Smart",
        "focus_areas": ["DSA", "Problem Solving", "System Design", "Googleyness"],
        "style": "dsa_heavy",
        "description": "Heavy focus on Data Structures & Algorithms, optimization, and scalability",
        "interview_rounds": [
            {"name": "Phone Screen", "type": "coding", "duration": 45},
            {"name": "Onsite 1", "type": "dsa", "duration": 45},
            {"name": "Onsite 2", "type": "dsa", "duration": 45},
            {"name": "System Design", "type": "system_design", "duration": 45},
            {"name": "Googleyness & Leadership", "type": "behavioral", "duration": 45},
        ],
        "question_distribution": {
            "dsa": 0.50,
            "system_design": 0.20,
            "behavioral": 0.15,
            "coding": 0.15,
        },
        "tips": [
            "Think out loud and communicate your approach clearly",
            "Always analyze time and space complexity",
            "Consider edge cases before coding",
            "Optimize your solution iteratively",
            "Show enthusiasm for Google's products and mission",
        ],
    },
    
    "amazon": {
        "name": "Amazon",
        "logo": "📦",
        "color": "#FF9900",
        "tagline": "Leadership Principles First",
        "focus_areas": ["Leadership Principles", "Behavioral", "System Design", "Coding"],
        "style": "leadership_behavioral",
        "description": "Strong emphasis on Amazon's 16 Leadership Principles with STAR method responses",
        "interview_rounds": [
            {"name": "Phone Screen", "type": "coding", "duration": 45},
            {"name": "Loop 1 - LP Deep Dive", "type": "behavioral", "duration": 60},
            {"name": "Loop 2 - Technical", "type": "coding", "duration": 60},
            {"name": "Loop 3 - System Design", "type": "system_design", "duration": 60},
            {"name": "Bar Raiser", "type": "behavioral", "duration": 60},
        ],
        "question_distribution": {
            "behavioral": 0.45,
            "coding": 0.25,
            "system_design": 0.20,
            "dsa": 0.10,
        },
        "leadership_principles": [
            "Customer Obsession",
            "Ownership",
            "Invent and Simplify",
            "Are Right, A Lot",
            "Learn and Be Curious",
            "Hire and Develop the Best",
            "Insist on the Highest Standards",
            "Think Big",
            "Bias for Action",
            "Frugality",
            "Earn Trust",
            "Dive Deep",
            "Have Backbone; Disagree and Commit",
            "Deliver Results",
            "Strive to be Earth's Best Employer",
            "Success and Scale Bring Broad Responsibility",
        ],
        "tips": [
            "Prepare 2-3 stories for each Leadership Principle",
            "Use the STAR method (Situation, Task, Action, Result)",
            "Quantify your impact with metrics",
            "Show ownership and customer focus",
            "Be specific, not generic in your responses",
        ],
    },
    
    "meta": {
        "name": "Meta",
        "logo": "♾️",
        "color": "#0668E1",
        "tagline": "Move Fast, Build Things",
        "focus_areas": ["Coding", "System Design", "Product Sense", "Behavioral"],
        "style": "coding_systems",
        "description": "Balance of coding excellence and system design with focus on scale",
        "interview_rounds": [
            {"name": "Initial Screen", "type": "coding", "duration": 45},
            {"name": "Coding 1", "type": "coding", "duration": 45},
            {"name": "Coding 2", "type": "coding", "duration": 45},
            {"name": "System Design", "type": "system_design", "duration": 45},
            {"name": "Behavioral", "type": "behavioral", "duration": 45},
        ],
        "question_distribution": {
            "coding": 0.40,
            "system_design": 0.30,
            "behavioral": 0.15,
            "dsa": 0.15,
        },
        "tips": [
            "Write clean, production-ready code",
            "Think about edge cases and error handling",
            "Design for Meta's scale (billions of users)",
            "Show product intuition and user empathy",
            "Demonstrate ability to iterate quickly",
        ],
    },
    
    "microsoft": {
        "name": "Microsoft",
        "logo": "🪟",
        "color": "#00A4EF",
        "tagline": "Empower Every Person",
        "focus_areas": ["Coding", "System Design", "Problem Solving", "Growth Mindset"],
        "style": "balanced",
        "description": "Balanced approach with focus on growth mindset and collaboration",
        "interview_rounds": [
            {"name": "Phone Screen", "type": "coding", "duration": 45},
            {"name": "Onsite 1", "type": "coding", "duration": 60},
            {"name": "Onsite 2", "type": "system_design", "duration": 60},
            {"name": "Onsite 3", "type": "behavioral", "duration": 60},
            {"name": "As Appropriate (AA)", "type": "behavioral", "duration": 30},
        ],
        "question_distribution": {
            "coding": 0.35,
            "system_design": 0.25,
            "behavioral": 0.25,
            "dsa": 0.15,
        },
        "tips": [
            "Show growth mindset and learning attitude",
            "Demonstrate collaboration skills",
            "Explain your thought process clearly",
            "Ask clarifying questions",
            "Show passion for technology and impact",
        ],
    },
    
    "apple": {
        "name": "Apple",
        "logo": "🍎",
        "color": "#555555",
        "tagline": "Think Different",
        "focus_areas": ["Technical Excellence", "Design Thinking", "Attention to Detail", "Innovation"],
        "style": "technical_detail",
        "description": "Deep technical expertise with focus on quality and user experience",
        "interview_rounds": [
            {"name": "Phone Screen", "type": "coding", "duration": 45},
            {"name": "Technical 1", "type": "coding", "duration": 60},
            {"name": "Technical 2", "type": "system_design", "duration": 60},
            {"name": "Design Review", "type": "behavioral", "duration": 60},
            {"name": "Hiring Manager", "type": "behavioral", "duration": 45},
        ],
        "question_distribution": {
            "coding": 0.35,
            "system_design": 0.25,
            "behavioral": 0.20,
            "dsa": 0.20,
        },
        "tips": [
            "Pay attention to code quality and elegance",
            "Think about user experience implications",
            "Show passion for Apple products",
            "Demonstrate attention to detail",
            "Be prepared for deep technical discussions",
        ],
    },
    
    "generic": {
        "name": "General Practice",
        "logo": "💼",
        "color": "#6366F1",
        "tagline": "All-Round Preparation",
        "focus_areas": ["DSA", "System Design", "Behavioral", "Coding"],
        "style": "balanced",
        "description": "Balanced preparation covering all major interview topics",
        "interview_rounds": [
            {"name": "Technical Screen", "type": "coding", "duration": 45},
            {"name": "Technical Round", "type": "dsa", "duration": 45},
            {"name": "System Design", "type": "system_design", "duration": 45},
            {"name": "Behavioral", "type": "behavioral", "duration": 45},
        ],
        "question_distribution": {
            "dsa": 0.30,
            "coding": 0.25,
            "system_design": 0.25,
            "behavioral": 0.20,
        },
        "tips": [
            "Practice a variety of problem types",
            "Prepare behavioral stories using STAR method",
            "Study common system design patterns",
            "Work on communication skills",
            "Review fundamentals regularly",
        ],
    },
}


# Company-specific question banks
COMPANY_QUESTIONS = {
    "google": {
        "dsa": [
            {
                "question": "Given an array of integers, find two numbers that add up to a specific target. Optimize for time complexity.",
                "difficulty": "medium",
                "topics": ["arrays", "hash_tables", "optimization"],
                "follow_up": "What if the array is sorted? Can you do better than O(n) space?",
            },
            {
                "question": "Design an algorithm to find the kth largest element in an unsorted array. What's the most efficient approach?",
                "difficulty": "medium",
                "topics": ["heaps", "quickselect", "sorting"],
                "follow_up": "How would you handle streaming data?",
            },
            {
                "question": "Given a binary tree, return the level order traversal of its nodes' values. Then modify it to return zigzag order.",
                "difficulty": "medium",
                "topics": ["trees", "bfs", "queues"],
                "follow_up": "What about a very wide tree that doesn't fit in memory?",
            },
            {
                "question": "Implement a trie (prefix tree) with insert, search, and startsWith methods. Analyze the complexity.",
                "difficulty": "medium",
                "topics": ["tries", "strings", "trees"],
                "follow_up": "How would you implement autocomplete using this?",
            },
            {
                "question": "Find the longest substring without repeating characters. Optimize your solution step by step.",
                "difficulty": "medium",
                "topics": ["strings", "sliding_window", "hash_tables"],
                "follow_up": "What if we need the longest substring with at most k distinct characters?",
            },
        ],
        "system_design": [
            {
                "question": "Design Google Search's autocomplete system. Consider latency, scale, and personalization.",
                "difficulty": "hard",
                "topics": ["distributed_systems", "caching", "trie"],
            },
            {
                "question": "Design YouTube's video recommendation system. How would you handle billions of videos?",
                "difficulty": "hard",
                "topics": ["ml_systems", "distributed_systems", "caching"],
            },
            {
                "question": "Design Google Maps navigation system. Consider real-time traffic and route optimization.",
                "difficulty": "hard",
                "topics": ["graphs", "real_time", "geospatial"],
            },
        ],
        "behavioral": [
            {
                "question": "Tell me about a time you had to make a decision with incomplete information. How did you handle it?",
                "principle": "Googleyness",
            },
            {
                "question": "Describe a situation where you had to push back on a decision you disagreed with.",
                "principle": "Googleyness",
            },
            {
                "question": "Tell me about a complex technical problem you solved. Walk me through your approach.",
                "principle": "Problem Solving",
            },
        ],
    },
    
    "amazon": {
        "behavioral": [
            {
                "question": "Tell me about a time when you went above and beyond for a customer.",
                "principle": "Customer Obsession",
                "star_prompts": ["What was the situation?", "What did you do?", "What was the measurable impact?"],
            },
            {
                "question": "Describe a time when you took ownership of a project that was outside your scope.",
                "principle": "Ownership",
                "star_prompts": ["Why did you step up?", "What challenges did you face?", "What was the outcome?"],
            },
            {
                "question": "Tell me about a time you invented or simplified a process.",
                "principle": "Invent and Simplify",
                "star_prompts": ["What problem were you solving?", "What was your innovation?", "How did you measure success?"],
            },
            {
                "question": "Give me an example of when you had to make a difficult decision quickly.",
                "principle": "Bias for Action",
                "star_prompts": ["What was at stake?", "How did you decide?", "Would you do it differently?"],
            },
            {
                "question": "Tell me about a time you disagreed with your manager or team.",
                "principle": "Have Backbone; Disagree and Commit",
                "star_prompts": ["What was your position?", "How did you communicate it?", "What happened after?"],
            },
            {
                "question": "Describe a situation where you had to dive deep into data to solve a problem.",
                "principle": "Dive Deep",
                "star_prompts": ["What was the problem?", "What did you discover?", "How did it change your approach?"],
            },
            {
                "question": "Tell me about your most significant accomplishment. Why is it significant?",
                "principle": "Deliver Results",
                "star_prompts": ["What was the goal?", "What obstacles did you overcome?", "What was the impact?"],
            },
            {
                "question": "Give an example of when you had to learn something new quickly.",
                "principle": "Learn and Be Curious",
                "star_prompts": ["What did you need to learn?", "How did you approach it?", "How do you continue learning?"],
            },
        ],
        "coding": [
            {
                "question": "Implement an LRU Cache with O(1) get and put operations.",
                "difficulty": "medium",
                "topics": ["data_structures", "design"],
            },
            {
                "question": "Find the optimal path in a warehouse for a robot picking items.",
                "difficulty": "medium",
                "topics": ["graphs", "optimization"],
            },
        ],
        "system_design": [
            {
                "question": "Design Amazon's product recommendation system.",
                "difficulty": "hard",
                "topics": ["ml_systems", "personalization", "scale"],
            },
            {
                "question": "Design a real-time inventory management system for Amazon warehouses.",
                "difficulty": "hard",
                "topics": ["distributed_systems", "consistency", "real_time"],
            },
        ],
    },
    
    "meta": {
        "coding": [
            {
                "question": "Given a list of integers, return the number of valid subarrays. A subarray is valid if the sum of its elements is equal to its length.",
                "difficulty": "medium",
                "topics": ["arrays", "prefix_sum"],
            },
            {
                "question": "Implement a function to serialize and deserialize a binary tree.",
                "difficulty": "medium",
                "topics": ["trees", "serialization"],
            },
            {
                "question": "Find all possible combinations of phone number letters (like T9 texting).",
                "difficulty": "medium",
                "topics": ["recursion", "backtracking"],
            },
            {
                "question": "Given a 2D grid, find the shortest path from start to end avoiding obstacles.",
                "difficulty": "medium",
                "topics": ["graphs", "bfs"],
            },
            {
                "question": "Implement a basic regex matcher supporting '.' and '*' characters.",
                "difficulty": "hard",
                "topics": ["dynamic_programming", "strings"],
            },
        ],
        "system_design": [
            {
                "question": "Design Facebook News Feed. Consider ranking, personalization, and real-time updates.",
                "difficulty": "hard",
                "topics": ["ranking", "caching", "real_time"],
            },
            {
                "question": "Design Instagram Stories feature. Think about storage, delivery, and ephemeral content.",
                "difficulty": "hard",
                "topics": ["storage", "cdn", "ephemeral_data"],
            },
            {
                "question": "Design WhatsApp messaging system. Focus on message delivery guarantees and encryption.",
                "difficulty": "hard",
                "topics": ["messaging", "encryption", "distributed"],
            },
        ],
        "behavioral": [
            {
                "question": "Tell me about a time you shipped a product feature under tight deadlines. What tradeoffs did you make?",
                "principle": "Move Fast",
            },
            {
                "question": "Describe a situation where you had to balance multiple competing priorities.",
                "principle": "Focus on Impact",
            },
            {
                "question": "Tell me about a technical decision you made that you later regretted. What did you learn?",
                "principle": "Be Open",
            },
        ],
    },
}


def get_company_config(company: str) -> Dict[str, Any]:
    """Get configuration for a specific company."""
    return COMPANY_MODES.get(company.lower(), COMPANY_MODES["generic"])


def get_company_questions(company: str, question_type: str = None) -> List[Dict]:
    """Get questions for a specific company and type."""
    company_qs = COMPANY_QUESTIONS.get(company.lower(), COMPANY_QUESTIONS.get("google"))
    
    if question_type:
        return company_qs.get(question_type, [])
    
    return company_qs


def get_all_companies() -> List[Dict[str, Any]]:
    """Get list of all available company modes."""
    return [
        {
            "id": key,
            "name": config["name"],
            "logo": config["logo"],
            "color": config["color"],
            "tagline": config["tagline"],
            "description": config["description"],
            "focus_areas": config["focus_areas"],
        }
        for key, config in COMPANY_MODES.items()
    ]


def get_interview_strategy(company: str) -> Dict[str, Any]:
    """Get interview preparation strategy for a company."""
    config = get_company_config(company)
    
    return {
        "company": config["name"],
        "style": config["style"],
        "focus_areas": config["focus_areas"],
        "question_distribution": config["question_distribution"],
        "tips": config["tips"],
        "rounds": config["interview_rounds"],
    }
