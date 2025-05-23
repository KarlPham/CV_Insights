-- Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resume Table
CREATE TABLE resume (
    resume_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    file_path VARCHAR(50),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job Description Table
CREATE TABLE job_description (
    job_desc_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    file_path VARCHAR(50),
    description_text TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Match Scores Table
CREATE TABLE match_scores (
    match_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    resume_id INTEGER REFERENCES resume(resume_id) ON DELETE CASCADE,
    job_desc_id INTEGER REFERENCES job_description(job_desc_id) ON DELETE CASCADE,
    match_score DECIMAL(5,2),
    did_well TEXT,
    not_well TEXT,
    need_focus TEXT,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Suggestion Table
CREATE TABLE suggestion (
    suggestion_id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES match_scores(match_id) ON DELETE CASCADE,
    tech_skills TEXT,
    soft_skills TEXT,
    work_exp TEXT,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interview Question Table
CREATE TABLE interview_question (
    question_id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES match_scores(match_id) ON DELETE CASCADE,
    tech_questions TEXT,
    behav_questions TEXT,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);