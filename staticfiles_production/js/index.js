// Adds an underline to the active or hovered navigation link on the navbar
$(document).ready(function() {
    // Get current path
    var currentPath = window.location.pathname;
    
    // Loop through nav-links and add 'active' to the matching one
    $('.nav-link').each(function() {
        if ($(this).attr('href') === currentPath) {
            $(this).addClass('active').attr('data-original-active', true);
        }
    });
});

// Add 'active' class on hover
$('.nav-link').hover(
    function() {
        $(this).addClass('active');
    },
    function() {
        // Check if this link was originally active
        if (!$(this).attr('data-original-active')) {
            $(this).removeClass('active');
        }
        
    }
);

// Enable/disable Clear Results btn
$(document).ready(function() {
    // Function to check for fixture tables
    function checkForFixtures() {
        if ($('.table-responsive').length > 0) {
            // Enable the "Clear Results" button if tables exist
            $('#clearResultsBtn').prop('disabled', false);
            $('#clearResultsBtn').prop('class', 'btn btn-info w-100');
            $('#clearResultsBtn').css({"pointer-events": "auto"});


        } else {
            // Disable the "Clear Results" button if no tables exist
            $('#clearResultsBtn').prop('disabled', true);
            $('#clearResultsBtn').prop('class', 'btn btn-secondary w-100');
            $('#clearResultsBtn').css({"pointer-events": "none"});
        }
    }

    // Initial check on page load
    checkForFixtures();

    // Check after results are requested
    $('#getFixturesBtn').click(function() {
        checkForFixtures();
    });
});