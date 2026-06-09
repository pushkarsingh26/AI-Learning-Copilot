import streamlit as st
import requests
import pandas as pd
import plotly.express as px

import os
import subprocess
import time
import sys

API_URL = os.getenv("API_URL", "http://127.0.0.1:8080")

# Auto-start FastAPI backend if running on localhost and not already online
if "127.0.0.1" in API_URL or "localhost" in API_URL:
    try:
        res = requests.get(f"{API_URL}/health", timeout=0.5)
        backend_online = (res.status_code == 200)
    except Exception:
        backend_online = False

    if not backend_online:
        try:
            subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8080"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(2.0)  # Give the backend a moment to spin up
        except Exception as e:
            print(f"Failed to auto-start backend: {e}")



st.set_page_config(page_title="AI Learning Copilot", layout="wide", page_icon="🎓")

# -- Navigation --
st.sidebar.title("🎓 AI Learning Copilot")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation Menu", 
    [
        "Dashboard",
        "Upload PDF", 
        "Ask Questions", 
        "Generate Quiz", 
        "Flashcards", 
        "Progress Tracking", 
        "Weak Topics", 
        "Adaptive Learning"
    ]
)

# Helper function
def check_health():
    try:
        res = requests.get(f"{API_URL}/health", timeout=3)
        return res.status_code == 200
    except:
        return False

# --- Page: Dashboard ---
if page == "Dashboard":
    st.title("📊 Dashboard")
    st.markdown("Welcome to your **AI Learning Copilot**. Here is an overview of your system and learning progress.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("System Status")
        with st.spinner("Checking API..."):
            is_healthy = check_health()
        if is_healthy:
            st.success("🟢 API is Online")
        else:
            st.error("🔴 API is Offline")
            
    try:
        progress_res = requests.get(f"{API_URL}/progress", timeout=5)
        weak_res = requests.get(f"{API_URL}/weak-topics", timeout=5)
        
        if progress_res.status_code == 200 and weak_res.status_code == 200:
            prog_data = progress_res.json()
            weak_data = weak_res.json()
            
            attempts = len(prog_data.get("attempts", []))
            accuracy = prog_data.get("overall_accuracy", 0.0)
            weak_count = len(weak_data)
            
            with col2:
                st.subheader("Total Quiz Attempts")
                st.metric(label="Quizzes Taken", value=attempts)
                
            with col3:
                st.subheader("Overall Accuracy")
                st.metric(label="Accuracy", value=f"{accuracy}%")
                
            st.markdown("---")
            if weak_count > 0:
                st.warning(f"⚠️ You have {weak_count} weak topic(s) to review.")
            else:
                st.success("🎉 You have no weak topics. Keep it up!")
        else:
            st.warning("Could not load analytics data. Ensure API is running.")
            
    except Exception as e:
        st.warning("Failed to connect to backend for analytics.")

# --- Page: Upload PDF ---
elif page == "Upload PDF":
    st.title("📄 Upload Learning Material")
    st.markdown("Upload your PDF documents to build your knowledge base.")
    
    uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])
    
    if st.button("Upload and Process"):
        if uploaded_file is not None:
            with st.spinner("Uploading, extracting, chunking, and embedding PDF..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{API_URL}/upload-pdf", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"✅ {data.get('message', 'PDF processed successfully')}!")
                        st.info(f"Generated {data.get('chunks', 0)} chunks for the knowledge base.")
                    else:
                        st.error(f"Error processing PDF: {response.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
        else:
            st.warning("Please choose a file to upload.")

# --- Page: Ask Questions ---
elif page == "Ask Questions":
    st.title("💬 Ask Questions")
    st.markdown("Query your uploaded documents using RAG.")
    
    question = st.text_input("What would you like to know?")
    
    if st.button("Ask Copilot"):
        if question.strip():
            with st.spinner("Finding answer from documents..."):
                try:
                    response = requests.post(f"{API_URL}/ask", json={"question": question.strip()})
                    if response.status_code == 200:
                        data = response.json()
                        st.markdown("### Answer")
                        st.info(data.get("answer", "No answer provided."))
                        
                        sources = data.get("sources", [])
                        if sources:
                            with st.expander("📚 Sources"):
                                for src in sources:
                                    st.write(f"- {src}")
                    else:
                        st.error(f"Failed to get answer: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
        else:
            st.warning("Please enter a question.")

# --- Page: Generate Quiz ---
elif page == "Generate Quiz":
    st.title("📝 Practice Quiz")
    st.markdown("Generate a 5-question multiple choice quiz on any topic.")
    
    topic = st.text_input("Enter Topic:")
    
    if st.button("Generate Quiz"):
        if topic.strip():
            with st.spinner(f"Generating quiz for '{topic}'..."):
                try:
                    response = requests.post(f"{API_URL}/generate-quiz", json={"topic": topic.strip()})
                    if response.status_code == 200:
                        st.session_state['quiz_data'] = response.json()
                        st.session_state['quiz_topic'] = topic.strip()
                        st.session_state['quiz_submitted'] = False
                        st.success("Quiz generated successfully!")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
        else:
            st.warning("Please enter a topic.")
            
    if 'quiz_data' in st.session_state and st.session_state.get('quiz_data'):
        st.markdown("---")
        st.subheader(f"Quiz: {st.session_state['quiz_topic']}")
        
        quiz = st.session_state['quiz_data']
        user_answers = {}
        
        with st.form("quiz_form"):
            for i, q in enumerate(quiz):
                st.markdown(f"**{i+1}. {q['question']}**")
                user_answers[i] = st.radio("Select your answer:", q['options'], key=f"q_{i}", index=None)
                st.markdown("<br>", unsafe_allow_html=True)
                
            submitted = st.form_submit_button("Submit Answers")
            
            if submitted:
                if None in user_answers.values():
                    st.warning("Please answer all questions before submitting.")
                else:
                    score = 0
                    for i, q in enumerate(quiz):
                        if user_answers[i] == q['answer']:
                            score += 1
                    
                    st.session_state['quiz_score'] = score
                    st.session_state['quiz_submitted'] = True

        if st.session_state.get('quiz_submitted'):
            score = st.session_state['quiz_score']
            total = len(quiz)
            pct = (score / total) * 100
            
            st.success(f"### Final Score: {score}/{total} ({pct:.1f}%)")
            
            # Show correct answers
            with st.expander("Review Answers"):
                for i, q in enumerate(quiz):
                    st.write(f"**Q{i+1}:** {q['question']}")
                    if user_answers[i] == q['answer']:
                        st.write(f"✅ Your Answer: {user_answers[i]}")
                    else:
                        st.write(f"❌ Your Answer: {user_answers[i]}")
                        st.write(f"**Correct Answer:** {q['answer']}")
                    st.write("---")
                        
            # Submit to backend
            try:
                submit_res = requests.post(f"{API_URL}/submit-quiz", json={
                    "topic": st.session_state['quiz_topic'],
                    "score": score,
                    "total": total
                })
                if submit_res.status_code == 200:
                    st.info("Score saved to progress tracker.")
            except Exception as e:
                st.error(f"Failed to record score: {e}")

# --- Page: Flashcards ---
elif page == "Flashcards":
    st.title("🗂️ Flashcards")
    st.markdown("Generate flashcards for quick revision.")
    
    topic = st.text_input("Enter Topic:")
    
    if st.button("Generate Flashcards"):
        if topic.strip():
            with st.spinner("Creating flashcards..."):
                try:
                    response = requests.post(f"{API_URL}/generate-flashcards", json={"topic": topic.strip()})
                    if response.status_code == 200:
                        cards = response.json()
                        st.success(f"Generated {len(cards)} flashcards!")
                        
                        for i, card in enumerate(cards):
                            with st.container():
                                st.markdown(f"#### Card {i+1}")
                                with st.expander(f"Q: {card['front']}"):
                                    st.info(f"**A:** {card['back']}")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
        else:
            st.warning("Please enter a topic.")

# --- Page: Progress Tracking ---
elif page == "Progress Tracking":
    st.title("📈 Progress Tracking")
    
    with st.spinner("Loading metrics..."):
        try:
            response = requests.get(f"{API_URL}/progress")
            if response.status_code == 200:
                data = response.json()
                overall = data.get("overall_accuracy", 0.0)
                attempts = data.get("attempts", [])
                
                st.metric("Overall Accuracy", f"{overall}%")
                
                if attempts:
                    st.subheader("Quiz History")
                    df = pd.DataFrame(attempts)
                    
                    df['created_at'] = pd.to_datetime(df['created_at'])
                    df['accuracy'] = (df['score'] / df['total']) * 100
                    
                    st.dataframe(df, use_container_width=True)
                    
                    st.subheader("Performance Trend")
                    fig = px.line(df, x='created_at', y='accuracy', markers=True, 
                                  title="Accuracy Over Time", 
                                  labels={'created_at': 'Date', 'accuracy': 'Accuracy (%)'},
                                  hover_data=['topic', 'score', 'total'])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.subheader("Performance By Topic")
                    topic_df = df.groupby('topic').agg({'score': 'sum', 'total': 'sum'}).reset_index()
                    topic_df['accuracy'] = (topic_df['score'] / topic_df['total']) * 100
                    fig2 = px.bar(topic_df, x='topic', y='accuracy', color='accuracy', 
                                  title="Average Accuracy by Topic",
                                  labels={'topic': 'Topic', 'accuracy': 'Average Accuracy (%)'},
                                  color_continuous_scale='RdYlGn')
                    st.plotly_chart(fig2, use_container_width=True)
                    
                else:
                    st.info("No quizzes taken yet. Complete a quiz to see your progress.")
            else:
                st.error("Failed to fetch progress data.")
        except Exception as e:
            st.error(f"Connection failed: {e}")

# --- Page: Weak Topics ---
elif page == "Weak Topics":
    st.title("🔍 Weak Topics")
    st.markdown("Review topics where your accuracy is below 70%.")
    
    with st.spinner("Analyzing topics..."):
        try:
            response = requests.get(f"{API_URL}/weak-topics")
            if response.status_code == 200:
                topics = response.json()
                if topics:
                    for t in topics:
                        st.warning(f"**{t['topic']}** - Accuracy: {t['accuracy']}%")
                        st.progress(t['accuracy'] / 100.0)
                else:
                    st.success("🎉 You don't have any weak topics right now! Great job.")
            else:
                st.error("Failed to load weak topics.")
        except Exception as e:
            st.error(f"Connection failed: {e}")

# --- Page: Adaptive Learning ---
elif page == "Adaptive Learning":
    st.title("🧠 Adaptive Learning")
    st.markdown("Let the Copilot generate a targeted quiz based on your weakest topic.")
    
    if st.button("Generate Adaptive Quiz"):
        with st.spinner("Finding weak topics and generating focused quiz..."):
            try:
                response = requests.get(f"{API_URL}/adaptive-quiz")
                if response.status_code == 200:
                    data = response.json()
                    if "message" in data:
                        st.info(data["message"])
                    else:
                        st.session_state['adaptive_data'] = data
                        st.session_state['adaptive_submitted'] = False
                        st.success(f"Generated adaptive module for your weakest topic: **{data['topic']}**")
                else:
                    st.error("Operation failed.")
            except Exception as e:
                 st.error(f"Connection failed: {e}")
                 
    if 'adaptive_data' in st.session_state and st.session_state.get('adaptive_data'):
        data = st.session_state['adaptive_data']
        quiz = data['quiz']
        topic = data['topic']
        
        st.markdown("---")
        st.subheader(f"Adaptive Quiz: {topic}")
        
        user_answers = {}
        
        with st.form("adaptive_form"):
            for i, q in enumerate(quiz):
                st.markdown(f"**{i+1}. {q['question']}**")
                user_answers[i] = st.radio("Select answer:", q['options'], key=f"adap_{i}", index=None)
                st.markdown("<br>", unsafe_allow_html=True)
                
            submitted = st.form_submit_button("Submit Adaptive Quiz")
            
            if submitted:
                if None in user_answers.values():
                    st.warning("Please answer all questions before submitting.")
                else:
                    score = 0
                    for i, q in enumerate(quiz):
                        if user_answers[i] == q['answer']:
                            score += 1
                            
                    st.session_state['adaptive_score'] = score
                    st.session_state['adaptive_submitted'] = True

        if st.session_state.get('adaptive_submitted'):
            score = st.session_state['adaptive_score']
            total = len(quiz)
            
            st.success(f"### Final Score: {score}/{total}")
            
            # Show review
            with st.expander("Review Adaptive Answers"):
                for i, q in enumerate(quiz):
                    st.write(f"**Q{i+1}:** {q['question']}")
                    if user_answers[i] == q['answer']:
                        st.write(f"✅ Your Answer: {user_answers[i]}")
                    else:
                        st.write(f"❌ Your Answer: {user_answers[i]}")
                        st.write(f"**Correct Answer:** {q['answer']}")
                    st.write("---")

            # Submit score to backend
            try:
                requests.post(f"{API_URL}/submit-quiz", json={
                    "topic": topic,
                    "score": score,
                    "total": total
                })
                st.info("Adaptive score recorded.")
            except Exception as e:
                st.error("Failed to record score.")
