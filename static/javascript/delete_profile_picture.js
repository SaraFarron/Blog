const delete_button = document.querySelector("#delete-btn");
const edit_button = document.querySelector("#edit-btn");
const delete_input = document.querySelector("#delete_img");
const current_img = document.querySelector("#profile-picture-image");

delete_button.addEventListener("click", () => {
    delete_input.setAttribute("value", "y");
    current_img.setAttribute("src", "/images/profile.png");
});

edit_button.addEventListener("click", () => {
    delete_input.setAttribute("value", "n");
});