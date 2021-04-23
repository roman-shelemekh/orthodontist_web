// like question

likeQuestion()

function likeQuestion() {
    const button = document.getElementsByClassName('like-btn')
    Array.from(button).forEach(element => {
        element.addEventListener('click', () => {
            const url = element.dataset.url
            const request = new XMLHttpRequest()
            request.responseType = 'json'
            request.open('GET', url)
            request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
            request.send()
            request.onload = function () {
                if (this.status >= 200 && this.status < 400) {
                    if (this.response.auth) {
                        window.location = this.response.auth
                    } else {
                        element.querySelector('.like_count').textContent = this.response.like_count
                        if (this.response.add) {
                            element.classList.add('active')
                        } else {
                            element.classList.remove('active')
                        }
                    }
                } else {
                    console.log('Did not get anything')
                }
            }
            request.onerror = function () {
                console.log('Connection error');
            }
        })
    })
}
//sorting field

const sortingField = document.getElementById('id_order_by')
const questionList = document.getElementById('question-list')
sortingField.addEventListener('change', (event) => {
    const url = sortingField.dataset.url + '?order_by=' + event.target.value
    fetch(url).then(response => response.json()).then(json => {
        questionList.innerHTML = ''
        for(const question of json.results){
            date = new Date(question.date)
            const el = document.createElement('div')
            el.classList.add('row', 'justify-content-center', 'my-3')
            el.innerHTML = '<div class="col-sm col-md-10">\n' +
                '                <div class="card">\n' +
                '                    <div class="card-body">\n' +
                '                        <div class="clearfix">\n' +
                '                            <div class="user-pic-question float-start mb-3">\n' +
                '                                <img src="' + question.author_image_url + '" alt="' + question.author_first_name + '">\n' +
                '                            </div>\n' +
                '                            <div class="float-start mt-3 ms-3">\n' +
                '                                <h6 class="card-subtitle mb-2 text-muted">Автор: <a style="color: gray; text-decoration: none;" href="' + question.author_url + '">' + question.author_first_name + ' ' + question.author_last_name + '</a></h6>\n' +
                '                                <h6 class="card-subtitle mb-2 text-muted">Дата: ' + formatDate(date) + '</h6>\n' +
                '                                <h6 class="card-subtitle mb-2 text-muted">Ответов: ' + question.answers_count + '</h6>\n' +
                '                            </div>\n' +
                '                        </div>\n' +
                '                        <h5 class="card-title">' + question.title + '</h5>\n' +
                '                        <p class="card-text">' + question.text + '</p>\n' +
                '                        <a href="' + question.question_url + '" class="btn btn-primary">Перейти к вопросу</a>\n' +
                '                        <button class="like-btn btn btn-sm btn-primary float-end" type="submit" data-url="' + question.like_url + '" data-qid="' + question.id + '"><i class="far fa-thumbs-up"></i> <span class="like_count">' + question.like_count + '</span></button>\n' +
                '                    </div>\n' +
                '                </div>\n' +
                '            </div>'
            const likeButton = el.querySelector('.like-btn')
            if(question.like){
                likeButton.classList.add('active')
            }
            questionList.appendChild(el)
        }
        likeQuestion()
    })
})


function formatDate(date) {
  const monthNames = [
    "января", "февраля", "марта",
    "апреля", "мая", "июня", "июля",
    "августа", "сентября", "октября",
    "ноября", "декабря"
  ]

  const day = date.getDate()
  const monthIndex = date.getMonth()
  const year = date.getFullYear()

  return day + ' ' + monthNames[monthIndex] + ' ' + year
}