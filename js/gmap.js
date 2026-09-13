var mapLocation = new google.maps.LatLng(41.4889, 24.8497); // Rudozem, Bulgaria
var marker;
var map;
function initialize() {
    var mapOptions = {
        zoom: 14, // Change zoom here
        center: mapLocation,
        scrollwheel: false,
        styles: [
            {"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#333333"}]},
            {"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2f2f2"}]},
            {"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},
            {"featureType":"poi","elementType":"labels.text","stylers":[{"visibility":"off"}]},
            {"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45}]},
            {"featureType":"road.highway","elementType":"geometry","stylers":[{"visibility":"simplified"},{"color":"#f6954d"}]},
            {"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#e3e2e2"}]},
            {"featureType":"transit","elementType":"all","stylers":[{"visibility":"off"}]},
            {"featureType":"water","elementType":"all","stylers":[{"color":"#a4c4c8"},{"visibility":"on"}]}]
    };
    
    map = new google.maps.Map(document.getElementById('map'),
    mapOptions);
    
     
    //change address details here
    var contentString = '<div class="map-info">' 
    + '<div class="map-title">' 
    + '<div class="brand" href="#"><img alt="" src="images/Logo.png"><div class="brand-info"><div class="brand-name">Kehayov Solar</div><div class="brand-text">Фотоволтаични системи</div></div></div></div>' 
    + '<p class="map-address">'
    + '<div class="map-address-row">'
    + '  <i class="fa fa-map-marker"></i>'
    + '  <span class="text"><strong>гр. Рудозем</strong><br>'
    + '  България</span>'
    + '</div>'
    + '<div class="map-address-row">'
    + '   <i class="fa fa-phone"></i>'
    + '   <span class="text">+359 87 848 9013</span>'
    + '</div>'
    + '<div class="map-address-row">'
    + '   <span class="map-email">'
    + '      <i class="fa fa-envelope"></i>'
    + '      <span class="text">hiki7787@gmail.com</span>'
    + '   </span>'
    + '</div>' 
    + '<p class="gmap-open"><a href="https://www.google.com/maps/search/?api=1&query=Rudozem+Bulgaria" target="_blank">Отвори в Google Maps</a></p></div>';
    
    
    var infowindow = new google.maps.InfoWindow({
        content: contentString,
    });
    

    // Uncomment down to show Marker


    marker = new google.maps.Marker({
        map: map,
        draggable: false,
        title: 'Kehayov Solar',
        animation: google.maps.Animation.DROP,
        position: mapLocation
    });

    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map, marker);
    });




}

if ($('#map').length) {
    google.maps.event.addDomListener(window, 'load', initialize);
}

