$(document).ready(function(){
    
    var sum = 0;
    var payVal = document.querySelectorAll(".price1");
    for (var i = 0; i < payVal.length; i++){
        var count = parseInt(payVal[i].innerHTML);
        sum += count;
        console.log(sum);
        console.log(count);
    }
    // var payTotal1 = $("#totalCurrent").html(sum);
    document.getElementById("totalCurrent").innerHTML = "$" + sum.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
})

$(document).ready(function(){
    var sum2 = 0;
    var payVal2 = document.querySelectorAll(".price2");
    for (var i = 0; i < payVal2.length; i++){
        var count2 = parseInt(payVal2[i].innerHTML);
        sum2 += count2;
        console.log(sum2);
    }
    // var payTotal2 = $("#totalPast").html(sum2);
    document.getElementById("totalPast").innerHTML = "$" + sum2.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
})
