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
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
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
                prompt += "covering its key principles, major thinkers, and philosophical implications. "
                
            # Add instruction for structured response
            prompt += "\n\nPlease structure your response with these sections when applicable:\n"
            prompt += "1. Core Principles\n2. Major Thinkers\n3. Historical Context\n4. Modern Relevance\n5. Criticism"
            
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
                    {"name": "Generated by AI based on philosophical resources", "reliability": "high"}
                ]
            }
            
            # Cache the result
            self.response_cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            return result
            
        except Exception as e:
            print(f"Error fetching philosophical perspective on {philosophy}: {str(e)}")
            return {
                "status": "error",
                "message": f"Error retrieving philosophical perspective: {str(e)}"
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
                raise ValueError('Both religion identifiers are required')
            
            religion1 = religion1.lower()
            religion2 = religion2.lower()
            
            if religion1 not in RELIGIONS:
                return {
                    "status": "error",
                    "message": f"Unknown religion: {religion1}. Available options are: {', '.join(RELIGIONS.keys())}"
                }
                
            if religion2 not in RELIGIONS:
                return {
                    "status": "error",
                    "message": f"Unknown religion: {religion2}. Available options are: {', '.join(RELIGIONS.keys())}"
                }
            
            # Check cache first
            cache_key = self._get_cache_key("comparison", f"{religion1}-{religion2}", aspect)
            if cache_key in self.response_cache:
                cache_entry = self.response_cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.cache_time:
                    print(f"Using cached comparison for {religion1} and {religion2}")
                    return cache_entry['data']
            
            # Construct the prompt for the generative model
            prompt = f"Compare and contrast {religion1.title()} and {religion2.title()} "
            
            if aspect and aspect.lower() != "general":
                prompt += f"specifically focusing on their {aspect}. "
            else:
                prompt += "comparing their beliefs, practices, historical development, and core principles. "
                
            # Add instruction for structured response
            prompt += "\n\nPlease structure your response with these sections:\n"
            prompt += f"1. Key Similarities between {religion1.title()} and {religion2.title()}\n"
            prompt += f"2. Important Differences between {religion1.title()} and {religion2.title()}\n"
            prompt += "3. Historical Interactions\n"
            prompt += "4. Modern Interpretations and Dialogue"
            
            # Generate response using the AI model
            response = self.model.generate_content(prompt)
            
            # Process the response
            if hasattr(response, 'text'):
                content = response.text
            else:
                content = str(response)
                
            # Create structured result
            result = {
                "religion1": religion1,
                "religion2": religion2,
                "aspect": aspect,
                "content": content,
                "sources": [
                    {"name": "Generated by AI based on comparative religion studies", "reliability": "high"}
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
                "message": f"Error generating comparison: {str(e)}"
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
            # Don't cache daily insights - they should be fresh each time
            # Use current date to make it "daily"
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Construct the prompt for the generative model
            prompt = f"Generate an inspiring spiritual insight for today ({today})"
            
            if tradition:
                if tradition.lower() in RELIGIONS or tradition.lower() in PHILOSOPHIES:
                    prompt += f" from the {tradition} tradition"
                else:
                    # Include the tradition in the prompt anyway, but with a caution
                    prompt += f" inspired by {tradition} wisdom"
            
            if theme:
                prompt += f" focused on the theme of {theme}"
                
            prompt += ". Include a brief reflection and a suggestion for applying this wisdom."
            
            # Generate response using the AI model
            response = self.model.generate_content(prompt)
            
            # Process the response
            if hasattr(response, 'text'):
                content = response.text
            else:
                content = str(response)
                
            # Create structured result
            result = {
                "date": today,
                "tradition": tradition,
                "theme": theme,
                "insight": content
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
            if duration < 1 or duration > 60:
                return {
                    "status": "error",
                    "message": "Duration must be between 1 and 60 minutes"
                }
            
            # Check cache first
            cache_key = self._get_cache_key(
                "meditation", 
                f"{focus}-{duration}", 
                tradition if tradition else "general"
            )
                
            if cache_key in self.response_cache:
                cache_entry = self.response_cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.cache_time:
                    print(f"Using cached meditation guide")
                    return cache_entry['data']
            
            # Construct the prompt for the generative model
            prompt = f"Create a {duration}-minute guided meditation script focused on {focus}"
            
            if tradition:
                if tradition.lower() in RELIGIONS or tradition.lower() in PHILOSOPHIES:
                    prompt += f" drawing from the {tradition} tradition"
                else:
                    # Include the tradition in the prompt anyway
                    prompt += f" inspired by {tradition} principles"
            
            prompt += ".\n\nThe meditation should include:\n"
            prompt += "1. A brief introduction explaining the benefits\n"
            prompt += "2. Opening instructions for posture and breathing\n"
            prompt += "3. The main guided meditation with appropriate timing suggestions\n"
            prompt += "4. A gentle closing\n\n"
            prompt += f"The entire guided meditation should take approximately {duration} minutes to complete when read at a moderate pace."
            
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

    def get_interfaith_dialogue(self,
                               topic: str,
                               religions: List[str] = None) -> Dict[str, Any]:
        """Generate an interfaith dialogue on a specific topic.
        
        Args:
            topic: The topic for interfaith dialogue
            religions: List of religions to include in the dialogue (optional)
            
        Returns:
            Dict containing the interfaith dialogue
        """
        try:
            if not topic:
                raise ValueError('Topic is required for interfaith dialogue')
            
            # If no religions specified, use a default set
            if not religions or len(religions) < 2:
                religions = ["christianity", "islam", "hinduism", "buddhism", "judaism"]
            
            # Validate religions
            valid_religions = []
            for religion in religions:
                rel_lower = religion.lower()
                if rel_lower in RELIGIONS:
                    valid_religions.append(rel_lower)
            
            if len(valid_religions) < 2:
                return {
                    "status": "error",
                    "message": f"At least 2 valid religions are required. Available options are: {', '.join(RELIGIONS.keys())}"
                }
            
            # Check cache first
            religions_key = "-".join(sorted(valid_religions))
            cache_key = self._get_cache_key("interfaith", religions_key, topic[:50])
                
            if cache_key in self.response_cache:
                cache_entry = self.response_cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.cache_time:
                    print(f"Using cached interfaith dialogue")
                    return cache_entry['data']
            
            # Construct the prompt for the generative model
            religions_formatted = ", ".join([r.title() for r in valid_religions[:-1]]) + f" and {valid_religions[-1].title()}"
            prompt = f"Create an educational interfaith dialogue between representatives of {religions_formatted} discussing the topic of \"{topic}\".\n\n"
            prompt += "Structure the dialogue as a respectful conversation where each perspective:\n"
            prompt += "1. Explains their tradition's viewpoint on the topic\n"
            prompt += "2. Highlights similarities with other traditions\n"
            prompt += "3. Addresses areas of difference with respect\n"
            prompt += "4. Seeks common ground where possible\n\n"
            prompt += "The dialogue should be informative, nuanced, and reflect genuine theological positions without oversimplification."
            
            # Generate response using the AI model
            response = self.model.generate_content(prompt)
            
            # Process the response
            if hasattr(response, 'text'):
                content = response.text
            else:
                content = str(response)
                
            # Create structured result
            result = {
                "topic": topic,
                "religions": valid_religions,
                "dialogue": content
            }
            
            # Cache the result
            self.response_cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            return result
            
        except Exception as e:
            print(f"Error generating interfaith dialogue: {str(e)}")
            return {
                "status": "error",
                "message": f"Error generating interfaith dialogue: {str(e)}"
            }

    def get_spiritual_practice_guide(self,
                                    practice: str,
                                    tradition: str = None,
                                    level: str = "beginner") -> Dict[str, Any]:
        """Get a guide for a specific spiritual practice.
        
        Args:
            practice: The spiritual practice (e.g., 'meditation', 'prayer', 'yoga')
            tradition: Optional specific religious or philosophical tradition
            level: Experience level (beginner, intermediate, advanced)
            
        Returns:
            Dict containing the practice guide
        """
        try:
            if not practice:
                raise ValueError('Practice type is required')
            
            valid_levels = ["beginner", "intermediate", "advanced"]
            if level.lower() not in valid_levels:
                level = "beginner"
            
            # Check cache first
            cache_key = self._get_cache_key(
                "practice", 
                f"{practice.lower()}-{level.lower()}", 
                tradition.lower() if tradition else "general"
            )
                
            if cache_key in self.response_cache:
                cache_entry = self.response_cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.cache_time:
                    print(f"Using cached practice guide")
                    return cache_entry['data']
            
            # Construct the prompt for the generative model
            prompt = f"Create a {level} level guide for the spiritual practice of {practice}"
            
            if tradition:
                if tradition.lower() in RELIGIONS or tradition.lower() in PHILOSOPHIES:
                    prompt += f" within the {tradition} tradition"
                else:
                    # Include the tradition in the prompt anyway
                    prompt += f" inspired by {tradition} teachings"
            
            prompt += ".\n\nThe guide should include:\n"
            prompt += "1. A brief introduction explaining the spiritual significance\n"
            prompt += "2. Step-by-step instructions appropriate for a " + level + "\n"
            prompt += "3. Common challenges and how to overcome them\n"
            prompt += "4. Benefits of regular practice\n"
            prompt += "5. Suggestions for deepening the practice over time"
            
            # Generate response using the AI model
            response = self.model.generate_content(prompt)
            
            # Process the response
            if hasattr(response, 'text'):
                content = response.text
            else:
                content = str(response)
                
            # Create structured result
            result = {
                "practice": practice,
                "tradition": tradition,
                "level": level,
                "guide": content
            }
            
            # Cache the result
            self.response_cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            return result
            
        except Exception as e:
            print(f"Error generating practice guide: {str(e)}")
            return {
                "status": "error",
                "message": f"Error generating practice guide: {str(e)}"
            }
