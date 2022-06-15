const userIsAuthenticated = document.body.getAttribute('data-user-is-authenticated') === 'true';

const ratingForms = document.querySelectorAll('[data-rating-form]');

ratingForms.forEach((form) => {
    const ratingLabel = form.querySelector('[data-rating-text]');
    const animLabel = form.querySelector('[data-animation-label]');
    const actionField = form.querySelector('[data-rating-action-field]');
    let change = 0;

    form.querySelector('[data-rating-upvote]').addEventListener('click', () => {
        if (userIsAuthenticated) {
            if (!ratingLabel.classList.contains('animating')) {
                ratingLabel.classList.add("animating");
                actionField.setAttribute("value", "upvote");
                const status = form.getAttribute("data-rating-form");
                if (status === 'upvoted') {
                    change = -1;
                    form.setAttribute("data-rating-form", "unvoted");
                }
                else if (status === 'downvoted') {
                    change = +2;
                    form.setAttribute("data-rating-form", "upvoted");
                }
                else {
                    change = +1;
                    form.setAttribute("data-rating-form", "upvoted");
                }
                animLabel.innerHTML = change > 0 ? `+${change}` : change;

                form.submit();
            }
        }
        else {
            showNotification('login-required');
        }
    });
    form.querySelector('[data-rating-downvote]').addEventListener('click', () => {
        if (userIsAuthenticated) {
            if (!ratingLabel.classList.contains('animating')) {
                ratingLabel.classList.add("animating");
                actionField.setAttribute("value", "downvote");
                const status = form.getAttribute("data-rating-form");
                if (status === 'upvoted') {
                    change = -2;
                    form.setAttribute("data-rating-form", "downvoted");
                }
                else if (status === 'downvoted') {
                    change = +1;
                    form.setAttribute("data-rating-form", "unvoted");
                }
                else {
                    change = -1;
                    form.setAttribute("data-rating-form", "downvoted");
                }
                animLabel.innerHTML = change > 0 ? `+${change}` : change;

                form.submit();
            }
        }
        else {
            showNotification('login-required');
        }
    });

    animLabel.addEventListener('animationend', () => {
        ratingLabel.innerHTML = parseInt(ratingLabel.innerHTML, 10) + change;
        setColor(ratingLabel);
        ratingLabel.classList.remove('animating');
    });
});

function setColor(label) {
    if (parseInt(label.innerHTML, 10) === 0)
    label.classList.remove('red', 'green');
    if (parseInt(label.innerHTML, 10) > 0) {
        label.classList.remove('red');
        label.classList.add('green');
    }
    if (parseInt(label.innerHTML, 10) < 0) {
        label.classList.remove('green');
        label.classList.add('red');
    }
}


const bookmarkForms = document.querySelectorAll('[data-bookmark-form]');

bookmarkForms.forEach((form) => {
    const icon_active = form.querySelector('[data-bookmark-icon-active]');
    const icon_inactive = form.querySelector('[data-bookmark-icon-inactive]');

    form.addEventListener('click', () => {
        if (userIsAuthenticated) {
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
        }
        else {
            showNotification('login-required');
        }
    });

    form.addEventListener('transitionend', () => {
        form.classList.remove('animating');
    });
});

function showNotification(templateName)
{
    notificationList = document.querySelector('[data-notification-list]');
    notificationTemplate = document.querySelector(`[data-notification-template="${templateName}"]`);
    if (notificationTemplate != null) {
        let notificationElement = notificationTemplate.cloneNode(true);
        notificationElement.style.display = "block";
        notificationList.append(notificationElement);
    }
}