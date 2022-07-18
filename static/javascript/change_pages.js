const pages = document.querySelectorAll('[data-page]');

const page1toggle = document.querySelector('[data-page-toggle="1"]');
const page2toggle = document.querySelector('[data-page-toggle="2"]');

const height1 = pages[0] ? pages[0].clientHeight : undefined;
const height2 = pages[1] ? pages[1].clientHeight : undefined;

const maxHeight = height1 && height2 ? Math.max(height1, height2) : undefined;

page1toggle?.addEventListener('click', () => {
    if (maxHeight) {
        pages[1].style.height = maxHeight + "px";
        pages[0].style.height = height1 + "px";
    }
    pages[0].classList.remove("hidden");
    pages[1]?.classList.add("hidden");
    page2toggle?.classList.remove("toggler-active");
    page1toggle.classList.add("toggler-active");
});

page2toggle?.addEventListener('click', () => {
    if (maxHeight) {
        pages[0].style.height = maxHeight + "px";
        pages[1].style.height = height2 + "px";
    }
    pages[1].classList.remove("hidden");
    pages[0]?.classList.add("hidden");
    page1toggle?.classList.remove("toggler-active");
    page2toggle.classList.add("toggler-active");
});