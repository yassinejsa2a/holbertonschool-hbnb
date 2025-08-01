/**
 * Extracts a cookie value by name from document.cookie
 * @param {string} name - Cookie name to retrieve
 * @returns {string|null} Cookie value or null if not found
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

/**
 * Extracts place ID from URL search parameters
 * @returns {string|null} Place ID from ?id= parameter
 */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Validates user authentication for review operations
 * Redirects to home page if user is not authenticated
 * @returns {string|null} JWT token if authenticated
 */
function checkAuthenticationForReview() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

/**
 * Updates UI based on authentication status
 * Toggles login/logout button visibility and fetches places data
 * @returns {string|null} JWT token if authenticated
 */
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');
    
    if (loginLink && logoutButton) {
        if (token) {
            loginLink.style.display = 'none';
            logoutButton.style.display = 'block';
        } else {
            loginLink.style.display = 'block';
            logoutButton.style.display = 'none';
        }
    }
    
    // Fetch places data only on index page when authenticated
    if (token && document.getElementById('places-list')) {
        fetchPlaces(token);
    }
    return token;
}

/**
 * Controls review form visibility based on authentication
 * Shows form to authenticated users, login prompt to others
 * @returns {string|null} JWT token if authenticated
 */
function checkAuthenticationForReviewForm() {
    const token = getCookie('token');
    const reviewSection = document.querySelector('.add-review');
    const loginMessage = document.getElementById('login-message');
    
    if (reviewSection) {
        if (token) {
            // Show review form for authenticated users
            reviewSection.style.display = 'block';
            if (loginMessage) {
                loginMessage.style.display = 'none';
            }
        } else {
            // Hide form and show login prompt for unauthenticated users
            reviewSection.style.display = 'none';
            if (!loginMessage) {
                // Create login prompt message
                const messageDiv = document.createElement('div');
                messageDiv.id = 'login-message';
                messageDiv.className = 'add-review';
                messageDiv.innerHTML = `
                    <h2>Add a Review</h2>
                    <p>You must be logged in to submit a review.</p>
                    <a href="login.html" class="details-button">Login</a>
                `;
                reviewSection.parentNode.insertBefore(messageDiv, reviewSection.nextSibling);
            } else {
                loginMessage.style.display = 'block';
            }
        }
    }
    
    return token;
}

/**
 * Fetches places data from API and renders them
 * @param {string} token - JWT authentication token
 */
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            document.getElementById('places-list').innerHTML = '<p>Error loading places.</p>';
        }
    } catch (error) {
        document.getElementById('places-list').innerHTML = '<p>API connection error.</p>';
    }
}

/**
 * Renders places list in the DOM
 * @param {Array} places - Array of place objects from API
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';
    places.forEach(async (place) => {
        const placeDiv = document.createElement('div');
        placeDiv.className = 'place-card';
        placeDiv.setAttribute('data-price', place.price);
        
        // Fetch amenities for place list display
        const token = getCookie('token');
        let amenitiesDisplay = 'None';
        
        // Enhanced amenities handling
        if (place.amenities && Array.isArray(place.amenities) && place.amenities.length > 0) {
            const amenityNames = await fetchAmenitiesNames(token, place.amenities);
            if (amenityNames.length > 0) {
                amenitiesDisplay = amenityNames.slice(0, 3).join(', ');
                if (amenityNames.length > 3) {
                    amenitiesDisplay += ` (+${amenityNames.length - 3} more)`;
                }
            }
        }
        
        placeDiv.innerHTML = `
            <img src="/images/appart.jpg" alt="${place.title}" class="place-image">
            <h3>${place.title}</h3>
            <p>${place.description}</p>
            <p>Location: ${place.latitude}, ${place.longitude}</p>
            <p>Price: ${place.price} €</p>
            <p>Amenities: ${amenitiesDisplay}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(placeDiv);
    });
}

/**
 * Initializes price filter dropdown and adds event handler
 * Filters places by maximum price threshold
 */
function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter && priceFilter.options.length === 0) {
        ['All', 10, 50, 100].forEach(val => {
            const opt = document.createElement('option');
            opt.value = val;
            opt.textContent = val;
            // Default to "All" option
            if (val === 'All') {
                opt.selected = true;
            }
            priceFilter.appendChild(opt);
        });
    }
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selected = event.target.value;
            document.querySelectorAll('.place-card').forEach(card => {
                const price = parseFloat(card.getAttribute('data-price'));
                if (selected === 'All' || price <= parseFloat(selected)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

/**
 * Authenticates user with email/password credentials
 * Stores JWT token in cookies and redirects on success
 * @param {string} email - User email address
 * @param {string} password - User password
 */
async function loginUser(email, password) {
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
    } else {
        // Display detailed error message from API response
        try {
            const errorData = await response.json();
            alert('Login failed: ' + (errorData.error || 'Unknown error'));
        } catch (parseError) {
            // Fallback to HTTP status text
            alert('Login failed: ' + response.statusText);
        }
    }
}

/**
 * Fetches and displays detailed information for a specific place
 * @param {string} token - JWT authentication token
 * @param {string} placeId - Unique place identifier
 */
async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            document.querySelector('.place-details').innerHTML = '<p>Error loading place details.</p>';
        }
    } catch (error) {
        document.querySelector('.place-details').innerHTML = '<p>API connection error.</p>';
    }
}

/**
 * Retrieves owner's full name from user API
 * @param {string} token - JWT authentication token
 * @param {string} ownerId - User ID of the place owner
 * @returns {Promise<string>} Owner's full name or 'Unknown'
 */
async function fetchOwnerDetails(token, ownerId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/users/${ownerId}`, {
            method: 'GET',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (response.ok) {
            const owner = await response.json();
            return `${owner.first_name} ${owner.last_name}`;
        }
    } catch (error) {
        console.error('Error fetching owner details:', error);
    }
    return 'Unknown';
}

/**
 * Fetches all reviews and filters by place ID
 * @param {string} token - JWT authentication token
 * @param {string} placeId - Place identifier to filter reviews
 * @returns {Promise<Array>} Array of review objects for the place
 */
async function fetchPlaceReviews(token, placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/reviews`, {
            method: 'GET',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (response.ok) {
            const allReviews = await response.json();
            // Filter reviews for this specific place
            return allReviews.filter(review => review.place_id === placeId);
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
    }
    return [];
}

/**
 * Retrieves user's full name for review attribution
 * @param {string} token - JWT authentication token
 * @param {string} userId - User identifier
 * @returns {Promise<string>} User's full name or 'Unknown User'
 */
async function fetchUserDetails(token, userId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/users/${userId}`, {
            method: 'GET',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (response.ok) {
            const user = await response.json();
            return `${user.first_name} ${user.last_name}`;
        }
    } catch (error) {
        console.error('Error fetching user details:', error);
    }
    return 'Unknown User';
}

/**
 * Fetches amenity details by ID
 * @param {string} token - JWT authentication token
 * @param {string} amenityId - Amenity identifier
 * @returns {Promise<string>} Amenity name or 'Unknown'
 */
async function fetchAmenityDetails(token, amenityId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/amenities/${amenityId}`, {
            method: 'GET',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });
        if (response.ok) {
            const amenity = await response.json();
            return amenity.name || 'Unknown';
        } else {
            console.error(`Failed to fetch amenity ${amenityId}:`, response.status);
        }
    } catch (error) {
        console.error('Error fetching amenity details:', error);
    }
    return 'Unknown';
}

/**
 * Fetches names for a list of amenity IDs
 * @param {string} token - JWT authentication token
 * @param {Array} amenityIds - Array of amenity IDs
 * @returns {Promise<Array>} Array of amenity names
 */
async function fetchAmenitiesNames(token, amenityIds) {
    // Handle null, undefined, empty array, or non-array cases
    if (!amenityIds || !Array.isArray(amenityIds) || amenityIds.length === 0) {
        return [];
    }
    
    console.log('Fetching amenities for IDs:', amenityIds); // Debug log
    
    try {
        const amenityNames = await Promise.all(
            amenityIds.map(id => fetchAmenityDetails(token, id))
        );
        
        console.log('Retrieved amenity names:', amenityNames); // Debug log
        
        // Filter out 'Unknown' amenities to avoid displaying them
        const validAmenities = amenityNames.filter(name => name !== 'Unknown' && name !== null);
        
        return validAmenities;
    } catch (error) {
        console.error('Error fetching amenities names:', error);
        return [];
    }
}

/**
 * Renders reviews section with user names and ratings
 * @param {string} token - JWT authentication token
 * @param {string} placeId - Place identifier for reviews
 */
async function displayReviews(token, placeId) {
    const reviewsSection = document.querySelector('.reviews');
    if (reviewsSection) {
        reviewsSection.innerHTML = '<p>Loading reviews...</p>';
        
        const reviews = await fetchPlaceReviews(token, placeId);
        reviewsSection.innerHTML = '';
        
        if (reviews && reviews.length > 0) {
            for (const review of reviews) {
                const userName = await fetchUserDetails(token, review.user_id);
                const reviewDiv = document.createElement('div');
                reviewDiv.className = 'review-card';
                reviewDiv.innerHTML = `
                    <p>${review.text}</p>
                    <p>User: ${userName}</p>
                    <p>Rating: ${review.rating}/5</p>
                `;
                reviewsSection.appendChild(reviewDiv);
            }
        } else {
            reviewsSection.innerHTML = '<p>No reviews yet.</p>';
        }
    }
}

/**
 * Renders place details including owner info, amenities, and reviews
 * @param {Object} place - Place object from API
 */
async function displayPlaceDetails(place) {
    const detailsSection = document.querySelector('.place-details');
    if (detailsSection) {
        // Fetch owner information for display
        const token = getCookie('token');
        const ownerName = place.owner_id ? await fetchOwnerDetails(token, place.owner_id) : 'Unknown';
        
        console.log('Place object:', place); // Debug log
        console.log('Place amenities:', place.amenities); // Debug log
        
        // Enhanced amenities handling
        let amenitiesDisplay = 'None';
        
        if (place.amenities && Array.isArray(place.amenities) && place.amenities.length > 0) {
            const amenityNames = await fetchAmenitiesNames(token, place.amenities);
            amenitiesDisplay = amenityNames.length > 0 ? amenityNames.join(', ') : 'None';
        } else if (place.amenities && !Array.isArray(place.amenities)) {
            console.warn('Amenities is not an array:', place.amenities);
            amenitiesDisplay = 'Invalid amenities format';
        }
        
        detailsSection.innerHTML = `
            <img src="/images/appart.jpg" alt="${place.title}" class="place-image">
            <h2>${place.title}</h2>
            <div class="place-info">
                <p>Host: ${ownerName}</p>
                <p>Price per night: ${place.price} €</p>
                <p>Description: ${place.description}</p>
                <p>Location: ${place.latitude}, ${place.longitude}</p>
                <p>Amenities: ${amenitiesDisplay}</p>
            </div>
        `;
    }

    // Load and display reviews for this place
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    await displayReviews(token, placeId);
}

/**
 * Renders place information for review submission page
 * @param {Object} place - Place object from API
 */
async function displayPlaceInfoForReview(place) {
    const placeInfoSection = document.getElementById('place-info');
    if (placeInfoSection) {
        placeInfoSection.innerHTML = `
            <h2>Reviewing: ${place.title}</h2>
            <div class="place-info">
                <p>Price per night: ${place.price} €</p>
                <p>Description: ${place.description}</p>
            </div>
        `;
    }
}

/**
 * Submits a new review to the API
 * @param {string} token - JWT authentication token
 * @param {string} placeId - Place identifier for the review
 * @param {string} reviewText - Review content text
 * @param {number} rating - Numeric rating (1-5)
 */
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating),
                place_id: placeId
                // user_id is extracted from JWT token on backend
            })
        });
        await handleReviewResponse(response);
    } catch (error) {
        alert('API connection error');
    }
}

/**
 * Processes review submission response and handles UI updates
 * @param {Response} response - Fetch API response object
 */
async function handleReviewResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        document.getElementById('review-form').reset();
        // Navigate back to place details page
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            window.location.href = `place.html?id=${placeId}`;
        }
    } else {
        try {
            const errorData = await response.json();
            // Check for different possible error message formats
            const errorMessage = errorData.message || errorData.error || errorData.description || 'Unknown error';
            alert('Failed to submit review: ' + errorMessage);
        } catch (parseError) {
            // Fallback if JSON parsing fails
            alert('Failed to submit review: ' + response.statusText);
        }
    }
}

/**
 * Clears authentication token and refreshes the page
 */
function logout() {
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT';
    window.location.reload();
}

/**
 * Main application initialization when DOM is loaded
 * Handles page-specific functionality and event listeners
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize authentication state across all pages
    checkAuthentication();

    // Login page functionality
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // Index page: places list and price filtering
    if (document.getElementById('places-list')) {
        setupPriceFilter();
        fetchPlaces(getCookie('token'));
    }

    // Place details page: show place info and reviews
    if (document.querySelector('.place-details')) {
        const placeId = getPlaceIdFromURL();
        const token = getCookie('token');
        fetchPlaceDetails(token, placeId);
        
        // Control review form visibility based on auth status
        checkAuthenticationForReviewForm();
    }

    // Add review page: authentication-protected functionality
    if (window.location.pathname.includes('add_review.html')) {
        // Ensure user is authenticated, redirect if not
        const token = checkAuthenticationForReview();
        const placeId = getPlaceIdFromURL();
        
        if (!placeId) {
            alert('No place ID provided. Redirecting to home page.');
            window.location.href = 'index.html';
            return;
        }
        
        // Load place information for context
        fetchPlaceDetails(token, placeId).then(() => {
            const placeDetailsSection = document.querySelector('.place-details');
            if (placeDetailsSection) {
                // Transfer content to review page layout
                const placeInfoSection = document.getElementById('place-info');
                if (placeInfoSection) {
                    placeInfoSection.innerHTML = placeDetailsSection.innerHTML;
                }
            }
        });
    }

    // Review form submission (works on both place.html and add_review.html)
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const placeId = getPlaceIdFromURL();
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Security check: verify authentication at submission time
            const token = getCookie('token');
            if (!token) {
                alert('You must be logged in to submit a review. Redirecting to login page...');
                window.location.href = 'login.html';
                return;
            }
            
            if (!placeId) {
                alert('No place ID provided.');
                return;
            }
            
            const reviewText = document.getElementById('review-text').value;
            const rating = document.getElementById('rating').value;
            
            if (!reviewText || !rating) {
                alert('Please fill in all fields.');
                return;
            }
            
            await submitReview(token, placeId, reviewText, rating);
        });
    }

    // Logout button functionality
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }
});