$(document).ready(function() {
    var urls = new Array();
    var dest_list = "";
    var day_val = $('input[name=options]:checked', '#radio-form-days').val();
    var future_val = $('input[name=future-options]:checked', '#radio-form-future').val();
    var url_value = "/travel/default/process_data/" + day_val + "/" + future_val;

    var btn_txt = "<a class='btn btn-primary' data-w2p_disable_with='default' data-w2p_method='POST' href=" + url_value + " id='refresh-btn'>Refresh</a>";
    console.log(url_value);
    console.log(btn_txt);
    function show_alert(value, class_name) {
        $('.' + class_name + '').html(value);
        setTimeout(function() {
            $('.' + class_name + '').html('');
        }, 3000);
    };

    function refresh_button(url_value){
        btn_txt = "<a class='btn btn-primary' data-w2p_disable_with='default' data-w2p_method='POST' href=" + url_value + " id='refresh-btn'>Refresh</a>";
        
        $(".refresh-area").html(btn_txt);
    }
    
    $('#radio-form-days input').on('change', function() {
        day_val = $('#radio-form-days .active input').val();
        url_value = "/travel/default/process_data/" + day_val + "/" + future_val;
        console.log(day_val)
        show_alert("Make Sure to Choose Your Destinations and then Click Refresh!", 'refresh-alert-text-days');
        refresh_button(url_value);
    });
    
    $('#radio-form-future input').on('change', function() {
        future_val = $('#radio-form-future .active input').val();
        url_value = "/travel/default/process_data/" + day_val + "/" + future_val + dest_list;
        show_alert("Make Sure to Choose Your Destinations and then Click Refresh!", 'refresh-alert-text-future');
        refresh_button(url_value);
//             console.log(dest_list);
//             console.log(url_value);
    });
    $(".refresh-area").html(btn_txt);



    var numDests = $('.dests').length
    //PIECE FOR ADDING DESTINATIONS
    $('.dests').click(function(e) { 
        e.preventDefault(); 
        if($(this).hasClass('active')){
            urls.pop($(this).attr("value"));
            $(this).removeClass('active');
            var item = "/" + $(this).attr("value");
            url_value = url_value.replace(item, '');
            dest_list = dest_list.replace(item,'');
            refresh_button(url_value);
        }
        else{
            urls.push($(this).attr("value"));
            $(this).addClass('active');
            dest_list += "/" + $(this).attr("value");
            url_value += "/" + $(this).attr("value");

            refresh_button(url_value);
        }
        
    });

    $('#refresh-btn').click(function(e){
        e.preventDefault();
        $("#primary-section").toggleClass('hidden');
    });

    $('#toggle-hide').click(function(e){
        e.preventDefault();
        $("#primary-section").toggleClass('hidden');
        if($("#toggle-hide").hasClass('glyphicon-menu-right')){
            $("#toggle-hide").removeClass('glyphicon-menu-right');
            $("#toggle-hide").addClass('glyphicon-menu-down');
        }
        else{
            $("#toggle-hide").removeClass('glyphicon-menu-down');
            $("#toggle-hide").addClass('glyphicon-menu-right');
        }
    });

    $('#highlight-all').click(function(e){
        e.preventDefault();
         if($('.flight-links').children().hasClass('active')){
            $('.dests').each(function(index,value){
                
                $(this).removeClass('active');
                urls.pop($(this).attr("value"));
                var item = "/" + $(this).attr("value");
                url_value = url_value.replace(item, '');
                dest_list = dest_list.replace(item, '');
                refresh_button(url_value);
            });
         }
         else{
            
            $('.dests').each(function(index,value){
                $(this).addClass('active');
                urls.push($(this).attr("value"));
                dest_list += "/" + $(this).attr("value");
                url_value += "/" + $(this).attr("value");
                refresh_button(url_value);
            });
         }
    });


});