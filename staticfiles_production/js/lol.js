// JQuery Autocomplete widget
$( function() {
    // LoL Power Ranking list
    var availableTags = [
        'Gen.G',
        'Bilibili Gaming Dreamsmart',
        'Hanwha Life Esports',
        'Top Esports',
        'G2 Esports',
        'T1',
        'Dplus Kia',
        'Beijing JDG Intel Esports',
        'kT Rolster',
        'Suzhou LNG Ninebot Esports',
        'WeiboGaming TapTap',
        'Shenzhen Ninjas In Pyjamas',
        'Fnatic',
        'Team Liquid Honda',
        "Anyone's Legend",
        'FlyQuest',
        'Team BDS',
        'FunPlus Phoenix',
        'PSG Talon',
        "Xi'an Team WE",
        'Kwangdong Freecs',
        'Cloud 9',
        'LGD Gaming',
        'Oh My God',
        'BNK FearX',
        'MAD Lions KOI',
        'Thunder Talk Gaming',
        'Invictus Gaming',
        'Shanghai Edward Gaming Hycan',
        'Nongshim Redforce',
        'Karmine Corp',
        'Rare Atom',
        'SK Gaming',
        '100 Thieves',
        'Team Vitality',
        'Royal Never Give Up',
        'GAM Esports',
        'NRG Kia',
        'Team Heretics',
        'Giantx',
        'DRX',
        'Shopify Rebellion',
        'Ultra Prime',
        'Dignitas',
        'Rogue',
        'OKSavingsBank Brion',
        'CTBC Flying Oyster',
        'Frank Esports',
        'Vikings Esports',
        'Movistar R7',
        'Immortals Progressive',
        'paiN Gaming',
        'Fukuoka SoftBank Hawks Gaming',
        'Deep Cross Gaming',
        'Loud',
        'Estral Esports',
        'Team Secret',
        'Team Whales',
        'Red Kalunga',
        'Ground Zero',
        'Sengoku Gaming',
        'Vivo Keyd Stars',
        'J Team',
        'DetonatioN FocusMe',
        'Isurus',
        'Team Bliss',
        'Cerberus Esports',
        'Furia',
        'Team Flash',
        'Infinity',
        'Fluxo',
        'Hell Pigs',
        'MGN Blue Esports',
        'Intz',
        'West Point Esports',
        'Los',
        'KaBum!',
        'Leviatan Esports',
        'Six Karma',
        'Liberty',
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
        $('#clubForm input[name="clubName"]').prop('required', false);
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