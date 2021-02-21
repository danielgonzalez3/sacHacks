import React, {useState} from 'react';

export default function App() {
    //this creates garbage variable i
    let i;
    // This initialises a request to the trivia database API
    var xmlhttp = new XMLHttpRequest();
    const url = "https://opentdb.com/api.php?amount=50&category=23&difficulty=medium&type=multiple";
    var question;
    var type;
    var correctAnswer;
    var fjsondata = 54;
    var jsondata = {results: new Array([54], [32], [45], [234], [234], [345], [45])};
    var incorrect1;
    var incorrect2;
    var incorrect3;

// This requests the data
    var getJSON = function (url, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.responseType = 'json';
        xhr.onload = function () {
            var status = xhr.status;
            if (status === 200) {
                callback(null, xhr.response);
            } else {
                callback(status, xhr.response);
            }
        };
        xhr.send();
    };
    getJSON(url,
        function (err, data) {
            if (err !== null) {
                alert('Something went wrong: ' + err);
            } else {
            }
            console.log(data);
        });

    xmlhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            jsondata = JSON.parse(this.responseText);
            getData(jsondata);
        } else {
            throw '';
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    // This function is used to extract the received data
    function getData(data) {
        // This is the question:
        question = data.results[0].question;
        // This is the question type eg. multiple choice
        type = data.results[0].type;
        // This is the correct answer
        correctAnswer = data.results[0].correct_answer;
        // These are the three incorrect answers
        incorrect1 = data.results[0].incorrect_answers[0];
        incorrect2 = data.results[0].incorrect_answers[1];
        incorrect3 = data.results[0].incorrect_answers[2];

        // randomly select answer and other options and place in array
        // then display elements from array on the buttons

        var randoms = []; // an array to store unique random numbers
        var random;

        // loop runs four times...
        for (i = 0; i < 4; i++) {
            // generates a random number between 0 and 3
            random = Math.floor(Math.random() * 4);
            // checks if random number already in array...
            while (randoms.includes(random)) {
                // generates another random number
                random = Math.floor(Math.random() * 4);
            }
            // adds random number to array
            randoms.push(random);
        }


        var options = [];
        console.log(randoms);
        options[randoms[0]] = correctAnswer;
        options[randoms[1]] = incorrect1;
        options[randoms[2]] = incorrect2;
        options[randoms[3]] = incorrect3;

        console.log(options);
    }

    const questions = [
        {
            questionText: 'helo world',
            answerOptions: [
                {answerText: 'New York', isCorrect: false},
                {answerText: 'London', isCorrect: false},
                {answerText: 'Paris', isCorrect: true},
                {answerText: 'Dublin', isCorrect: false},
            ],
        },
        {
            questionText: 'What is the capital of France?',
            answerOptions: [
                {answerText: 'New York', isCorrect: false},
                {answerText: 'London', isCorrect: false},
                {answerText: 'Paris', isCorrect: true},
                {answerText: 'Dublin', isCorrect: false},
            ],
        },
        {
            questionText: 'Who is CEO of Tesla?',
            answerOptions: [
                {answerText: 'Jeff Bezos', isCorrect: false},
                {answerText: 'Elon Musk', isCorrect: true},
                {answerText: 'Bill Gates', isCorrect: false},
                {answerText: 'Tony Stark', isCorrect: false},
            ],
        },
        {
            questionText: 'The iPhone was created by which company?',
            answerOptions: [
                {answerText: 'Apple', isCorrect: true},
                {answerText: 'Intel', isCorrect: false},
                {answerText: 'Amazon', isCorrect: false},
                {answerText: 'Microsoft', isCorrect: false},
            ],
        },
        {
            questionText: 'How many Harry Potter books are there?',
            answerOptions: [
                {answerText: '1', isCorrect: false},
                {answerText: '4', isCorrect: false},
                {answerText: '6', isCorrect: false},
                {answerText: '7', isCorrect: true},
            ],
        },
    ];
    questions[0].questionText = jsondata.results[0]

    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [showScore, setShowScore] = useState(false);
    const [score, setScore] = useState(0);

    const handleAnswerOptionClick = (isCorrect) => {
        if (isCorrect) {
            setScore(score + 1);
        }

        const nextQuestion = currentQuestion + 1;
        if (nextQuestion < questions.length) {
            setCurrentQuestion(nextQuestion);
        } else {
            setShowScore(true);
        }
    };
    return (
        <div className='app'>
            {showScore ? (
                <div className='score-section'>
                    You scored {score} out of {questions.length}
                </div>
            ) : (
                <>
                    <div className='question-section'>
                        <div className='question-count'>
                            <span>Question {currentQuestion + 1}</span>/{questions.length}
                        </div>
                        <div className='question-text'>{questions[currentQuestion].questionText}</div>
                    </div>
                    <div className='answer-section'>
                        {questions[currentQuestion].answerOptions.map((answerOption) => (
                            <button
                                onClick={() => handleAnswerOptionClick(answerOption.isCorrect)}>{answerOption.answerText}</button>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
}
