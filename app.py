import streamlit as st
    
# Define class schedule with added URLs for materials
classes = {
    "Monday": [
        {"time": "8:30 - 10:30", "subject": "Operation Research 1", "classroom": "Ae", "link": "https://stem.elearning.unipd.it/course/view.php?id=6475"},
        {"time": "10:30 - 12:30", "subject": "Machine Learning", "classroom": "Ae", "link": "https://stem.elearning.unipd.it/course/view.php?id=7045"}
    ],
    "Tuesday": [
        {"time": "12:30 - 14:30", "subject": "Automata", "classroom": "Ae", "link": "https://stem.elearning.unipd.it/course/view.php?id=6403"},
        {"time": "14:30 - 16:30", "subject": "Operation Research 1", "classroom": "De", "link": "https://stem.elearning.unipd.it/course/view.php?id=6475"},
        {"time": "16:30 - 18:30", "subject": "Intelligent Robotics", "classroom": "Te,Ue", "link": "#"}
    ],
    "Wednesday": [
        {"time": "12:30 - 14:30", "subject": "Automata", "classroom": "Ce", "link": "https://stem.elearning.unipd.it/course/view.php?id=6403"},
        {"time": "12:30 - 14:30", "subject": "Intelligent Robotics", "classroom": "Le", "link": "#"},
        {"time": "14:30 - 16:30", "subject": "Operation Research 1", "classroom": "Ve", "link": "https://stem.elearning.unipd.it/course/view.php?id=6475"}
    ],
    "Friday": [
        {"time": "10:30 - 12:30", "subject": "Machine Learning", "classroom": "Ae", "link": "https://stem.elearning.unipd.it/course/view.php?id=7045"},
        {"time": "12:30 - 14:30", "subject": "Automata", "classroom": "Ae", "link": "https://stem.elearning.unipd.it/course/view.php?id=6403"},
        {"time": "14:30 - 16:30", "subject": "Intelligent Robotics", "classroom": "De", "link": "#"}
    ]
}

# Extract unique subjects for filtering
unique_subjects = sorted(set([cls['subject'] for day in classes for cls in classes[day]]))

def display_classes(day, subject_filter=None):
    st.markdown(f"## 📅 {day}'s Schedule")
    classes_for_day = classes.get(day, [])
    if subject_filter:
        classes_for_day = [cls for cls in classes_for_day if cls['subject'] == subject_filter]
    
    if not classes_for_day:
        st.markdown("### 🎉 No classes today!")
        return
    
    # Display the schedule with enhanced UI
    for cls in classes_for_day:
        with st.expander(f"{cls['time']}: {cls['subject']} 📘", expanded=True):
            st.markdown(f"🕒 **Time**: {cls['time']}")
            st.markdown(f"🚪 **Classroom**: {cls['classroom']}")
            st.markdown(f"[🔗 Go to Materials]({cls['link']})", unsafe_allow_html=True)



def main():
    st.title("🦅 Orari But Better (OBB)")
    st.markdown("### Specialized App for Computer Engineering Courses @UNIPD")
    
    page = st.sidebar.selectbox("Navigate", ["Home", "Monday", "Tuesday", "Wednesday", "Friday"])

    if page == "Home":
        st.markdown("#### 🏠 Welcome to the **OBB** App!")
        st.markdown("Navigate to a specific day using the dropdown on the left to view the class schedules.")
    else:
        subject_filter = st.sidebar.selectbox("Filter by Subject (optional)", ["All"] + unique_subjects)
        if subject_filter == "All":
            subject_filter = None
        display_classes(page, subject_filter)

if __name__ == "__main__":
    main()
