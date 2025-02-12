import streamlit as st
import pandas as pd
import os
import time
from langchain_groq import ChatGroq
from dotenv import load_dotenv

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

# Helper Functions
def save_user(name, email, password):
    """Save user credentials to CSV file."""
    file_path = "D:\\Breast_cancer_web\\username.csv"
    if not os.path.exists(file_path):
        pd.DataFrame(columns=["name", "email", "password"]).to_csv(file_path, index=False)

    user_data = pd.read_csv(file_path)
    if email in user_data["email"].values:
        st.warning("User already exists. Please log in.")
    else:
        new_user = pd.DataFrame({"name": [name], "email": [email], "password": [password]})
        new_user.to_csv(file_path, mode="a", header=False, index=False)
        st.success("User registered successfully! Please log in.")

def verify_user(email, password):
    """Verify user credentials from CSV file."""
    file_path = "D:\\Breast_cancer_web\\username.csv"
    if os.path.exists(file_path):
        user_data = pd.read_csv(file_path)
        for _, row in user_data.iterrows():
            if (
                row["email"].strip().lower() == email.strip().lower()
                and row["password"].strip() == password.strip()
            ):
                return True
    return False

# Sidebar Navigation
# Initialize session state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🔑 Login/Signup"
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""

# Sidebar Navigation
st.sidebar.title("Navigation")
sections = ["🔑 Login/Signup", "🏠 Home", "🛠 Techniques", "📚 Resources", "📞 Contact", "🤖 AI Assistant"]

# Update current_page based on sidebar selection
if st.session_state["current_page"] != "🔑 Login/Signup":  # Prevent navigation before login
    selected_page = st.sidebar.radio("Go to", sections, index=sections.index(st.session_state["current_page"]))
    if selected_page != st.session_state["current_page"]:
        st.session_state["current_page"] = selected_page

# Page Navigation Logic
choice = st.session_state["current_page"]

# Login/Signup Page
if choice == "🔑 Login/Signup":
    st.title("Login/Signup")
    action = st.selectbox("Choose Action", ["Login", "Signup"])

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    def save_user(name, email, password):
        file_path = "D:\\Breast_cancer_web\\username.csv"
        if not os.path.exists(file_path):
            pd.DataFrame(columns=["name", "email", "password"]).to_csv(file_path, index=False)

        user_data = pd.read_csv(file_path)
        if email in user_data["email"].values:
            st.warning("User already exists. Please log in.")
        else:
            new_user = pd.DataFrame({"name": [name], "email": [email], "password": [password]})
            new_user.to_csv(file_path, mode="a", header=False, index=False)
            st.success("User registered successfully! Please log in.")

    def verify_user(name, email, password):
        file_path = "D:\\Breast_cancer_web\\username.csv"
        if os.path.exists(file_path):
            user_data = pd.read_csv(file_path)
            for _, row in user_data.iterrows():
                if (
                    row["name"].strip().lower() == name.strip().lower()
                    and row["email"].strip().lower() == email.strip().lower()
                    and row["password"].strip() == password.strip()
                ):
                    return True
        return False

    if action == "Signup":
        if st.button("Sign Up"):
            if not name.strip():
                st.warning("Name cannot be empty.")
            else:
                save_user(name, email, password)
    elif action == "Login":
        if st.button("Log In"):
            if verify_user(name, email, password):
                st.session_state["user_name"] = name
                st.session_state["current_page"] = "🏠 Home"  # Redirect to Home
            else:
                st.error("Invalid name, email, or password.")

# Home Page
if choice == "🏠 Home":
    user_name = st.session_state.get("user_name", "User")
    st.markdown(f'<div class="header"> Women\'s Health !</div>', unsafe_allow_html=True)
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.image("Screenshot 2024-11-30 202011.png", caption="Awareness is Key!", width=500)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="introduction-box">
            <h3>Introduction</h3>
            <p>
                Breast cancer is one of the most common cancers seen among women in the reproductive age group. With
                an estimated 2.3 million cases every year, there are approximately 1.15 million people globally diagnosed
                with breast cancer. It is further estimated that the global burden of breast cancer will be more than
                2 million in 2030. In India, it was estimated in 2018 that breast cancer accounted for 32.8% of all
                cancers in women between 25 and 49 years of age, with a mortality of 27.7%. The BSE is easy to perform
                by oneself, cost-effective, and non-invasive, and recommended every month after the menstrual period.
                BSE is one of the competencies every girl/woman has to learn. Moreover, you will be a healthcare
                professional, so you are expected to do BSE yourself and impart health education to the general public
                about BSE. At the preservice level, you might have anxiety and lack of confidence related to doing BSE
                and have to gain confidence in performing BSE before you empower the general public. The virtual world
                is being used increasingly in medical education and clinical practice. Your familiarity with the technology
                can be considered essential while giving clinical skills to the general public. This project uses an
                AI-assisted simulation to help you learn the procedure. We wish you a happy and fruitful learning!!
            </p>
        </div>
        """, unsafe_allow_html=True)
    # Language selection for the video
    st.markdown('<div class="video-container">', unsafe_allow_html=True)
    st.write("Choose the language for the video:")
    language = st.radio("", options=["Bengali", "Hindi"], horizontal=True)
    if language == "Bengali":
        video_path = "bse video bengali-comp.mp4"  # Hindi video path
        st.video(video_path, format="video/mp4", start_time=0)
    elif language == "Hindi":
        video_path_bengali = "practices.webm"  # Bengali video path
        st.video(video_path_bengali, format="video/mp4", start_time=0)
        
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2024 Women\'s Health. All Rights Reserved.</div>', unsafe_allow_html=True)

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

