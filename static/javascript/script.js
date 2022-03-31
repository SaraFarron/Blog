function showPopup(post_id)
{
    id = "popup-"+post_id;
    if(document.getElementById(id).classList.contains("popup-hidden")){
        document.getElementById(id).classList.remove("popup-hidden");
        document.getElementById(id).classList.add("popup-shown");
    }
}

function hidePopup(post_id)
{
    id = "popup-"+post_id;
    if(document.getElementById(id).classList.contains("popup-shown")){
        document.getElementById(id).classList.add("popup-hidden");
        document.getElementById(id).classList.remove("popup-shown")
    }
}