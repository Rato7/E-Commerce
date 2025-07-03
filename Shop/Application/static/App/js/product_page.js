document.addEventListener('DOMContentLoaded', function () {
    const mainImage = document.querySelector('.main-image');
    const thumbnails = document.querySelectorAll('.thumb-image');

    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', () => {
            mainImage.src = thumb.src;
        });
    });
});