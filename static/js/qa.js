$(function () {

    function getCookie(name) {
        if (document.cookie && document.cookie.length) {
            var cookies = document.cookie
                .split(';')
                .filter(function (cookie) {
                    return cookie.indexOf(name + "=") !== -1;
                })[0];
            try {
                return decodeURIComponent(cookies.trim().substring(name.length + 1));
            } catch (e) {
                if (e instanceof TypeError) {
                    console.info("No cookie with key \"" + name + "\". Wrong name?");
                    return null;
                }
                throw e;
            }
        }
        return null;
    }

    function csrfSafeMethod(method) {
        // These HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');
    // 设置Ajax请求头
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#publish").click(function () {
        // function to operate the Publish button in the question form, marking
        // the question status as published.
        $("input[name='status']").val("O");
        $("#question-form").submit();
    });

    $("#draft").click(function () {
        // Function to operate the Draft button in the question form, marking
        // the question status as draft.
        $("input[name='status']").val("D");
        $("#question-form").submit();
    });

    $(".question-vote").click(function () {
        // 给问题投票
        var span = $(this);
        var question_id = $(this).closest(".question").attr("question-id");
        var question = $(this).closest(".question");
        vote = null;
        if ($(this).hasClass("up-vote")) {
            vote = "U";
        } else {
            vote = "D";
        }
        $.ajax({
            url: '/qa/question/vote/',
            data: {
                'question': question_id,
                'value': vote
            },
            type: 'post',
            cache: false,
            success: function (data) {
                // $('.vote', span).removeClass('voted');
                // if (vote === "U") {
                //     $(span).addClass('voted');
                // }
                $("#questionUpVote").removeClass('voted');
                $("#questionDownVote").removeClass('voted');
                if(data.status == 1)
                    $("#questionUpVote").addClass('voted');
                if(data.status == 0)
                    $("#questionDownVote").addClass('voted');
                $("#questionVotes").text(data.votes);
            }
        });
    });

    $(".answer-vote").click(function () {
        // 给回答投票
        const answer_id = $(this).closest(".answer").attr("answer-id");
        const answer = $('div[answer-id=' + answer_id + '] .votes');
        if ($(this).hasClass("up-vote")) {
            vote = "U";
        } else {
            vote = "D";
        }
        $.ajax({
            url: '/qa/answer/vote/',
            data: {
                'answer': answer_id,
                'value': vote
            },
            type: 'post',
            cache: false,
            success: function (data) {
                if (vote === "U") {
                    $('div[answer-id=' + answer_id + '] .down-vote').removeClass('voted');
                    $('div[answer-id=' + answer_id + '] .up-vote').addClass('voted');
                } else {
                    $('div[answer-id=' + answer_id + '] .up-vote').removeClass('voted');
                    $('div[answer-id=' + answer_id + '] .down-vote').addClass('voted');
                }
                answer.text(data.votes);
            }
        });
    });

    $(".acceptAnswer").click(function () {
        // 接受回答
        const answer_id = $(this).closest(".answer").attr("answer-id");
        const answer = $('div[answer-id=' + answer_id + '] .acceptAnswer');
        $.ajax({
            url: '/qa/accept-answer/',
            data: {
                'answer': answer_id
            },
            type: 'post',
            cache: false,
            success: function (data) {
                $(".accepted").removeClass("accepted");
                $(".accepted").prop("title", "点击接受回答");
                answer.addClass("accepted");
                answer.prop("title", "该回答已被采纳");
            }
        });
    });
});
