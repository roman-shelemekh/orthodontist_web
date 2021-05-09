document.addEventListener('DOMContentLoaded', ()=>{
    const selectClinic = document.getElementById('id_clinic')
    selectClinic.innerHTML = '<option disabled selected value> -- выберите клинику -- </option>'
    const selectDates = document.getElementById('id_date')
    selectDates.innerHTML = '<option disabled selected value> -- дата -- </option>'
    const selectTimetable = document.getElementById('id_time')
    selectTimetable.innerHTML = '<option disabled selected value> -- время -- </option>'

    const url = selectClinic.parentElement.dataset.url
    fetch(url, {
        method:'GET',
        headers: {'X-Requested-With': 'XMLHttpRequest'}
    }).then(response => response.json()).then(json => {
        selectClinic.innerHTML = '<option disabled selected value> -- выберите клинику -- </option>'
        for(let i of json.clinics){
            const opt = document.createElement('option')
            opt.value = i
            opt.innerHTML = i
            selectClinic.appendChild(opt)
        }
    })

    selectClinic.addEventListener('change', (event)=>{
        const dateURL = selectDates.parentElement.dataset.url + '?clinic=' + event.target.value
        fetch(dateURL, {
            method:'GET',
            headers: {'X-Requested-With': 'XMLHttpRequest'}
        }).then(response => response.json()).then(json => {
            selectDates.innerHTML = '<option disabled selected value> -- дата -- </option>'
            selectTimetable.innerHTML = '<option disabled selected value> -- время -- </option>'
            for(let i of json.dates){
                let date = new Date(i)
                const opt = document.createElement('option')
                opt.value = i
                opt.innerHTML = date.toLocaleDateString('ru-RU')
                selectDates.appendChild(opt)
            }
        })
    })

    selectDates.addEventListener('change', (event)=>{
        const clinic = selectClinic.value
        const timeURL = selectTimetable.parentElement.dataset.url + '?clinic=' + clinic + '&date=' + event.target.value
        fetch(timeURL, {
            method:'GET',
            headers: {'X-Requested-With': 'XMLHttpRequest'}
        }).then(response => response.json()).then(json => {
            selectTimetable.innerHTML = '<option disabled selected value> -- время -- </option>'
            for(let i of json.timetable){
                const opt = document.createElement('option')
                opt.value = i
                opt.innerHTML = i.split(':')[0] + ':' + i.split(':')[1]
                selectTimetable.appendChild(opt)
            }
        })
    })
})