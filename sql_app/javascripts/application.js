function submitGetUser(){
    const form = document.forms.getUser;
    window.location.href = form.action + form.elements.user_id.value;
}

function submitPostUsers(){
    const form = document.forms.postUsers;
    const j = {
        "email": form.elements.email.value,
        "password": form.elements.password.value,
    };

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            window.location.href = window.location.href;
        } else if(this.readyState == 4 && this.status != 200) {
            alert('userを登録できませんでした');
        }
    };

    xhr.open(form.method, form.action, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(j));
}

function submitPostItems(){
    const form = document.forms.postItems;
    const j = {
        "title": form.elements.title.value,
        "description": form.elements.description.value,
    };

    const action = "/users/" + form.elements.id.value + "/items/";
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            window.location.href = window.location.href;
        } else if(this.readyState == 4 && this.status != 200) {
            alert('itemを登録できませんでした');
        }
    };

    xhr.open(form.method, action, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(j));
}