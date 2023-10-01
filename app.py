import streamlit as st

# Define class schedule
classes = {
    "Monday": [
        {"time": "8:30 - 10:30", "subject": "Operation Research 1", "classroom": "Ae"},
        {"time": "10:30 - 12:30", "subject": "Machine Learning", "classroom": "Ae"}
    ],
    "Tuesday": [
        {"time": "12:30 - 14:30", "subject": "Automata", "classroom": "Ae"},
        {"time": "14:30 - 16:30", "subject": "Operation Research 1", "classroom": "De"},
        {"time": "16:30 - 18:30", "subject": "Intelligent Robotics", "classroom": "Te,Ue"}
    ],
    "Wednesday": [
        {"time": "12:30 - 14:30", "subject": "Automata", "classroom": "Ce"},
        {"time": "12:30 - 14:30", "subject": "Intelligent Robotics", "classroom": "Le"},
        {"time": "14:30 - 16:30", "subject": "Operation Research 1", "classroom": "Ve"}
    ],
    "Friday": [
        {"time": "10:30 - 12:30", "subject": "Machine Learning", "classroom": "Ae"},
        {"time": "12:30 - 14:30", "subject": "Automata", "classroom": "Ae"},
        {"time": "14:30 - 16:30", "subject": "Intelligent Robotics", "classroom": "De"}
    ]
}

# Extract unique subjects for filtering
unique_subjects = sorted(set([cls['subject'] for day in classes for cls in classes[day]]))

def display_classes(day, subject_filter=None):
    """
    Display classes for a given day.
    """
    classes_for_day = classes.get(day, [])
    if subject_filter:
        classes_for_day = [cls for cls in classes_for_day if cls['subject'] == subject_filter]

    st.markdown(f"### {day}'s Schedule")

    if not classes_for_day:
        st.markdown("No classes today! 🎉")
        return

    # Use tables for a cleaner display
    table_data = [("Time", "Subject", "Classroom")]
    for cls in classes_for_day:
        table_data.append((cls['time'], cls['subject'], cls['classroom']))
    st.table(table_data)

def main():
    st.title("🦅 Orari But Better (OBB)")
    st.markdown("Specialized App for Computer Engineering Courses @UNIPD")
    st.markdown("Choose a day to view the classes:")

    day = st.selectbox("Select Day", list(classes.keys()))
    subject_filter = st.selectbox("Filter by Subject (optional)", ["All"] + unique_subjects)
    if subject_filter == "All":
        subject_filter = None
    display_classes(day, subject_filter)

if __name__ == "__main__":
    main()
