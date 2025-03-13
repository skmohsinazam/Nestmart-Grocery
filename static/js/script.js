const carousel = document.querySelector('.carousell-inner');
const items = document.querySelectorAll('.carousell-item');
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');

let currentIndex = 0;

function showSlide(index) {
    carousel.style.transform = `translateX(-${index * 100}%)`;
}

prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex === 0) ? items.length - 1 : currentIndex - 1;
    showSlide(currentIndex);
});

nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex === items.length - 1) ? 0 : currentIndex + 1;
    showSlide(currentIndex);

});
    