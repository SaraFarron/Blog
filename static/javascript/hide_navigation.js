const toggler = document.querySelector('#toggle-navigation');
const navigation = document.querySelector('.navigation');

window.onresize = () => {

}

navigation.addEventListener('transitionend', (e) => {
    if (!toggler.checked) {
        navigation.classList.add("hidden");
    }
});

navigation.addEventListener('transitionstart', () => {
    if (toggler.checked) {
        navigation.classList.remove("hidden");
    }
});