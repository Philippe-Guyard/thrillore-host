$(document).ready(() => {
  //Team animations
  $('.team-item .stack-top').hover(function () {
    $(this).stop(true, true).animate({ 'opacity': '0' }, 500);
  });
  $('.team-item .stack-top').mouseleave(function () {
    $(this).stop(true, true).animate({ 'opacity': '100%' }, 500);
  });

  //Filling the leaderboard with real data
  const fillTable = (tBody, data) => {
    const rowTemplateStr = $('#leaderboard #row-template').html();
    tBody.html('');

    for (let row of data) {
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

  //Cool scroll top animation
  $(document).on('click', 'a[href^="#"]', function (event) {
    event.preventDefault();

    $('html, body').animate({
      scrollTop: $($.attr(this, 'href')).offset().top
    }, 500);
  });

  // Sticky Nav
  $(window).on('scroll', function () {
    if ($(window).scrollTop() > 200) {
      $('.scrolling-navbar').addClass('top-nav-collapse');
    } else {
      $('.scrolling-navbar').removeClass('top-nav-collapse');
    }
  });

  // One Page navigation 
  $('.navbar-nav').onePageNav({
    currentClass: 'active'
  });
});