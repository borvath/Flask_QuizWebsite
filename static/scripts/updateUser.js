function openUserUpdateForm(userid, username, firstname, lastname) {
    document.getElementById("update-user-form").style.display = "block";
    document.getElementById("update-userid").value = userid;
    document.getElementById("update-username").value = username;
    document.getElementById("update-firstname").value = firstname;
    document.getElementById("update-lastname").value = lastname;
}

function closeUserUpdateForm(){
    document.getElementById("update-user-form").style.display = "none";
    document.getElementById("update-userid").value = -1;
    document.getElementById("update-username").value = '';
    document.getElementById("update-firstname").value = '';
    document.getElementById("update-lastname").value = '';
}
