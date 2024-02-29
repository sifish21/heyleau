var username = document.getElementById('floatingInput');
var password = document.getElementById('floatingPassword');
var bouton = document.getElementById('submit-button');
var form = document.getElementById('form');

form.addEventListener('change', function() {
    if(check_username_field() && check_password_field()){
        bouton.disabled = false;
        bouton.style.backgroundColor = 'pink';
    } else {
        bouton.disabled = true;
        bouton.style.color = 'ligthgray';
    }
});

password.addEventListener('input', function(){
    if(check_username_field() && check_password_field()){
        bouton.disabled = false;
        bouton.style.backgroundColor = 'pink';
    }
})

function check_username_field(){
    var regex = new RegExp("^[a-zA-Z]{3,20}$");
    return regex.test(username.value);
}

function check_password_field(){
    var regex = new RegExp("^[a-zA-Z]{3,20}$");
    return regex.test(password.value);
}

