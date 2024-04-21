

document.addEventListener('DOMContentLoaded', function() {
    // Initialize with one question for each class
    ['COP 3363 Introduction to C++',
    'COP 3330 Data Structures, Algorithms, and Generic Programming I',
    'CDA 3100 Computer Organization I',
    'CEN 4020 Software Engineering I',
    'CEN 4090L Software Engineering Capstone',
    'CIS 3250 Ethics in Computer Science',
    'COP 4610 Operating Systems & Concurrent Programming',
    'COP 4530 Data Structures, Algorithms, and Generic Programming II',
    'COP 4521 Secure Parallel & Distributed Programming w/ Python',
    'COT 4420 Theory of Computation'].forEach(className => {
        newQuestion(className);
    });
});

function newQuestion() {
    const questionsContainer = document.getElementById('questions-container');
    const questionNumber = questionsContainer.children.length + 1;
    const questionContainer = document.createElement('div');
    questionContainer.className = 'question-container';
    questionContainer.innerHTML = getNewQuestionHtml(questionNumber);
    questionsContainer.appendChild(questionContainer);
    newAnswer(questionNumber); // Add one initial answer choice
}

function getNewQuestionHtml(questionNumber) {
    return `<div id="question-${questionNumber}">
                <h2 class="question-header">Question:</h2>
                <textarea class="question-text" id="question-text-${questionNumber}"></textarea>
                <div id="answer-container-${questionNumber}">
                    <!-- Answer choices will be added here -->
                </div>
                <button type="button" onclick="newAnswer(${questionNumber})">Add Answer Choice</button>
                <button type="button" onclick="submitQuestion(${questionNumber})">Submit Question</button>
                <button type="button" onclick="resetQuestion(${questionNumber})">Reset Question</button>
                <button type="button" class="delete-question" onclick="deleteQuestion(this)">Delete Question</button>
            </div>`;
}

function newAnswer(questionNumber) {
    const answerContainer = document.getElementById(`answer-container-${questionNumber}`);
    const answer = document.createElement('div');
    const answerNumber = answerContainer.children.length + 1;
    answer.className = 'answer';
    answer.innerHTML = getNewAnswerHtml(questionNumber, answerNumber);
    answerContainer.appendChild(answer);
}

function getNewAnswerHtml(questionNumber, answerNumber) {
    return `<label class="answer-select">
                <input type="radio" name="answer-${questionNumber}" class="answer-choice-${questionNumber}">
            </label>
            <label class="answer-text-label">
                <textarea class="answer-text" id="text-answer-${questionNumber}-${answerNumber}"></textarea>
            </label>
            <button type="button" class="delete-answer" onclick="this.parentNode.remove()">X</button>`;
}

function resetQuestion(questionNumber) {
    const questionContainer = document.getElementById(`question-${questionNumber}`);
    questionContainer.querySelector('.question-text').value = '';
    questionContainer.querySelectorAll('.answer').forEach(answer => answer.remove());
    newAnswer(questionNumber); // Add one new answer choice
}

function resetForm() {
    document.getElementById('questions-container').innerHTML = '';
    newQuestion(); // Start fresh with one new question
}

function deleteQuestion(button) {
    const questionContainer = button.parentNode.parentNode;
    questionContainer.remove();// Remove the entire question container
}

function saveQuiz() {
    const quizTitle = document.getElementById('quiz-title').value.trim();
    const quizDescription = document.getElementById('quiz-description').value.trim();
    const questions = [];

    document.querySelectorAll('.question-container').forEach(container => {
        const questionText = container.querySelector('.question-text').value.trim();
        const answerChoices = Array.from(container.querySelectorAll('.answer-text')).map(area => area.value.trim());
        const correctAnswer = Array.from(container.querySelectorAll('.answer-choice')).findIndex(choice => choice.checked);
        questions.push({ questionText, answerChoices, correctAnswer });
    });

    console.log(JSON.stringify({ quizTitle, quizDescription, questions }));
    window.location.href = "/quizzes";
}