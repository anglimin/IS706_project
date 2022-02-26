require("dotenv").config();
const stackexchange = require("stackexchange");
const fs = require("fs");

const options = {version: 2.2};
const context = new stackexchange(options);

const filter ={
    key: process.env.KEY,
    pagesize: 100,
    tagged: ['sklearn'],
    sort: "activity",
    order: "asc"
};

// call the questions
context.questions.questions(filter, function(err, results) {
    if (err) throw err;
    else {
        console.log("checking results", results);
        fs.writeFile("test.txt", JSON.stringify(results), (err) => console.log(err));
    }
})