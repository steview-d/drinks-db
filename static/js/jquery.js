$(document).ready(function() {
    // Materialize SideNav
    $('.sidenav').sidenav();
    // Materialize Select
    $('select').formSelect();


    // Back button
    $('.history-back').click(function() {
        window.history.back();
    });

    //

});
