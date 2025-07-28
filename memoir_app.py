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

# 52 Week Themes
week_themes = [
    "Childhood Beginnings", "Family Bonds", "First Experiences", "Overcoming Challenges", 
    "Family Traditions", "Early Lessons", "Historical Moments", "Personal Achievements",
    "Important Relationships", "Core Values", "Favorite Media", "Special Places",
    "Learning Skills", "Difficult Decisions", "Changing Times", "Legacy & Impact",
    "Childhood Fears", "Helping Others", "Technological Changes", "Dreams & Aspirations",
    "Learning New Things", "Food Memories", "Spirituality & Beliefs", "Beautiful Experiences",
    "Summer Adventures", "Life Regrets", "Standing Up", "Parental Wisdom",
    "World Change", "School Days", "Family Recipes", "Embarrassing Moments",
    "First Car", "Birthday Celebrations", "Saying Goodbye", "Gratitude Moments",
    "Childhood Dreams", "Meaningful Gifts", "Career Failures", "First Home",
    "Taking Risks", "Important Advice", "Parenting Moments", "Memorable Vacations",
    "Inner Peace", "Entertainment Memories", "Technology Evolution", "Retirement Dreams",
    "Childhood Games", "Personal Growth", "Historical Events", "Life Summary"
]

# Question templates for each theme (7 questions per theme)
theme_questions = {
    "Childhood Beginnings": [
        "What is your earliest childhood memory?",
        "What games did you play as a young child?",
        "Who were your childhood heroes?",
        "What did you want to be when you grew up?",
        "Describe your favorite childhood toy or possession.",
        "What was your favorite bedtime story?",
        "How did your childhood differ from your children's childhood?"
    ],
    "Family Bonds": [
        "Who was your best friend growing up and why?",
        "Describe a special family tradition from your childhood.",
        "What family member influenced you the most?",
        "Tell me about a family vacation you remember fondly.",
        "What was your relationship like with your siblings?",
        "Describe a time your family pulled together during a crisis.",
        "What family recipe holds special memories for you?"
    ],
    "First Experiences": [
        "What was your first job and what did you learn from it?",
        "Describe your first day of school.",
        "What was your first date like?",
        "Tell me about learning to drive.",
        "What was your first time living away from home like?",
        "Describe your first major purchase.",
        "What was your first experience with technology?"
    ],
    "Overcoming Challenges": [
        "Describe a time you overcame a significant challenge.",
        "What was the hardest decision you ever made?",
        "Tell me about a time you failed and how you recovered.",
        "Describe a period when you felt lost and how you found your way.",
        "What obstacle took you the longest to overcome?",
        "Tell me about a time you had to stand up for yourself.",
        "What challenge made you stronger?"
    ],
    "Family Traditions": [
        "What traditions did your family have during holidays?",
        "Describe a weekly family ritual you enjoyed.",
        "What cultural traditions were important to your family?",
        "Tell me about a family recipe passed down through generations.",
        "What birthday traditions did your family have?",
        "Describe a family gathering that was especially meaningful.",
        "What traditions would you like to pass on to future generations?"
    ]
}

# Add remaining themes with 7 questions each
for theme in week_themes[5:]:
    if theme not in theme_questions:
        theme_questions[theme] = [
            f"What {theme.lower()} experience was most meaningful to you?",
            f"How did {theme.lower()} shape who you are today?",
            f"Tell me about a time when {theme.lower()} was challenging.",
            f"What lesson did you learn from {theme.lower()}?",
            f"Describe your most memorable {theme.lower()} moment.",
            f"How has {theme.lower()} changed over the years?",
            f"What advice would you give about {theme.lower()}?"
        ]

# Sample responses data structure
sample_responses = {
    "1_0": {
        "week": 1,
        "theme": "Childhood Beginnings",
        "question_index": 0,
        "question": "What is your earliest childhood memory?",
        "answer": "Playing in the backyard with my sister. We had a big oak tree we used to climb.",
        "status": "answered",
        "timestamp": "2023-01-01 10:30:00"
    },
    "1_1": {
        "week": 1,
        "theme": "Childhood Beginnings",
        "question_index": 1,
        "question": "What games did you play as a young child?",
        "answer": "We loved playing hide and seek in the neighborhood.",
        "status": "answered",
        "timestamp": "2023-01-02 14:15:00"
    },
    "2_0": {
        "week": 2,
        "theme": "Family Bonds",
        "question_index": 0,
        "question": "Who was your best friend growing up and why?",
        "answer": "Tommy. We did everything together - fishing, playing baseball, exploring the woods.",
        "status": "answered",
        "timestamp": "2023-01-08 09:45:00"
    }
}

# Initialize responses if not already done
if not st.session_state.responses:
    st.session_state.responses = sample_responses

def get_week_theme(week_number):
    """Get theme for a specific week"""
    if 1 <= week_number <= 52:
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
        return "Tell me about this week's theme."

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
    answered = 0
    total = 7
    for i in range(7):
        response_key = f"{week_number}_{i}"
        if response_key in st.session_state.responses and st.session_state.responses[response_key].get("status") == "answered":
            answered += 1
    return answered, total

def get_overall_progress():
    """Get overall progress across all weeks"""
    total_questions = 52 * 7
    answered_count = len([r for r in st.session_state.responses.values() if r.get("status") == "answered"])
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
                    "timestamp": response.get("timestamp", "")
                })
    
    # Sort by week and question index
    results.sort(key=lambda x: (x["week"], x["question"]))
    return results

def export_responses():
    """Export all responses as JSON"""
    return json.dumps(st.session_state.responses, indent=2)

# Main app
st.set_page_config(page_title="52 Weeks Memoir", page_icon="📖", layout="wide")

# Title and description
st.title("📖 52 Weeks Memoir")
st.markdown("""
*Build a lifetime of memories with 7 questions per week*
""")

# User selection
if not st.session_state.user_type:
    st.subheader("Who are you?")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👨 Parent (Respond to Questions)", use_container_width=True):
            st.session_state.user_type = "parent"
            st.session_state.current_user = "parent"
            st.rerun()
    
    with col2:
        if st.button("👨‍👦 Child (Review & Guide Responses)", use_container_width=True):
            st.session_state.user_type = "child"
            st.session_state.current_user = "child"
            st.rerun()
    
    st.info("Select your role to get started")
    
    # Show sample week structure
    st.markdown("### Sample Week Structure")
    sample_data = []
    for i in range(1, 4):
        theme = get_week_theme(i)
        sample_data.append({"Week": i, "Theme": theme, "Questions": "7 questions per theme"})
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True, hide_index=True)

# Parent's view
elif st.session_state.user_type == "parent":
    st.subheader("Answer Weekly Questions")
    
    # Week navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("◀ Previous Week"):
            if st.session_state.view_week:
                new_week = max(1, st.session_state.view_week - 1)
                st.session_state.view_week = new_week
            else:
                st.session_state.view_week = 51
            st.session_state.current_question_index = 0
            st.rerun()
    
    with col2:
        if st.session_state.view_week:
            selected_week = st.number_input("Select week:", min_value=1, max_value=52, value=st.session_state.view_week)
        else:
            selected_week = st.number_input("Select week:", min_value=1, max_value=52, value=1)
        
        if st.session_state.view_week != selected_week:
            st.session_state.view_week = selected_week
            st.session_state.current_question_index = 0
            st.rerun()
    
    with col3:
        if st.button("Next Week ▶"):
            if st.session_state.view_week:
                new_week = min(52, st.session_state.view_week + 1)
                st.session_state.view_week = new_week
            else:
                st.session_state.view_week = 2
            st.session_state.current_question_index = 0
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
    st.caption(f"Week Progress: {answered}/{total} questions answered")
    
    st.markdown(f"### Week {week_number}: {theme}")
    
    # Question navigation within week
    question_col1, question_col2, question_col3 = st.columns([1, 3, 1])
    
    with question_col1:
        if st.button("◀ Previous Question"):
            st.session_state.current_question_index = max(0, st.session_state.current_question_index - 1)
            st.rerun()
    
    with question_col2:
        question_index = st.slider("Question", 0, 6, st.session_state.current_question_index, 
                                 format="Question %d")
        if st.session_state.current_question_index != question_index:
            st.session_state.current_question_index = question_index
            st.rerun()
    
    with question_col3:
        if st.button("Next Question ▶"):
            st.session_state.current_question_index = min(6, st.session_state.current_question_index + 1)
            st.rerun()
    
    # Display current question
    current_question = get_current_question(week_number, st.session_state.current_question_index)
    st.markdown(f"**Question {st.session_state.current_question_index + 1}/7:** {current_question}")
    
    # Check if already answered
    response_key = f"{week_number}_{st.session_state.current_question_index}"
    if response_key in st.session_state.responses and st.session_state.responses[response_key].get("status") == "answered":
        st.success("✅ You've already answered this question!")
        st.markdown(f"**Your response:** {st.session_state.responses[response_key]['answer']}")
        
        if st.button("📝 Edit Response"):
            st.session_state.editing_week = week_number
            st.rerun()
    else:
        # Show response form
        with st.form("response_form"):
            answer = st.text_area("Your response:", height=200, 
                                value=st.session_state.responses.get(response_key, {}).get("answer", ""))
            submitted = st.form_submit_button("Save Response")
            
            if submitted:
                save_response(week_number, st.session_state.current_question_index, answer)
                st.success("Response saved!")
                # Move to next question
                if st.session_state.current_question_index < 6:
                    st.session_state.current_question_index += 1
                st.rerun()
    
    # Question options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⏭️ Skip Question"):
            skip_question(week_number, st.session_state.current_question_index)
            if st.session_state.current_question_index < 6:
                st.session_state.current_question_index += 1
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
            for i in range(st.session_state.current_question_index + 1, 7):
                check_key = f"{week_number}_{i}"
                if check_key not in st.session_state.responses or st.session_state.responses[check_key].get("status") != "answered":
                    st.session_state.current_question_index = i
                    found = True
                    break
            if not found:
                st.info("All questions in this week are answered!")
            st.rerun()
    
    # Navigation
    st.markdown("---")
    if st.button("⬅️ Back to Role Selection"):
        st.session_state.user_type = None
        st.session_state.editing_week = None
        st.session_state.view_week = None
        st.session_state.current_question_index = 0
        st.rerun()

# Child's view
elif st.session_state.user_type == "child":
    st.subheader("Review & Guide Responses")
    
    # Overall stats
    answered_count, percentage = get_overall_progress()
    col1, col2, col3 = st.columns(3)
    col1.metric("Questions Answered", answered_count, "364 total")
    col2.metric("Completion", f"{percentage:.1f}%", "Progress")
    col3.metric("Questions Remaining", 364 - answered_count)
    
    # Progress bar
    st.progress(percentage / 100)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📚 By Week", "📊 Stats", "💾 Export"])
    
    with tab1:
        st.markdown("### 🔍 Search Responses")
        search_query = st.text_input("Search by keyword, theme, or question:")
        
        if search_query:
            st.session_state.search_results = search_responses(search_query)
            st.markdown(f"### Search Results ({len(st.session_state.search_results)} found)")
            
            for result in st.session_state.search_results:
                with st.expander(f"**Week {result['week']}: {result['theme']}**"):
                    st.markdown(f"**Question:** {result['question']}")
                    st.markdown(f"**Answer:** {result['answer']}")
                    if result['timestamp']:
                        st.caption(f"Answered: {result['timestamp']}")
        else:
            st.info("Enter a search term to find specific responses")
    
    with tab2:
        st.markdown("### 📚 Responses by Week")
        
        # Week selector
        selected_week = st.selectbox("Select week to view:", 
                                   options=list(range(1, 53)), 
                                   index=0)
        
        theme = get_week_theme(selected_week)
        questions = get_week_questions(selected_week)
        answered, total = get_week_progress(selected_week)
        
        st.markdown(f"#### Week {selected_week}: {theme}")
        st.progress(answered / total)
        st.caption(f"Progress: {answered}/{total} questions answered")
        
        # Show all questions for this week
        for i in range(7):
            response_key = f"{selected_week}_{i}"
            question = questions[i] if i < len(questions) else f"Question {i+1}"
            
            with st.expander(f"**Q{i+1}: {question[:50]}...**"):
                if response_key in st.session_state.responses and st.session_state.responses[response_key].get("status") == "answered":
                    st.markdown(f"**Question:** {question}")
                    st.markdown(f"**Answer:** {st.session_state.responses[response_key]['answer']}")
                    st.caption(f"Answered: {st.session_state.responses[response_key].get('timestamp', '')}")
                else:
                    st.info("Not yet answered")
                    
                    # Show if skipped or requested new
                    if selected_week in st.session_state.skipped_questions and i in st.session_state.skipped_questions[selected_week]:
                        st.caption("⏭️ Skipped")
                    elif selected_week in st.session_state.requested_new_questions and i in st.session_state.requested_new_questions[selected_week]:
                        st.caption("🔄 New question requested")
    
    with tab3:
        st.markdown("### 📊 Progress Statistics")
        
        # Weekly completion chart
        weekly_data = []
        for week in range(1, 53):
            answered, total = get_week_progress(week)
            weekly_data.append({"Week": week, "Completion": (answered / total) * 100 if total > 0 else 0})
        
        weekly_df = pd.DataFrame(weekly_data)
        st.markdown("**Weekly Completion**")
        st.bar_chart(weekly_df.set_index("Week"))
        
        # Theme completion
        st.markdown("**Theme Sections**")
        theme_sections = [
            ("Foundation", 1, 10),
            ("Growth", 11, 20),
            ("Experiences", 21, 30),
            ("Wisdom", 31, 40),
            ("Reflections", 41, 52)
        ]
        
        section_data = []
        for section_name, start_week, end_week in theme_sections:
            section_total = (end_week - start_week + 1) * 7
            section_answered = 0
            for week in range(start_week, end_week + 1):
                answered, _ = get_week_progress(week)
                section_answered += answered
            section_data.append({
                "Section": section_name,
                "Completion": (section_answered / section_total) * 100 if section_total > 0 else 0
            })
        
        section_df = pd.DataFrame(section_data)
        st.bar_chart(section_df.set_index("Section"))
    
    with tab4:
        st.markdown("### 💾 Export Data")
        st.markdown("Download all responses as a JSON file:")
        
        # Create download button
        json_data = export_responses()
        st.download_button(
            label="📥 Download All Responses (JSON)",
            data=json_data,
            file_name="memoir_responses.json",
            mime="application/json"
        )
        
        st.markdown("### 📋 Summary")
        if st.session_state.responses:
            total_words = sum(len(response.get("answer", "").split()) 
                            for response in st.session_state.responses.values() 
                            if response.get("status") == "answered")
            st.metric("Total Words Written", f"{total_words:,}")
            
            # Show sample weeks
            st.markdown("**Sample Completed Weeks:**")
            completed_weeks = set()
            for response_key in st.session_state.responses:
                if st.session_state.responses[response_key].get("status") == "answered":
                    week_num = st.session_state.responses[response_key]["week"]
                    completed_weeks.add(week_num)
            
            completed_weeks = sorted(list(completed_weeks))[:5]  # Show first 5
            for week in completed_weeks:
                theme = get_week_theme(week)
                st.markdown(f"**Week {week}: {theme}**")
        else:
            st.info("No responses to export yet")
    
    # Navigation
    st.markdown("---")
    if st.button("⬅️ Back to Role Selection"):
        st.session_state.user_type = None
        st.rerun()

# Footer
st.markdown("---")
st.caption("52 Weeks Memoir - 7 questions per week, 364 memories to preserve")
