// LIGHTBOX SCRIPT

const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightboxImg");
const closeBtn = document.getElementById("closeLightbox");

document.querySelectorAll(".gallery-grid img").forEach(img => {
    img.addEventListener("click", () => {
        lightbox.style.display = "flex";
        lightboxImg.src = img.src;
    });
});

// Close on clicking X
closeBtn.addEventListener("click", () => {
    lightbox.style.display = "none";
});

// Close on clicking outside the image
lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) {
        lightbox.style.display = "none";
    }
});

