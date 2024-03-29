"""
Modules for extracting text from a string utilizing RAKE and other methods.
"""

from . import parser

# Helper Function:
def trim_string(s):
    # Find the index of the first occurrence of '{'
    start_index = s.find('{')
    # Find the index of the last occurrence of '}'
    end_index = s.rfind('}')
    # Check if both '{' and '}' are found
    if start_index != -1 and end_index != -1:
        # Return the substring including '{' and '}'
        return s[start_index:end_index+1]
    else:
        # Return the original string if '{' or '}' not found
        return s

try:
    import nltk
    from rake_nltk import Rake
except:
    def extract_text_with_rake(para: str):
        tempReq = ["nltk", "rake_nltk"]
        print("For extract_text_with_rake to operate, please install the following dependencies: ")
        for i in tempReq:
            print(f"\ti")
        raise Exception("Missing Dependencies...")
finally:
    def extract_text_with_rake(para: str):
        rakeInstance = Rake()
        rakeInstance.extract_keywords_from_text(para)
        tempList = rakeInstance.get_ranked_phrases()
        return tempList


# Uses GPT-3 to power nlp text extraction and paragraph generation, this is 
# placed into one function/module to minimize costs for generation.
try:
    from openai import OpenAI
    import re
except:
    def extract__and_generate_with_gpt(
            job_desc: str, resume: str, openai_api_key: str, 
            para_count: int = 3, gpt_model: str = "gpt-3.5-turbo"):
        tempReq = ["openai"]
        print("For extract_text_with_rake to operate, please install the following dependencies: ")
        for i in tempReq:
            print(f"\ti")
        raise Exception("Missing Dependencies...")
finally:
    def extract__and_generate_with_gpt(
            job_desc: str, resume: str, openai_api_key: str, 
            para_count: int = 3, gpt_model: str = "gpt-3.5-turbo"):
        openai_client = OpenAI(api_key=openai_api_key)
        response = openai_client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role":    "system", 
                 "content": f"You are a helpful assistant who will help me write a cover letter paragraph based on my given skill, resume, and the job description. Know that for every prompt, assume that there is already an introduction and ending paragraphs written. Here is the job positing I will be applying to: {job_desc}; Here is my resume: {resume}."},
                
                {"role": "user", 
                 "content": f"""Taking into account this job description and my resume, generate {para_count} distinctly named skills (preferably soft skills) and write me a cover letter paragraphs for each skill, each of around 80 words. 
                 
                 Note that all three paragraphs will eventually be in one cover letter, so avoid repetition among paragraphs, assume paragraphs will be in order, and try to make the paragraphs flow well together, so dont make it seem like dot jots. Incorporate some phrases or names from the job description and resume into the paragraphs if possible, but do not force it.

                 The tone of the paragraphs will be formal, but not too serious, and avoid repeating traits already mentioned in the resume, you can make simple implies from the resume. Make sure that the paragraphs are not too similar to each other. Try to keep the beginning of each paragraph unique, and try to make the paragraphs flow well together.
                 
                 Response text should be formatted like a json in key value pairs, where the key is the skill and nothing else, and value being the paragraph, here is an example: {{"teamwork": "I am a great team player, and I have worked in many teams in the past, and I have always been a great asset to the team. I have always been a great team player, and I have worked in many teams in the past, and I have always been a great asset to the team.", "communication": "I am a great communicator, and I have always been able to communicate well with my team, and I have always been able to communicate well with my team. I have always been a great communicator, and I have always been able to communicate well with my team, and I have always been able to communicate well with my team.", "leadership": "I am a great leader, and I have always been able to lead my team well, and I have always been able to lead my team well. I have always been a great leader, and I have always been able to lead my team well, and I have always been able to lead my team well."}}
                 """}
            ]
        )

        # print(response.choices[0].message.content)
        try:
            para = parser.json_str_to_dict(trim_string(response.choices[0].message.content))
        except:
            print(trim_string(response.choices[0].message.content))
            print("Error: OpenAI response is not in JSON format.")

        # LLM may result undesired characters, remove them
        #updated_data = {}
        #for key, value in para.items():
        #    new_key = re.sub(r"Skill\s\d+:\s?", '', key, flags=re.IGNORECASE)
        #    updated_data[new_key] = value


        token_cost = response.usage.total_tokens
        return [para, token_cost]
        

def extract__and_generate_with_rtx(job_desc: str, rtx_port: str, rtx_address: str = "http://localhost", para_count: int = 3):
    pass



debug = True

# Uses local machine to power nlp text extraction
# input: 
#       job: string of job title
#       para: string of text to be analyzed
# output:
#       lst: list of keywords extracted from text sorted by importance
try:
    # extract_text_with_nlp dependency
    import numpy as np
    import pandas as pd
    import string
    from nlk.corpus import stopwords
    from nltk.naive_bayes import MultinomialNB
    from sklearn.feature_extraction.text import TFidfVectorizer
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    #matplotlib inline
    from textblob import Word
    from textblob import TextBlob
except:
    def extract_text_with_nlp(job: str, para: str):
        tempReq = ["nltk", "sklearn", "wordcloud", "matplotlib", "textblob"]
        print("For extract_text_with_nlp to operate, please install the following dependencies: ")
        for i in tempReq:
            print(f"\ti")
        raise Exception("Missing Dependencies...")
finally:
    def extract_text_with_nlp(job: str, para: str):
        ##DATAFRAME CREATION
        d = {'job': [job], 'description': [para]}
        df = pd.DataFrame(data=d)
            
        if debug:
            print(df.head())
            print(df.shape)

        ##PREPROCESSING
        # lower case
        df['description'] = df['description'].apply(lambda x: " ".join(x.lower() for x in x.split()))
        # remove punctuation
        df['description'] = df['description'].str.replace('[^\w\s]','')
        # remove digits
        df['description'] = df['description'].str.replace('\d','')
        # remove stopwords
        stop = stopwords.words('english')
        df['description'] = df['description'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
        other_stop = ['junior', 'senior','experience','etc','job','work','company','technique',
                            'candidate','skill','skills','language','menu','inc','new','plus','years',
                            'technology','organization','ceo','cto','account','manager','data','scientist','mobile',
                            'developer','product','revenue','strong']
        df['description'] = df['description'].apply(lambda x: " ".join(x for x in x.split() if x not in other_stop))
        # lemmatization
        df['description'] = df['description'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
        
        # good programming languages would not require the above commments about what the code does
        # the code would be self explanitory
        # proof that eithe I am dogshit at python or python is dogshit

        if debug:
            print(df.head())


        ##MODELING
        vectorize = TfidfVectorizer()

        x = vectorize.fit_transform(df.description)
        y = df.job

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=109)

        clf = MultinomialNB()
        clf.fit(x_train, y_train)
        y.predict = clf.predict(x_test)

        if debug:
            y_test.hist()
            y_train.hist()

        ##EVALUATION
        if debug:
            print("score: ", accuracy_score(y_test, y.predict))
            print("classes: ", classification_report(y_test, y.predict))

        ##FEATURE EXTRACTION
        # list of technical skills may need expansion
        technical = ['python', 'c','r', 'c++','java','hadoop','scala','flask','pandas','spark','scikit-learn',
                        'numpy','php','sql','mysql','css','mongdb','nltk','fastai' , 'keras', 'pytorch','tensorflow',
                    'linux','Ruby','JavaScript','django','react','reactjs','ai','ui','tableau']

        feature_array = vectorizer.get_feature_names()
        features = len(feature_array)
        n_max = int(features * 0.1)

        output = pd.DataFrame()
        for i in range(0,len(clf.classes_)):
            print("\n****" ,clf.classes_[i],"****\n")
            class_prob_indices_sorted = clf.feature_log_prob_[i, :].argsort()[::-1]
            raw_skills = np.take(feature_array, class_prob_indices_sorted[:n_max])
            print("list of unprocessed skills :")
            print(raw_skills)
            
            ## Extract technical skills
            top_technical_skills= list(set(technical_skills).intersection(raw_skills))[:6]
            #print("Top technical skills",top_technical_skills)
            
            ## Extract adjectives
            
            # Delete technical skills from raw skills list
            ## At this steps, raw skills list doesnt contain the technical skills
            #raw_skills = [x for x in raw_skills if x not in top_technical_skills]
            #raw_skills = list(set(raw_skills) - set(top_technical_skills))

            # transform list to string
            txt = " ".join(raw_skills)
            blob = TextBlob(txt)
            #top 6 adjective
            top_adjectives = [w for (w, pos) in TextBlob(txt).pos_tags if pos.startswith("JJ")][:6]
            #print("Top 6 adjectives: ",top_adjectives)
            
            output = output.append({'job_title':clf.classes_[i],
                                'technical_skills':top_technical_skills,
                                'soft_skills':top_adjectives },
                            ignore_index=True)

            print(output.T)

        ##OUTPUT
        output_array = output.to_numpy()
        output_list = output_array.tolist()
        return output_list
    
