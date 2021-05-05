$(document).ready(() => {
    $('.team-item .stack-top').hover(function() {
        $(this).stop(true, true).animate({'opacity': '0'}, 500);
    });
    $('.team-item .stack-top').mouseleave(function() {
        $(this).stop(true, true).animate({'opacity': '100%'}, 500);
    });

    const fillTable = (tBody, data) => {
        const rowTemplateStr = $('#leaderboard #row-template').html();
        tBody.html('');

        for(let row of data) {
            const newRow = rowTemplateStr
                        .replace('{{RANK}}', row.rank)
                        .replace('{{HANDLE}}', row.handle)
                        .replace('{{POINTS}}', row.points);
            
            tBody.append(newRow);
        }
    }

    $.getJSON('/api/leaderboard')
    .then(data => {
        fillTable($('#leaderboard #daily tbody'), data.dailyPoints);
        fillTable($('#leaderboard #weekly tbody'), data.weeklyPoints);
    });
});