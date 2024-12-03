document.addEventListener('DOMContentLoaded', function() {
    function preloadImage(url, onSuccess, onError) {
        const img = new Image();
        img.onload = function() {
            onSuccess(url);
        };
        img.onerror = function() {
            onError();
        };
        img.src = url;
    }

    document.querySelector('#platform-form').addEventListener('submit', function(event) {
        event.preventDefault();
        
        let platforms = Array.from(document.querySelectorAll('input[name="platforms"]:checked'))
                            .map(checkbox => checkbox.value);
        
        if (platforms.length === 0) {
            alert("Please select at least one platform.");
            return;
        }
        
        fetch(`/movie/random?platforms=${platforms.join(',')}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.statusText}`);
                }
                return response.json();
            })
            .then(movie => {
                if (movie.error) {
                    alert(movie.error);
                    // Optionally, redirect back to platform selection
                    document.querySelector('#platform-container').style.display = 'block';
                    document.querySelector('#movie-container').style.display = 'none';
                } else {
                    preloadImage(movie.poster_url, 
                        function(url) {
                            document.querySelector('#movie-poster').src = url;
                        }, 
                        function() {
                            document.querySelector('#movie-poster').src = 'default-poster.jpg';

                        }
                    );
                    
                    document.querySelector('#movie-title').innerText = movie.title;
                    document.querySelector('#movie-release-date').innerText = movie.release_date;
                    document.querySelector('#movie-genres').innerText = movie.genres;
                    document.querySelector('#movie-runtime').innerText = movie.runtime;
                    document.querySelector('#movie-stars').innerText = movie.stars;
                    document.querySelector('#movie-platforms').innerText = 'Streaming on: ' + movie.platforms;
                    document.querySelector('#movie-overview').innerText = movie.overview;

                    document.querySelector('#platform-container').style.display = 'none';
                    document.querySelector('#movie-container').style.display = 'flex';
                }
            })
            .catch(error => {
                console.error('Error fetching movie:', error);
                alert('An error occurred while fetching the movie. Please try again later.');
            });
    });

    document.querySelector('#next-movie-btn').addEventListener('click', function() {
        let platforms = Array.from(document.querySelectorAll('input[name="platforms"]:checked'))
                            .map(checkbox => checkbox.value);

        fetch(`/movie/random?platforms=${platforms.join(',')}`)

            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.statusText}`);
                }
                return response.json();
            })
            .then(movie => {
                if (movie.error) {
                    alert(movie.error);
                    // Optionally, redirect back to platform selection
                    document.querySelector('#platform-container').style.display = 'block';
                    document.querySelector('#movie-container').style.display = 'none';
                } else {
                    preloadImage(movie.poster_url, 
                        function(url) {
                            document.querySelector('#movie-poster').src = url;
                        }, 
                        function() {
                            document.querySelector('#movie-poster').src = '../static/default-poster.jpg';
                        }
                    );
                    
                    document.querySelector('#movie-title').innerText = movie.title;
                    document.querySelector('#movie-release-date').innerText = movie.release_date;
                    document.querySelector('#movie-genres').innerText = movie.genres;
                    document.querySelector('#movie-runtime').innerText = movie.runtime;
                    document.querySelector('#movie-stars').innerText = movie.stars;
                    document.querySelector('#movie-platforms').innerText = 'Streaming on: ' + movie.platforms;
                    document.querySelector('#movie-overview').innerText = movie.overview;
                }
            })
            .catch(error => {
                console.error('Error fetching movie:', error);
                alert('An error occurred while fetching the movie. Please try again later.');
            });
    });
});