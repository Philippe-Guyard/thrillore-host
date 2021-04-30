$(document).ready(() => {
    $('.team-item .stack-top').hover(function() {
        $(this).stop(true, true).animate({'opacity': '0'}, 500);
    });
    $('.team-item .stack-top').mouseleave(function() {
        $(this).stop(true, true).animate({'opacity': '100%'}, 500);
    });

    $.getJSON('/api/leaderboard')
    .then(data => {
        const rowTemplateStr = $('#leaderboard #row-template').html();
        //Remove previous html
        $('#leaderboard tbody').html('');
        for(let row of data.points) {
            const newRow = rowTemplateStr
                        .replace('{{RANK}}', row.rank)
                        .replace('{{HANDLE}}', row.login)
                        .replace('{{POINTS}}', row.points);
            
            $('#leaderboard tbody').append(newRow);
        }
    });
});