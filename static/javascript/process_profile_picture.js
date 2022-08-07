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

// current_img.onerror= () => {
//     current_img.src = localStorage.getItem('last_chosen_img');
// }

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
        postToImgbb('beed806b3aa8cbd114d226e6a927a5a6', img_input_field.files[0])
            .then(res => {
                const url = JSON.parse(res).data.url;
                picture_filed.setAttribute('value', url);
                //localStorage.setItem('last_chosen_img', url)
                document.querySelector('form').submit();
            });
    }
    else {
        document.querySelector('form').submit();
    }
        
});

const postToImgbb = async (apiKey, image) => {
    
    const formData = new FormData();
    formData.append('image', image)
    
    const settings = {
        "url": `https://api.imgbb.com/1/upload?key=${apiKey}`,
        "method": "POST",
        "timeout": 0,
        "processData": false,
        "mimeType": "multipart/form-data",
        "contentType": false,
        "data": formData
    };
    
    return await $.ajax(settings).done(function (response) {});
};