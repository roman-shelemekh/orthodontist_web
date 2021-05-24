ymaps.ready(init);

function init() {

    var myMap = new ymaps.Map("map", {
            center: [45.042483, 38.996926],
            zoom: 11
        }, {
            searchControlProvider: 'yandex#search'
        })

    fetch('/appointment/get_clinics_for_map/', {
        method:'GET',
        headers: {'X-Requested-With': 'XMLHttpRequest'}
    }).then(response => response.json()).then(json => {
        for(let clinic in json){
            console.log(json[clinic])
            myMap.geoObjects
                .add(new ymaps.Placemark([parseFloat(json[clinic].latitude), parseFloat(json[clinic].longitude)], {
                    balloonContent: '<b>' + json[clinic].name + '</b></br>Адрес: ' + json[clinic].address + '</br>Телефон: ' + json[clinic].phone_number1 + ', ' + json[clinic].phone_number2,
                    iconCaption: json[clinic].name
                }, {
                    preset: 'islands#blueMedicalIcon'
                }))
        }
    })




    myMap.geoObjects
        .add(new ymaps.Placemark([45.041687, 38.954787], {
            balloonContent: '<b>ДЕНТиК на Тургенева</b></br>Адрес: ул. Тургенева, 23</br>Телефон:',
            iconCaption: 'ДЕНТиК на Тургенева'
        }, {
            preset: 'islands#blueMedicalIcon'
        }))

}


