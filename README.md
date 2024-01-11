# Risshun Server

Auto curriculum vitae generation using Python. Also serves as a local template engine similar to EJS and React.


## **Local Methods for Generation**:

| Preset Name | Keyword-Extraction | Paragraph-Generation | Status            | HW Requirement |
|-------------|--------------------|----------------------|-------------------|----------------|
| nltk_lut    | NLTK Custom        | Look-Up Table        | Under Development | Medium         |
| rake_lut    | RAKE-NLTK          | Look-Up Table        | Under Development | Low            |
| nltk_llama  | NLTK Custom        | Llama                | Under Development | High           |

## **API Required Generation**

| Preset Name | Keyword-Extraction       | Paragraph-Generation     | Status      | HW Requirement |
|-------------|--------------------------|--------------------------|-------------|----------------|
| gpt         | OpenAI Chat Completition | OpenAI Chat Completition | Operational | Low            |

### **Setup Instruction for Local Generation**
---
1. Install Leo Chai's Chrome Extension [here](https://github.com/TheLeoChai/CoverLetterGeneration).
2. Replace the `resume.docx`/`resume.pdf` and `template.docx` with your own.
3. Make a copy of `.env.example` and rename it to `.env`; Configure it as seem fit.
4. Run `_server.py` and use the chrome extension to queue jobs.


### **Notes for Configuration**
The JSON Config File Structure:
```
.json = {
    UID: "123456"                   <- Job Unique ID
    TYPE: "gpt"                     <- Preset Name Goes Here
    DATA: {                         <- Data About Posting
        "TITLE": "...",             <- REQUIRED | Posting/Job Title
        "COMPANY": "...",
        "JOB_SUM": "...",
        "JOB_RESP": "...",
        "JOB_SKILL": "...",
        ...
    }
}
