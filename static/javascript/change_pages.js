const pages = document.querySelectorAll('[data-page]');

const page1toggle = document.querySelector('[data-page-toggle="1"]');
const page2toggle = document.querySelector('[data-page-toggle="2"]');

page1toggle?.addEventListener('click', () => {
    pages[0]?.classList.remove("hidden");
    pages[1]?.classList.add("hidden");
    page2toggle?.classList.remove("toggler-active");
    page1toggle.classList.add("toggler-active");
});

page2toggle?.addEventListener('click', () => {
    pages[1]?.classList.remove("hidden");
    pages[0]?.classList.add("hidden");
    page1toggle?.classList.remove("toggler-active");
    page2toggle.classList.add("toggler-active");
});