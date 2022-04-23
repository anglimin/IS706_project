import pandas as pd
import requests
import re
import math
from collections import Counter
from bs4 import BeautifulSoup
from tqdm import tqdm

######################## HELPER FUNCTIONS ##################################

def text_to_vector(text):
    """
    Transform text into vector
    """
    WORD = re.compile(r"\w+")
    words = WORD.findall(text)
    return Counter(words)

def get_cosine(vec1, vec2):
    """
    Derive cosine similarity between two vectors
    """
    intersection = set(vec1.keys() & vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

###################### API REPLACEMENT FUNCTIONS #####################################
def match_replacement_api(missing_api: str, answer_body:str, question_body: str) -> str:
    """
    Purpose:
    1) Remove the phenomemon whereby the answers enhance the original question body code by changing it from the original api with the new api
    2) 

    """
    soup = BeautifulSoup(answer_body, "html.parser")
    candidate_apis = [link.get_text() for link in soup.select("code")]
    missing_api_vector = text_to_vector(missing_api)
    question_soup = BeautifulSoup(question_body,"html.parser")
    question_code_snippets = [link.get_text() for link in question_soup.select("code")]
    
    cosine_dict = {}
    # if length of candidate apis is only one --> that should be it
    if len(candidate_apis) == 1:
        return candidate_apis[0]
    elif len(candidate_apis) > 1:
        for candidate in candidate_apis:
            candidate_vector = text_to_vector(candidate)
            cosine_similarity = get_cosine(missing_api_vector, candidate_vector)
            cosine_dict[candidate] = cosine_similarity
            # if the candidate has perfect cosine similarity then reject
        


        # if question body's cosine similarity is same with the answer body cosine similarity
        # for question in question_code_snippets:
        #     print(question)
    else:
        # if there are not code tags in the candidate apis -> return the entire p tags
        # this might indicate that there are api deletion
        candidate_texts = [link.get_text() for link in soup.select("p")]
        candidate_string = " ".join(candidate_texts)
        return candidate_string


def possible_replacement_api(missing_api:str, answer_body: str) -> str:
    # done via cosine similarity method
    soup = BeautifulSoup(answer_body, "html.parser")
    candidate_apis = [link.get_text() for link in soup.select("code")]
    missing_api_vector = text_to_vector(missing_api)
    cosine_dict = {}
    if len(candidate_apis) > 1:
        for candidate in candidate_apis:
            candidate_vector = text_to_vector(candidate)
            cosine_similarity = get_cosine(missing_api_vector, candidate_vector)
            cosine_dict[candidate] = cosine_similarity
        # sort by descending
        cosine_items = list(cosine_dict.items())
        sorted_cosine_items = sorted(cosine_items, key= lambda x: x[1], reverse=True)
        
        # reject the one that has perfect cosine similarity
        if sorted_cosine_items[0][1] == 1:
            return sorted_cosine_items[1][0]
        else:
            return sorted_cosine_items[0][0]

    elif len(candidate_apis) == 1:
        return candidate_apis[0]
    else:
        return


########################## MAIN FUNCTION ########################################
def getStackQuestionsv2(missing_api:str, top_only:bool) -> pd.DataFrame:
    questionQueryURL = "https://api.stackexchange.com/2.3/search/advanced?"
    answerQueryURL = "https://api.stackexchange.com/2.3/questions/{}/answers?"
    questionfilter_dict = {
        "body" : missing_api,
        "sort": "votes",
        "order": "desc",
        "site": "stackoverflow",
        "filter" : "!0WAfAKLVhyg2Bjytoa)ZVCaM5"
    }
    questionAnswersFilter = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "filter": "!3ubsrEfVBpYHFpKQ5"
    }

    baseQuestionFilter_dict = {
        "body" : missing_api,
        "sort" : "votes",
        "order" : "desc",
        "site" : "stackoverflow",
        "filter" : "!nKzQURF6Y5"
    }

    for key, value in questionfilter_dict.items():
        questionQueryURL += "{}={}&".format(key, value)
    ## slice the last element away
    questionQueryURL = questionQueryURL[:-1]
    # for the answers portion
    for key, value in questionAnswersFilter.items():
        answerQueryURL += "{}={}&".format(key, value)
    answerQueryURL = answerQueryURL[:-1]
    # get request
    r = requests.get(questionQueryURL)
    data = r.json()
    print(data)
    questionArr = data["items"]
    # filter away the not answered question
    filteredArr = []
    # return empty string if there is no related question found
    if len(questionArr) == 0:
        return ""
    else:
        # accept top 1 answers
        for question in tqdm(questionArr):
            if question["is_answered"]:
                answerURL = answerQueryURL.format(question["question_id"])
                response = requests.get(answerURL)
                if len(response.json()["items"]) == 0:
                    continue
                answerData = response.json()["items"][0]
                question["answer_score"] = answerData["score"]
                question["answer_body"] = answerData["body"]
                filteredArr.append(question)
            else:
                # return empty string if the question is not answered
                return ""
            
    
        df = pd.json_normalize(filteredArr)
        df["possible_replacement"] = df["answer_body"].apply(lambda x: possible_replacement_api(missing_api,x))
        if top_only:
            top_candidate = list(df["possible_replacement"])[0]
            return top_candidate
        else:
            return df

if __name__  == "__main__":
    pass