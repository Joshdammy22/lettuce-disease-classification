// static/js/script.js
$(document).ready(function() {
    // Example: Add an elastic effect to elements with the 'hero-section' class on hover
    $('.hero-section').hover(
        function() {
            $(this).animate({ transform: 'scale(1.05)' }, 500);
        }, function() {
            $(this).animate({ transform: 'scale(1)' }, 500);
        }
    );

    // Example: Toggle class on button click
    $('.btn').on('click', function() {
        $(this).toggleClass('active');
    });
});
