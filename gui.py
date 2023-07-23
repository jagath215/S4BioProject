import streamlit as st
import predictor
import base64
import pandas as pd
import matplotlib.pyplot as plt

# Function to read image file and convert it to base64
def get_local_img_as_base64(file_path):
    try:
        with open(file_path, 'rb') as file:
            image_content = file.read()
            base64_image = base64.b64encode(image_content).decode('utf-8')
            return base64_image
    except IOError as e:
        print(f'Error: {e}')
        return None

# Set the background color to white
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-position: top left;
        background-attachment: local;
    }
    body {
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Roboto', sans-serif;
        margin: 0;
    }
    .reportview-container {
        background-color: #FFFFFF;
        background-image: none;
    }
    .sidebar-content {
        display: none;
    }
    .main {
        padding: 2rem;
    }
    .title {
        font-size: 48px;
        text-align: center;
        padding: 1rem 0;
    }
    .stRow > div {
        padding: 0 1rem;
    }
    .description {
        font-size: 18px;
    }
    </style>
    """
    % get_local_img_as_base64('image.jpg'),  # Load background image
    unsafe_allow_html=True,
)

# Set the title
st.markdown("<h1 class='title'>Alzheimer's Disease Prediction</h1>", unsafe_allow_html=True)

# First row: split into two columns
col1, col2 = st.columns([1, 1])
with col1:
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], accept_multiple_files=False)

with col2:
    if uploaded_image:
        st.image(uploaded_image, caption='Uploaded Image', width=128)

# Second row: model selection in a horizontal layout
st.subheader("Select Model")
model_selection = st.radio("Select Model", ("Model 1", "Model 2", "Model 3", "Model 4"), index=0)

# Third row: Description
st.markdown("<p class='description'>Model 1 and Model 2 implement CNN and Transfer Learning on dataset 1.<br>Model 3 and Model 4 implement CNN and Transfer Learning on dataset 2.</p>",
            unsafe_allow_html=True,  # Allow HTML in the description
            )

# Fourth row: Submit button
if st.button("Submit"):
    if uploaded_image is None:
        st.warning("Please upload an image.")
    elif not model_selection:
        st.warning("Please select a model.")
    else:
        pred = predictor.predict(img=uploaded_image, myModel=model_selection)
        lis = ["Mild_Demented", "Moderate_Demented", "Non_Demented", "Very_Mild_Demented"]
        total = pred/sum(pred)
        data = {
            'Category': lis,
            'Values': pred
        }
        df = pd.DataFrame(data)
        # Create the pie chart using matplotlib
        fig, ax = plt.subplots(figsize=(6, 6))  # Adjust the size of the chart (width, height)
        wedges, texts, autotexts = ax.pie(df['Values'], labels=None, autopct='%1.1f%%', shadow=False, startangle=90)

        # Get the label and color information
        labels = df['Category']
        colors = [wedge.get_facecolor() for wedge in wedges]

        # Create the legend with colored tags
        ax.legend(wedges, labels, title='Categories', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), prop={'size': 12})

        ax.axis('equal') 
        st.pyplot(fig)
        st.success(f"Prediction: {lis[pred.index(max(pred))]}")

        
    
