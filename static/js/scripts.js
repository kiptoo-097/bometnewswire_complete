$(window).scroll(function() {
    if ($(this).scrollTop() > 50) {
        $('.navbar').addClass('scrolled');
    } else {
        $('.navbar').removeClass('scrolled');
    }
});

document.addEventListener("DOMContentLoaded", function() {
    // Loop through all the canvas elements that have the class 'pdf-preview'
    document.querySelectorAll('.pdf-preview').forEach(function(canvas) {
        var url = canvas.getAttribute('data-pdf-url');  // Get PDF URL from data attribute
        var context = canvas.getContext('2d');
        var scale = 0.5;  // Scale of the preview image

        // Load and render the PDF document on the canvas
        pdfjsLib.getDocument(url).promise.then(function(pdf) {
            pdf.getPage(1).then(function(page) {
                var viewport = page.getViewport({ scale: scale });
                canvas.height = viewport.height;
                canvas.width = viewport.width;

                page.render({
                    canvasContext: context,
                    viewport: viewport
                });
            });
        });
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const audio = document.getElementById("radioPlayer");
    const playPauseBtn = document.getElementById("playPauseBtn");
    const volumeIcon = document.querySelector(".volume-icon");
    const volumeBar = document.getElementById("volumeBar");

    // Set initial volume
    audio.volume = 0.5;

    // Play/Pause toggle
    playPauseBtn.addEventListener("click", function () {
        if (audio.paused) {
            audio.play();
            playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
        } else {
            audio.pause();
            playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
        }
    });

    // Show/Hide volume bar on icon click
    volumeIcon.addEventListener("click", function () {
        volumeBar.style.display = volumeBar.style.display === "none" ? "block" : "none";
    });

    // Update audio volume
    volumeBar.addEventListener("input", function () {
        audio.volume = this.value;

        // Change icon based on volume level
        if (audio.volume === 0) {
            volumeIcon.className = "volume-icon fas fa-volume-mute";
        } else if (audio.volume < 0.5) {
            volumeIcon.className = "volume-icon fas fa-volume-down";
        } else {
            volumeIcon.className = "volume-icon fas fa-volume-up";
        }
    });
});

// Optional: Add this to your scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('darkModeToggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
        });
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const mainNewsContainer = document.getElementById('main-news-container');
    const newsItems = mainNewsContainer.querySelectorAll('.news-item');
    let currentIndex = 0;

    function showNextNews() {
        // Hide the current news item
        if (newsItems[currentIndex]) {
            newsItems[currentIndex].classList.remove('active');
            newsItems[currentIndex].classList.add('fade-out');
        }

        // Move to the next news item
        currentIndex = (currentIndex + 1) % newsItems.length;

        // Show the next news item
        if (newsItems[currentIndex]) {
            newsItems[currentIndex].classList.remove('d-none');
            newsItems[currentIndex].classList.add('active');
        }
    }

    // Start the animation
    setInterval(showNextNews, 5000); // Adjust the interval as needed

    // Show the first news item immediately
    if (newsItems.length > 0) {
        newsItems[0].classList.add('active');
    }
});