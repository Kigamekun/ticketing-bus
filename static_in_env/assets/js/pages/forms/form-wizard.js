$(function () {
    //Horizontal form basic
    // $('#wizard_horizontal_icon').steps({
    //     headerTag: 'h2',
    //     bodyTag: 'section',
    //     transitionEffect: 'slideLeft',
    //     onInit: function (event, currentIndex) {
    //         setButtonWavesEffect(event);
    //     },
    //     onStepChanged: function (event, currentIndex, priorIndex) {
    //         setButtonWavesEffect(event);
    //     }
    // });
    
    // //Horizontal form basic
    // $('#wizard_horizontal').steps({
    //     headerTag: 'h2',
    //     bodyTag: 'section',
    //     transitionEffect: 'slideLeft',
    //     onInit: function (event, currentIndex) {
    //         setButtonWavesEffect(event);
    //     },
    //     onStepChanged: function (event, currentIndex, priorIndex) {
    //         setButtonWavesEffect(event);
    //     }
    // });

    // //Vertical form basic
    // $('#wizard_vertical').steps({
    //     headerTag: 'h2',
    //     bodyTag: 'section',
    //     transitionEffect: 'slideLeft',
    //     stepsOrientation: 'vertical',
    //     onInit: function (event, currentIndex) {
    //         setButtonWavesEffect(event);
    //     },
    //     onStepChanged: function (event, currentIndex, priorIndex) {
    //         setButtonWavesEffect(event);
    //     }
    // });

    //Advanced form with validation
    var form = $('#wizard_with_validation').show();
        form.steps({
        headerTag: 'h3',
        bodyTag: 'fieldset',
        transitionEffect: 'slideLeft',        
        onStepChanging: function (event, currentIndex, newIndex) {
            if (currentIndex > newIndex) { return true; }

            if (currentIndex < newIndex) {
                if(currentIndex == 0){
                    
                    var track1 = $('select[name="track1 *"]').val();
                    var track2 = $('select[name="track2 *"]').val();
                    var tanggal = $('input[name="tanggal"]').val();

                    $.ajax({
                        url: 'cari/'+track1+"/"+track2+"/"+tanggal,
                        type: 'get',
                        success: function(data) {
                            $('#busList').html(data);
                        },
                        failure: function(data) { 
                            alert('Got an error dude');
                        }
                    }); 
                    
                }
                form.find('.body:eq(' + newIndex + ') label.error').remove();
                form.find('.body:eq(' + newIndex + ') .error').removeClass('error');
            }

            form.validate().settings.ignore = ':disabled,:hidden';
            return form.valid();
        },
        onStepChanged: function (event, currentIndex, priorIndex) {
            setButtonWavesEffect(event);
        },
        onFinishing: function (event, currentIndex) {
            form.validate().settings.ignore = ':disabled';
            return form.valid();
        },
        onFinished: function (event, currentIndex) {
            var selected = [];
            var chck = document.getElementById("busList");
            var selck = chck.getElementsByTagName("input");
           
            for(var i=0;i<selck.length;i++){
                if(selck[i].checked){
                    selected.push(selck[i].value);
                }
            }
           
            // console.log(selected);
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = cookies[i].trim();
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            var csrftoken = getCookie('csrftoken');
            if ( $('#acceptTerms').is(':checked') ) {
                $.ajax({
                    type: "POST",
                    url: "beli_tiket/",
                    data: {    
                    csrfmiddlewaretoken:jQuery("[name=csrfmiddlewaretoken]").val(),
                    'selected[]':selected,
                    'nama': $('input[name=nama]').val(),
                    'track1':$('select[name="track1 *"]').val(),
                    'track2':$('select[name="track2 *"]').val(),
                    'tanggal':$('input[name="tanggal"]').val(),
                    },
                    success: function () {
                      console.log("berhasil");
                      window.location.href = '/pesan/';
                    }
                  });
                
             }
             else {
                
                    event.preventDefault();

                    swal({
                        title: 'Make sure your booking dude',
                        text: "you don't accept the terms !",
                        icon: 'warning',
                        buttons: "Emm ok sorry ",
                    });
              
             }


           
        }
    });

    form.validate({
        highlight: function (input) {
            $(input).parents('.form-line').addClass('error');
        },
        unhighlight: function (input) {
            $(input).parents('.form-line').removeClass('error');
        },
        errorPlacement: function (error, element) {
            $(element).parents('.form-group').append(error);
        },
        rules: {
            'confirm': {
                equalTo: '#password'
            }
        }
    });
});

function setButtonWavesEffect(event) {
    $(event.currentTarget).find('[role="menu"] li a').removeClass('');
    $(event.currentTarget).find('[role="menu"] li:not(.disabled) a').addClass('');
}