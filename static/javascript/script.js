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

function Expand(expandable_id, toggle_btn_id, confirm_btn_id, cancel_btn_id)
{
    if(!document.getElementById(expandable_id).classList.contains("expanded")){
        document.getElementById(expandable_id).classList.add("expanded");
        document.getElementById(toggle_btn_id).style.display = "none";
        document.getElementById(confirm_btn_id).style.display = "inline-block";
        document.getElementById(cancel_btn_id).style.opacity = "100%";
    }
}

function Shrink(expandable_id, toggle_btn_id, confirm_btn_id, cancel_btn_id)
{
    if(document.getElementById(expandable_id).classList.contains("expanded")){
        document.getElementById(expandable_id).classList.remove("expanded");
        document.getElementById(toggle_btn_id).style.display = "inline-block";
        document.getElementById(confirm_btn_id).style.display = "none";
        document.getElementById(cancel_btn_id).style.opacity = "0%";
    }
}