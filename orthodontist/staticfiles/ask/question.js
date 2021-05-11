import { likeQuestion } from '../main.js'

document.addEventListener('DOMContentLoaded', ()=>{
    likeQuestion()
    editQuestion()
})


function editQuestion() {
    const editButton = document.getElementById('edit-button')
    editButton.addEventListener('click', (event)=>{
        const url = editButton.dataset.url
        const editField = document.getElementById('edit-field')
        const title = editField.getElementsByClassName('card-title')[0].innerText
        const text = editField.getElementsByClassName('card-text')[0].innerText
        editField.innerHTML = '<form method="post">\n' +
                              '    <input id="title-input" type="text" name="title" class="form-control mb-2" maxlength="255" required id="id_title" value="' + title + '">\n' +
                              '    <textarea id="text-input" name="text" cols="40" rows="5" class="form-control mb-2" maxlength="1000">' + text + '</textarea>\n' +
                              '    <input class="btn btn-primary" type="submit" id="update-button" value="Изменить">\n' +
                              '</form>'
        const updateButton = document.getElementById('update-button')
        const titleInput = document.getElementById("title-input")
        const textInput = document.getElementById("text-input")
        var formData = new FormData()
        titleInput.oninput = (e)=>{formData.set('title', e.target.value)}
        textInput.oninput = (e)=>{formData.set('text', e.target.value)}
        updateButton.addEventListener('click', (event)=>{
            fetch(url,{
                method: 'PATCH',
                body: formData,
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(response => response.json()).then(json => {
                editField.innerHTML = '<h5 class="card-title">' + json.title + '</h5>\n' +
                                      '<p class="card-text support-line-breaks">' + json.text + '</p>'
            }).catch(err => console.error(err))
            event.preventDefault()
        })
    })
}


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