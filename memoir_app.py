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

# 52 Week Themed Questions - Building Progressively
week_themes = [
    # Foundation & Early Life (Weeks 1-10)
    ("Childhood Beginnings", "What is your earliest childhood memory?"),
    ("Family Bonds", "Who was your best friend growing up and why?"),
    ("First Experiences", "What was your first job and what did you learn from it?"),
    ("Overcoming Challenges", "Describe a time you overcame a significant challenge."),
    ("Family Traditions", "What traditions did your family have during holidays?"),
    ("Early Lessons", "What advice would you give to your younger self?"),
    ("Historical Moments", "What moment in history do you wish you could have witnessed?"),
    ("Personal Achievements", "What was your proudest achievement and why?"),
    ("Important Relationships", "How did you meet your spouse/partner?"),
    ("Core Values", "What values did your parents teach you that you still live by?"),
    
    # Growth & Development (Weeks 11-20)
    ("Favorite Media", "What was your favorite book or movie as a child?"),
    ("Special Places", "Describe a place that holds special meaning for you."),
    ("Learning Skills", "What skill do you wish you had learned earlier in life?"),
    ("Difficult Decisions", "What was the most difficult decision you ever had to make?"),
    ("Changing Times", "How has your hometown changed since you were young?"),
    ("Legacy & Impact", "What do you want to be remembered for?"),
    ("Childhood Fears", "What was your biggest fear growing up and how did you overcome it?"),
    ("Helping Others", "Describe a time when you helped someone in need."),
    ("Technological Changes", "What invention in your lifetime has impacted you the most?"),
    ("Dreams & Aspirations", "What would you do if you knew you couldn't fail?"),
    
    # Life Experiences (Weeks 21-30)
    ("Learning New Things", "What is something you've always wanted to learn?"),
    ("Food Memories", "Describe a meal that brings back fond memories."),
    ("Spirituality & Beliefs", "What role did faith or spirituality play in your life?"),
    ("Beautiful Experiences", "What was the most beautiful place you've ever visited?"),
    ("Summer Adventures", "How did you spend your summers as a child?"),
    ("Life Regrets", "What was your biggest regret and what did you learn from it?"),
    ("Standing Up", "Describe a time when you had to stand up for what you believed in."),
    ("Parental Wisdom", "What was the most important lesson your parents taught you?"),
    ("World Change", "What would you change about the world if you could?"),
    ("School Days", "What was your favorite subject in school and why?"),
    
    # Deeper Reflections (Weeks 31-40)
    ("Family Recipes", "Describe a family recipe and its significance."),
    ("Embarrassing Moments", "What was the most embarrassing moment of your life?"),
    ("First Car", "What was your first car and what memories do you have with it?"),
    ("Birthday Celebrations", "How did you celebrate your 16th birthday?"),
    ("Saying Goodbye", "What was the hardest goodbye you've had to say?"),
    ("Gratitude Moments", "Describe a time when you felt truly grateful."),
    ("Childhood Dreams", "What was your dream job as a child?"),
    ("Meaningful Gifts", "What was the most meaningful gift you've received?"),
    ("Career Failures", "How did you handle failure in your career?"),
    ("First Home", "What was your first apartment or house like?"),
    
    # Wisdom & Maturity (Weeks 41-50)
    ("Taking Risks", "Describe a time when you took a leap of faith."),
    ("Important Advice", "What was the most important piece of advice you received?"),
    ("Parenting Moments", "What was your favorite way to spend time with your children?"),
    ("Memorable Vacations", "What was the most memorable vacation you took?"),
    ("Inner Peace", "Describe a time when you felt completely at peace."),
    ("Entertainment Memories", "What was your first concert or show?"),
    ("Technology Evolution", "What was the most important technological change during your lifetime?"),
    ("Retirement Dreams", "How did you envision your retirement?"),
    ("Childhood Games", "What was your favorite game to play as a child?"),
    ("Personal Growth", "Describe a time when you surprised yourself."),
    
    # Final Reflections (Weeks 51-52)
    ("Historical Events", "What was the most important political event during your lifetime?"),
    ("Life Summary", "Looking back, what would you say was the most important theme of your life?")
]

# Sample responses data structure
sample_responses = {
    "1": {
        "week": 1,
        "theme": "Childhood Beginnings",
        "question": "What is your earliest childhood memory?",
        "answer": "Playing in the backyard with my sister. We had a big oak tree we used to climb.",
        "depth_prompt": "Can you describe the tree in more detail? What made it special to you?",
        "status": "answered",
        "timestamp": "2023-01-01 10:30:00"
    },
    "2": {
        "week": 2,
        "theme": "Family Bonds",
        "question": "Who was your best friend growing up and why?",
        "answer": "Tommy. We did everything together - fishing, playing baseball, exploring the woods.",
        "depth_prompt": "What was the most memorable adventure you had with Tommy?",
        "status": "answered",
        "timestamp": "2023-01-08 14:15:00"
    },
    "3": {
        "week": 3,
        "theme": "First Experiences",
        "question": "What was your first job and what did you learn from it?",
        "answer": "I worked at the local grocery store bagging groceries. I learned the value of hard work.",
        "depth_prompt": "What was the most challenging part of that job?",
        "status": "answered",
        "timestamp": "2023-01-15 09:45:00"
    }
}

# Initialize responses if not already done
if not st.session_state.responses:
    st.session_state.responses = sample_responses

def get_week_info(week_number):
    """Get theme and question for a specific week"""
    if 1 <= week_number <= 52:
        theme, question = week_themes[week_number - 1]
        return theme, question
    else:
        # Default to first week
        theme, question = week_themes[0]
        return theme, question

def save_response(week_number, answer):
    """Save a response to the session state"""
    week_str = str(week_number)
    if week_str not in st.session_state.responses:
        st.session_state.responses[week_str] = {}
    
    # Get theme and question for this week
    theme, question = get_week_info(week_number)
    st.session_state.responses[week_str]["week"] = week_number
    st.session_state.responses[week_str]["theme"] = theme
    st.session_state.responses[week_str]["question"] = question
    
    st.session_state.responses[week_str]["answer"] = answer
    st.session_state.responses[week_str]["status"] = "answered"
    st.session_state.responses[week_str]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add depth prompt if not already there
    if "depth_prompt" not in st.session_state.responses[week_str]:
        st.session_state.responses[week_str]["depth_prompt"] = generate_depth_prompt(
            st.session_state.responses[week_str]["question"], answer
        )

def generate_depth_prompt(question, answer):
    """Generate a prompt for deeper reflection (mock AI function)"""
    prompts = [
        f"Can you tell me more about {answer.split()[0] if answer else 'that'}?",
        f"What made that experience particularly meaningful to you?",
        f"How did that shape who you are today?",
        f"What would you want your children to know about that time?",
        f"If you could go back, what would you do differently?",
        f"What advice would you give to someone in a similar situation?"
    ]
    return random.choice(prompts)

def search_responses(query):
    """Search responses using natural language (mock AI function)"""
    results = []
    query_lower = query.lower()
    
    for week_str, response in st.session_state.responses.items():
        if "answer" in response and "question" in response:
            answer_lower = response["answer"].lower()
            question_lower = response["question"].lower()
            theme_lower = response["theme"].lower()
            
            # Simple keyword matching (in a real app, use embeddings)
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
    
    # Sort by week (ascending)
    results.sort(key=lambda x: x["week"])
    return results

def get_response_stats():
    """Get statistics about responses"""
    total_questions = 52
    answered_count = len([r for r in st.session_state.responses.values() if r.get("status") == "answered"])
    percentage = (answered_count / total_questions) * 100 if total_questions > 0 else 0
    
    return answered_count, percentage

def export_responses():
    """Export all responses as JSON"""
    return json.dumps(st.session_state.responses, indent=2)

def get_theme_progression():
    """Get theme progression statistics"""
    themes = {}
    for week_str, response in st.session_state.responses.items():
        if response.get("status") == "answered":
            theme = response["theme"]
            if theme not in themes:
                themes[theme] = 0
            themes[theme] += 1
    return themes

# Main app
st.set_page_config(page_title="52 Weeks Memoir", page_icon="📖", layout="wide")

# Title and description
st.title("📖 52 Weeks Memoir")
st.markdown("""
*Build a lifetime of memories, one themed week at a time*
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
    
    # Show sample week progression
    st.markdown("### Sample Week Progression")
    sample_weeks = pd.DataFrame([
        {"Week": 1, "Theme": "Childhood Beginnings", "Question": "What is your earliest childhood memory?"},
        {"Week": 2, "Theme": "Family Bonds", "Question": "Who was your best friend growing up?"},
        {"Week": 3, "Theme": "First Experiences", "Question": "What was your first job?"},
        {"Week": 52, "Theme": "Life Summary", "Question": "Looking back, what would you say was the most important theme of your life?"}
    ])
    st.dataframe(sample_weeks, use_container_width=True, hide_index=True)

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
                st.session_state.view_week = 51  # Go to week 51 if no current week
            st.rerun()
    
    with col2:
        if st.session_state.view_week:
            selected_week = st.number_input("Select week:", min_value=1, max_value=52, value=st.session_state.view_week)
        else:
            selected_week = st.number_input("Select week:", min_value=1, max_value=52, value=1)
        
        if st.session_state.view_week != selected_week:
            st.session_state.view_week = selected_week
            st.rerun()
    
    with col3:
        if st.button("Next Week ▶"):
            if st.session_state.view_week:
                new_week = min(52, st.session_state.view_week + 1)
                st.session_state.view_week = new_week
            else:
                st.session_state.view_week = 2  # Go to week 2 if no current week
            st.rerun()
    
    # Display question for selected week
    if st.session_state.view_week:
        week_number = st.session_state.view_week
    else:
        week_number = 1
    
    theme, question = get_week_info(week_number)
    
    st.markdown(f"### Week {week_number}")
    st.markdown(f"#### Theme: {theme}")
    st.markdown(f"**Question:** {question}")
    
    # Check if already answered
    week_str = str(week_number)
    if week_str in st.session_state.responses and st.session_state.responses[week_str].get("status") == "answered":
        st.success("✅ You've already answered this week's question!")
        st.markdown(f"**Your response:** {st.session_state.responses[week_str]['answer']}")
        
        if st.button("📝 Edit Response"):
            st.session_state.editing_week = week_number
            st.rerun()
    else:
        # Show response form
        with st.form("response_form"):
            answer = st.text_area("Your response:", height=200, 
                                value=st.session_state.responses.get(week_str, {}).get("answer", ""))
            submitted = st.form_submit_button("Save Response")
            
            if submitted:
                save_response(week_number, answer)
                st.success("Response saved!")
                st.rerun()
    
    # Editing existing response
    if st.session_state.editing_week:
        st.markdown("---")
        st.subheader(f"Editing Response for Week {st.session_state.editing_week}")
        edit_week_str = str(st.session_state.editing_week)
        edit_response = st.session_state.responses[edit_week_str]
        st.markdown(f"**Theme:** {edit_response['theme']}")
        st.markdown(f"**Question:** {edit_response['question']}")
        
        with st.form("edit_form"):
            edited_answer = st.text_area("Your response:", height=200, 
                                       value=edit_response.get("answer", ""))
            edit_submitted = st.form_submit_button("Update Response")
            
            if edit_submitted:
                save_response(st.session_state.editing_week, edited_answer)
                st.success("Response updated!")
                st.session_state.editing_week = None
                st.rerun()
    
    # Navigation
    st.markdown("---")
    if st.button("⬅️ Back to Role Selection"):
        st.session_state.user_type = None
        st.session_state.editing_week = None
        st.session_state.view_week = None
        st.rerun()

# Child's view
elif st.session_state.user_type == "child":
    st.subheader("Review & Guide Responses")
    
    # Stats
    answered_count, percentage = get_response_stats()
    col1, col2, col3 = st.columns(3)
    col1.metric("Weeks Completed", answered_count, "52 total")
    col2.metric("Completion", f"{percentage:.1f}%", "Progress")
    col3.metric("Weeks Remaining", 52 - answered_count)
    
    # Progress bar
    st.progress(percentage / 100)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📚 All Responses", "📊 Stats", "💾 Export"])
    
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
        st.markdown("### 📚 All Responses by Week")
        
        # Show all responses organized by week
        answered_weeks = []
        for week_str, response in st.session_state.responses.items():
            if response.get("status") == "answered":
                answered_weeks.append(int(week_str))
        
        if answered_weeks:
            answered_weeks.sort()
            
            # Create tabs for different theme sections
            theme_sections = [
                ("Foundation", 1, 10),
                ("Growth", 11, 20),
                ("Experiences", 21, 30),
                ("Wisdom", 31, 40),
                ("Reflections", 41, 52)
            ]
            
            section_tabs = st.tabs([section[0] for section in theme_sections])
            
            for i, (section_name, start_week, end_week) in enumerate(theme_sections):
                with section_tabs[i]:
                    st.markdown(f"#### {section_name} ({start_week}-{end_week})")
                    
                    section_weeks = [w for w in answered_weeks if start_week <= w <= end_week]
                    
                    if section_weeks:
                        for week_num in section_weeks:
                            week_str = str(week_num)
                            response = st.session_state.responses[week_str]
                            with st.expander(f"**Week {week_num}: {response['theme']}**"):
                                st.markdown(f"**Question:** {response['question']}")
                                st.markdown(f"**Answer:** {response['answer']}")
                                
                                # Depth prompt section
                                if response.get('depth_prompt'):
                                    st.markdown("**Suggested follow-up:**")
                                    st.info(response['depth_prompt'])
                                
                                # Send prompt button (mock)
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.caption(f"Answered: {response.get('timestamp', '')}")
                                with col2:
                                    if st.button("📤 Send Depth Prompt", key=f"send_{week_str}"):
                                        st.success(f"Depth prompt sent to parent for Week {week_num}")
                    else:
                        st.info(f"No responses yet in the {section_name} section.")
        else:
            st.info("No responses yet. Encourage your parent to start answering questions!")
    
    with tab3:
        st.markdown("### 📊 Response Statistics")
        
        # Theme progression
        theme_stats = get_theme_progression()
        if theme_stats:
            st.markdown("**Theme Completion:**")
            theme_df = pd.DataFrame(list(theme_stats.items()), columns=["Theme", "Completed"])
            theme_df = theme_df.sort_values("Theme")
            st.bar_chart(theme_df.set_index("Theme"))
            
            # Completion by section
            st.markdown("**Completion by Theme Section:**")
            section_completion = {}
            theme_sections = [
                ("Foundation", 1, 10),
                ("Growth", 11, 20),
                ("Experiences", 21, 30),
                ("Wisdom", 31, 40),
                ("Reflections", 41, 52)
            ]
            
            for section_name, start_week, end_week in theme_sections:
                section_total = end_week - start_week + 1
                section_answered = len([w for w in range(start_week, end_week + 1) 
                                      if str(w) in st.session_state.responses and 
                                      st.session_state.responses[str(w)].get("status") == "answered"])
                section_completion[section_name] = (section_answered / section_total) * 100 if section_total > 0 else 0
            
            section_df = pd.DataFrame(list(section_completion.items()), columns=["Section", "Completion %"])
            st.bar_chart(section_df.set_index("Section"))
        else:
            st.info("No response data available for statistics")
    
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
        
        st.markdown("### 📋 Response Summary")
        if st.session_state.responses:
            total_words = sum(len(response.get("answer", "").split()) 
                            for response in st.session_state.responses.values() 
                            if response.get("status") == "answered")
            st.metric("Total Words Written", f"{total_words:,}")
            
            # Show sample of responses
            st.markdown("**Sample Responses:**")
            sample_responses_list = list(st.session_state.responses.items())
            for week_str, response in sample_responses_list[:5]:
                if response.get("status") == "answered":
                    st.markdown(f"**Week {response['week']}: {response['theme']}**")
        else:
            st.info("No responses to export yet")
    
    # Navigation
    st.markdown("---")
    if st.button("⬅️ Back to Role Selection"):
        st.session_state.user_type = None
        st.rerun()

# Footer
st.markdown("---")
st.caption("52 Weeks Memoir - Preserving memories one week at a time")
