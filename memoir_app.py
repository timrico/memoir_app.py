import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import json

# Initialize session state
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'editing_week' not in st.session_state:
    st.session_state.editing_week = None
if 'view_week' not in st.session_state:
    st.session_state.view_week = None
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'skipped_questions' not in st.session_state:
    st.session_state.skipped_questions = {}
if 'requested_new_questions' not in st.session_state:
    st.session_state.requested_new_questions = {}
if 'detail_prompt_active' not in st.session_state:
    st.session_state.detail_prompt_active = False
if 'current_response_key' not in st.session_state:
    st.session_state.current_response_key = None

# Baby Milestone Themes (52 weeks from birth to toddler)
week_themes = [
    # Birth & Newborn Period (Weeks 1-4)
    "Birth Story", "First Days Home", "Two Weeks Old", "One Month Checkup",
    
    # Infant Milestones (Months 1-6)
    "Two Months Old", "Three Months Old", "Four Months Old", "Five Months Old", 
    "Six Months Old", "Six Month Checkup",
    
    # Growing Infant (Months 6-12)
    "Seven Months Old", "Eight Months Old", "Nine Months Old", "Ten Months Old",
    "Eleven Months Old", "Twelve Months Old", "First Birthday",
    
    # Toddler Years (Months 12-36)
    "Thirteen Months", "Fourteen Months", "Fifteen Months", "Sixteen Months",
    "Seventeen Months", "Eighteen Months", "Eighteen Month Checkup",
    "Nineteen Months", "Twenty Months", "Twenty-One Months", "Two Years Old",
    "Two Year Checkup", "Twenty-Five Months", "Twenty-Six Months", 
    "Twenty-Seven Months", "Twenty-Eight Months", "Twenty-Nine Months", 
    "Thirty Months", "Thirty-One Months", "Thirty-Two Months", "Thirty-Three Months",
    "Thirty-Four Months", "Thirty-Five Months", "Three Years Old", "Three Year Checkup",
    
    # Additional Milestones
    "First Words", "First Steps", "First Foods", "Sleep Patterns",
    "Personality Development", "Social Interactions", "Favorite Toys & Activities",
    "Health & Growth", "Family Traditions", "Special Memories"
]

# Question templates for each theme
theme_questions = {
    # Birth Story - Most comprehensive
    "Birth Story": [
        "Date, time, and place of birth",
        "Baby's weight and length at birth",
        "Details about labor and delivery",
        "Who was present during the birth?",
        "What was the birth experience like?",
        "Baby's Apgar scores",
        "Any special circumstances or complications?",
        "First moments with baby",
        "Initial health checks and procedures",
        "First feeding experience"
    ],
    
    # First Days Home
    "First Days Home": [
        "How did the first night home go?",
        "Baby's first sleep patterns at home",
        "First bath at home",
        "Family's first impressions",
        "Adjustments to life with baby",
        "Biggest surprises about baby",
        "Most challenging moments",
        "Sweetest moments",
        "How older siblings reacted",
        "Support received from family/friends"
    ],
    
    # Standard milestone weeks (7 questions each)
    "Two Months Old": [
        "Current weight and measurements",
        "Sleep patterns and routines",
        "Feeding habits and preferences",
        "New skills or milestones reached",
        "Favorite activities or toys",
        "Personality traits becoming visible",
        "Health checkup details"
    ],
    
    "Three Months Old": [
        "Current weight and measurements",
        "Sleep patterns and routines",
        "Feeding habits and preferences",
        "New skills or milestones reached",
        "Favorite activities or toys",
        "Personality traits becoming visible",
        "Health checkup details"
    ],
    
    "Four Months Old": [
        "Current weight and measurements",
        "Sleep patterns and routines",
        "Feeding habits and preferences",
        "New skills or milestones reached",
        "Favorite activities or toys",
        "Personality traits becoming visible",
        "Health checkup details"
    ],
    
    "Six Months Old": [
        "Current weight and measurements",
        "Introduction to solid foods",
        "Sleep patterns and routines",
        "New skills or milestones reached",
        "Favorite activities or toys",
        "Personality traits becoming visible",
        "Health checkup and vaccinations"
    ],
    
    "Nine Months Old": [
        "Current weight and measurements",
        "Crawling or mobility progress",
        "Favorite games and activities",
        "New sounds or words",
        "Social interactions",
        "Sleep patterns and routines",
        "Health checkup details"
    ],
    
    "Twelve Months Old": [
        "Current weight and measurements",
        "Walking progress",
        "Favorite words or first words",
        "Favorite foods",
        "Personality development",
        "Social skills",
        "Health checkup and vaccinations"
    ],
    
    "First Birthday": [
        "Birthday celebration details",
        "Favorite birthday gifts",
        "Reactions to birthday cake",
        "Family and friends who attended",
        "Baby's personality on display",
        "Milestone achievements this year",
        "Looking ahead to next year"
    ],
    
    "Eighteen Months": [
        "Current weight and measurements",
        "Walking and running progress",
        "Vocabulary development",
        "Favorite activities and toys",
        "Temperament and personality",
        "Sleep patterns",
        "Health checkup details"
    ],
    
    "Two Years Old": [
        "Current weight and measurements",
        "Speech and language development",
        "Favorite games and activities",
        "Social interactions with others",
        "Favorite books and stories",
        "Potty training progress",
        "Health checkup and vaccinations"
    ],
    
    "Three Years Old": [
        "Current weight and measurements",
        "Speech and language skills",
        "Imagination and creativity",
        "Friendships and social skills",
        "Favorite activities and interests",
        "Independence and self-help skills",
        "Health checkup details"
    ],
    
    # Special milestone themes
    "First Words": [
        "First word spoken",
        "Date and circumstances",
        "Family's reaction",
        "Words that followed quickly",
        "Baby's communication style",
        "How baby uses words to express needs",
        "Funniest or most memorable first words"
    ],
    
    "First Steps": [
        "Date of first steps",
        "Where and how it happened",
        "Family's reaction",
        "Baby's expression and excitement",
        "How walking changed daily life",
        "Baby's new favorite activities",
        "Safety adjustments made at home"
    ],
    
    "First Foods": [
        "First solid food introduced",
        "Baby's reaction and taste preferences",
        "Messiest meal experiences",
        "Favorite first foods",
        "Allergic reactions or sensitivities",
        "Family meals with baby",
        "Transition from purees to finger foods"
    ],
    
    "Sleep Patterns": [
        "Newborn sleep patterns",
        "Establishing bedtime routines",
        "Night waking patterns",
        "Nap schedules and changes",
        "Sleep regression experiences",
        "Co-sleeping or crib arrangements",
        "Current sleep situation"
    ],
    
    "Health & Growth": [
        "Vaccination schedule and reactions",
        "Growth spurts and changes",
        "Common illnesses and recovery",
        "Doctor visits and checkups",
        "Medications or treatments",
        "Emergency room visits",
        "Overall health observations"
    ],
    
    "Favorite Toys & Activities": [
        "Most loved comfort items",
        "Favorite toys at different ages",
        "Games baby enjoys most",
        "Creative play activities",
        "Outdoor activities and preferences",
        "Musical toys and reactions",
        "Books and reading time"
    ],
    
    "Personality Development": [
        "Shy or outgoing tendencies",
        "Favorite ways to be comforted",
        "Reactions to strangers",
        "Emotional expressions",
        "Favorite routines and rituals",
        "Unique quirks and habits",
        "Changes in personality over time"
    ],
    
    "Social Interactions": [
        "Interactions with family members",
        "Reactions to other children",
        "Stranger anxiety experiences",
        "Favorite family activities",
        "Playdate experiences",
        "Grandparent relationships",
        "Community interactions"
    ],
    
    "Family Traditions": [
        "Holiday celebrations with baby",
        "Family routines and rituals",
        "Special family activities",
        "Cultural or religious traditions",
        "Weekly family activities",
        "Birthday and celebration traditions",
        "Family memories created"
    ],
    
    "Special Memories": [
        "Most precious moments",
        "Unexpected joys",
        "Challenging but rewarding times",
        "Family bonding experiences",
        "Milestone celebrations",
        "Travel experiences with baby",
        "Photos and videos that capture special times"
    ]
}

# Add remaining standard weeks with 7 questions each
standard_milestone_weeks = [
    "Two Weeks Old", "One Month Checkup", "Five Months Old", 
    "Seven Months Old", "Eight Months Old", "Ten Months Old",
    "Eleven Months Old", "Six Month Checkup", "Seventeen Months",
    "Nineteen Months", "Twenty Months", "Twenty-One Months",
    "Two Year Checkup", "Twenty-Five Months", "Twenty-Six Months",
    "Twenty-Seven Months", "Twenty-Eight Months", "Twenty-Nine Months",
    "Thirty Months", "Thirty-One Months", "Thirty-Two Months",
    "Thirty-Three Months", "Thirty-Four Months", "Thirty-Five Months",
    "Three Year Checkup"
]

for theme in standard_milestone_weeks:
    if theme not in theme_questions:
        theme_questions[theme] = [
            "Current weight and measurements",
            "Sleep patterns and routines",
            "Feeding habits and preferences",
            "New skills or milestones reached",
            "Favorite activities or toys",
            "Personality traits becoming visible",
            "Health checkup details"
        ]

# Sample responses data structure
sample_responses = {
    "1_0": {
        "week": 1,
        "theme": "Birth Story",
        "question_index": 0,
        "question": "Date, time, and place of birth",
        "answer": "Baby was born on June 15, 2023 at 3:30 AM at St. Mary's Hospital in downtown. It was a beautiful sunny morning when we arrived.",
        "status": "answered",
        "timestamp": "2023-06-16 10:30:00",
        "expanded": True
    },
    "1_1": {
        "week": 1,
        "theme": "Birth Story",
        "question_index": 1,
        "question": "Baby's weight and length at birth",
        "answer": "7 pounds 4 ounces and 20 inches long.",
        "status": "answered",
        "timestamp": "2023-06-16 10:35:00",
        "expanded": False
    },
    "2_0": {
        "week": 2,
        "theme": "First Days Home",
        "question_index": 0,
        "question": "How did the first night home go?",
        "answer": "The first night was challenging but wonderful. Baby cried a lot but we managed to get some sleep.",
        "status": "answered",
        "timestamp": "2023-06-22 09:45:00",
        "expanded": False
    },
    "6_0": {
        "week": 6,
        "theme": "Six Months Old",
        "question_index": 0,
        "question": "Current weight and measurements",
        "answer": "Baby now weighs 16 pounds and is 26 inches long. Growing so fast!",
        "status": "answered",
        "timestamp": "2023-12-15 14:15:00",
        "expanded": False
    }
}

# Initialize responses if not already done
if not st.session_state.responses:
    st.session_state.responses = sample_responses

def get_week_theme(week_number):
    """Get theme for a specific week"""
    if 1 <= week_number <= len(week_themes):
        return week_themes[week_number - 1]
    else:
        return week_themes[0]  # Default to first theme

def get_week_questions(week_number):
    """Get all questions for a specific week"""
    theme = get_week_theme(week_number)
    return theme_questions.get(theme, [f"Tell me about your experience with {theme}."])

def get_current_question(week_number, question_index):
    """Get the current question for a week"""
    questions = get_week_questions(week_number)
    if 0 <= question_index < len(questions):
        return questions[question_index]
    else:
        return "Tell me about this milestone."

def save_response(week_number, question_index, answer):
    """Save a response to the session state"""
    response_key = f"{week_number}_{question_index}"
    if response_key not in st.session_state.responses:
        st.session_state.responses[response_key] = {}
    
    # Get theme and question
    theme = get_week_theme(week_number)
    question = get_current_question(week_number, question_index)
    
    st.session_state.responses[response_key]["week"] = week_number
    st.session_state.responses[response_key]["theme"] = theme
    st.session_state.responses[response_key]["question_index"] = question_index
    st.session_state.responses[response_key]["question"] = question
    st.session_state.responses[response_key]["answer"] = answer
    st.session_state.responses[response_key]["status"] = "answered"
    st.session_state.responses[response_key]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if answer needs expansion
    word_count = len(answer.split())
    st.session_state.responses[response_key]["expanded"] = word_count >= 15  # Higher threshold for baby book
    
    return word_count

def skip_question(week_number, question_index):
    """Mark a question as skipped"""
    if week_number not in st.session_state.skipped_questions:
        st.session_state.skipped_questions[week_number] = []
    if question_index not in st.session_state.skipped_questions[week_number]:
        st.session_state.skipped_questions[week_number].append(question_index)

def request_new_question(week_number, question_index):
    """Mark a question as requested for replacement"""
    if week_number not in st.session_state.requested_new_questions:
        st.session_state.requested_new_questions[week_number] = []
    if question_index not in st.session_state.requested_new_questions[week_number]:
        st.session_state.requested_new_questions[week_number].append(question_index)

def get_week_progress(week_number):
    """Get progress for a specific week"""
    total_questions = len(get_week_questions(week_number))
    answered = 0
    for i in range(total_questions):
        response_key = f"{week_number}_{i}"
        if response_key in st.session_state.responses and st.session_state.responses[response_key].get("status") == "answered":
            answered += 1
    return answered, total_questions

def get_overall_progress():
    """Get overall progress across all weeks"""
    total_questions = 0
    answered_count = 0
    
    for week_num in range(1, len(week_themes) + 1):
        _, week_total = get_week_progress(week_num)
        total_questions += week_total
        answered_count += len([r for r in st.session_state.responses.values() 
                              if r.get("status") == "answered" and r.get("week") == week_num])
    
    percentage = (answered_count / total_questions) * 100 if total_questions > 0 else 0
    return answered_count, percentage

def search_responses(query):
    """Search responses using natural language"""
    results = []
    query_lower = query.lower()
    
    for response_key, response in st.session_state.responses.items():
        if "answer" in response and "question" in response:
            answer_lower = response["answer"].lower()
            question_lower = response["question"].lower()
            theme_lower = response["theme"].lower()
            
            # Simple keyword matching
            if (query_lower in answer_lower or 
                query_lower in question_lower or
                query_lower in theme_lower or
                any(word in answer_lower for word in query_lower.split()) or
                any(word in question_lower for word in query_lower.split()) or
                any(word in theme_lower for word in query_lower.split())):
                results.append({
                    "week": response["week"],
                    "theme": response["theme"],
                    "question": response["question"],
                    "answer": response["answer"],
                    "timestamp": response.get("timestamp", ""),
                    "expanded": response.get("expanded", True)
                })
    
    # Sort by week and question index
    results.sort(key=lambda x: (x["week"], x["question"]))
    return results

def export_responses():
    """Export all responses as JSON"""
    return json.dumps(st.session_state.responses, indent=2)

def generate_expansion_prompt(question, answer):
    """Generate a prompt to encourage more detailed responses"""
    prompts = [
        f"You mentioned '{answer}'. Can you tell me more details about that?",
        f"That's interesting! What else can you remember about {answer.split()[-1] if answer else 'that'}?",
        f"I'd love to hear the full story about {answer.split()[0] if answer else 'that'}.",
        f"What made {answer.split()[0] if answer else 'that'} so special?",
        f"Can you describe that experience in more detail?",
        f"What emotions come up when you think about {answer.split()[-1] if answer else 'that'}?",
        f"What would someone else want to know about {answer.split()[0] if answer else 'that'}?"
    ]
    return random.choice(prompts)

# Main app
st.set_page_config(page_title="Baby Milestone Journal", page_icon="👶", layout="wide")

# Title and description
st.title("👶 Baby Milestone Journal")
st.markdown("""
*Capture every precious moment from birth through toddler years*
""")

# User selection
if not st.session_state.user_type:
    st.subheader("Who are you?")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👩 Parent (Record Milestones)", use_container_width=True):
            st.session_state.user_type = "parent"
            st.session_state.current_user = "parent"
            st.rerun()
    
    with col2:
        if st.button("👨‍👩‍👧 Family (Review & Cherish)", use_container_width=True):
            st.session_state.user_type = "family"
            st.session_state.current_user = "family"
            st.rerun()
    
    st.info("Select your role to get started")
    
    # Show sample structure
    st.markdown("### Sample Milestone Structure")
    sample_data = []
    for i in range(1, 6):
        theme = get_week_theme(i)
        questions = get_week_questions(i)
        sample_data.append({"Milestone": i, "Theme": theme, "Questions": f"{len(questions)} questions"})
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True, hide_index=True)

# Parent's view
elif st.session_state.user_type == "parent":
    st.subheader("Record Baby Milestones")
    
    # Week navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("◀ Previous Milestone"):
            if st.session_state.view_week:
                new_week = max(1, st.session_state.view_week - 1)
                st.session_state.view_week = new_week
            else:
                st.session_state.view_week = len(week_themes) - 1
            st.session_state.current_question_index = 0
            st.session_state.detail_prompt_active = False
            st.rerun()
    
    with col2:
        if st.session_state.view_week:
            selected_week = st.number_input("Select milestone:", min_value=1, max_value=len(week_themes), value=st.session_state.view_week)
        else:
            selected_week = st.number_input("Select milestone:", min_value=1, max_value=len(week_themes), value=1)
        
        if st.session_state.view_week != selected_week:
            st.session_state.view_week = selected_week
            st.session_state.current_question_index = 0
            st.session_state.detail_prompt_active = False
            st.rerun()
    
    with col3:
        if st.button("Next Milestone ▶"):
            if st.session_state.view_week:
                new_week = min(len(week_themes), st.session_state.view_week + 1)
                st.session_state.view_week = new_week
            else:
                st.session_state.view_week = 2
            st.session_state.current_question_index = 0
            st.session_state.detail_prompt_active = False
            st.rerun()
    
    # Display current week
    if st.session_state.view_week:
        week_number = st.session_state.view_week
    else:
        week_number = 1
        st.session_state.view_week = 1
    
    theme = get_week_theme(week_number)
    questions = get_week_questions(week_number)
    
    # Week progress
    answered, total = get_week_progress(week_number)
    st.progress(answered / total)
    st.caption(f"Milestone Progress: {answered}/{total} questions answered")
    
    st.markdown(f"### Milestone {week_number}: {theme}")
    
    # Question navigation within week
    question_col1, question_col2, question_col3 = st.columns([1, 3, 1])
    
    with question_col1:
        if st.button("◀ Previous Question"):
            st.session_state.current_question_index = max(0, st.session_state.current_question_index - 1)
            st.session_state.detail_prompt_active = False
            st.rerun()
    
    with question_col2:
        question_index = st.slider("Question", 0, total-1, st.session_state.current_question_index, 
                                 format="Question %d")
        if st.session_state.current_question_index != question_index:
            st.session_state.current_question_index = question_index
            st.session_state.detail_prompt_active = False
            st.rerun()
    
    with question_col3:
        if st.button("Next Question ▶"):
            st.session_state.current_question_index = min(total-1, st.session_state.current_question_index + 1)
            st.session_state.detail_prompt_active = False
            st.rerun()
    
    # Display current question
    current_question = get_current_question(week_number, st.session_state.current_question_index)
    st.markdown(f"**Question {st.session_state.current_question_index + 1}/{total}:** {current_question}")
    
    # Check if already answered
    response_key = f"{week_number}_{st.session_state.current_question_index}"
    st.session_state.current_response_key = response_key
    
    if response_key in st.session_state.responses and st.session_state.responses[response_key].get("status") == "answered":
        answer = st.session_state.responses[response_key]['answer']
        word_count = len(answer.split())
        expanded = st.session_state.responses[response_key].get('expanded', True)
        
        st.success("✅ You've already answered this question!")
        st.markdown(f"**Your response ({word_count} words):** {answer}")
        
        # Check if response needs more detail
        if word_count < 15 and not expanded:
            st.warning("📝 This response is quite brief. Would you like to add more details?")
            expansion_prompt = generate_expansion_prompt(current_question, answer)
            st.info(f"**Suggestion:** {expansion_prompt}")
            
            if st.button("Add More Details"):
                st.session_state.detail_prompt_active = True
                st.rerun()
        elif st.button("📝 Edit Response"):
            st.session_state.detail_prompt_active = False
            st.session_state.editing_week = week_number
            st.rerun()
    else:
        # Show response form or detail prompt
        if st.session_state.detail_prompt_active and response_key in st.session_state.responses:
            # Show expansion form
            existing_answer = st.session_state.responses[response_key]['answer']
            expansion_prompt = generate_expansion_prompt(current_question, existing_answer)
            
            st.warning("📝 Let's add more details to your response!")
            st.info(f"**Suggestion:** {expansion_prompt}")
            
            with st.form("expansion_form"):
                expanded_answer = st.text_area("Add more details:", 
                                             value=existing_answer, 
                                             height=200)
                col1, col2 = st.columns(2)
                with col1:
                    expand_submitted = st.form_submit_button("Save Expanded Response")
                with col2:
                    cancel_expand = st.form_submit_button("Cancel")
                
                if expand_submitted:
                    word_count = save_response(week_number, st.session_state.current_question_index, expanded_answer)
                    st.session_state.detail_prompt_active = False
                    st.success(f"Expanded response saved! ({word_count} words)")
                    st.rerun()
                elif cancel_expand:
                    st.session_state.detail_prompt_active = False
                    st.rerun()
        else:
            # Show regular response form
            with st.form("response_form"):
                answer = st.text_area("Your response:", height=200, 
                                    value=st.session_state.responses.get(response_key, {}).get("answer", ""))
                submitted = st.form_submit_button("Save Response")
                
                if submitted:
                    word_count = save_response(week_number, st.session_state.current_question_index, answer)
                    st.success(f"Response saved! ({word_count} words)")
                    
                    # If response is too brief, prompt for more details
                    if word_count < 15:
                        st.warning("📝 This response is quite brief. Would you like to add more details?")
                        expansion_prompt = generate_expansion_prompt(current_question, answer)
                        st.info(f"**Suggestion:** {expansion_prompt}")
                        if st.button("Add More Details"):
                            st.session_state.detail_prompt_active = True
                            st.rerun()
                        else:
                            # Move to next question automatically after a brief pause
                            if st.session_state.current_question_index < total - 1:
                                st.session_state.current_question_index += 1
                            st.rerun()
                    else:
                        # Move to next question
                        if st.session_state.current_question_index < total - 1:
                            st.session_state.current_question_index += 1
                        st.rerun()
    
    # Question options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⏭️ Skip Question"):
            skip_question(week_number, st.session_state.current_question_index)
            if st.session_state.current_question_index < total - 1:
                st.session_state.current_question_index += 1
            st.session_state.detail_prompt_active = False
            st.rerun()
    
    with col2:
        if st.button("🔄 Request New Question"):
            request_new_question(week_number, st.session_state.current_question_index)
            # In a real app, this would generate a new question
            st.info("New question requested! (In demo, using same question)")
            st.rerun()
    
    with col3:
        if st.button("➡️ Next Unanswered"):
            # Find next unanswered question
            found = False
            for i in range(st.session_state.current_question_index + 1, total):
                check_key = f"{week_number}_{i}"
                if check_key not in st.session_state.responses or st.session_state.responses[check_key].get("status") != "answered":
                    st.session_state.current_question_index = i
                    found = True
                    break
            if not found:
                st.info("All questions in this milestone are answered!")
            st.session_state.detail_prompt_active = False
            st.rerun()
    
    # Navigation
    st.markdown("---")
    if st.button("⬅️ Back to Role Selection"):
        st.session_state.user_type = None
        st.session_state.editing_week = None
        st.session_state.view_week = None
        st.session_state.current_question_index = 0
        st.session_state.detail_prompt_active = False
        st.session_state.current_response_key = None
        st.rerun()

# Family view
elif st.session_state.user_type == "family":
    st.subheader("Cherish Baby Memories")
    
    # Overall stats
    answered_count, percentage = get_overall_progress()
    col1, col2, col3 = st.columns(3)
    col1.metric("Memories Recorded", answered_count, f"{len(week_themes) * 7} total")
    col2.metric("Completion", f"{percentage:.1f}%", "Progress")
    col3.metric("Memories Remaining", "Many precious moments", "to capture")
    
    # Progress bar
    st.progress(percentage / 100)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📚 By Milestone", "📊 Stats", "💾 Export"])
    
    with tab1:
        st.markdown("### 🔍 Search Memories")
        search_query = st.text_input("Search by keyword, milestone, or memory:")
        
        if search_query:
            st.session_state.search_results = search_responses(search_query)
            st.markdown(f"### Search Results ({len(st.session_state.search_results)} found)")
            
            for result in st.session_state.search_results:
                with st.expander(f"**Milestone {result['week']}: {result['theme']}**"):
                    st.markdown(f"**Question:** {result['question']}")
                    word_count = len(result['answer'].split())
                    status = "✅ Detailed" if result.get('expanded', True) else "📝 Brief"
                    st.markdown(f"**Memory ({word_count} words, {status}):** {result['answer']}")
                    if result['timestamp']:
                        st.caption(f"Recorded: {result['timestamp']}")
        else:
            st.info("Enter a search term to find specific memories")
    
    with tab2:
        st.markdown("### 📚 Memories by Milestone")
        
        # Milestone selector
        selected_week = st.selectbox("Select milestone to view:", 
                                   options=list(range(1, len(week_themes) + 1)), 
                                   index=0)
        
        theme = get_week_theme(selected_week)
        questions = get_week_questions(selected_week)
        answered, total = get_week_progress(selected_week)
        
        st.markdown(f"#### Milestone {selected_week}: {theme}")
        st.progress(answered / total)
        st.caption(f"Progress: {answered}/{total} questions answered")
        
        # Show all questions for this milestone
        brief_count = 0
        for i in range(len(questions)):
            response_key = f"{selected_week}_{i}"
            question = questions[i] if i < len(questions) else f"Question {i+1}"
            
            if response_key in st.session_state.responses and st.session_state.responses[response_key].get("status") == "answered":
                answer = st.session_state.responses[response_key]['answer']
                word_count = len(answer.split())
                expanded = st.session_state.responses[response_key].get('expanded', True)
                status = "✅ Detailed" if expanded else "📝 Brief"
                if not expanded:
                    brief_count += 1
                
                with st.expander(f"**Q{i+1}: {question[:50]}... ({word_count} words, {status})**"):
                    st.markdown(f"**Question:** {question}")
                    st.markdown(f"**Memory:** {answer}")
                    st.caption(f"Recorded: {st.session_state.responses[response_key].get('timestamp', '')}")
                    
                    if not expanded:
                        st.warning("This memory is brief and could use more details.")
            else:
                with st.expander(f"**Q{i+1}: {question[:50]}...**"):
                    st.info("Not yet recorded")
                    
                    # Show if skipped or requested new
                    if selected_week in st.session_state.skipped_questions and i in st.session_state.skipped_questions[selected_week]:
                        st.caption("⏭️ Skipped")
                    elif selected_week in st.session_state.requested_new_questions and i in st.session_state.requested_new_questions[selected_week]:
                        st.caption("🔄 New question requested")
        
        if brief_count > 0:
            st.warning(f"⚠️ {brief_count} memories in this milestone are brief and could use more details.")
    
    with tab3:
        st.markdown("### 📊 Memory Statistics")
        
        # Milestone completion chart
        weekly_data = []
        brief_responses = 0
        total_responses = 0
        
        for week in range(1, len(week_themes) + 1):
            answered, total = get_week_progress(week)
            weekly_data.append({"Milestone": week, "Completion": (answered / total) * 100 if total > 0 else 0})
            
            # Count brief responses
            for i in range(total):
                response_key = f"{week}_{i}"
                if response_key in st.session_state.responses and st.session_state.responses[response_key].get("status") == "answered":
                    total_responses += 1
                    if not st.session_state.responses[response_key].get("expanded", True):
                        brief_responses += 1
        
        weekly_df = pd.DataFrame(weekly_data)
        st.markdown("**Milestone Completion**")
        st.bar_chart(weekly_df.set_index("Milestone"))
        
        # Brief responses stats
        if total_responses > 0:
            brief_percentage = (brief_responses / total_responses) * 100
            st.markdown(f"**Memory Quality:** {brief_responses}/{total_responses} ({brief_percentage:.1f}%) memories are brief")
            if brief_responses > 0:
                st.warning("Consider encouraging more detailed memories for better baby book quality.")
        
        # Age group completion
        st.markdown("**Age Group Progress**")
        age_groups = [
            ("Newborn (0-1 month)", 1, 4),
            ("Infant (1-6 months)", 5, 10),
            ("Baby (6-12 months)", 11, 17),
            ("Toddler (12-36 months)", 18, len(week_themes))
        ]
        
        section_data = []
        for section_name, start_week, end_week in age_groups:
            section_total = 0
            section_answered = 0
            for week in range(start_week, end_week + 1):
                answered, total = get_week_progress(week)
                section_total += total
                section_answered += answered
            section_data.append({
                "Age Group": section_name,
                "Completion": (section_answered / section_total) * 100 if section_total > 0 else 0
            })
        
        section_df = pd.DataFrame(section_data)
        st.bar_chart(section_df.set_index("Age Group"))
    
    with tab4:
        st.markdown("### 💾 Export Baby Book")
        st.markdown("Download all memories as a JSON file:")
        
        # Create download button
        json_data = export_responses()
        st.download_button(
            label="📥 Download Baby Book (JSON)",
            data=json_data,
            file_name="baby_milestone_book.json",
            mime="application/json"
        )
        
        st.markdown("### 📋 Baby Book Summary")
        if st.session_state.responses:
            total_words = sum(len(response.get("answer", "").split()) 
                            for response in st.session_state.responses.values() 
                            if response.get("status") == "answered")
            st.metric("Total Words Recorded", f"{total_words:,}")
            
            # Count brief responses
            brief_count = sum(1 for response in st.session_state.responses.values() 
                            if response.get("status") == "answered" and not response.get("expanded", True))
            if brief_count > 0:
                st.metric("Brief Memories", f"{brief_count}", "Consider expanding")
            
            # Show sample milestones
            st.markdown("**Sample Recorded Milestones:**")
            completed_weeks = set()
            for response_key in st.session_state.responses:
                if st.session_state.responses[response_key].get("status") == "answered":
                    week_num = st.session_state.responses[response_key]["week"]
                    completed_weeks.add(week_num)
            
            completed_weeks = sorted(list(completed_weeks))[:5]  # Show first 5
            for week in completed_weeks:
                theme = get_week_theme(week)
                st.markdown(f"**Milestone {week}: {theme}**")
        else:
            st.info("No memories recorded yet")
    
    # Navigation
    st.markdown("---")
    if st.button("⬅️ Back to Role Selection"):
        st.session_state.user_type = None
        st.rerun()

# Footer
st.markdown("---")
st.caption("👶 Baby Milestone Journal - Capturing precious moments from birth to toddler years")
