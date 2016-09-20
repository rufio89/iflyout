jQuery(function(){
    var MAIN = new Ractive({
      el: '#target',
      template: '#template',
      data: {
          "color": "Red"
        },
      delimiters : ['{%','%}']
    });
});
