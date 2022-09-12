const delete_button = document.querySelector("#delete-btn");
// const edit_button = document.querySelector("#edit-btn");
const delete_input = document.querySelector("#delete_img");
const current_img = document.querySelector("#profile-picture-image");
const img_input_field = document.querySelector("#profile_picture_input");
const picture_filed = document.querySelector("#profile_picture")
const submit_btn = document.querySelector('#submit-btn')

delete_button.addEventListener("click", () => {
    delete_input.setAttribute("value", "y");
    current_img.setAttribute("src", "/images/profile.png");
    img_input_field.value = '';
    delete_button.classList.add('hidden');
});

img_input_field.onchange = () => {
    if (img_input_field.files[0]) {
        current_img.src = URL.createObjectURL(img_input_field.files[0]);
        
        delete_input.setAttribute("value", "n");
        delete_button.classList.remove('hidden');
    }
};

submit_btn.addEventListener('click', (e) => {
    e.preventDefault();
    if (img_input_field.files[0] && delete_input.getAttribute('value') === 'n') {
        postToImageBan("GahZN7n1FqHJ2orzdylQ", img_input_field.files[0]);
    }
    else {
        document.querySelector('form').submit();
    }
        
});

const postToImageBan = (apiKey, image) => {
    const formData = new FormData();
    formData.append('image', image);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "https://api.imageban.ru/v1");
    xhr.onload = function() {
        const url = JSON.parse(xhr.responseText).data.link;
        picture_filed.setAttribute('value', url);
        document.querySelector('form').submit();
    }
    xhr.setRequestHeader('Authorization', `TOKEN ${apiKey}`);
    xhr.send(formData);
}