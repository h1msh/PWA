// Function to handle login
document.getElementById('login-form')?.addEventListener('submit', async function (e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
    });
    const result = await response.json();
    if (response.status === 200) {
        alert(result.message);
        window.location.href = 'reviews.html'; // Redirect to reviews page
    } else {
        alert(result.message);
    }
});

// Fetch and display reviews
async function loadReviews() {
    const response = await fetch('http://localhost:5000/reviews');
    const reviews = await response.json();
    const reviewsList = document.getElementById('reviews-list');
    reviews.forEach(review => {
        const reviewDiv = document.createElement('div');
        reviewDiv.innerHTML = `
            <h3>${review.title}</h3>
            <p><strong>${review.username}</strong> | ${new Date(review.review_date).toLocaleDateString()}</p>
            <p>Rating: ${review.rating}</p>
            <p>${review.review_text}</p>
        `;
        reviewsList.appendChild(reviewDiv);
    });
}

loadReviews();
