import streamlit as st
import joblib,os

# from sklearn.linear_model import LogisticRegression


#NLP pkgs
import spacy
nlp = spacy.blank("en")

# EDA Packages
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')

# Word Cloud
from wordcloud import WordCloud
from PIL import Image

# Load Downloaded Verctorizers
crime_vectorizer = open("models/final_news_cv_vectorizer.pkl", "rb")
crime_cv = joblib.load(crime_vectorizer)

# Load Models
def load_pred_model(model_file):
    loaded_models = joblib.load(open(os.path.join(model_file), "rb"))
    return loaded_models

# Get Label for Output Results
def get_keys(val, my_dict):
    for key,value in my_dict.items():
        if val == value:
            return key
st.set_option('deprecation.showPyplotGlobalUse', False)
def main():
    """News Classifier App with Streamlit"""
    
    st.title("News Classifier App")
    # st.subheader("NLP and ML App with Streamlit")
    
    # Side Bar Activities
    options = ["Classification", "NLP"]
    ChoiceML = st.sidebar.selectbox("Choose ML Activity", options)
    
    # Side Bar Activities
    optionsUS = ["Crime", "Use Cases"]
    ChoiceUS = st.sidebar.selectbox("Use Case based ML", optionsUS)
    
    # Do Prediction Activity
    if ChoiceML == "Classification":
        st.info("Classify News based on Text")
        
        crime_text = st.text_area("Enter News Description here")
        model_list = ["Logistic Regression", "Naive Bayes", "Random Forest", "Decision Tree"]
        model_choice = st.selectbox("Select Classifier", model_list)
        pred_labels = {'business':0, 'tech':1, 'sport':2, 'health':3, 'politics':4, 'entertainment':5}
        
        # Convert Text to Vectors
        if st.button("Classify"):
            st.text("Original text ::\n{}".format(crime_text))
            vect_txt = crime_cv.transform([crime_text]).toarray()
            
            # Load Models based on Choice
            if model_choice == 'Logistic Regression':
                predictor = load_pred_model("models/newsclassifier_Logit_model.pkl")
                classification = predictor.predict(vect_txt)
                # st.write(classification)
            elif model_choice ==  "Naive Bayes":
                predictor = load_pred_model("models/newsclassifier_NB_model.pkl")
                #predictor = load_pred_model("models/lr_model_py_02_feb_2022.pkl")
                classification = predictor.predict(vect_txt)
                # st.write(classification)            
            elif model_choice ==  "Random Forest":
                predictor = load_pred_model("models/newsclassifier_RFOREST_model.pkl")
                classification = predictor.predict(vect_txt)
                # st.write(classification)            
            elif model_choice ==  "Decision Tree":
                predictor = load_pred_model("models/newsclassifier_CART_model.pkl")
                classification = predictor.predict(vect_txt)
                # st.write(classification)
                
            final_result = get_keys(classification,pred_labels)
            st.success("News Classified as:  **{}**".format(final_result))
 
        
    #Do NLP Activity    
    if ChoiceML == "NLP":
        st.info("Analyze News Description to Gain Insights")
        crime_text = st.text_area("Enter News Description here")
        nlp_tasks = ["Tokenization", "Name Editing Recognition", "Lemmatization", "POS Tags"]
        task_choice = st.selectbox("Select NLP Task", nlp_tasks)
        if st.button("Analyze"):
            st.info("Original Text:: **{}**".format(crime_text))
            
            # Create NLP Object
            docx = nlp(crime_text)
            if task_choice == 'Tokenization':
                result = [ token.text for token in docx ]
            elif task_choice == 'Lemmatization':
                result = [ "'Token':{}, 'Lemma':{}".format(token.text,token.lemma_) for token in docx ]
            elif task_choice == 'Name Editing Recognition':
               result = [ (entity.text,entity.label_) for entity in docx.ents ]
            elif task_choice == 'POS Tags':
               result = [ "'Token':{}, 'POS':{}, 'Dependency':{}".format(word.text,word.tag_,word.dep_) for word in docx ]
               
            st.json(result)
            
        if st.button("View as Table"):
            docx = nlp(crime_text)
            c_tokens = [ token.text for token in docx ]
            c_lemma =  [(token.text,token.lemma_) for token in docx]
            c_pos =    [(word.text,word.tag_,word.dep_) for word in docx ]
            
            crime_df_tab = pd.DataFrame(zip(c_tokens,c_lemma,c_pos),columns=['Tokens','Lemma','POS'])
            st.dataframe(crime_df_tab)
            
        if st.checkbox("Wordcloud"):
             wordcloud = WordCloud().generate(crime_text)
             plt.imshow(wordcloud,interpolation='bilinear')
             plt.axis("Off")
             st.pyplot()
             
    
    
    


if __name__ == '__main__':
    main()
    