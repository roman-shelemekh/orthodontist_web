import { likeQuestion } from './main.js'

document.addEventListener('DOMContentLoaded', ()=>{
    const url = document.getElementById('question-list').dataset.url
    getQuestionList(url)
    SortingListener()
})

function getQuestionList(url) {
    const questionList = document.getElementById('question-list')
    fetch(url, {
        method:'GET',
        headers: {'X-Requested-With': 'XMLHttpRequest'}
    }).then(response => response.json()).then(json => {

        // Questions List loading
        questionList.innerHTML = ''
        for(const question of json.results){
            const date = new Date(question.date)
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
                '                        <p class="card-text support-line-breaks">' + question.text + '</p>\n' +
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

        // Pagination Links loading
        const pagination = document.getElementById('pagination')
        pagination.innerHTML = ''
        if (json.links.first){
            pagination.innerHTML += '<li class="page-item"><a class="page-link text-primary" href="' + json.links.first + '">Первая</a></li>'
        } else {
            pagination.innerHTML += '<li class="page-item disabled"><a class="page-link text-primary" href="#" disabled>Первая</a></li>'
        }
        if (json.links.second_previous){
            pagination.innerHTML += '<li class="page-item"><a class="page-link text-primary" href="' + json.links.second_previous + '">' + (json.current - 2) + '</a></li>'
        }
        if (json.links.previous){
            pagination.innerHTML += '<li class="page-item"><a class="page-link text-primary" href="' + json.links.previous + '">' + (json.current - 1) + '</a></li>'
        }
        pagination.innerHTML += '<li class="page-item active"><span class="page-link bg-primary">' + json.current + '</span></li>'
        if (json.links.next){
            pagination.innerHTML += '<li class="page-item"><a class="page-link text-primary" href="' + json.links.next + '">' + (json.current + 1) + '</a></li>'
        }
        if (json.links.second_next){
            pagination.innerHTML += '<li class="page-item"><a class="page-link text-primary" href="' + json.links.second_next + '">' + (json.current + 2) + '</a></li>'
        }
        if (json.links.last){
            pagination.innerHTML += '<li class="page-item"><a class="page-link text-primary" href="' + json.links.last + '">Последняя</a></li>'
        } else {
            pagination.innerHTML += '<li class="page-item disabled"><a class="page-link text-primary" href="#" disabled>Последняя</a></li>'
        }

        likeQuestion()
        PaginationListener()
    })
}

function PaginationListener() {
    const pagesLinks = document.getElementsByClassName('page-link')
    Array.from(pagesLinks).forEach(element => {
        element.addEventListener('click', (event) => {
            const url = element.getAttribute('href')
            if (url) {
                getQuestionList(url)
                window.scrollTo({top: 0, behavior: 'smooth'})
            }
            event.preventDefault()
        }, false)
    })
}

function SortingListener(){
    const questionList = document.getElementById('question-list')
    const sortingField = document.getElementById('id_order_by')
    sortingField.addEventListener('change', (event)=>{
        const url = questionList.dataset.url + '?order_by=' + event.target.value
        getQuestionList(url)
    })
}

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