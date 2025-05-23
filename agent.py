import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
from google.adk.agents import Agent
import google.generativeai as genai
from openai import OpenAI
from spiritual_api import SpiritualKnowledgeAPI

# Load environment variables
load_dotenv()

# Configure the Google Generative AI client with the API key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    
# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = None
if openai_api_key:
    openai_client = OpenAI(api_key=openai_api_key)

# Initialize the Spiritual Knowledge API client
spiritual_client = SpiritualKnowledgeAPI()

def get_religious_information(religion: str, category: str = "general", specific_query: Optional[str] = None) -> Dict[str, Any]:
    """Get information about a specific religion.
    
    Args:
        religion: The religion to query (e.g., 'christianity', 'islam')
        category: Category of information (general, rituals, philosophy, etc.)
        specific_query: A specific question about the religion
        
    Returns:
        Dict containing the requested religious information
    """
    try:
        result = spiritual_client.get_religious_information(
            religion=religion,
            category=category,
            specific_query=specific_query
        )
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching religious information: {str(e)}"
        }

def get_philosophical_perspective(philosophy: str, topic: Optional[str] = None) -> Dict[str, Any]:
    """Get information about a philosophical perspective.
    
    Args:
        philosophy: The philosophical tradition (e.g., 'stoicism', 'existentialism')
        topic: A specific philosophical topic or question
        
    Returns:
        Dict containing the philosophical perspective
    """
    try:
        result = spiritual_client.get_philosophical_perspective(
            philosophy=philosophy,
            topic=topic
        )
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching philosophical perspective: {str(e)}"
        }

def compare_religions(religion1: str, religion2: str, aspect: str = "general") -> Dict[str, Any]:
    """Compare two religions on a specific aspect.
    
    Args:
        religion1: First religion to compare
        religion2: Second religion to compare
        aspect: Aspect to compare (e.g., 'beliefs', 'practices', 'ethics')
        
    Returns:
        Dict containing the comparison
    """
    try:
        result = spiritual_client.compare_religions(
            religion1=religion1,
            religion2=religion2,
            aspect=aspect
        )
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error comparing religions: {str(e)}"
        }

def get_daily_spiritual_insight(tradition: Optional[str] = None, theme: Optional[str] = None) -> Dict[str, Any]:
    """Get a daily spiritual insight or quote.
    
    Args:
        tradition: Optional specific religious or philosophical tradition
        theme: Optional theme for the insight (e.g., 'peace', 'wisdom', 'compassion')
        
    Returns:
        Dict containing the daily insight
    """
    try:
        result = spiritual_client.get_daily_spiritual_insight(
            tradition=tradition,
            theme=theme
        )
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating daily insight: {str(e)}"
        }

def get_meditation_guide(tradition: Optional[str] = None, duration: int = 10, focus: str = "mindfulness") -> Dict[str, Any]:
    """Get a guided meditation based on spiritual traditions.
    
    Args:
        tradition: Optional specific religious or philosophical tradition
        duration: Meditation duration in minutes (default: 10)
        focus: Focus of meditation (e.g., 'mindfulness', 'compassion', 'gratitude')
        
    Returns:
        Dict containing the meditation guide
    """
    try:
        result = spiritual_client.get_meditation_guide(
            tradition=tradition,
            duration=duration,
            focus=focus
        )
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating meditation guide: {str(e)}"
        }

def get_available_religions() -> Dict[str, Any]:
    """Get a list of available religions in the knowledge base.
    
    Returns:
        Dict containing the list of available religions
    """
    try:
        from spiritual_api import RELIGIONS
        
        return {
            "status": "success",
            "religions": list(RELIGIONS.keys())
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching available religions: {str(e)}"
        }

def get_available_philosophies() -> Dict[str, Any]:
    """Get a list of available philosophical traditions in the knowledge base.
    
    Returns:
        Dict containing the list of available philosophical traditions
    """
    try:
        from spiritual_api import PHILOSOPHIES
        
        return {
            "status": "success",
            "philosophies": list(PHILOSOPHIES.keys())
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching available philosophies: {str(e)}"
        }

def get_interfaith_dialogue(topic: str, religions: Optional[List[str]] = None) -> Dict[str, Any]:
    """Generate an interfaith dialogue on a specific topic.
    
    Args:
        topic: The topic for interfaith dialogue
        religions: List of religions to include in the dialogue (optional)
        
    Returns:
        Dict containing the interfaith dialogue
    """
    try:
        from spiritual_api import RELIGIONS
        
        # If no religions specified, use a default set of major world religions
        if not religions or len(religions) < 2:
            religions = ["christianity", "islam", "hinduism", "buddhism", "judaism"]
        
        # Validate religions
        valid_religions = []
        for religion in religions:
            if religion.lower() in RELIGIONS:
                valid_religions.append(religion.lower())
        
        if len(valid_religions) < 2:
            return {
                "status": "error",
                "message": "At least two valid religions are required for interfaith dialogue"
            }
        
        # Construct the prompt for the generative model
        prompt = f"Create an educational interfaith dialogue on the topic of '{topic}' between representatives of "
        prompt += ", ".join([r.title() for r in valid_religions[:-1]])
        prompt += f", and {valid_religions[-1].title()}. "
        
        # Add instruction for structured response
        prompt += "\n\nPlease structure the dialogue to:\n"
        prompt += "1. Respectfully represent each tradition's perspective\n"
        prompt += "2. Highlight areas of agreement and disagreement\n"
        prompt += "3. Demonstrate mutual respect and understanding\n"
        prompt += "4. Conclude with insights gained from the dialogue"
        
        # Generate response using the AI model
        response = genai.GenerativeModel('gemini-1.5-pro').generate_content(prompt)
        
        # Process the response
        if hasattr(response, 'text'):
            content = response.text
        else:
            content = str(response)
            
        # Create structured result
        result = {
            "status": "success",
            "topic": topic,
            "religions": valid_religions,
            "dialogue": content
        }
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating interfaith dialogue: {str(e)}"
        }

def get_spiritual_practice_guide(practice: str, tradition: Optional[str] = None, level: str = "beginner") -> Dict[str, Any]:
    """Get a guide for a specific spiritual practice.
    
    Args:
        practice: The spiritual practice (e.g., 'meditation', 'prayer', 'yoga')
        tradition: Optional specific religious or philosophical tradition
        level: Experience level (beginner, intermediate, advanced)
        
    Returns:
        Dict containing the practice guide
    """
    try:
        # Validate level
        valid_levels = ["beginner", "intermediate", "advanced"]
        if level.lower() not in valid_levels:
            level = "beginner"
        
        # Construct the prompt for the generative model
        prompt = f"Create a {level} level guide for the spiritual practice of {practice} "
        
        if tradition:
            prompt += f"in the {tradition.title()} tradition. "
        else:
            prompt += "that is accessible to people of various spiritual backgrounds. "
        
        # Add instruction for structured response
        prompt += "\n\nPlease structure the guide with:\n"
        prompt += "1. Introduction and benefits\n"
        prompt += "2. Historical and spiritual context\n"
        prompt += "3. Step-by-step instructions\n"
        prompt += "4. Common challenges and solutions\n"
        prompt += "5. Tips for deepening the practice\n"
        prompt += "6. Resources for further learning"
        
        # Generate response using the AI model
        response = genai.GenerativeModel('gemini-1.5-pro').generate_content(prompt)
        
        # Process the response
        if hasattr(response, 'text'):
            content = response.text
        else:
            content = str(response)
            
        # Create structured result
        result = {
            "status": "success",
            "practice": practice,
            "tradition": tradition,
            "level": level,
            "guide": content
        }
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating practice guide: {str(e)}"
        }

# The tools are defined as functions above and will be directly provided to the Agent

# Create the Spiritual Guidance Agent
root_agent = Agent(
    name="MasterversAcharya",
    model="gpt-4o",
    description="""
    MasterversAcharya is a spiritual guide who provides brief, conversational insights on spiritual and religious topics.
    You will talk in the language the user is talking
    You are MasterversAcharya, a friendly spiritual guide who speaks in a casual, human-like manner. Your responses should be:
    
    1. Brief and concise - typically 1-3 short paragraphs at most
    2. Conversational and warm, as if talking to a friend and keep the convesrations engaging with the user to keeo him interested to talk around your topic
    3. Free of academic jargon unless specifically requested
    4. Relatable with occasional use of simple metaphors or examples
    5. Balanced across different traditions without being overly formal
    
    When responding:
    - Use simple, everyday language rather than scholarly terms
    - Avoid lengthy explanations and historical details unless specifically asked
    - Respond as a wise friend might, not as an encyclopedia
    - Be warm and personable, using contractions (I'm, you're, etc.) and conversational phrases
    - Keep your answers focused and to-the-point
    Use suitable tools while necessary
    Remember that spirituality is deeply personal, and your role is to provide brief, friendly guidance,
    not lengthy academic explanations. Take contexts from relional beliefs in your conversation like Hinuism or Islam or Christianity or Judaism or Buddhism or Taoism or Sikhism or Jainism or any religion or belief what the user follows.
    """,
    tools=[
        get_religious_information,
        get_philosophical_perspective,
        compare_religions,
        get_daily_spiritual_insight,
        get_meditation_guide,
        get_available_religions,
        get_available_philosophies,
        get_interfaith_dialogue,
        get_spiritual_practice_guide
    ]
)
