require("dotenv").config();
const stackexchange = require("stackexchange");

const options = {version: 2.2};
const context = new stackexchange(options);

const filter ={
    key: process.env.KEY,
    pagesize: 50,
    tagged: "node.js",
    sort: "activity",
    order: "asc"
};

context.questions.questions(filter, function(err, results) {
    if (err) throw err;
    console.log(results.items);
    console.log(results.has_more);
})