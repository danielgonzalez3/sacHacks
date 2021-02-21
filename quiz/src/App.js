import React, {useState, useEffect} from "react";
import data from './data/data.json';

export default function App() {
    //this creates garbage variable i
    let i;
    // This initialises a request to the trivia database API
    const url = "https://opentdb.com/api.php?amount=50&category=23&difficulty=medium&type=multiple";
    var question;
    var type;
    var correctAnswer;
    var incorrect1;
    var incorrect2;
    var incorrect3;
    console.log(data);


    // This function is used to extract the received data
    function getData(input) {
        // This is the question:
        question = data.results[input].question;
        // This is the question type eg. multiple choice
        type = data.results[input].type;
        // This is the correct answer
        correctAnswer = data.results[input].correct_answer;
        // These are the three incorrect answers
        incorrect1 = data.results[input].incorrect_answers[0];
        incorrect2 = data.results[input].incorrect_answers[1];
        incorrect3 = data.results[input].incorrect_answers[2];

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
        options[randoms[0]] = correctAnswer;
        options[randoms[1]] = incorrect1;
        options[randoms[2]] = incorrect2;
        options[randoms[3]] = incorrect3;
        console.log(options);
        return options;


    }

    var numbers = []; // an array to store unique random numbers
    var numberinos;

    // loop runs four times...
    for (i = 0; i < 5; i++) {
        // generates a random number between 0 and 48
        numberinos = Math.floor(Math.random() * 48);
        // checks if random number already in array...
        while (numbers.includes(numberinos)) {
            // generates another random number
            numberinos = Math.floor(Math.random() * 48);
        }
        // adds random number to array
        numbers.push(numberinos);
    }
    console.log(numbers);
    var question1 = getData(numbers[0])
    var question2 = getData(numbers[1])
    var question3 = getData(numbers[2])
    var question4 = getData(numbers[3])
    var question5 = getData(numbers[4])

    console.log(
        question1 = getData(numbers[0])
    )
    ;
    const questions = [
        {
            questionText: data.results[numbers[0]].question,
            answerOptions: [
                {
                    answerText: question1[0],
                    isCorrect: question1[0] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question1[1],
                    isCorrect: question1[1] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question1[2],
                    isCorrect: question1[2] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question1[3],
                    isCorrect: question1[3] === data.results[numbers[0]].correct_answer
                },
            ],
        },
        {
            questionText: data.results[numbers[0]].question,
            answerOptions: [
                {
                    answerText: question2[0],
                    isCorrect: question2[0] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question2[1],
                    isCorrect: question2[1] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question2[2],
                    isCorrect: question2[2] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question2[3],
                    isCorrect: question2[3] === data.results[numbers[0]].correct_answer
                },
            ],
        },
        {
            questionText: data.results[numbers[0]].question,
            answerOptions: [
                {
                    answerText: question3[0],
                    isCorrect: question3[0] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question3[1],
                    isCorrect: question3[1] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question3[2],
                    isCorrect: question3[2] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question3[3],
                    isCorrect: question3[3] === data.results[numbers[0]].correct_answer
                },
            ],
        },
        {
            questionText: data.results[numbers[0]].question,
            answerOptions: [
                {
                    answerText: question4[0],
                    isCorrect: question4[0] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question4[1],
                    isCorrect: question4[1] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question4[2],
                    isCorrect: question4[2] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question4[3],
                    isCorrect: question4[3] === data.results[numbers[0]].correct_answer
                },
            ],
        },
        {
            questionText: data.results[numbers[0]].question,
            answerOptions: [
                {
                    answerText: question5[0],
                    isCorrect: question5[0] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question5[1],
                    isCorrect: question5[1] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question5[2],
                    isCorrect: question5[2] === data.results[numbers[0]].correct_answer
                },
                {
                    answerText: question5[3],
                    isCorrect: question5[3] === data.results[numbers[0]].correct_answer
                },
            ],
        },
    ];

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
