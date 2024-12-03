document.addEventListener('DOMContentLoaded', function() {
    const POPULAR_PLATFORMS = [
        "Netflix", "Hulu", "Disney+", "HBO Max", "Amazon Prime Video", 
        "Apple TV+", "Peacock", "Paramount+", "YouTube", "Crunchyroll",
        "BBC America", "AMC+", "Shudder", "Starz", "Criterion Channel",
        "MGM+", "MUBI", "Kanopy", "Curiosity Stream", "Acorn TV", 
        "BritBox", "RetroCrush", "fuboTV", "HiDive", "AsianCrush",
        "VIX", "iQIYI", "Lifetime Movie Club", "Sundance Now", 
        "Pure Flix", "ScreenPix", "ShortsTV", "Night Flight Plus",
        "Dekkoo", "IndieFlix", "Metrograph", "Troma NOW", "Cinemax",
        "Full Moon", "Midnight Pulp", "TBS", "TNT", "USA Network",
        "tru TV", "History Vault", "Hallmark Plus", "Epix", "GuideDoc",
        "Hoopla", "PBS Masterpiece", "Freeform", "BET+", "Cineverse",
        "FilmBox+", "Film Movement Plus", "Fandor", "Kino Film Collection",
        "Klassiki", "Kocowa", "ALLBLK", "ARROW", "Chai Flicks",
        "Cohen Media", "Cultpix", "Hoichoi", "Magellan TV", "Here TV",
        "Screambox", "Sundance Now", "Shahid VIP", "UP Faith & Family",
        "Strand Releasing", "Eros Now Select", "aha"
    ];

    const platformCheckboxes = document.getElementById("platform-checkboxes");
    const anyCheckbox = document.createElement("input");
    anyCheckbox.type = "checkbox";
    anyCheckbox.id = "any-platform";
    anyCheckbox.value = "any";
    anyCheckbox.name = "platforms";
    const anyLabel = document.createElement("label");
    anyLabel.appendChild(anyCheckbox);
    anyLabel.appendChild(document.createTextNode(" Any Platform"));
    platformCheckboxes.appendChild(anyLabel);

    POPULAR_PLATFORMS.forEach(platform => {
        const label = document.createElement("label");
        const input = document.createElement("input");
        input.type = "checkbox";
        input.name = "platforms";
        input.value = platform;
        label.appendChild(input);
        label.appendChild(document.createTextNode(` ${platform}`));
        platformCheckboxes.appendChild(label);
    });

    anyCheckbox.addEventListener("change", function () {
        const isChecked = anyCheckbox.checked;
        const checkboxes = platformCheckboxes.querySelectorAll('input[type="checkbox"]:not(#any-platform)');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
            checkbox.disabled = isChecked;
        });
    });

    function preloadImage(url, onSuccess, onError) {
        const img = new Image();
        img.onload = function () {
            onSuccess(url);
        };
        img.onerror = function () {
            onError();
        };
        img.src = url;
    }

    document.querySelector('#platform-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const platforms = anyCheckbox.checked
            ? null // Indicating no filter for "Any Platform"
            : Array.from(document.querySelectorAll('input[name="platforms"]:checked'))
                  .map(checkbox => checkbox.value);

        let apiUrl = "/movie/random";
        if (platforms) {
            apiUrl += `?platforms=${platforms.join(',')}`;
        }

        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.statusText}`);
                }
                return response.json();
            })
            .then(movie => {
                if (movie.error) {
                    alert(movie.error);
                    document.querySelector('#platform-container').style.display = 'block';
                    document.querySelector('#movie-container').style.display = 'none';
                } else {
                    preloadImage(movie.poster_url,
                        function (url) {
                            document.querySelector('#movie-poster').src = url;
                        },
                        function () {
                            document.querySelector('#movie-poster').src = 'default-poster.jpg';
                        }
                    );

                    document.querySelector('#movie-title').innerText = movie.title;
                    document.querySelector('#movie-release-date').innerText = movie.release_date;
                    document.querySelector('#movie-genres').innerText = movie.genres;
                    document.querySelector('#movie-runtime').innerText = movie.runtime;
                    document.querySelector('#movie-stars').innerText = movie.stars;
                    document.querySelector('#movie-platforms').innerText = 'Streaming on: ' + (movie.platforms || "No platform listed");
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
        const platforms = anyCheckbox.checked
            ? null
            : Array.from(document.querySelectorAll('input[name="platforms"]:checked'))
                  .map(checkbox => checkbox.value);

        let apiUrl = "/movie/random";
        if (platforms) {
            apiUrl += `?platforms=${platforms.join(',')}`;
        }

        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.statusText}`);
                }
                return response.json();
            })
            .then(movie => {
                if (movie.error) {
                    alert(movie.error);
                    document.querySelector('#platform-container').style.display = 'block';
                    document.querySelector('#movie-container').style.display = 'none';
                } else {
                    preloadImage(movie.poster_url,
                        function (url) {
                            document.querySelector('#movie-poster').src = url;
                        },
                        function () {
                            document.querySelector('#movie-poster').src = 'default-poster.jpg';
                        }
                    );

                    document.querySelector('#movie-title').innerText = movie.title;
                    document.querySelector('#movie-release-date').innerText = movie.release_date;
                    document.querySelector('#movie-genres').innerText = movie.genres;
                    document.querySelector('#movie-runtime').innerText = movie.runtime;
                    document.querySelector('#movie-stars').innerText = movie.stars;
                    document.querySelector('#movie-platforms').innerText = 'Streaming on: ' + (movie.platforms || "No platform listed");
                    document.querySelector('#movie-overview').innerText = movie.overview;
                }
            })
            .catch(error => {
                console.error('Error fetching movie:', error);
                alert('An error occurred while fetching the movie. Please try again later.');
            });
    });
});
