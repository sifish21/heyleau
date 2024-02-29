var nom_field = document.getElementById('nom_field');
var nombre_field = document.getElementById('nombre_field');
var depot_field = document.getElementById('depot-field');
var fin_a_payer_field = document.getElementById('fin_payer_field');
var total_field = document.getElementById('total_field');
var form = document.getElementById('formulaire-nouveau');
var bouton_autre = document.getElementById('submit-button-autre');
var bouton_enregistrer = document.getElementById('submit-button-enregistrer');

document.querySelectorAll('.type-paiement').forEach(box => {
    box.addEventListener('click', function() {
      document.querySelectorAll('.type-paiement').forEach(otherBox => {
        otherBox.style.backgroundColor = 'white';
      });
      this.style.backgroundColor = 'lightgreen';
    });
});


form.addEventListener('input', function() {
    console.log('caca');
    if(check_all_fields()){
        console.log('caca');
        bouton_autre.style.backgroundColor = 'pink';
        bouton_enregistrer.style.backgroundColor = 'pink';
        bouton_autre.disabled = false;
        bouton_enregistrer.disabled = true;
    }
});

function check_type_paiement(){
    var divs = document.querySelectorAll('.type-paiement');
    var valid = false;
    Array.from(divs).forEach(function(div){
        var style = window.getComputedStyle(div);
        var color = style.backgroundColor;
        console.log(color);
        if(color === 'rgb(144, 238, 144)'){
            valid = true;
        }
    });
    return valid;
}

function check_nom_field(){
    console.log('caca');
    var regex = new RegExp("^[a-zA-Z-]{3,20}$");
    return regex.test(nom_field.value);
}

function check_nombre_field(){
    if(isNaN(nombre_field.value)){
        return false;
    } else {
        return nombre_field.value > 0 && nombre_field.value.includes(',') == false;
    }
}

function check_depot_field(){
    if(isNaN(depot_field.value)){
        return false;
    } else {
        return depot_field.value > 0 && depot_field.value.includes(',') == false;
    }
}

function check_fin_payer_field(){
    if(isNaN(fin_a_payer_field.value)){
        return false;
    } else {
        return fin_a_payer_field.value > 0;
    }
}

function check_total_field(){
    if(isNaN(total_field.value)){
        return false;
    } else {
        return total_field.value > 0;
    }
}

function check_all_fields(){
    return check_depot_field() && check_fin_payer_field() &&
    check_nom_field() && check_nombre_field() && check_total_field() &&
    check_type_paiement();
}