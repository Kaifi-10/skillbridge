def get_career_path_prompt(skills, interests, education, experience):
    return f"""
    I am a career coach. Analyze the following user skills and suggest 3 suitable career paths with reasons for each.
    Skills: {skills}
    Interests: {interests}
    Education: {education}
    Experience: {experience}
    """

def get_roadmap_prompt(skills, goal):
    return f"""
    Based on the user’s current skills: {skills} and their goal to become a {goal},
    generate a 3-month weekly learning roadmap including:
    - Skills to learn
    - Recommended online resources
    - Project ideas
    """

def get_resume_feedback_prompt(resume_text, job_role):
    return f"""
    You are an expert resume reviewer. Review this resume and suggest:
    - Key improvements
    - Missing skills or experience
    - Summary and formatting suggestions
    Resume:
    {resume_text}
    Job Role: {job_role}
    """
