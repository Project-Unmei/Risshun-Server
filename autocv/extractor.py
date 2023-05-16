"""
Modules for extracting text from a string utilizing RAKE and other methods.
"""

from . import parser

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
    import openai
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
        openai.api_key = openai_api_key
        response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=[
                {"role": "system", 
                 "content": f"""You are a helpful assistant who will help me generate a cover letter paragraph based on 
                                the given skill, my resume, and the job description. Know that for every prompt, assume 
                                that there is already an introduction and ending paragraphs written. Here is the job 
                                description: {job_desc}; Here is my resume: {resume}."""},
                {"role": "user", 
                 "content": f"""Taking into account this job description and my resume, generate {para_count} distinctly 
                                named skills (preferably soft skills) and write me a cover letter paragraphs for each 
                                skill, each of around 80 words. Note that all three paragraphs will eventually be in one 
                                cover letter, so avoid repetition among paragraphs, assume paragraphs will be in order. 
                                The tone of the paragraphs will be formal, and avoid repeating traits already mentioned 
                                in the resume. Respond text should be formatted like a json, where key is the name of 
                                the skill without enumeration or the word skill, and value is the paragraph. DO NOT MAKE
                                UP SKILLS THAT ARE NOT IN MY RESUME."
                                """}
            ]
        )
        
        para = parser.json_str_to_dict(response['choices'][0]['message']['content'])
        token_cost = response['usage']
        return [para, token_cost]
        


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
    
