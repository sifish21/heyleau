// GLOBAL VARIABLES
var nom_field = document.getElementById('nom_field');
var nombre_field = document.getElementById('nombre_field');
var depot_field = document.getElementById('depot-field');
var fin_a_payer_field = document.getElementById('fin_payer_field');
var total_field = document.getElementById('total_field');
var type_field = document.getElementById('paiement-choisi');
var form = document.getElementById('formulaire-nouveau');
var bouton_autre = document.getElementById('submit-button-autre');
var bouton_enregistrer = document.getElementById('submit-button-enregistrer');
var visa_div = document.getElementById('visa');
var mastercard_div = document.getElementById('mastercard');
var interac_div = document.getElementById('interac');
var dollar_div = document.getElementById('dollar-sign');
var taxes_div = document.getElementById('taxes-div');

// EVENT LISTENERS
document.querySelectorAll('.type-paiement').forEach(box => {
    box.addEventListener('click', function() {
      document.querySelectorAll('.type-paiement').forEach(otherBox => {
        otherBox.style.backgroundColor = 'white';
      });
      this.style.backgroundColor = 'lightgreen';
      verifie_form();

    });
});

dollar_div.addEventListener('click', function() {
    change_type_field("cash")
});

visa_div.addEventListener('click', function() {
    change_type_field("visa")
});

interac_div.addEventListener('click', function() {
    change_type_field("interac")
});

mastercard_div.addEventListener('click', function() {
    change_type_field("mastercard")
});


bouton_autre.addEventListener('click', function(){
    document.getElementById('checkbox').checked = true;
});

bouton_enregistrer.addEventListener('click', function(){
    document.getElementById('checkbox').checked = false;
});

form.addEventListener('input', function() {
    verifie_form();
});

form.addEventListener('change', function() {
    verifie_form();
});

taxes_div.addEventListener('click', function() {
    var par = document.getElementById('taxes-par');
    if(window.getComputedStyle(taxes_div).backgroundColor === 'rgb(255, 255, 255)'){
        taxes_div.style.backgroundColor = 'rgba(255, 0, 0, 0.5)'
        document.getElementById('checkbox-taxes').checked = true;
        par.textContent = "Pas de Taxes";
    } else {
        taxes_div.style.backgroundColor = 'white'
        document.getElementById('checkbox-taxes').checked = false;
        par.textContent = "Taxes";
    }
});


// FUNCTIONS
function verifie_form(){
    if(check_all_fields()){
        bouton_autre.style.backgroundColor = 'pink';
        bouton_enregistrer.style.backgroundColor = 'pink';
        bouton_autre.disabled = false;
        bouton_enregistrer.disabled = false;
    } else {
        bouton_autre.style.backgroundColor = 'rgba(211, 211, 211, 0.4)';
        bouton_enregistrer.style.backgroundColor = 'rgba(211, 211, 211, 0.4)';
        bouton_autre.disabled = true;
        bouton_enregistrer.disabled = true;
    }
}

function change_type_field(string){
    console.log(string);
    document.getElementById('paiement-choisi').value = string;
}



function check_type_paiement(){
    var divs = document.querySelectorAll('.type-paiement');
    var valid = false;
    Array.from(divs).forEach(function(div){
        var style = window.getComputedStyle(div);
        var color = style.backgroundColor;
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