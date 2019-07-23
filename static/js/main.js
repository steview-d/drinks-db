$(document).ready(function() {

    // Materialize Framework Iniitialisations

    // Materialize SideNav
    $('.sidenav').sidenav();
    // Materialize Select
    $('select').formSelect();
    // Materialize Tool Tip
    $('.tooltipped').tooltip();
    // Materialize Modal
    $('.modal').modal();
    // Materialize Character Counter
    $('input#imageUrl, textarea#textarea2').characterCounter();
    // MaterialBoxed
    $('.materialboxed').materialbox();
    // Material Tabs
    $('.tabs').tabs();


    // Back button
    $('.history-back').click(function() {
        window.history.back();
    });


    // Add / Remove Ingredients
    var num_fields = $('#ingredients-container .ingredient_field').length;
    var min_fields = 1;
    var max_fields = 10;
    var num_list = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten'];

    // Add
    $('#add_ingredient').click(function() {
        if (num_fields < max_fields) {
            $('#ingredients-container').append(
                "<div class='col s4 l2 measure_field'>" +
                "<div class='input-field'>" +
                "<input id='measure_" + (num_fields + 1) + "' name='measure_" + (num_fields + 1) + "' type='text' class='validate' required>" +
                "<label for='measure_" + (num_fields + 1) + "'>Measure " + num_list[(num_fields)] + "</label>" +
                "</div>" +
                "</div>" +
                "<div class='col s8 l4 ingredient_field'>" +
                "<div class='input-field'>" +
                "<input id='ingredient_" + (num_fields + 1) + "' name='ingredient_" + (num_fields + 1) + "' type='text' class='validate' required>" +
                "<label for='ingredient_" + (num_fields + 1) + "'>Ingredient " + num_list[(num_fields)] + "</label>" +
                "</div>" +
                "</div>"

            );
            num_fields += 1;
        }
    });

    // Remove
    $('#remove_ingredient').click(function() {
        if (num_fields > min_fields) {
            $('.measure_field').filter(':last').remove();
            $('.ingredient_field').filter(':last').remove();
            num_fields -= 1;
        }
    });


    // Fix to make sure validation text is displayed for select boxes when required
    $("select[required]").css({ display: "block", height: 0, padding: 0, width: 0 });


    // Web Storage - Remembering page states on a per user basis
    // Filter Tabs - Open / Close State
    if (localStorage.getItem('filterTabsState') == 1 && $('#filter-tabs').hasClass('hidden')) {
        $('#filter-tabs').removeClass('hidden');
    }

    $('#tabs-title-btn').click(function() {
        $('#filter-tabs').toggleClass('hidden');
        if ($('#filter-tabs').hasClass('hidden')) {
            localStorage.setItem('filterTabsState', '0');
        }
        else {
            localStorage.setItem('filterTabsState', '1');
        }
    });

    // Filter Tabs - Select tab from stored value
    $('.tabs').tabs('select', localStorage.getItem('currentTab'));
    // Store value of active tab
    $('.tabs > li').click(function() {
        localStorage.setItem('currentTab', $(this).children('a').attr('href').substring(1));
    });


    // Sort Options
    if (localStorage.getItem('sortOptionsState') == 1 && $('#sort-options').hasClass('hidden')) {
        $('#sort-options').removeClass('hidden');
    }

    $('#sort-options-btn').click(function() {
        $('#sort-options').toggleClass('hidden');
        if ($('#sort-options').hasClass('hidden')) {
            localStorage.setItem('sortOptionsState', '0');
        }
        else {
            localStorage.setItem('sortOptionsState', '1');
        }
    });

    // Set menu active highlight on side nan
    $('#mobile-nav li > .active').css('background-color', 'rgba(255,255,255,0.3');

    // Close displayed flash message
    $('.close-btn').click(function() {
        $('#flashed-message').remove();
    });
    
    
    
});
