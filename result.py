import streamlit as st
from match_score import get_match_score
import pandas as pd
import matplotlib.pyplot as plt
from skills_suggestion import get_skill_suggestions

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
        st.subheader("AI-Generated Interview Questions")
        st.info("🚧 Coming soon: This section will provide tailored interview questions based on your resume and job description.")