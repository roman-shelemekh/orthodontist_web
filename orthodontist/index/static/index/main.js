$(document).ready(function() {
    $('.like-btn').click(function (){
        $.ajax({
            url: $(this).attr('data-url'),
            success: (response) => {
                if(response.auth){
                    window.location.href = response.auth
                } else {

                    $(this).children("span").empty().append(response.like_count)
                    if(response.add){
                        $(this).addClass('active')
                    } else {
                        $(this).removeClass('active')
                    }
                }
            }
        })
    })

});