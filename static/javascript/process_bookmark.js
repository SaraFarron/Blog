const bookmarkForms = document.querySelectorAll('[data-bookmark-form]');

bookmarkForms.forEach((form) => {
    const icon_active = form.querySelector('[data-bookmark-icon-active]');
    const icon_inactive = form.querySelector('[data-bookmark-icon-inactive]');

    form.addEventListener('click', () => {
        if (!form.classList.contains('animating')) {
            form.classList.add("animating");
            const status = form.getAttribute("data-bookmark-form");
            if (status === 'saved') {
                icon_active.classList.add('hidden');
                icon_inactive.classList.remove('hidden');
                form.setAttribute("data-bookmark-form", "not-saved");
            }
            else if (status === 'not-saved') {
                icon_active.classList.remove('hidden');
                icon_inactive.classList.add('hidden');
                form.setAttribute("data-bookmark-form", "saved");
            }

            form.submit();
        }
    });

    form.addEventListener('transitionend', () => {
        form.classList.remove('animating');
    });
});