import streamlit as st
import pandas as pd
import os
import time
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
import json
import os
# Load environment variables
load_dotenv()

# Initialize AI Chatbot
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.2-90b-vision-preview"  # Replace with a valid model name
)

# Page Configuration
st.set_page_config(
    page_title="Women's Health",
    page_icon="🎀",
    layout="wide",
)

# Custom CSS Styles
st.markdown("""
    <style>
        body {
            background-color: #ffe4e1; /* Light pink background */
        }
        .header {
            text-align: left;
            font-family: Arial, sans-serif;
            font-size: 48px; /* Increased header font size */
            font-weight: bold;
            color: #e012e0;
            margin-bottom: 20px;
        }
        .introduction-box {
            background-color: white;
            border: 2px solid #ffb6c1; /* Soft pink border */
            border-radius: 10px;
            padding: 20px;
            font-family: Arial, sans-serif;
            font-size: 20px; /* Increased text font size */
            color: #4d004d; /* Dark pink text */
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin: 20px auto; /* Center the box horizontally with margin */
            width: 80%;
        }
        h1, h2, h3 {
            font-size: 32px; /* Increased header sizes for h1, h2, h3 */
            color: #4d004d; /* Consistent dark pink color */
        }
        label {
            font-size: 18px; /* Increased font size for labels */
            color: #4d004d; /* Consistent dark pink color */
        }
        .video-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .footer {
            background-color: #ffb6c1; /* Soft pink footer */
            padding: 10px;
            text-align: center;
            border-radius: 10px;
            font-size: 18px; /* Increased footer font size */
            color: #4d004d; /* Dark pink text */
        }
        .centered {
            display: flex;
            justify-content: center;
        }
        .chatbot-container {
            margin-top: 30px;
            padding: 20px;
            background-color: #fce4ec; /* Light pink background for chatbot */
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .sidebar .css-17eq0hr {
            font-size: 20px; /* Increased sidebar font size */
        }
        .stTextInput > div > input {
            font-size: 18px; /* Increased input font size */
        }
        .stButton > button {
            font-size: 18px; /* Increased button font size */
        }
        .stSelectbox > div > div {
            font-size: 18px; /* Increased selectbox font size */
        }
    </style>
""", unsafe_allow_html=True)


# Define the JSON file path
USER_FILE = "users.json"

# Helper function to load user data
def load_users():
    if not os.path.exists(USER_FILE):
        return {}  # Return empty dict if file doesn't exist
    with open(USER_FILE, "r") as file:
        try:
            return json.load(file)  # Load JSON data
        except json.JSONDecodeError:
            return {}  # Return empty if file is corrupted

# Helper function to save user data
def save_user(name, email, password):
    users = load_users()
    if email in users:
        st.warning("User already exists. Please log in.")
    else:
        users[email] = {"name": name, "password": password}
        with open(USER_FILE, "w") as file:
            json.dump(users, file, indent=4)  # Save to JSON
        st.success("User registered successfully! Please log in.")

# Helper function to verify user credentials
def verify_user(email, password):
    users = load_users()
    if email in users and users[email]["password"] == password:
        return users[email]["name"]  # Return user name if authenticated
    return None

# Sidebar Navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🔑 Login/Signup"
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""

# Sidebar Navigation
st.sidebar.title("Navigation")
sections = ["🔑 Login/Signup", "🏠 Home", "🛠 Techniques", "📚 Resources", "📞 Contact", "🤖 AI Assistant"]

if st.session_state["current_page"] != "🔑 Login/Signup":
    selected_page = st.sidebar.radio("Go to", sections, index=sections.index(st.session_state["current_page"]))
    if selected_page != st.session_state["current_page"]:
        st.session_state["current_page"] = selected_page

# Login/Signup Page
if st.session_state["current_page"] == "🔑 Login/Signup":
    st.title("Login/Signup")
    action = st.selectbox("Choose Action", ["Login", "Signup"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if action == "Signup":
        name = st.text_input("Name")
        if st.button("Sign Up"):
            if not name.strip():
                st.warning("Name cannot be empty.")
            else:
                save_user(name, email, password)

    elif action == "Login":
        if st.button("Log In"):
            user_name = verify_user(email, password)
            if user_name:
                st.session_state["user_name"] = user_name
                st.session_state["current_page"] = "🏠 Home"  # Redirect to Home
            else:
                st.error("Invalid email or password.")

# Home Page
if st.session_state["current_page"] == "🏠 Home":
    user_name = st.session_state.get("user_name", "User")
    st.markdown(f"<h1>Welcome, {user_name}!</h1>", unsafe_allow_html=True)


# Techniques Page
elif choice == "🛠 Techniques":
    st.title("Breast Self Exam!")
    # Define image paths
    image_paths = [
        "Slide1.PNG",
        "Slide2.PNG",
        "Slide3.PNG",
        "Slide4.PNG",
        "Slide5.PNG",
        "Slide6.PNG",
        "Slide7.PNG",
    ]

    # Verify image files exist
    missing_images = [img for img in image_paths if not os.path.exists(img)]
    if missing_images:
        st.error(f"Missing images: {', '.join(missing_images)}")
        st.stop()

    # Initialize session state for slideshow
    if "current_image_index" not in st.session_state:
        st.session_state.current_image_index = 0
    if "slideshow_running" not in st.session_state:
        st.session_state.slideshow_running = False

    # Buttons for controlling the slideshow
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start"):
            st.session_state.slideshow_running = True
    with col2:
        if st.button("Stop"):
            st.session_state.slideshow_running = False

    # Placeholder for image display
    placeholder = st.empty()

    # Slideshow logic
    if st.session_state.slideshow_running:
        # Display images in a loop until stopped
        for index in range(len(image_paths)):
            if not st.session_state.slideshow_running:
                break
            st.session_state.current_image_index = index
            placeholder.image(
                image_paths[st.session_state.current_image_index],
                caption=f"Technique of Palpation ({st.session_state.current_image_index + 1}/{len(image_paths)})",
                use_container_width=True,  # Set to False to allow manual size control
                #width=800,  # Set desired width for the images
            )
            time.sleep(5)
    else:
        # Display the current image statically
        placeholder.image(
            image_paths[st.session_state.current_image_index],
            caption=f"Technique of Palpation ({st.session_state.current_image_index + 1}/{len(image_paths)})",
            use_container_width=False,  # Set to False to allow manual size control
            width=800,  # Set desired width for the images
        )


# Resources Page
elif choice == "📚 Resources":
    st.title("Resources")
    st.markdown("""
            Here are some valuable resources:
            - [American Cancer Society](https://www.cancer.org)
            - [Breastcancer.org](https://www.breastcancer.org)
            - [World Health Organization](https://www.who.int)
        """)


# Contact Page
elif choice == "📞 Contact":
    st.title("Contact Us")
    st.markdown("""
        - **Email**:
        - **Phone**:
    """)

# AI Assistant Page
elif choice == "🤖 AI Assistant":
    st.title("AI Health Assistant")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Clear chat button functionality
    if st.button("🗑️ Clear Chat", key="clear_chat", help="Clear the chat history"):
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"<div style='text-align: left; background-color: #fce4ec; padding: 10px;'>"
                        f"<b>User:</b> {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; background-color: #e8f5e9; padding: 10px;'>"
                        f"<b>AI:</b> {message['content']}</div>", unsafe_allow_html=True)

    # Input field for user
    user_input = st.text_input("Ask your question:", placeholder="Type your question here...")

    # Send button functionality
    if st.button("Send", key="send_message"):
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            try:
                response = llm.invoke(user_input)  # Replace with your AI model invocation
                st.session_state.chat_history.append({"role": "assistant", "content": response.content})
            except Exception as e:
                error_message = f"An error occurred: {e}"
                st.session_state.chat_history.append({"role": "assistant", "content": error_message})
