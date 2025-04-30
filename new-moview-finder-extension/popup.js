document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('search');
    // const queryInput = document.getElementById('query');
    const streamingInputs = document.getElementsByName('streaming');
    const topkInput = document.getElementById('topK');
    const resultDiv = document.getElementById('result');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const movieTitleDiv = document.getElementById('movie-title');
    const movieInfoDiv = document.getElementById('movie-info');
    const streamingLinksDiv = document.getElementById('streaming-links');

    // API endpoint - update this to your FastAPI server URL
    const API_URL = 'http://localhost:8000/query';

    searchButton.addEventListener('click', async function() {
        const streaming_options = [];
        streamingInputs.forEach(si => {if(si.checked) {streaming_options.push(si.value.trim())}});
        // const query = queryInput.value.trim();
        if (!streaming_options && streaming_options.length == 0) {
            showError('Please select atleast one radio');
            return;
        }
        const topK = topkInput.value.trim();

        // Show loading state
        loadingDiv.style.display = 'block';
        resultDiv.style.display = 'none';
        errorDiv.style.display = 'none';

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ topK: topK,  streaming_option: streaming_options[0]})
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Clear previous results
            resultDiv.innerHTML = '';
            
            // Create a container for all movies
            const moviesContainer = document.createElement('div');
            moviesContainer.className = 'movies-container';
            
            // Process each movie
            data.movies.forEach(movie => {
                const movieCard = document.createElement('div');
                movieCard.className = 'movie-card';
                
                // Create movie title
                const titleElement = document.createElement('div');
                titleElement.className = 'movie-title';
                titleElement.textContent = movie.title;
                
                // Create movie info
                const infoElement = document.createElement('div');
                infoElement.className = 'movie-info';
                infoElement.textContent = `Released in ${movie.year} | IMDB Rating: ${movie.rating}`;
                
                // Create streaming links
                const linksElement = document.createElement('div');
                linksElement.className = 'streaming-links';
                
                movie.streaming_links.forEach(link => {
                    const linkElement = document.createElement('a');
                    linkElement.href = link;
                    linkElement.textContent = link;
                    linkElement.className = 'streaming-link';
                    linkElement.target = '_blank';
                    linksElement.appendChild(linkElement);
                });
                
                // Assemble the movie card
                movieCard.appendChild(titleElement);
                movieCard.appendChild(infoElement);
                movieCard.appendChild(linksElement);
                
                // Add the movie card to the container
                moviesContainer.appendChild(movieCard);
            });
            
            // Add the movies container to the result div
            resultDiv.appendChild(moviesContainer);
            
            // Show results
            resultDiv.style.display = 'block';
            loadingDiv.style.display = 'none';
        } catch (error) {
            showError('Error fetching movie information. Please try again.');
            console.error('Error:', error);
        }
    });

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        loadingDiv.style.display = 'none';
        resultDiv.style.display = 'none';
    }

    // Allow search on Enter key
    // queryInput.addEventListener('keypress', function(e) {
    //     if (e.key === 'Enter') {
    //         searchButton.click();
    //     }
    // });
}); 