import streamlit as st
import replicate
#import os
def generate_llama2_response(prompt_input):
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-13B'], key='selected_model')
    llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
        
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        string_dialogue += f"{dict_message['role'].capitalize()}: {dict_message['content']}\n\n"
    output = replicate.run(llm, 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                "repetition_penalty": 1})
    return output

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    
    
# This function handles the users' tasks
def handle_tasks(user):
    if user:
        st.subheader(f"{user}'s Tasks")
        general_tasks = ['Attend Machine Learning Lecture', 'Submit Assignment', 'Prepare for Exams']
        
        # Creating a key for each user to store their specific tasks
        user_tasks_key = f"{user}_tasks"
        if user_tasks_key not in st.session_state:
            st.session_state[user_tasks_key] = {}
        
        # Displaying general tasks and user's progress
        for task in general_tasks:
            if task not in st.session_state[user_tasks_key]:
                st.session_state[user_tasks_key][task] = "Not Started"
            
            st.session_state[user_tasks_key][task] = st.selectbox(
                f"{task} - Status", ["Not Started", "In Progress", "Completed"], 
                key=f"{user}_{task}", 
                index=["Not Started", "In Progress", "Completed"].index(st.session_state[user_tasks_key][task])
            )



# Define class schedule with added URLs for materials
classes = {
    "Monday": [
        {"time": "8:30 - 10:30", "subject": "Operation Research 1", "classroom": "Ae", "link": "https://stem.elearning.unipd.it/course/view.php?id=6475", "exam": "January 26, Time: 10:00 AM"},
        {"time": "10:30 - 12:30", "subject": "Machine Learning", "classroom": "Ae", "link": "https://stem.elearning.unipd.it/course/view.php?id=7045", "exam": "January 23,  Time: 2:00 PM"}
    ],
    "Tuesday": [
        {"time": "12:30 - 14:30", "subject": "Automata", "classroom": "Ae", "link": "https://stem.elearning.unipd.it/course/view.php?id=6403","exam":"TBD"},
        {"time": "14:30 - 16:30", "subject": "Operation Research 1", "classroom": "De", "link": "https://stem.elearning.unipd.it/course/view.php?id=6475","exam":"January 26, Time: 10:00 AM"},
        {"time": "16:30 - 18:30", "subject": "Intelligent Robotics", "classroom": "Te,Ue", "link": "#","exam":"TBD"}
    ],
    "Wednesday": [
        {"time": "12:30 - 14:30", "subject": "Automata", "classroom": "Ce", "link": "https://stem.elearning.unipd.it/course/view.php?id=6403","exam":"TBD"},
        {"time": "12:30 - 14:30", "subject": "Intelligent Robotics", "classroom": "Le", "link": "#","exam":"TBD"},
        {"time": "14:30 - 16:30", "subject": "Operation Research 1", "classroom": "Ve", "link": "https://stem.elearning.unipd.it/course/view.php?id=6475","exam":"January 26, Time: 10:00 AM"}
    ],
    "Friday": [
        {"time": "10:30 - 12:30", "subject": "Machine Learning", "classroom": "Ae", "link": "https://stem.elearning.unipd.it/course/view.php?id=7045","exam":"January 23,  Time: 2:00 PM"},
        {"time": "12:30 - 14:30", "subject": "Automata", "classroom": "Ae", "link": "https://stem.elearning.unipd.it/course/view.php?id=6403","exam":"TBD"},
        {"time": "14:30 - 16:30", "subject": "Intelligent Robotics", "classroom": "De", "link": "#","exam":"TBD"}
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
            st.markdown(f"😟⏰ **Exam Date**: {cls['exam']} ")

def main():
    st.title("🦅 Orari But Better (OBB)")
    st.markdown("### Specialized App for Computer Engineering Courses @UNIPD")
    
    page = st.sidebar.selectbox("Navigate", ["Home","Class" "Monday", "Tuesday", "Wednesday", "Friday"])

    if page == "Home":
        st.markdown("#### 🏠 Welcome to the **OBB** App!")
        st.markdown("Navigate to a specific day using the dropdown on the left to view the class schedules.")
        st.link_button('Login to University Profile', url='https://stem.elearning.unipd.it/login/index.php')
        
        user = st.sidebar.selectbox("Users", ["Select a User", "User1", "User2"])  # User selection
        if user != "Select a User":
            handle_tasks(user)
            
        if st.checkbox("Enable Chat Assistant 🤖"):
            replicate_api = st.secrets['replicate']['API_KEY']  # Corrected key reference
            #os.environ['REPLICATE_API_TOKEN'] = replicate_api  # Set API token as an environment variable
            st.subheader('Assistant Chatbot 🤖')
            if "messages" not in st.session_state:
                st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

            if prompt := st.chat_input(disabled=not replicate_api):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)

            if st.session_state.messages[-1]["role"] != "assistant":
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = generate_llama2_response(prompt)
                        placeholder = st.empty()
                        full_response = ''.join(response)
                        placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})         
                   
    
    else:
        subject_filter = st.sidebar.selectbox("Filter by Subject (optional)", ["All"] + unique_subjects)
        if subject_filter == "All":
            subject_filter = None
        display_classes(page, subject_filter)

if __name__ == "__main__":
    main()
