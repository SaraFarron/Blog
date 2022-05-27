const ratingForms = document.querySelectorAll('[data-rating-form]');

ratingForms.forEach((form) => {
    const text = form.querySelector('[data-rating-text]');
    const actionField = form.querySelector('[data-rating-action-field]');

    form.querySelector('[data-rating-upvote]').addEventListener('click', () => {
        actionField.setAttribute("value", "upvote");
        const status = form.getAttribute("data-rating-form");
        if (status === 'upvoted') {
            text.innerHTML = parseInt(form.querySelector('[data-rating-text]').innerHTML, 10) - 1;
            form.setAttribute("data-rating-form", "unvoted");
        }
        else if (status === 'downvoted') {
            text.innerHTML = parseInt(form.querySelector('[data-rating-text]').innerHTML, 10) + 2;
            form.setAttribute("data-rating-form", "upvoted");
        }
        else {
            text.innerHTML = parseInt(form.querySelector('[data-rating-text]').innerHTML, 10) + 1;
            form.setAttribute("data-rating-form", "upvoted");
        }
        setColor(text);
        form.submit();
    });
    form.querySelector('[data-rating-downvote]').addEventListener('click', () => {
        actionField.setAttribute("value", "downvote");
        const status = form.getAttribute("data-rating-form");
        if (status === 'upvoted') {
            text.innerHTML = parseInt(form.querySelector('[data-rating-text]').innerHTML, 10) - 2;
            form.setAttribute("data-rating-form", "downvoted");
        }
        else if (status === 'downvoted') {
            text.innerHTML = parseInt(form.querySelector('[data-rating-text]').innerHTML, 10) + 1;
            form.setAttribute("data-rating-form", "unvoted");
        }
        else {
            text.innerHTML = parseInt(form.querySelector('[data-rating-text]').innerHTML, 10) - 1;
            form.setAttribute("data-rating-form", "downvoted");
        }
        setColor(text);
        form.submit();
    });
});

function setColor(text) {
    if (text.innerHTML === '0')
    text.classList.remove('red', 'green');
    if (text.innerHTML === '1') {
        text.classList.remove('red');
        text.classList.add('green');
    }
    if (text.innerHTML === '-1') {
        text.classList.remove('green');
        text.classList.add('red');
    }
}