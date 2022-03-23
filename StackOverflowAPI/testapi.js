import fetch from "node-fetch";

/**
 * 
 * @param {string} missing_api missing api in the list
 * @param {boolean} advanceSearch if true, will trigger advance search instead
 * @param {boolean} includeComments if true , comments will be included in both questions and answers
 * 
 * Purpose:
 * 1) Find missing api in stackoverflow to rectify the issue in less popular libraries
 * 2) Advance Search -> able to search the api in the question body
 * 3) normal search -> able to search the api in the question title
 */
async function retrieveQuestions(missing_api, advanceSearch, includeComments) {
    // filter=!nKzQURF6Y5 for questions and answers path
    
    const questionFilter = {
        intitle: missing_api,
        sort: "votes",
        order: "desc",
        site: "stackoverflow",
        filter: "!nKzQUR3Egv"
    };

    const advancedQuestionFilter = {
        body: missing_api,
        sort: "votes",
        order: "desc",
        site: "stackoverflow",
        filter: "!nKzQUR3Egv"
    }

    const questionAnswersFilter = {
        order: "desc",
        sort: "votes",
        site: "stackoverflow",
        filter: "!nKzQURF6Y5"
    };

    const questionCommentsFilter = {
        order: "desc",
        sort: "votes",
        site: "stackoverflow",
        filter: "!nKzQURB9EO"
    }

    if (advanceSearch) {
        
    }

    let questionQueryURL = "https://api.stackexchange.com/2.3/search/advanced?";

    for (const attr in advancedQuestionFilter) {
        questionQueryURL += `${attr}=${advancedQuestionFilter[attr]}&`
    }
    // remove the last and symbol
    questionQueryURL = questionQueryURL.slice(0,-1)
    const questionsArr = await fetch(questionQueryURL).then(
        response => response.json()
    ).then(data => {
        if (data.items.length > 0) {
            let questionsArr = [];
            for (const question of data.items) {
                const {is_answered, question_id, title, body, link} = question;
                if (is_answered) {
                    questionsArr.push({
                        question_id: question_id,
                        title: title,
                        question_body: body,
                        question_link: link
                    })
                }
            }
            return questionsArr;
        }
        else {
            return [];
        }
    });
    for (const question of questionsArr) {
        const {question_id} = question;
        ////////////////////// ANSWER PORTION ///////////////////////////
        let answerQueryURL = `https://api.stackexchange.com/2.3/questions/${question_id}/answers?`;
        for (const attr in questionAnswersFilter) {
            answerQueryURL += `${attr}=${questionAnswersFilter[attr]}&`;
        }
        answerQueryURL = answerQueryURL.slice(0,-1);
        const answersResponse = await fetch(answerQueryURL).then(response => response.json()).then(data=> {
            if (data.items.length > 0) {
                let answersArr = [];
                for (const answer of data.items) {
                    const {body, answer_id} = answer;
                    answersArr.push({
                        answer_id: answer_id,
                        answer_body: body
                    });
                }
                return answersArr;
            } else {
                return [];
            }
        });
        question["answers"] = answersResponse;
        ///////////////////////////// COMMENT PORTION //////////////////////////
        let commentQueryURL =  `https://api.stackexchange.com/2.3/questions/${question_id}/comments?`;
        for (const attr in questionCommentsFilter) {
            commentQueryURL += `${attr}=${questionCommentsFilter[attr]}&`
        } 
        commentQueryURL = commentQueryURL.slice(0,-1);
        const commentResponse = await fetch(commentQueryURL).then(response => response.json()).then(data => {
            if (data.items.length > 0) {
                let commentsArr = [];
                for (const comment in data.items) {
                    const {body, comment_id} = comment;
                    commentsArr.push({
                        comment_id: comment_id,
                        comment_body: body
                    })
                }
                return commentsArr;
            } else {
                return [];
            }
        })
        question["comments"] = commentResponse;
    }

    //////////////////// GET COMMENTS FROM THE ANSWERS???? ///////////////////

    return questionsArr
}

// Test case
const checking = await retrieveQuestions("sklearn.externals.joblib", true, true);
for (const question of checking) {
    console.log(question.question_body);
    console.log(question.question_link);
    console.log(question.answers);
}

// break the results into 