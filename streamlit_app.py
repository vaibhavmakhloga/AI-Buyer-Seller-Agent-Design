import streamlit as st
from swarm import Swarm
from agents import create_story_agent, PROBLEM_SCENARIOS
from story_manager import StoryManager, NUM_CHAPTERS
import pandas as pd
from datetime import datetime
import time
import streamlit.components.v1 as components

def set_custom_style():
    st.markdown("""
        <style>
        /* Modern, high-contrast theme */
        .stApp {
            max-width: 1400px;
            margin: 0 auto;
            background-color: #ffffff !important;
        }
        
        /* Reinstated Story box with paper-like appearance */
        .story-box {        
            background-color: #fff9f0;  /* Slightly off-white, paper-like color */
            border-radius: 3px;
            padding: 30px;
            margin: 15px 0;
            font-family: 'Crimson Text', Georgia, serif;  /* More story-like font */
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            color: #2c3e50;
            font-size: 18px; /* Adjusted font size */
            line-height: 1.8;
            border: none;
            position: relative;
            /* Add subtle lines */
            background-image: linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px);
            background-size: 100% 1.8em; /* Match line-height */
            min-height: 200px;
            text-align: left;
            padding-left: 40px; /* Add space for line numbers/effects if needed */
        }
        
        /* Optional: Paper texture (can be subtle) */
        .story-box::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            /* You can use a base64 encoded texture or a URL */
            /* background-image: url('data:image/png;base64,...'); */ /* Example texture */
            opacity: 0.02; /* Make it very subtle */
            pointer-events: none;
            z-index: -1; /* Ensure it's behind text */
        }
        
        /* Optional: Binder effect on the left */
        .story-box::after {
            content: '';
            position: absolute;
            left: 15px; /* Adjust position */
            top: 0;
            width: 2px; /* Thickness of the line */
            height: 100%;
            background: linear-gradient(to bottom, #d4d4d4, #d4d4d4 95%, transparent 95%); /* Dashed/dotted line */
            background-size: 100% 15px; /* Control dash/dot spacing */
            /* border-left: 1px solid #e0e0e0; */ /* Alternative solid line */
        }
        
        /* Story line animation (keeping fade-in) */
        .story-line {
            opacity: 0;
            animation: fadeInLine 0.7s ease-out forwards; /* Slightly faster fade */
            position: relative;
            margin-bottom: 1.8em; /* Match line-height for spacing */
            /* padding-left: 10px; */ /* Removed padding here, handled by story-box */
        }
        
        /* Optional: Re-add Pen cursor effect */
        /*
        .story-line::before {
            content: '✎';
            position: absolute;
            left: -25px; // Adjust position relative to story-box padding
            top: 2px; // Fine-tune vertical alignment
            opacity: 0;
            color: #3498db;
            animation: writingCursor 0.5s ease-in-out forwards;
            animation-delay: inherit; // Inherit delay from parent .story-line
            font-size: 1.1em;
        }
        
        @keyframes writingCursor {
            0% {
                opacity: 0;
                transform: translateX(-10px);
            }
            50% {
                opacity: 1;
            }
            100% {
                opacity: 0;
                transform: translateX(5px);
            }
        }
        */
        
        /* Enhanced typing animation */
        @keyframes fadeInLine {
            0% {
                opacity: 0;
                transform: translateY(10px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Keep existing delay classes */
        .delay-0 { animation-delay: 0.1s; } /* Start earlier */
        .delay-1 { animation-delay: 0.4s; }
        .delay-2 { animation-delay: 0.7s; }
        .delay-3 { animation-delay: 1.0s; }
        .delay-4 { animation-delay: 1.3s; }
        .delay-5 { animation-delay: 1.6s; }
        /* Add more delays as needed for longer stories */
        .delay-6 { animation-delay: 1.9s; }
        .delay-7 { animation-delay: 2.2s; }
        .delay-8 { animation-delay: 2.5s; }
        
        /* Story header styling */
        .header-style {
            font-family: 'Inter', sans-serif;
            color: #1f77b4; /* Match story box accent */
            font-size: 22px;
            font-weight: 600;
            margin: 30px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #1f77b4;
        }
        
        /* Challenge box */
        .challenge-box {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px 20px;
            margin: 12px 0;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            color: #2c3e50;
            border-left: 4px solid #e74c3c;
        }
        
        /* Headers */
        .header-style {
            color: #2c3e50;
            font-size: 24px;
            font-weight: 600;
            margin: 25px 0 15px 0;
            font-family: 'Inter', sans-serif;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
        }
        
        /* Info boxes */
        .stAlert {
            background-color: #f8f9fa !important;
            color: #2c3e50 !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
        }
        
        /* Buttons */
        .stButton button {
            background-color: #3498db !important;
            color: white !important;
            font-weight: 500 !important;
            border: none !important;
            padding: 10px 20px !important;
            border-radius: 8px !important;
        }
        
        /* Text areas */
        .stTextArea textarea {
            background-color: #ffffff !important;
            border-radius: 8px !important;
            border: 2px solid #e0e0e0 !important;
            padding: 12px !important;
            font-size: 16px !important;
            color: #2c3e50 !important;
        }
        
        /* Text area placeholder */
        .stTextArea textarea::placeholder {
            color: #95a5a6 !important;
            opacity: 1 !important;
        }
        
        /* Text area focus state */
        .stTextArea textarea:focus {
            border-color: #3498db !important;
            box-shadow: 0 0 0 1px #3498db !important;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: #f8f9fa !important;
        }
        
        /* Text colors */
        p, h1, h2, h3, h4, h5, h6, .stMarkdown {
            color: #2c3e50 !important;
        }
        
        /* Example text */
        em {
            color: #666666 !important;
        }
        
        /* Typing animation */
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        
        .typing-effect {
            overflow: hidden;
            white-space: pre-wrap;
            animation: typing 2s steps(40, end);
        }
        
        /* Section dividers */
        hr {
            margin: 30px 0;
            border: none;
            border-top: 2px solid #e0e0e0;
        }
        
        /* Toggle switch styling */
        .stCheckbox {
            background-color: white !important;
            padding: 10px !important;
            border-radius: 8px !important;
            border: 1px solid #e0e0e0 !important;
        }
        
        .stCheckbox label {
            color: #2c3e50 !important;
            font-weight: 500 !important;
        }
        
        /* Info text under design input */
        .stAlert > div {
            color: #2c3e50 !important;
            background-color: #f8f9fa !important;
            border: 1px solid #e0e0e0 !important;
        }
        
        /* Improved typing animation */
        @keyframes fadeInLine {
            from { 
                opacity: 0;
                transform: translateY(10px);
            }
            to { 
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .story-line {
            opacity: 0;
            animation: fadeInLine 0.5s ease-out forwards;
        }
        
        .delay-1 { animation-delay: 0.5s; }
        .delay-2 { animation-delay: 1.0s; }
        .delay-3 { animation-delay: 1.5s; }
        /* Add more delays as needed */
        
        .instruction-box {
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 20px 25px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .instruction-box h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .instruction-box h4 {
            color: #3498db;
            margin: 20px 0 10px 0;
            font-size: 1.1em;
        }
        
        .instruction-box ol, .instruction-box ul {
            margin-left: 20px;
            color: #2c3e50;
        }
        
        .instruction-box li {
            margin: 8px 0;
            line-height: 1.5;
        }
        
        .instruction-box p {
            color: #2c3e50;
            line-height: 1.6;
        }
        
        .feature-box {
            background-color: #1e1e1e;
            border-left: 3px solid #3498db;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        
        .feature-number {
            color: #3498db;
            font-weight: bold;
            font-size: 1.1em;
            margin-right: 10px;
        }
        
        .feature-text {
            color: #ffffff;
            margin-top: 5px;
            font-size: 0.95em;
            line-height: 1.4;
        }
        
        /* Specific styling for ranking feature text to prevent color conflict */
        .ranking-feature-text {
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 12px 15px;
            margin: 8px 0;
            border-radius: 4px;
            font-size: 15px;
            color: #2c3e50;
            line-height: 1.4;
        }
        
        /* Style the number input */
        div[data-testid="stNumberInput"] input {
            font-size: 16px;
            font-weight: bold;
            text-align: center;
        }
        
        /* Add space between ranking rows */
        .stForm > div > div > div {
            margin-bottom: 8px;
        }
        
        /* Custom styling for the Prolific ID input */
        [data-testid="stTextInput"] input {
            border: 1px solid #e0e0e0 !important;
            border-radius: 6px !important;
            padding: 12px 15px !important;
            font-size: 16px !important;
            transition: border-color 0.3s ease !important;
            background-color: #f9f9fa !important;
            color: #2c3e50 !important;  /* Adding dark text color for visibility */
        }
        [data-testid="stTextInput"] input::placeholder {
            color: #95a5a6 !important;  /* Adding placeholder color for better contrast */
            opacity: 1 !important;
        }
        [data-testid="stTextInput"] input:focus {
            border-color: #3498db !important;
            box-shadow: 0 0 0 1px #3498db !important;
        }
        /* Style the warning message */
        .stAlert > div {
            border-radius: 6px !important;
            padding: 10px 15px !important;
        }
        
        /* Style to identify our special text area */
        .no-paste-text-area textarea {
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            padding: 12px !important;
            font-size: 16px !important;
            background-color: #ffffff !important;
            color: #2c3e50 !important;
            height: 100px;
            width: 100%;
        }

        /* Reflection input prompt area */
        .reflection-prompt {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 15px 20px;
            margin-bottom: 15px;
            font-size: 15px;
            color: #2c3e50;
        }
        .reflection-prompt strong {
             color: #1f77b4;
        }
        .reflection-prompt ul {
            margin-top: 10px;
            margin-left: 20px;
            list-style-type: disc;
        }
        .reflection-prompt li {
            margin-bottom: 5px;
        }

        /* Style for the displayed problem description */
        .problem-description-box {
            background-color: #eef5f9;
            border-left: 4px solid #1f77b4;
            padding: 15px 20px;
            margin: 10px 0 20px 0;
            border-radius: 4px;
            font-style: italic;
            color: #2c3e50;
        }
        .problem-description-box h4 {
             margin-top: 0;
             margin-bottom: 8px;
             color: #1f77b4;
             font-style: normal;
             font-size: 1.1em;
        }
        </style>
    """, unsafe_allow_html=True)

def display_story_with_animation(story_text, container):
    # Split story into lines
    lines = story_text.split('\n')
    story_html = ""
    
    for i, line in enumerate(lines):
        if line.strip():  # Only process non-empty lines
            # Convert markdown-style bold to HTML bold
            line = line.replace('**', '<strong>')  # First occurrence
            line = line.replace('**', '</strong>', 1)  # Second occurrence
            
            delay_class = f"delay-{i}"
            story_html += f'<div class="story-line {delay_class}">{line}</div>'
    
    container.markdown(
        f"""<div class="story-box">
            {story_html}
        </div>""",
        unsafe_allow_html=True
    )

def display_instructions():
    # Professional Prolific ID input with clean styling
    st.markdown("""
        <style>
        .prolific-container {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .prolific-label {
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 10px;
            color: #2c3e50;
            display: flex;
            align-items: center;
        }
        .required-asterisk {
            color: #e74c3c;
            font-weight: bold;
            font-size: 18px;
            margin-left: 4px;
        }
        .prolific-input {
            margin-top: 5px;
        }
        .prolific-note {
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 8px;
            font-style: italic;
        }
        </style>
        <div class="prolific-container">
            <div class="prolific-label">
                Prolific ID <span class="required-asterisk">*</span>
            </div>
            <div class="prolific-note">Required for study participation</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Get prolific_id from session state or initialize it
    prolific_id = st.session_state.get('prolific_id', '')
    
    # Add the input field within the custom container
    prolific_id = st.text_input(
        "",  # No label (we use the custom one above)
        key="prolific_id_input",
        placeholder="Enter your Prolific ID"
    )
    
    # Store in session state
    st.session_state.prolific_id = prolific_id
    
    # Simple validation message with cleaner styling
    if not prolific_id:
        st.warning("Please enter your Prolific ID to continue.")
    
    st.markdown("""
    ### About the AI Agent Sales Simulation
    <div style='width: 100%; height: 3px; background: linear-gradient(to right, #1f77b4, #f8f9fa); margin: 10px 0 25px 0;'></div>
    
    Welcome! You are participating in a research study exploring how humans supervise AI agents performing complex tasks. In this simulation, you have tasked an AI agent with selling a specific camera (e.g., a used Sony Alpha a7 III) on your behalf in an online marketplace. The AI has been pre-prompted (i.e., instructed) to potential buyers via text chat.

    You will proceed through **6 chapters**. Each chapter presents a short story where your AI sales agent encounters a specific challenge or exhibits unexpected behavior during the sales process.

    ### Your Task
    <div style='width: 100%; height: 2px; background: linear-gradient(to right, #1f77b4, transparent); margin: 10px 0 20px 0;'></div>
    
    1.  Read the story presented in each chapter.
    2.  Reflect on the AI agent's actions in the scenario.
    3.  In the text box provided, answer the following:
        *   **Was the agent's behavior appropriate or inappropriate in this situation? Why?**
        *   **What, if anything, could you have done differently when initially defining the task or instructions for the agent to potentially prevent this outcome or handle it better?**
        *   **What rules or information should the user have given the agent beforehand to prevent this?**
    4.  Submit your reflection to proceed to the next chapter.
    5.  The session concludes after you submit your reflection for Chapter 6.
    
    ### Guidelines
    <div style='width: 100%; height: 2px; background: linear-gradient(to right, #1f77b4, transparent); margin: 10px 0 20px 0;'></div>
    
    *   There are no right or wrong answers. We are interested in your reasoning and perspective.
    *   Be specific in your reflections. Explain *why* you think the behavior was appropriate/inappropriate and *how* different instructions or execution might change things.
    *   Consider the goals of selling the camera effectively while adhering to any implicit or explicit rules.
    *   Your reflections will help us understand how to design better human-AI interaction systems.
    """, unsafe_allow_html=True)
    
    # Add space before the button
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Center the start button using columns
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # Only enable the button if Prolific ID is provided
        if prolific_id:
            start_button = st.button("Start Simulation", use_container_width=True, type="primary")
            if start_button:
                # Show loading progress bar while initializing - use a simpler approach
                st.markdown("<p style='text-align:center; color:#1f77b4;'>Initializing simulation...</p>", unsafe_allow_html=True)
                progress_bar = st.progress(0)
                
                # Use fewer steps to reduce potential for ElementNode errors
                for percent_complete in [0, 50, 100]:
                    progress_bar.progress(percent_complete)
                    time.sleep(0.2)  # Slower updates are less likely to cause rendering issues
                
                # Store Prolific ID in session state
                st.session_state.prolific_id = prolific_id
                st.session_state.story_manager.set_prolific_id(prolific_id)
                st.session_state.story_manager.start_session()
                return True
        else:
            # Disabled button (for visual consistency)
            st.button("Start Simulation", use_container_width=True, type="primary", disabled=True)
    
    return False

def end_session():
    """Handle end of session and save data"""
    try:
        # Explicitly ensure we've saved the latest data before ending
        session_saved = st.session_state.story_manager.save_session()
        
        # Double-check that all 6 chapters are saved
        if len(st.session_state.story_manager.user_reflections) < NUM_CHAPTERS:
            st.warning(f"Only {len(st.session_state.story_manager.user_reflections)} out of {NUM_CHAPTERS} chapters have reflections. Attempting to save anyway.")
        
        # Make one more save attempt if the initial one failed
        if not session_saved:
            st.warning("Initial save attempt failed. Trying again...")
            session_saved = st.session_state.story_manager.save_session()
        
        # Clear the screen by setting session state
        st.session_state.ended = True
        st.session_state.save_status = session_saved  # Track save status
        st.rerun()
        
    except Exception as e:
        st.error(f"Error saving session data: {str(e)}")

def main():
    st.set_page_config(
        page_title="AI Agent Sales Simulation",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Georgia&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    set_custom_style()
    
    # Initialize session state
    if 'story_manager' not in st.session_state:
        try:
            st.session_state.story_manager = StoryManager()
            st.session_state.client = Swarm()
            # Create the single story agent
            st.session_state.story_agent = create_story_agent()
            st.session_state.started = False
            st.session_state.current_chapter_index = 0
            st.session_state.session_id = st.session_state.story_manager.session_id
            st.session_state.input_key_counter = 0
            st.session_state.prolific_id = ""
            st.session_state.ended = False
            st.session_state.save_status = None
        except ConnectionError as e:
            st.error(f"Error connecting to MongoDB database: {e}")
            st.warning("The application requires a MongoDB connection to run. Please check your connection settings and try again.")
            # Add a retry button
            if st.button("Retry Connection"):
                st.rerun()
            # Stop execution to prevent further errors
            st.stop()
    
    # Main content
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>AI Agent Sales Simulation</h1>", unsafe_allow_html=True)
    
    # Check if session has ended
    if st.session_state.get('ended', False):
        # Clean, centered layout
        st.markdown("""
            <style>
            .session-complete {
                text-align: center;
                max-width: 700px;
                margin: 40px auto;
                padding: 30px;
                background-color: #f8f9fa;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .completion-code {
                background-color: #e9ecef;
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 15px;
                margin: 25px auto;
                font-size: 18px;
                font-weight: bold;
                max-width: 350px;
                color: #495057;
            }
            .data-status-box {
                background-color: #f0f9ff;
                border-left: 4px solid #3498db;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }
            .data-status-box.error {
                background-color: #fff7f7;
                border-left-color: #e74c3c;
            }
            .data-status-box h4 {
                margin-top: 0;
                color: #2c3e50;
            }
            .data-status-box p {
                margin-bottom: 5px;
                color: #2c3e50 !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='session-complete'>", unsafe_allow_html=True)
        
        # Display completion message
        save_status = st.session_state.get('save_status', False)
        if save_status:
            st.success("Session data successfully saved.")
        else:
            st.error("There was an issue saving some session data. Your participation is still recorded.")

        st.markdown("<h2>Simulation Complete</h2>", unsafe_allow_html=True)
        st.markdown("<p>Thank you for participating in this study.</p>", unsafe_allow_html=True)
                        
        # Data Status Box
        status_class = "data-status-box"
        status_symbol = "✓"
        status_text = "Session data saved successfully."
        if not save_status:
            status_class += " error"
            status_symbol = "✗"
            status_text = "Session data could not be saved completely. Your submission has been recorded, but some data may be incomplete."

        st.markdown(f"""
        <div class="{status_class}">
            <h4 style="margin-top: 0; color: #2c3e50;">Data Status</h4>
            <p style="margin-bottom: 5px;"><strong>{status_symbol}</strong> {status_text}</p>
        </div>
        """, unsafe_allow_html=True)
            
        # Display completion code
        st.markdown("<p>Please copy the completion code below and paste it in Prolific:</p>", unsafe_allow_html=True)
        st.markdown("<div class='completion-code'>AISELLERCOMPLETED</div>", unsafe_allow_html=True)
        
        # New session button
        st.markdown("<div style='margin-top: 40px;'>", unsafe_allow_html=True)
        if st.button("Start New Simulation", type="primary"):
            # Clear relevant session state keys before rerun
            keys_to_clear = ['story_manager', 'client', 'story_agent', 'started',
                            'current_chapter_index', 'session_id', 'input_key_counter',
                            'prolific_id', 'ended', 'save_status']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Generate background story
    if not st.session_state.started:
        if display_instructions():
            # Clear any existing session data
            st.session_state.story_manager = StoryManager()
            st.session_state.client = Swarm()
            st.session_state.story_agent = create_story_agent()
            st.session_state.current_chapter_index = 0
            
            # Set started state and rerun
            st.session_state.started = True
            st.session_state.initialized = True
            st.rerun()
        return

    # Only show the rest of the interface if started
    if st.session_state.started:
        current_chapter_num = st.session_state.current_chapter_index + 1

        # Check if we need to generate the story for the current chapter
        if current_chapter_num <= NUM_CHAPTERS and not st.session_state.story_manager.get_story_for_chapter(current_chapter_num):
            st.markdown(f"<p style='text-align:center; color:#1f77b4;'>Generating story for Chapter {current_chapter_num}...</p>", unsafe_allow_html=True)
            progress_bar = st.progress(0)
            try:
                chapter_title, chapter_desc = st.session_state.story_manager._get_problem_for_chapter(current_chapter_num)
                progress_bar.progress(33)
                time.sleep(0.1)

                # Call the Story Agent
                response_story = st.session_state.client.run(
                    agent=st.session_state.story_agent,
                    messages=[{
                        "role": "system",
                        "content": f"""
                            Chapter Number: {current_chapter_num}
                            Problem Description: {chapter_desc}
                            Generate the story for this chapter.
                        """
                    }]
                )
                progress_bar.progress(66)
                time.sleep(0.1)

                if response_story and response_story.messages and "STORY:" in response_story.messages[-1]["content"]:
                    story_text = response_story.messages[-1]["content"]
                    st.session_state.story_manager.add_story_segment(current_chapter_num, story_text)
                else:
                    # Fallback story
                    fallback_story = f"STORY: Your AI agent encountered an issue related to: {chapter_title}. (Error generating detailed story)"
                    st.session_state.story_manager.add_story_segment(current_chapter_num, fallback_story)
                    st.warning(f"Could not generate detailed story for Chapter {current_chapter_num}. Using fallback.")

                progress_bar.progress(100)
                time.sleep(0.2)
                progress_bar.empty()
                st.rerun()
                return

            except Exception as e:
                st.error(f"Error generating story for Chapter {current_chapter_num}: {str(e)}")
                progress_bar.empty()
                # Potentially add a retry button here
                return

        # Display Story
        story = st.session_state.story_manager.get_story_for_chapter(current_chapter_num)
        if story:
            display_story_with_animation(story, st)
        else:
            st.warning("Story not available for this chapter yet.")

        # Reflection Input Area
        st.markdown("<div class='header-style'>Your Reflection</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="reflection-prompt">
        Based on the story above:
        <ul>
            <li>If this agent was acting on your behalf, what part of its behavior felt wrong or surprising to you? Why?</li>
            <li>What rule, instruction, or boundary would you give the agent next time to prevent this? and why? 
            <li>At what point do you think the agent should have checked in with you — or not acted alone?
    
        </ul>
        </div>
        """, unsafe_allow_html=True)

        # Use a unique key for the text area based on chapter and counter
        input_key = f"reflection_input_{current_chapter_num}_{st.session_state.input_key_counter}"
        user_reflection = st.text_area(
            "Enter your reflection here:",
            key=input_key,
            height=150,
            placeholder="Explain your thoughts on the agent's appropriateness and potential changes..."
        )

        # Submit Reflection Button
        submit_col, _, _ = st.columns([1, 2, 1])
        with submit_col:
            submit_button = st.button(f"Submit Reflection & Proceed", use_container_width=True, type="primary")

        if submit_button:
            # Count words (split by whitespace and count non-empty elements)
            word_count = len([w for w in user_reflection.split() if w.strip()])
            
            if user_reflection and word_count >= 50:
                # Add reflection to story manager
                st.session_state.story_manager.add_user_reflection(current_chapter_num, user_reflection)
                st.session_state.current_chapter_index += 1
                st.session_state.input_key_counter += 1
                
                # Save after each reflection
                save_success = st.session_state.story_manager.save_session()
                
                # Show a brief success message
                if save_success:
                    st.success(f"Reflection saved. Word count: {word_count}")
                else:
                    st.warning(f"Reflection recorded but there may have been an issue saving to the database. Continuing anyway.")
                
                # If this was the final chapter, call end_session to save everything
                if st.session_state.current_chapter_index >= NUM_CHAPTERS:
                    # Show a message before ending
                    st.info("Completing the simulation and saving all data. Please wait...")
                    time.sleep(1)  # Brief pause to show the message
                    end_session()
                else:
                    st.rerun()
            else:
                st.warning(f"Please provide a more detailed reflection (at least 50 words). Current count: {word_count} words.")
                
        # Add divider
        st.markdown("""
        <div style='margin: 40px 0 20px 0; height: 1px; background-color: #e0e0e0;'></div>
        """, unsafe_allow_html=True)

        if current_chapter_num > NUM_CHAPTERS:
            st.info("You have completed all chapters.")
            if st.button("View Final Summary"):
                end_session()

if __name__ == "__main__":
    main() 