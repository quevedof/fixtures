// JQuery Autocomplete widget
$( function() {
  var availableTags = [
    // Premier League
    "Arsenal",
    "Aston Villa",
    "Bournemouth",
    "Brentford",
    "Brighton & Hove Albion",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Ipswich Town",
    "Leicester City",
    "Liverpool",
    "Manchester City",
    "Manchester United",
    "Newcastle United",
    "Nottingham Forest",
    "Southampton",
    "Tottenham Hotspur",
    "West Ham United",
    "Wolverhampton Wanderers",
    // La Liga
    "Alaves",
    "Athletic Bilbao",
    "Atletico Madrid",
    "Barcelona",
    "Celta Vigo",
    "Espanyol",
    "Getafe",
    "Girona",
    "Las Palmas",
    "Leganes",
    "Mallorca",
    "Osasuna",
    "Rayo Vallecano",
    "Real Betis",
    "Real Madrid",
    "Real Sociedad",
    "Sevilla",
    "Valencia",
    "Valladolid",
    "Villareal",
    // Ligue 1
    "Angers",
    "Auxerre",
    "Brest",
    "Le Havre",
    "Lille",
    "Lyon",
    "Marseille",
    "Monaco",
    "Montpellier",
    "Nantes",
    "Nice",
    "PSG",
    "Paris Saint-Germain",
    "RC Lens",
    "Reims",
    "Rennes",
    "St Etienne",
    "Strasbourg",
    "Toulouse",
    // Bundesliga
    "Augsburg",
    "Leverkusen",
    "Bayern",
    "Vfl Bochum",
    "Dortmund",
    "Borussia Monchengladbach",
    "Eintracht Frankfurt",
    "SC Freiburg",
    "Heidenheim",
    "Hoffenheim",
    "Holstein Kiel",
    "Mainz",
    "RB Leipzig",
    "FC St. Pauli",
    "VfB Stuttgart",
    "Union Berlin",
    "Werder",
    "Wolfsburg",
    // Serie A
    "AC Milan",
    "Atalanta",
    "Bologna",
    "Cagliari",
    "Como",
    "Empoli",
    "Fiorentina",
    "Genoa",
    "Inter Milan",
    "Juventus",
    "Lazio",
    "Lecce",
    "Monza",
    "Napoli",
    "Parma",
    "Roma",
    "Torino",
    "Udinense",
    "Venezia",
    "Verona",
    // International
    "Argentina",
    "France",
    "Spain",
    "England",
    "Brazil",
    "Belgium",
    "Netherlands",
    "Portugal",
    "Colombia",
    "Italy",
    "Uruguay",
    "Croatia",
    "Germany",
    "Morocco",
    "Switzerland",
    "USA",
    "Mexico",
    "Japan",
    "Senegal",
    "Iran",
    "Denmark",
    "Austria",
    "Korea Republic",
    "Australia",
    "Ukraine",
    "Turkey",
    "Ecuador",
    "Poland",
    "Sweden",
    "Wales",
    "Hungary",
    "Serbia",
    "Russia",
    "Qatar",
    "Panama",
    "Egypt",
    "Venezuela",
    "Cote d'Ivore",
    "Nigeria",
    "Canada",
    "Tunisia",
    "Peru",
    "Chile",
    "Slovakia",
    "Romania",
    "Algeria",
    "Czech Republic",
    "Scotland",
    "Costa Rica",
    "Norway",
  ];
  $( "#clubName" ).autocomplete({
    source: availableTags,
    minLength: 2,
  });
} );

// allows the submission of Clear Results button when the input field is empty
$(document).ready(function() {
$('#clearResultsBtn').click(function() {
    // Remove required attribute from input field
    $('#clubForm input[name="club_name"]').prop('required', false);
});
});

// Removes a fixtures table
function removeTable(table_no) {
fetch('', {
    method: 'DELETE',
    headers: {
         'Content-Type':'application/json',
         'X-CSRFToken': getCookie('csrftoken'),
    },
    body:JSON.stringify({'table_no': table_no})
})
.then(res => {
    if (res.ok) {
        window.location.href = window.location.pathname;
    } else {
        console.error('Error deleting resource:', res.status);
    }
})
.catch(error => console.error('Error deleting resource:', error));
}

// returns csrf token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}