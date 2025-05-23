import os
import json
import requests
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import time
import google.generativeai as genai

# Map religions to their numerical IDs for API calls
RELIGIONS = {
    "christianity": 1,
    "islam": 2,
    "hinduism": 3,
    "buddhism": 4,
    "judaism": 5,
    "sikhism": 6,
    "taoism": 7,
    "jainism": 8,
    "shintoism": 9,
    "zoroastrianism": 10,
    "bahai": 11,
    "confucianism": 12,
    "atheism": 13,
    "agnosticism": 14,
    "humanism": 15
}

# Map philosophical traditions to their numerical IDs
PHILOSOPHIES = {
    "stoicism": 1,
    "existentialism": 2,
    "nihilism": 3,
    "pragmatism": 4,
    "utilitarianism": 5,
    "hedonism": 6,
    "rationalism": 7,
    "empiricism": 8,
    "idealism": 9,
    "materialism": 10
}

# Map categories of spiritual questions
CATEGORIES = {
    "general": "General religious and spiritual information",
    "rituals": "Religious rituals and practices",
    "philosophy": "Philosophy and ethics",
    "life": "Life guidance and spirituality",
    "comparative": "Comparative religion and interfaith",
    "nonreligious": "Non-religious and secular perspectives",
    "history": "Historical and cultural context"
}

class SpiritualKnowledgeAPI:
    def __init__(self, api_key: str = None):
        """Initialize the Spiritual Knowledge API client.
        
        Args:
            api_key: API key for Google Generative AI (optional)
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Cache for responses to reduce API calls
        self.response_cache = {}
        self.cache_time = 24 * 60 * 60  # 24 hours in seconds

    def _get_cache_key(self, query_type: str, identifier: str, category: str = None) -> str:
        """Generate a cache key based on query parameters."""
        if category:
            return f"{query_type}-{identifier}-{category}"
        return f"{query_type}-{identifier}"

    def get_religious_information(self, 
                                 religion: str,
                                 category: str = "general",
                                 specific_query: str = None) -> Dict[str, Any]:
        """Get information about a specific religion.
        
        Args:
            religion: The religion to query (e.g., 'christianity', 'islam')
            category: Category of information (general, rituals, philosophy, etc.)
            specific_query: A specific question about the religion
            
        Returns:
            Dict containing the requested religious information
        """
        try:
            if not religion:
                raise ValueError('Religion identifier is required')
            
            religion = religion.lower()
            if religion not in RELIGIONS:
                return {
                    "status": "error",
                    "message": f"Unknown religion: {religion}. Available options are: {', '.join(RELIGIONS.keys())}"
                }
            
            # Check cache first
            cache_key = self._get_cache_key("religion", religion, category)
            if specific_query:
                cache_key += f"-{specific_query[:50]}"  # Use first 50 chars of query for cache key
                
            if cache_key in self.response_cache:
                cache_entry = self.response_cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.cache_time:
                    print(f"Using cached information for {religion}")
                    return cache_entry['data']
            
            # Construct the prompt for the generative model
            prompt = f"Provide accurate, respectful, and educational information about {religion.title()} "
            
            if category in CATEGORIES:
                prompt += f"focusing on {CATEGORIES[category]}. "
            else:
                prompt += "covering its core beliefs, practices, and principles. "
                
            if specific_query:
                prompt += f"Specifically address this question: {specific_query}"
            
            # Add instruction for structured response
            prompt += "\n\nPlease structure your response with these sections when applicable:\n"
            prompt += "1. Core Beliefs\n2. Key Practices\n3. Sacred Texts\n4. Historical Context\n5. Modern Interpretation"
            
            # Generate response using the AI model
            response = self.model.generate_content(prompt)
            
            # Process the response
            if hasattr(response, 'text'):
                content = response.text
            else:
                content = str(response)
                
            # Create structured result
            result = {
                "religion": religion,
                "category": category,
                "query": specific_query,
                "content": content,
                "sources": [
                    {"name": "Generated by AI based on scholarly sources", "reliability": "high"}
                ]
            }
            
            # Cache the result
            self.response_cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            return result
            
        except Exception as e:
            print(f"Error fetching information about {religion}: {str(e)}")
            return {
                "status": "error",
                "message": f"Error retrieving information: {str(e)}"
            }

    def get_philosophical_perspective(self, 
                                     philosophy: str,
                                     topic: str = None) -> Dict[str, Any]:
        """Get information about a philosophical perspective.
        
        Args:
            philosophy: The philosophical tradition (e.g., 'stoicism', 'existentialism')
            topic: A specific philosophical topic or question
            
        Returns:
            Dict containing the philosophical perspective
        """
        try:
            if not philosophy:
                raise ValueError('Philosophy identifier is required')
            
            philosophy = philosophy.lower()
            if philosophy not in PHILOSOPHIES:
                return {
                    "status": "error",
                    "message": f"Unknown philosophy: {philosophy}. Available options are: {', '.join(PHILOSOPHIES.keys())}"
                }
            
            # Check cache first
            cache_key = self._get_cache_key("philosophy", philosophy)
            if topic:
                cache_key += f"-{topic[:50]}"  # Use first 50 chars of topic for cache key
                
            if cache_key in self.response_cache:
                cache_entry = self.response_cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.cache_time:
                    print(f"Using cached information for {philosophy}")
                    return cache_entry['data']
            
            # Construct the prompt for the generative model
            prompt = f"Provide an educational explanation of {philosophy} philosophy "
            
            if topic:
                prompt += f"specifically addressing: {topic}. "
            else:
                prompt += "covering its key principles, notable thinkers, and practical applications. "
                
            # Add instruction for structured response
            prompt += "\n\nPlease structure your response with these sections:\n"
            prompt += "1. Core Principles\n2. Key Thinkers\n3. Historical Context\n4. Modern Relevance\n5. Practical Applications"
            
            # Generate response using the AI model
            response = self.model.generate_content(prompt)
            
            # Process the response
            if hasattr(response, 'text'):
                content = response.text
            else:
                content = str(response)
                
            # Create structured result
            result = {
                "philosophy": philosophy,
                "topic": topic,
                "content": content,
                "sources": [
                    {"name": "Generated by AI based on philosophical sources", "reliability": "high"}
                ]
            }
            
            # Cache the result
            self.response_cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            return result
            
        except Exception as e:
            print(f"Error fetching information about {philosophy}: {str(e)}")
            return {
                "status": "error",
                "message": f"Error retrieving information: {str(e)}"
            }

    def compare_religions(self, 
                         religion1: str,
                         religion2: str,
                         aspect: str = "general") -> Dict[str, Any]:
        """Compare two religions on a specific aspect.
        
        Args:
            religion1: First religion to compare
            religion2: Second religion to compare
            aspect: Aspect to compare (e.g., 'beliefs', 'practices', 'ethics')
            
        Returns:
            Dict containing the comparison
        """
        try:
            if not religion1 or not religion2:
                raise ValueError('Both religions are required for comparison')
            
            religion1 = religion1.lower()
            religion2 = religion2.lower()
            
            if religion1 not in RELIGIONS:
                return {
                    "status": "error",
                    "message": f"Unknown religion: {religion1}"
                }
                
            if religion2 not in RELIGIONS:
                return {
                    "status": "error",
                    "message": f"Unknown religion: {religion2}"
                }
            
            # Check cache first
            cache_key = self._get_cache_key("comparison", f"{religion1}-{religion2}", aspect)
                
            if cache_key in self.response_cache:
                cache_entry = self.response_cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.cache_time:
                    print(f"Using cached comparison for {religion1} and {religion2}")
                    return cache_entry['data']
            
            # Construct the prompt for the generative model
            prompt = f"Provide a respectful, educational, and balanced comparison between {religion1.title()} and {religion2.title()} "
            
            if aspect and aspect != "general":
                prompt += f"focusing specifically on their {aspect}. "
            else:
                prompt += "covering their core beliefs, practices, and historical contexts. "
                
            # Add instruction for structured response
            prompt += "\n\nPlease structure your response with these sections:\n"
            prompt += f"1. {religion1.title()} Overview\n2. {religion2.title()} Overview\n"
            prompt += "3. Key Similarities\n4. Notable Differences\n5. Historical Interactions\n6. Modern Coexistence"
            
            # Generate response using the AI model
            response = self.model.generate_content(prompt)
            
            # Process the response
            if hasattr(response, 'text'):
                content = response.text
            else:
                content = str(response)
                
            # Create structured result
            result = {
                "religions": {
                    "first": religion1,
                    "second": religion2
                },
                "aspect": aspect,
                "comparison": content,
                "sources": [
                    {"name": "Generated by AI based on comparative religious studies", "reliability": "high"}
                ]
            }
            
            # Cache the result
            self.response_cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            return result
            
        except Exception as e:
            print(f"Error comparing {religion1} and {religion2}: {str(e)}")
            return {
                "status": "error",
                "message": f"Error performing comparison: {str(e)}"
            }

    def get_daily_spiritual_insight(self, 
                                   tradition: str = None,
                                   theme: str = None) -> Dict[str, Any]:
        """Get a daily spiritual insight or quote.
        
        Args:
            tradition: Optional specific religious or philosophical tradition
            theme: Optional theme for the insight (e.g., 'peace', 'wisdom', 'compassion')
            
        Returns:
            Dict containing the daily insight
        """
        try:
            # Create a unique cache key for today's date
            today = datetime.now().strftime("%Y-%m-%d")
            cache_key = f"daily-{today}"
            
            if tradition:
                cache_key += f"-{tradition}"
            if theme:
                cache_key += f"-{theme}"
                
            # Check cache first
            if cache_key in self.response_cache:
                cache_entry = self.response_cache[cache_key]
                # For daily insights, we want a fresh one each day
                if datetime.now().strftime("%Y-%m-%d") == today:
                    print(f"Using cached daily insight")
                    return cache_entry['data']
            
            # Construct the prompt for the generative model
            prompt = "Provide an inspiring and thought-provoking spiritual insight for today "
            
            if tradition:
                if tradition in RELIGIONS:
                    prompt += f"from the {tradition.title()} tradition "
                elif tradition in PHILOSOPHIES:
                    prompt += f"from {tradition.title()} philosophy "
                    
            if theme:
                prompt += f"focusing on the theme of {theme}. "
            else:
                prompt += "that encourages reflection and personal growth. "
                
            # Add instruction for structured response
            prompt += "\n\nPlease include:\n"
            prompt += "1. A meaningful quote or saying\n2. The source or attribution\n3. A brief reflection (2-3 sentences)\n4. A simple practice or contemplation for the day"
            
            # Generate response using the AI model
            response = self.model.generate_content(prompt)
            
            # Process the response
            if hasattr(response, 'text'):
                content = response.text
            else:
                content = str(response)
                
            # Extract the quote if possible (simple parsing)
            quote = ""
            for line in content.split('\n'):
                if line.strip().startswith('"') or line.strip().startswith('"'):
                    quote = line.strip()
                    break
            
            # Create structured result
            result = {
                "date": today,
                "tradition": tradition,
                "theme": theme,
                "quote": quote,
                "full_insight": content
            }
            
            # Cache the result
            self.response_cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            return result
            
        except Exception as e:
            print(f"Error generating daily insight: {str(e)}")
            return {
                "status": "error",
                "message": f"Error generating daily insight: {str(e)}"
            }

    def get_meditation_guide(self, 
                            tradition: str = None,
                            duration: int = 10,
                            focus: str = "mindfulness") -> Dict[str, Any]:
        """Get a guided meditation based on spiritual traditions.
        
        Args:
            tradition: Optional specific religious or philosophical tradition
            duration: Meditation duration in minutes (default: 10)
            focus: Focus of meditation (e.g., 'mindfulness', 'compassion', 'gratitude')
            
        Returns:
            Dict containing the meditation guide
        """
        try:
            # Check cache first
            cache_key = f"meditation-{duration}-{focus}"
            if tradition:
                cache_key += f"-{tradition}"
                
            if cache_key in self.response_cache:
                cache_entry = self.response_cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.cache_time:
                    print(f"Using cached meditation guide")
                    return cache_entry['data']
            
            # Construct the prompt for the generative model
            prompt = f"Create a {duration}-minute guided meditation script "
            
            if tradition:
                if tradition in RELIGIONS:
                    prompt += f"based on {tradition.title()} practices "
                elif tradition in PHILOSOPHIES:
                    prompt += f"inspired by {tradition.title()} philosophy "
                    
            prompt += f"focusing on {focus}. "
                
            # Add instruction for structured response
            prompt += "\n\nPlease structure the meditation guide with:\n"
            prompt += "1. A brief introduction explaining the benefits and context\n"
            prompt += "2. Preparation instructions\n"
            prompt += "3. Step-by-step meditation guidance with appropriate timing\n"
            prompt += "4. A gentle conclusion\n"
            prompt += "5. Suggestions for integrating the practice into daily life"
            
            # Generate response using the AI model
            response = self.model.generate_content(prompt)
            
            # Process the response
            if hasattr(response, 'text'):
                content = response.text
            else:
                content = str(response)
                
            # Create structured result
            result = {
                "tradition": tradition,
                "duration": duration,
                "focus": focus,
                "guide": content
            }
            
            # Cache the result
            self.response_cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            return result
            
        except Exception as e:
            print(f"Error generating meditation guide: {str(e)}")
            return {
                "status": "error",
                "message": f"Error generating meditation guide: {str(e)}"
            }
