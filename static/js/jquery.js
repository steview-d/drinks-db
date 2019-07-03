$(document).ready(function() {
    // Materialize SideNav
    $('.sidenav').sidenav();
    // Materialize Select
    $('select').formSelect();


    // Back button
    $('.history-back').click(function() {
        window.history.back();
    });

    // Add Ingredients
    var num_fields = 4;
    var max_fields = 10;
    $('#add_ingredient').click(function() {
        
        if (num_fields < max_fields) {
        
        var num_list = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
        $('#ingredients-container').append(
            "<div class='col s4'>"+
                "<div class='input-field'>"+
                    "<input id='ingredient_" + (num_fields +1) +"' name='ingredient_" + (num_fields +1) +"' type='text' class='validate'>"+
                    "<label for='ingredient_" + (num_fields +1) +"'>Ingredient " + num_list[(num_fields)] +"</label>"+
                "</div>"+
                "</div>"+
                "<div class='col s2'>"+
                    "<div class='input-field'>"+
                        "<input id='measure_" + (num_fields +1) +"' name='measure_" + (num_fields +1) +"' type='text' class='validate'>"+
                        "<label for='measure_" + (num_fields +1) +"'>Measure " + num_list[(num_fields)] +"</label>"+
                    "</div>"+
               "</div>"+
            "</div>"
        );
        num_fields += 1;
        }
    });

});

