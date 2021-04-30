$(document).ready(() => {
    $('.team-item .stack-top').hover(function() {
        $(this).stop(true, true).animate({'opacity': '0'}, 500);
    });
    $('.team-item .stack-top').mouseleave(function() {
        $(this).stop(true, true).animate({'opacity': '100%'}, 500);
    });
});