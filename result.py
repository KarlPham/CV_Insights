import streamlit as st
from match_score import get_match_score
import pandas as pd
import matplotlib.pyplot as plt
from skills_suggestion import get_skill_suggestions
from question_generator import generate_and_save_interview_questions

def show_result(conn):
    st.title(" CV_insights result")

    # Check if resume & JD text are available
    if "resume_text" not in st.session_state or "jd_text" not in st.session_state:
        st.warning(" Resume and Job Description not found. Please upload them first.")
        return


    # Display Tabs
    tab1, tab2, tab3 = st.tabs([" Match Score", " Skill Suggestions", " Interview Questions"])

    with tab1:
        st.subheader(" Resume vs Job Description Match")

        if "match_score_result" not in st.session_state:
            if st.button("Analyze"):
                with st.spinner("Analyzing your resume and job description..."):
                    result_obj = get_match_score(
                        conn,
                        st.session_state["resume_text"],
                        st.session_state["jd_text"]
                    )
                st.rerun()
        else:
            result = st.session_state["match_score_result"]

            # Overall Match Score
            score = result.match_score
            st.subheader(f" Overall Match Score: {score}/100")
            st.progress(score / 100)

            st.divider()
            # 📊 Bar chart
            criteria = result.criteria.model_dump()
            df = pd.DataFrame(list(criteria.items()), columns=["Criteria", "Score"]).set_index("Criteria")
            st.markdown("###  Score Breakdown (Line Chart)")
            st.line_chart(df)

            st.divider()
            # 🥧 Pie Chart
            st.markdown("### Criteria Distribution (Pie Chart)")
            labels = list(criteria.keys())
            sizes = list(criteria.values())

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

            st.divider()

            # ✅🛠️ Feedback
            st.markdown("### What You Did Well")
            for item in result.did_well:
                st.success(f"• {item}")

            st.markdown("### What You Didn’t Do Well")
            for item in result.not_well:
                st.error(f"• {item}")

            st.markdown("###  What You Can Improve")
            for item in result.need_improve:
                st.info(f"• {item}")



    with tab2:
        st.subheader("Suggestions Skills")

        if "skills_suggestions" not in st.session_state:
            if st.button("test"):
                with st.spinner("Analyzing skills suggestions for your resume and job description..."):
                    result_obj = get_skill_suggestions(
                        conn,
                        st.session_state["resume_text"],
                        st.session_state["jd_text"]
                    )
                st.rerun()
        else:
            result = st.session_state["skills_suggestions"]

            st.success("✅ Suggestions generated successfully!")
            st.markdown("Below are categorized skill suggestions based on your resume and the job description:")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### Technical Skills")
                for skill in result.tech_skills:
                    st.markdown(
                        f"<div style='background-color:#e8f0fe;padding:8px;border-radius:8px;margin-bottom:6px; color:black;'> {skill}</div>",
                        unsafe_allow_html=True)

            with col2:
                st.markdown("#### Soft Skills")
                for skill in result.soft_skills:
                    st.markdown(
                        f"<div style='background-color:#fcefe3;padding:8px;border-radius:8px;margin-bottom:6px;color:black;'> {skill}</div>",
                        unsafe_allow_html=True)

            with col3:
                st.markdown("#### Work Experience")
                for exp in result.work_exp:
                    st.markdown(
                        f"<div style='background-color:#e6ffee;padding:8px;border-radius:8px;margin-bottom:6px;color:black;'> {exp}</div>",
                        unsafe_allow_html=True)

        with tab3:
            st.subheader("🗣️ AI-Generated Interview Questions")

        # Ensure match_id is available
            if "match_id" not in st.session_state:
                st.warning("❗ Please analyze your resume first to generate interview questions.")
                return

            if "interview_questions" not in st.session_state:
                if st.button("Generate Interview Questions"):
                    with st.spinner("Generating interview questions..."):
                        try:
                            result_obj = generate_and_save_interview_questions(
                                conn,
                                st.session_state["resume_text"],
                                st.session_state["jd_text"],
                                st.session_state["match_id"]
                            )
                            st.session_state["interview_questions"] = result_obj
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Failed to generate questions: {e}")
            else:
                questions = st.session_state["interview_questions"]

                if questions.tech_questions:
                    st.subheader("💻 Technical Questions")
                    for q in questions.tech_questions:
                        st.markdown(f"- {q}")
                else:
                    st.info("No technical questions generated.")

                if questions.behav_questions:
                    st.subheader("🧠 Behavioral Questions")
                    for q in questions.behav_questions:
                        st.markdown(f"- {q}")
                else:
                    st.info("No behavioral questions generated.")
