var content_list = document.getElementById('recherche-list');
var animals_list = content_list.querySelectorAll('div > div');    
var nb_animals = animals_list.length;
for(let i = 1; i <= nb_animals; i++){
    (function(id) {
        document.getElementById(id).addEventListener('mousedown', function() {
            document.getElementById(id).style.backgroundColor = 'rgb(106, 11, 30)';
        });
        document.getElementById(id).addEventListener('mouseup', function(){
            document.getElementById(id).style.backgroundColor = 'rgba(220, 20, 60, 0.2)';
        });
        document.getElementById(id).addEventListener('click', function() {
            animal_id = 'id_' + i;
            id_number = document.getElementById(animal_id).innerHTML;
            window.location.href = '/animal/' + id_number;
        });
    })("animal_" + i);
}
