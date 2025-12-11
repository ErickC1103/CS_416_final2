$(document).ready(function() {
    // Apply dark mode if previously enabled
    if (localStorage.getItem("darkMode") === "enabled") {
        $("body").addClass("dark-mode");
    }

    // Toggle dark mode on button click
    $("#darkModeBtn").click(function() {
        $("body").toggleClass("dark-mode");

        // Save preference
        if ($("body").hasClass("dark-mode")) {
            localStorage.setItem("darkMode", "enabled");
        } else {
            localStorage.setItem("darkMode", "disabled");
        }
    });
});