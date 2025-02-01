// main.js

document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('searchForm');
    const resultsDiv = document.getElementById('results');

    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(searchForm);
        const searchParams = new URLSearchParams(formData).toString();

        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: searchParams,
        })
        .then(response => response.json())
        .then(data => {
            renderSearchResults(data);
        })
        .catch(error => {
            console.error('Error searching donors:', error);
            renderSearchResults([]);
        });
    });

    function renderSearchResults(results) {
        resultsDiv.innerHTML = '';
        if (results.length === 0) {
            resultsDiv.innerHTML = '<p>No donors found.</p>';
            return;
        }

        const ul = document.createElement('ul');
        results.forEach(donor => {
            const li = document.createElement('li');
            li.textContent = `${donor.firstName} ${donor.lastName} (${donor.email}) - ${donor.bloodGroup}`;
            ul.appendChild(li);
        });

        resultsDiv.appendChild(ul);
    }
});
