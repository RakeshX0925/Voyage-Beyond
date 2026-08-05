// quiz.js – Handles quiz scoring

document.addEventListener("DOMContentLoaded", () => {
    const quizForm = document.getElementById("quizForm");
    const resultBox = document.getElementById("result");

    quizForm.addEventListener("submit", function (e) {
        e.preventDefault();

        let score = 0;

        // Correct Answers
        const answers = {
            q1: "Jupiter",
            q2: "Milky Way",
            q3: "Star",
            q4: "Mercury",
            q5: "Sagittarius A*"
        };

        // Check all answers
        let allAnswered = true;

        for (let key in answers) {
            const selected = quizForm.elements[key].value;

            if (!selected) {
                allAnswered = false;
                break;
            }

            if (selected === answers[key]) {
                score++;
            }
        }

        // If any question not answered
        if (!allAnswered) {
            resultBox.style.display = "block";
            resultBox.textContent = "Please answer all questions!";
            resultBox.style.background = "rgba(255, 100, 100, 0.2)";
            return;
        }

        // Display Score
        resultBox.style.display = "block";
        resultBox.style.background = "rgba(0, 255, 150, 0.2)";
        resultBox.textContent = `Your Score: ${score} / 5`;
    });
});
