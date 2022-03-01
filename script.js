$(document).ready(function(){
  
  $(".lab").hide();

  $(".satoshi-btn").click(function(){
    if ($( ".tesla" ).is( ":hidden") && $( ".pausch" ).is( ":hidden") && $( ".mc-carthy" ).is( ":hidden" ))
    {
      $(".satoshi").toggle(300);
    }
    
  });
  
  $(".tesla-btn").click(function(){

    if ($( ".satoshi" ).is( ":hidden") && $( ".pausch" ).is( ":hidden") && $( ".mc-carthy" ).is( ":hidden" ))
    {
      $(".tesla").toggle(300);
    }
    

  });

  $(".mc-carthy-btn").click(function(){

    if ($( ".satoshi" ).is( ":hidden") && $( ".pausch" ).is( ":hidden") && $( ".tesla" ).is( ":hidden" ))
    {
      $(".mc-carthy").toggle(300);
    }

  });

  $(".pausch-btn").click(function(){
    if ($( ".satoshi" ).is( ":hidden") && $( ".mc-carthy" ).is( ":hidden") && $( ".tesla" ).is( ":hidden" ))
    {
      $(".pausch").toggle(300);
    }
  });

});

var video = document.querySelector("#video");

if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
    })
    .catch(function (error) {
      console.log("Something went wrong!"+str(error));
    });
}
