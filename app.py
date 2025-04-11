import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import base64

# Load the environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini
def get_gemini_response(input_prompt, image):
    try:
        # Update to the new model 'gemini-1.5-flash'
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to set up the image for the input
def input_image_setup(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()
        # Convert the image to base64
        image_base64 = base64.b64encode(bytes_data).decode('utf-8')
        image_parts = [
            {
                "mime_type": upload_file.type,
                "data": image_base64
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app initialize
st.set_page_config(page_title="Calories Advisor App")
st.header("Gemini Health App")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to submit and get the response
submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert in nutrition where you need to see the food items from the image 
and calculate the total calories, also provide the details of every 
food item with calories intake
in the below format 

1. Item 1 - no of calories
2. Item 2 - no of calories
...
Finally, you can also mention whether the food is healthy or not and also 
mention the percentage split of the ratio of carbohydrates, fats, fiber, sugar, and other important things required in our diet.
"""

if submit:
    try:
        # Preparing the image data
        image_data = input_image_setup(uploaded_file)
        
        # Getting the response from Gemini
        response = get_gemini_response(input_prompt, image_data)
        
        # Displaying the response
        st.header("The Response is:")
        st.write(response)
    
    except FileNotFoundError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
