import pandas as pd
from datetime import datetime
from mongo_utils import MongoManager

# Import problem scenarios from agents.py
try:
    from agents import PROBLEM_SCENARIOS
except ImportError:
    # Define fallback if import fails (e.g., during direct execution)
    PROBLEM_SCENARIOS = {i: {"title": f"Problem {i}", "description": "Description missing."} for i in range(1, 7)}

# Define the total number of chapters/problems
NUM_CHAPTERS = 6

class StoryManager:
    def __init__(self, session_id=None, prolific_id=None):
        self.session_id = session_id if session_id else datetime.now().strftime("%Y%m%d_%H%M%S")
        self.prolific_id = prolific_id
        self.session_story = [] # List of dictionaries: {'chapter': int, 'problem_title': str, 'problem_desc': str, 'story': str}
        self.user_reflections = [] # List of dictionaries: {'chapter': int, 'reflection': str, 'timestamp': datetime}
        self.feature_rankings = [] # Keep for now, might repurpose or remove later if ranking isn't needed
        self.current_chapter = 0 # Track the chapter the user is currently generating story FOR
        
        # Initialize MongoDB connection
        self.mongo = MongoManager()

    def set_prolific_id(self, prolific_id):
        self.prolific_id = prolific_id

    def start_session(self):
        """Initializes the session, prepares for Chapter 1."""
        self.current_chapter = 1
        # Initial save to create the session in the database
        self.save_session()

    def _get_problem_for_chapter(self, chapter_num):
        """Gets the problem title and description for a given chapter."""
        if chapter_num in PROBLEM_SCENARIOS:
            return PROBLEM_SCENARIOS[chapter_num]['title'], PROBLEM_SCENARIOS[chapter_num]['description']
        else:
            return "Unknown Problem", "No description available."

    def add_story_segment(self, chapter_num, story_text):
        """Adds a generated story segment for a specific chapter."""
        # Remove existing story for this chapter if updating
        self.session_story = [s for s in self.session_story if s['chapter'] != chapter_num]

        title, desc = self._get_problem_for_chapter(chapter_num)
        # Extract story text after "STORY:"
        if "STORY:" in story_text:
             story_only = story_text.split("STORY:", 1)[1].strip()
        else:
             story_only = story_text # Assume it's just the story if marker is missing

                self.session_story.append({
            'chapter': chapter_num,
            'problem_title': title,
            'problem_desc': desc,
            'story': story_only,
            'timestamp': datetime.now()
        })
        # Sort stories by chapter just in case
        self.session_story.sort(key=lambda x: x['chapter'])
        
        # Save after adding story segment
        self.save_session()

    def add_user_reflection(self, chapter_num, reflection_text):
        """Adds the user's reflection for a specific chapter."""
        # Remove existing reflection for this chapter if updating
        self.user_reflections = [r for r in self.user_reflections if r['chapter'] != chapter_num]

        self.user_reflections.append({
            'chapter': chapter_num,
            'reflection': reflection_text,
            'timestamp': datetime.now()
        })
        # Sort reflections by chapter
        self.user_reflections.sort(key=lambda x: x['chapter'])
        
        # Save after adding reflection
        self.save_session()

    def get_story_for_chapter(self, chapter_num):
        """Retrieves the story for a specific chapter."""
        for segment in self.session_story:
            if segment['chapter'] == chapter_num:
                return segment['story']
        return None

    def get_reflection_for_chapter(self, chapter_num):
        """Retrieves the reflection for a specific chapter."""
        for reflection in self.user_reflections:
            if reflection['chapter'] == chapter_num:
                return reflection['reflection']
        return "" # Return empty string if no reflection yet

    def get_current_chapter_number(self):
        """Returns the number of the next chapter to generate or reflect on."""
        # The next chapter is usually one more than the number of reflections added
        return len(self.user_reflections) + 1

    def is_session_complete(self):
        """Checks if all chapters have reflections."""
        return len(self.user_reflections) >= NUM_CHAPTERS

    def save_session(self):
        """Saves the session data to MongoDB only."""
        # Prepare session data
        session_data = {
            "session_id": self.session_id,
            "prolific_id": self.prolific_id,
            "completed": self.is_session_complete(),
            "completed_timestamp": datetime.now().isoformat() if self.is_session_complete() else None,
            "stories": self.session_story,
            "reflections": self.user_reflections,
            "rankings": self.feature_rankings,
            "updated_at": datetime.now().isoformat()
        }
        
        # Save to MongoDB only
        return self.mongo.save_session(session_data)

    # Save rankings function (can keep as is)
    def save_rankings(self, rankings_data):
        """Save the rankings data."""
        self.feature_rankings = rankings_data
        return self.save_session() 