document.addEventListener('DOMContentLoaded', function() {
    populateClassDropdown(); // Call the function to populate the class dropdown
    submitQuiz(); // Initialize with one question
});

function calculateScore() {
    let score = 0;
    questions.forEach((question, index) => {
        if (question.correctAnswer === correctAnswers[index]) {
            score++;
        }
    });
    let totalQuestions = questions.length;
    console.log(`Score: ${score} out of ${totalQuestions}`);
}

function submitQuiz() {
    const quizTitle = document.getElementById('quiz-title').value.trim();
    const quizDescription = document.getElementById('quiz-description').value.trim();
    const questions = [];
    const correctAnswers = [];

    document.querySelectorAll('.question-container').forEach(container => {
        const questionText = container.querySelector('.question-text').value.trim();
        const answerChoices = Array.from(container.querySelectorAll('.answer-text')).map(area => area.value.trim());
        const correctAnswer = Array.from(container.querySelectorAll('.answer-choice')).findIndex(choice => choice.checked);
        questions.push({ questionText, answerChoices, correctAnswer });
        correctAnswers.push(correctAnswer);
    });
    console.log(JSON.stringify({ quizTitle, quizDescription, questions }));

    calculateScore();
}


