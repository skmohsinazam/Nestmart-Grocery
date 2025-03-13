document.addEventListener("DOMContentLoaded", function() {
    let searchInput = document.getElementById("search-input");

    if (searchInput) { // Ensure search bar exists before adding event listener
        searchInput.addEventListener('keyup', function() {
            let query = this.value;

            if (query.length > 0) {
                let baseUrl = window.location.origin; // Get base domain
                fetch(`${baseUrl}/search/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    let resultsContainer = document.getElementById('search-results');
                    resultsContainer.innerHTML = "";  // Clear previous results

                    data.forEach(product => {
                        let item = document.createElement('div');
                        item.classList.add("search-item");

                        let productUrl = `/product/${product.id}/`;  

                        item.innerHTML = `
                            <a href="${productUrl}" style="text-decoration:none; display: flex; align-items: center; ">
                                <img src="${product.image}" alt="${product.name}" width="50" style="margin-right: 10px;">
                                <span>${product.name} - ₹${product.price}</span>
                            </a>
                        `;

                        resultsContainer.appendChild(item);
                    });
                });
            } else {
                document.getElementById('search-results').innerHTML = "";
            }
        });
    }
});
