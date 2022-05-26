const ratingForms = document.querySelectorAll('[data-rating-form]');

ratingForms.forEach((form) => {
    const text = form.querySelector('[data-rating-text]');
    const actionField = form.querySelector('[data-rating-action-field]');
    form.querySelector('[data-rating-upvote]').addEventListener('click', () => {
        actionField.setAttribute("value", "upvote");
        text.innerHTML = parseInt(form.querySelector('[data-rating-text]').innerHTML, 10) + 1;
        if (text.innerHTML === '0')
            text.classList.remove('red', 'green');
        if (text.innerHTML === '1') {
            text.classList.remove('red');
            text.classList.add('green');
        }
        form.submit();
    });
    form.querySelector('[data-rating-downvote]').addEventListener('click', () => {
        actionField.setAttribute("value", "downvote");
        text.innerHTML = parseInt(form.querySelector('[data-rating-text]').innerHTML, 10) - 1;
        if (text.innerHTML === '0')
        text.classList.remove('red', 'green');
        if (text.innerHTML === '-1') {
            text.classList.remove('green');
            text.classList.add('red');
        }
        form.submit();
    });
});