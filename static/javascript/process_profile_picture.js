const delete_button = document.querySelector("#delete-btn");
// const edit_button = document.querySelector("#edit-btn");
const delete_input = document.querySelector("#delete_img");
const current_img = document.querySelector("#profile-picture-image");
const img_input_field = document.querySelector("#profile_picture");

delete_button.addEventListener("click", () => {
    delete_input.setAttribute("value", "y");
    current_img.setAttribute("src", "/images/profile.png");
    img_input_field.value = '';
    delete_button.classList.add('hidden');
});

current_img.onerror= () => {
    current_img.src = localStorage.getItem('last_chosen_img');
}

img_input_field.onchange = () => {
    if (img_input_field.files) {
        current_img.src = URL.createObjectURL(img_input_field.files[0]);
        reader.readAsDataURL(img_input_field.files[0]);
        
        delete_input.setAttribute("value", "n");
        delete_button.classList.remove('hidden');
    }
};

const reader = new FileReader();

reader.addEventListener("load", function () {
    // convert image file to base64 string and save to localStorage
    localStorage.setItem("last_chosen_img", reader.result);
}, false);