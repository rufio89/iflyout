$(document).ready(function() {
    var urls = new Array();
    var dest_list = "";
    var day_val = $('input[name=options]:checked', '#radio-form-days').val();
    var future_val = $('input[name=future-options]:checked', '#radio-form-future').val();
    var url_value = "/travel/flights/process_data/" + day_val + "/" + future_val;

    
   
    console.log(url_value);
    function show_alert(value, class_name) {
        $('.' + class_name + '').html(value);
        setTimeout(function() {
            $('.' + class_name + '').html('');
        }, 3000);
    };

    function get_flights(){
        console.log("HEre" + url_value);
        $.ajax({
          type: "GET",
          url: url_value,
          dataType:"json",
        }).done(function( data ) {
            console.log(data);
           show_data(data);
        });
    };
    
    var Div = class{
        constructor(url, price, airline, departure_date,arrival_airport, return_date){
            this.url = url;
            this.price = price;
            this.airline = airline;
            this.departure_date = departure_date;
            this.arrival_airport = arrival_airport;
            this.return_date = return_date;
        };
        
        create_div(){
            var destination = "<h1 class='destination-item'>" + this.arrival_airport + "</h2>";
            var heading = "<h2 class='price-item'>Price: " + this.price + "</h2>";
            var airline = "<h3 class='airline-item'>Airline: " + this.airline + "</h3>";
            var departure_info = "<p class='departure-info'>" + this.departure_date + "</hp>";
            var return_info = "<p>" + this.return_date + "</p>";
            var text = "<a target='_blank' href=" + this.url + "><div class='flight-item shadow'>" + destination + heading + airline + departure_info + return_info + "</div></a>";
            return text;
        };
    };
    
    function get_type(thing){
    if(thing===null)return "[object Null]"; // special case
    return Object.prototype.toString.call(thing);
}
    
    function show_data(data){
        var items = [];
        var div_list = [];
        for(var i=0;i<data.length;i++){
                 var obj = JSON.parse(data[i]);
                 items[i] = new Div(obj.url,obj.price, obj.airline, obj.departure_date,obj.arrival_airport, obj.return_date, obj.url);
        }
        var result_set = document.getElementById("results");
        for(var j=0;j<items.length;j++){
            div_list[j] = items[j].create_div();
            result_set.innerHTML = result_set.innerHTML + div_list[j];
        }
        
    };
    
    
    
    $('#radio-form-days input').on('change', function() {
        day_val = $('#radio-form-days .active input').val();
        url_value = "/travel/flights/process_data/" + day_val + "/" + future_val;
        console.log(day_val)
        show_alert("Make Sure to Choose Your Destinations and then Click Refresh!", 'refresh-alert-text-days');
    });
    
    $('#radio-form-future input').on('change', function() {
        future_val = $('#radio-form-future .active input').val();
        url_value = "/travel/flights/process_data/" + day_val + "/" + future_val + dest_list;
        show_alert("Make Sure to Choose Your Destinations and then Click Refresh!", 'refresh-alert-text-future');
//             console.log(dest_list);
//             console.log(url_value);
    });

    $('#refresh-btn').click(function(e){
        e.preventDefault();
        $('#results').text();
      var $this = $(this);
      $this.button('loading');
        setTimeout(function(){get_flights();$this.button('reset');}, 8000);
        
        
    });

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
        }
        else{
            urls.push($(this).attr("value"));
            $(this).addClass('active');
            dest_list += "/" + $(this).attr("value");
            url_value += "/" + $(this).attr("value");
        }
        
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
            });
         }
         else{
            
            $('.dests').each(function(index,value){
                $(this).addClass('active');
                urls.push($(this).attr("value"));
                dest_list += "/" + $(this).attr("value");
                url_value += "/" + $(this).attr("value");
            });
         }
    });


});
