import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import json
from collections import defaultdict

# Initialize session state
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'editing_date' not in st.session_state:
    st.session_state.editing_date = None
if 'view_date' not in st.session_state:
    st.session_state.view_date = None

# Sample questions database
sample_questions = [
    "What is your earliest childhood memory?",
    "Who was your best friend growing up and why?",
    "What was your first job and what did you learn from it?",
    "Describe a time you overcame a significant challenge.",
    "What traditions did your family have during holidays?",
    "What advice would you give to your younger self?",
    "What moment in history do you wish you could have witnessed?",
    "What was your proudest achievement and why?",
    "How did you meet your spouse/partner?",
    "What values did your parents teach you that you still live by?",
    "What was your favorite book or movie as a child?",
    "Describe a place that holds special meaning for you.",
    "What skill do you wish you had learned earlier in life?",
    "What was the most difficult decision you ever had to make?",
    "How has your hometown changed since you were young?",
    "What do you want to be remembered for?",
    "What was your biggest fear growing up and how did you overcome it?",
    "Describe a time when you helped someone in need.",
    "What invention in your lifetime has impacted you the most?",
    "What would you do if you knew you couldn't fail?",
    "What is something you've always wanted to learn?",
    "Describe a meal that brings back fond memories.",
    "What role did faith or spirituality play in your life?",
    "What was the most beautiful place you've ever visited?",
    "How did you spend your summers as a child?",
    "What was your biggest regret and what did you learn from it?",
    "Describe a time when you had to stand up for what you believed in.",
    "What was the most important lesson your parents taught you?",
    "What would you change about the world if you could?",
    "What was your favorite subject in school and why?",
    "Describe a family recipe and its significance.",
    "What was the most embarrassing moment of your life?",
    "What was your first car and what memories do you have with it?",
    "How did you celebrate your 16th birthday?",
    "What was the hardest goodbye you've had to say?",
    "Describe a time when you felt truly grateful.",
    "What was your dream job as a child?",
    "What was the most meaningful gift you've received?",
    "How did you handle failure in your career?",
    "What was your first apartment or house like?",
    "Describe a time when you took a leap of faith.",
    "What was the most important piece of advice you received?",
    "What was your favorite way to spend time with your children?",
    "What was the most memorable vacation you took?",
    "Describe a time when you felt completely at peace.",
    "What was your first concert or show?",
    "What was the most important technological change during your lifetime?",
    "How did you envision your retirement?",
    "What was your favorite game to play as a child?",
    "Describe a time when you surprised yourself.",
    "What was the most important political event during your lifetime?",
    "What was your biggest financial lesson?",
    "How did you balance work and family life?",
    "What was the most interesting person you've met?",
    "Describe a time when you felt truly proud of someone else.",
    "What was your first experience with technology?",
    "What was the most beautiful sunset or sunrise you've seen?",
    "How did you handle major life transitions?",
    "What was your favorite holiday tradition?",
    "Describe a time when you had to forgive someone.",
    "What was the most important relationship in your life?",
    "What was your biggest act of kindness?",
    "How did you stay healthy throughout your life?",
    "What was the most memorable wedding you attended?",
    "Describe a time when you felt completely understood.",
    "What was your first experience with travel?",
    "What was the most important social change during your lifetime?",
    "How did you handle loss in your family?",
    "What was your favorite decade and why?",
    "Describe a time when you felt truly inspired.",
    "What was the most important lesson from your career?",
    "What was your biggest financial success?",
    "How did you maintain friendships over the years?",
    "What was the most memorable birthday celebration?",
    "Describe a time when you had to make a sacrifice for someone else.",
    "What was your first experience with nature?",
    "What was the most important cultural event during your lifetime?",
    "How did you handle major world events?",
    "What was your favorite way to relax?",
    "Describe a time when you felt completely fulfilled.",
    "What was your first experience with art or music?",
    "What was the most important scientific advancement during your lifetime?",
    "How did you handle aging?",
    "What was your favorite family tradition?",
    "Describe a time when you felt truly loved.",
    "What was your first experience with literature?",
    "What was the most important educational change during your lifetime?",
    "How did you handle changes in your community?",
    "What was your favorite way to celebrate achievements?",
    "Describe a time when you felt completely at home.",
    "What was your first experience with sports?",
    "What was the most important economic change during your lifetime?",
    "How did you handle changes in your family?",
    "What was your favorite way to spend time alone?",
    "Describe a time when you felt truly accomplished.",
    "What was your first experience with food from another culture?",
    "What was the most important environmental change during your lifetime?",
    "How did you handle changes in technology?",
    "What was your favorite way to spend time with friends?",
    "Describe a time when you felt truly hopeful.",
    "What was your first experience with a different religion?",
    "What was the most important medical advancement during your lifetime?",
    "How did you handle changes in politics?",
    "What was your favorite way to learn something new?",
    "Describe a time when you felt truly connected to others.",
    "What was your first experience with a different country?",
    "What was the most important legal change during your lifetime?",
    "How did you handle changes in fashion?",
    "What was your favorite way to express creativity?",
    "Describe a time when you felt truly grateful for your health.",
    "What was your first experience with a different generation?",
    "What was the most important communication advancement during your lifetime?",
    "How did you handle changes in transportation?",
    "What was your favorite way to help others?",
    "Describe a time when you felt truly proud of your community.",
    "What was your first experience with a different socioeconomic background?",
    "What was the most important space exploration during your lifetime?",
    "How did you handle changes in entertainment?",
    "What was your favorite way to preserve memories?",
    "Describe a time when you felt truly grateful for your family.",
    "What was your first experience with a different race or ethnicity?",
    "What was the most important discovery during your lifetime?",
    "How did you handle changes in gender roles?",
    "What was your favorite way to share knowledge?",
    "Describe a time when you felt truly grateful for your opportunities.",
    "What was your first experience with a different political system?",
    "What was the most important architectural change during your lifetime?",
    "How did you handle changes in family structures?",
    "What was your favorite way to celebrate milestones?",
    "Describe a time when you felt truly grateful for your freedom.",
    "What was your first experience with a different educational system?",
    "What was the most important artistic movement during your lifetime?",
    "How did you handle changes in work environments?",
    "What was your favorite way to connect with nature?",
    "Describe a time when you felt truly grateful for your friendships.",
    "What was your first experience with a different economic system?",
    "What was the most important philosophical idea during your lifetime?",
    "How did you handle changes in social norms?",
    "What was your favorite way to contribute to society?",
    "Describe a time when you felt truly grateful for your experiences."
]

# Initialize questions if not already done
if not st.session_state.questions:
    st.session_state.questions = sample_questions

# Sample responses data structure
sample_responses = {
    "2023-01-01": {
        "question": "What is your earliest childhood memory?",
        "answer": "Playing in the backyard with my sister. We had a big oak tree we used to climb.",
        "depth_prompt": "Can you describe the tree in more detail? What made it special to you?",
        "status": "answered",
        "timestamp": "2023-01-01 10:30:00"
    },
    "2023-01-02": {
        "question": "Who was your best friend growing up and why?",
        "answer": "Tommy. We did everything together - fishing, playing baseball, exploring the woods.",
        "depth_prompt": "What was the most memorable adventure you had with Tommy?",
        "status": "answered",
        "timestamp": "2023-01-02 14:15:00"
    },
    "2023-01-03": {
        "question": "What was your first job and what did you learn from it?",
        "answer": "I worked at the local grocery store bagging groceries. I learned the value of hard work.",
        "depth_prompt": "What was the most challenging part of that job?",
        "status": "answered",
        "timestamp": "2023-01-03 09:45:00"
    }
}

# Initialize responses if not already done
if not st.session_state.responses:
    st.session_state.responses = sample_responses

def get_question_for_date(date_str):
    """Get question for a specific date"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        day_of_year = date_obj.timetuple().tm_yday
        question_index = (day_of_year - 1) % len(st.session_state.questions)
        return st.session_state.questions[question_index]
    except ValueError:
        # Fallback to today's question
        _, question = get_todays_question()
        return question

def get_todays_question():
    """Get today's question based on the date"""
    today = datetime.now().strftime("%Y-%m-%d")
    day_of_year = datetime.now().timetuple().tm_yday
    
    # Use day of year to select question (cycling through if needed)
    question_index = (day_of_year - 1) % len(st.session_state.questions)
    question = st.session_state.questions[question_index]
    
    return today, question

def save_response(date, answer):
    """Save a response to the session state"""
    if date not in st.session_state.responses:
        st.session_state.responses[date] = {}
    
    # Get question for this date
    question = get_question_for_date(date)
    st.session_state.responses[date]["question"] = question
    
    st.session_state.responses[date]["answer"] = answer
    st.session_state.responses[date]["status"] = "answered"
    st.session_state.responses[date]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add depth prompt if not already there
    if "depth_prompt" not in st.session_state.responses[date]:
        st.session_state.responses[date]["depth_prompt"] = generate_depth_prompt(
            st.session_state.responses[date]["question"], answer
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
    
    for date, response in st.session_state.responses.items():
        if "answer" in response and "question" in response:
            answer_lower = response["answer"].lower()
            question_lower = response["question"].lower()
            
            # Simple keyword matching (in a real app, use embeddings)
            if (query_lower in answer_lower or 
                query_lower in question_lower or
                any(word in answer_lower for word in query_lower.split()) or
                any(word in question_lower for word in query_lower.split())):
                results.append({
                    "date": date,
                    "question": response["question"],
                    "answer": response["answer"],
                    "timestamp": response.get("timestamp", "")
                })
    
    # Sort by date (newest first)
    results.sort(key=lambda x: x["date"], reverse=True)
    return results

def get_response_stats():
    """Get statistics about responses"""
    total_questions = 365
    answered_count = len([r for r in st.session_state.responses.values() if r.get("status") == "answered"])
    percentage = (answered_count / total_questions) * 100 if total_questions > 0 else 0
    
    return answered_count, percentage

def export_responses():
    """Export all responses as JSON"""
    return json.dumps(st.session_state.responses, indent=2)

def get_monthly_stats():
    """Get monthly response statistics"""
    monthly_data = {}
    for date_str, response in st.session_state.responses.items():
        if response.get("status") == "answered":
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                month_key = date_obj.strftime("%Y-%m")
                if month_key not in monthly_data:
                    monthly_data[month_key] = 0
                monthly_data[month_key] += 1
            except ValueError:
                pass  # Skip invalid dates
    return monthly_data

# Main app
st.set_page_config(page_title="52 Weeks Memoir", page_icon="📖", layout="wide")

# Title and description
st.title("📖 52 Weeks Memoir")
st.markdown("""
*Build a lifetime of memories, one question at a time*
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
    
    # Show some sample responses to demonstrate functionality
    st.markdown("### Sample Responses")
    sample_df = pd.DataFrame([
        {"Date": "2023-01-01", "Question": "What is your earliest childhood memory?", "Answer": "Playing in the backyard with my sister..."},
        {"Date": "2023-01-02", "Question": "Who was your best friend growing up?", "Answer": "Tommy. We did everything together..."},
        {"Date": "2023-01-03", "Question": "What was your first job?", "Answer": "I worked at the local grocery store..."}
    ])
    st.dataframe(sample_df, use_container_width=True, hide_index=True)

# Parent's view
elif st.session_state.user_type == "parent":
    st.subheader("Answer Questions")
    
    # Date navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("◀ Previous Day"):
            if st.session_state.view_date:
                current_date = datetime.strptime(st.session_state.view_date, "%Y-%m-%d")
                new_date = current_date - timedelta(days=1)
                st.session_state.view_date = new_date.strftime("%Y-%m-%d")
            else:
                current_date = datetime.now()
                new_date = current_date - timedelta(days=1)
                st.session_state.view_date = new_date.strftime("%Y-%m-%d")
            st.rerun()
    
    with col2:
        if st.session_state.view_date:
            selected_date = st.date_input("Select date:", datetime.strptime(st.session_state.view_date, "%Y-%m-%d"))
        else:
            selected_date = st.date_input("Select date:", datetime.now())
        
        if st.session_state.view_date != selected_date.strftime("%Y-%m-%d"):
            st.session_state.view_date = selected_date.strftime("%Y-%m-%d")
            st.rerun()
    
    with col3:
        if st.button("Next Day ▶"):
            if st.session_state.view_date:
                current_date = datetime.strptime(st.session_state.view_date, "%Y-%m-%d")
                new_date = current_date + timedelta(days=1)
                st.session_state.view_date = new_date.strftime("%Y-%m-%d")
            else:
                current_date = datetime.now()
                new_date = current_date + timedelta(days=1)
                st.session_state.view_date = new_date.strftime("%Y-%m-%d")
            st.rerun()
    
    # Display question for selected date
    if st.session_state.view_date:
        date_str = st.session_state.view_date
        question = get_question_for_date(date_str)
    else:
        date_str, question = get_todays_question()
    
    st.markdown(f"### 📅 {date_str}")
    st.markdown(f"#### {question}")
    
    # Check if already answered
    if date_str in st.session_state.responses and st.session_state.responses[date_str].get("status") == "answered":
        st.success("✅ You've already answered this question!")
        st.markdown(f"**Your response:** {st.session_state.responses[date_str]['answer']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Edit Response"):
                st.session_state.editing_date = date_str
                st.rerun()
    else:
        # Show response form
        with st.form("response_form"):
            answer = st.text_area("Your response:", height=200, 
                                value=st.session_state.responses.get(date_str, {}).get("answer", ""))
            submitted = st.form_submit_button("Save Response")
            
            if submitted:
                save_response(date_str, answer)
                st.success("Response saved!")
                st.rerun()
    
    # Editing existing response
    if st.session_state.editing_date:
        st.markdown("---")
        st.subheader(f"Editing Response for {st.session_state.editing_date}")
        edit_response = st.session_state.responses[st.session_state.editing_date]
        st.markdown(f"**Question:** {edit_response['question']}")
        
        with st.form("edit_form"):
            edited_answer = st.text_area("Your response:", height=200, 
                                       value=edit_response.get("answer", ""))
            edit_submitted = st.form_submit_button("Update Response")
            
            if edit_submitted:
                save_response(st.session_state.editing_date, edited_answer)
                st.success("Response updated!")
                st.session_state.editing_date = None
                st.rerun()
    
    # Navigation
    st.markdown("---")
    if st.button("⬅️ Back to Role Selection"):
        st.session_state.user_type = None
        st.session_state.editing_date = None
        st.session_state.view_date = None
        st.rerun()

# Child's view
elif st.session_state.user_type == "child":
    st.subheader("Review & Guide Responses")
    
    # Stats
    answered_count, percentage = get_response_stats()
    col1, col2, col3 = st.columns(3)
    col1.metric("Questions Answered", answered_count, "365 total")
    col2.metric("Completion", f"{percentage:.1f}%", "Progress")
    col3.metric("Days Remaining", 365 - answered_count)
    
    # Progress bar
    st.progress(percentage / 100)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📚 Recent", "📊 Stats", "💾 Export"])
    
    with tab1:
        st.markdown("### 🔍 Search Responses")
        search_query = st.text_input("Search by keyword or phrase:")
        
        if search_query:
            st.session_state.search_results = search_responses(search_query)
            st.markdown(f"### Search Results ({len(st.session_state.search_results)} found)")
            
            for result in st.session_state.search_results:
                with st.expander(f"**{result['date']}**: {result['question'][:50]}..."):
                    st.markdown(f"**Question:** {result['question']}")
                    st.markdown(f"**Answer:** {result['answer']}")
                    if result['timestamp']:
                        st.caption(f"Answered: {result['timestamp']}")
        else:
            st.info("Enter a search term to find specific responses")
    
    with tab2:
        st.markdown("### 📚 Recent Responses")
        
        # Convert responses to DataFrame for easier handling
        df_data = []
        for date, response in st.session_state.responses.items():
            if response.get("status") == "answered":
                df_data.append({
                    "Date": date,
                    "Question": response["question"][:60] + "..." if len(response["question"]) > 60 else response["question"],
                    "Answer": response["answer"][:100] + "..." if len(response["answer"]) > 100 else response["answer"],
                    "Depth Prompt": response.get("depth_prompt", ""),
                    "Timestamp": response.get("timestamp", "")
                })
        
        if df_data:
            df = pd.DataFrame(df_data)
            df = df.sort_values("Date", ascending=False)
            
            # Show recent responses
            for i, row in df.head(15).iterrows():
                with st.expander(f"**{row['Date']}**: {row['Question']}"):
                    st.markdown(f"**Question:** {st.session_state.responses[row['Date']]['question']}")
                    st.markdown(f"**Answer:** {st.session_state.responses[row['Date']]['answer']}")
                    
                    # Depth prompt section
                    if row['Depth Prompt']:
                        st.markdown("**Suggested follow-up:**")
                        st.info(row['Depth Prompt'])
                    
                    # Send prompt button (mock)
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.caption(f"Answered: {row['Timestamp']}")
                    with col2:
                        if st.button("📤 Send Depth Prompt", key=f"send_{row['Date']}"):
                            st.success(f"Depth prompt sent to parent for {row['Date']}")
        else:
            st.info("No responses yet. Encourage your parent to start answering questions!")
    
    with tab3:
        st.markdown("### 📊 Response Statistics")
        
        # Monthly activity
        monthly_stats = get_monthly_stats()
        if monthly_stats:
            st.markdown("**Monthly Activity:**")
            monthly_df = pd.DataFrame(list(monthly_stats.items()), columns=["Month", "Responses"])
            monthly_df = monthly_df.sort_values("Month")
            st.bar_chart(monthly_df.set_index("Month"))
            
            # Weekly trend (last 8 weeks)
            st.markdown("**Recent Weekly Activity:**")
            weekly_data = {}
            for date_str in st.session_state.responses.keys():
                if st.session_state.responses[date_str].get("status") == "answered":
                    try:
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        # Get start of week (Monday)
                        week_start = date_obj - timedelta(days=date_obj.weekday())
                        week_key = week_start.strftime("%Y-%m-%d")
                        if week_key not in weekly_data:
                            weekly_data[week_key] = 0
                        weekly_data[week_key] += 1
                    except ValueError:
                        pass
            
            if weekly_data:
                weekly_df = pd.DataFrame(list(weekly_data.items()), columns=["Week", "Responses"])
                weekly_df = weekly_df.sort_values("Week").tail(8)
                st.line_chart(weekly_df.set_index("Week"))
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
            for date, response in sample_responses_list[:5]:
                if response.get("status") == "answered":
                    st.markdown(f"**{date}**: {response['question'][:50]}...")
        else:
            st.info("No responses to export yet")
    
    # Navigation
    st.markdown("---")
    if st.button("⬅️ Back to Role Selection"):
        st.session_state.user_type = None
        st.rerun()

# Footer
st.markdown("---")
st.caption("52 Weeks Memoir - Preserving memories one question at a time")
