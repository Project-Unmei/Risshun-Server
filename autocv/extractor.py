"""
Modules for extract the input file utilizing LUTs, GPT, and other methods.
"""

try:
    import nltk
    
    from rake_nltk import Rake
finally:
    def extract_text_with_rake(para: str):
        rakeInstance = Rake()
        rakeInstance.extract_keywords_from_text(para)
        tempList = rakeInstance.get_ranked_phrases()
        return tempList

def extract_text_with_spacy(para: str):
    # Input: Just a paragraph
    """"""
    doc = []
    # Return a list of words
    return doc



