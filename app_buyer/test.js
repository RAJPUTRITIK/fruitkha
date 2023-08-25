// what is NaN?
// Diffrence bettwen null or userdefined?

// var data='riitk raput'
// console.log('riitk' - 'raput')
// console.log(typeof('riitkraput'))


// var num=29
// if(num%2==0){
//     console.log('its even number')
// }else{
//     console.log('its odd number')
// }


var num=20
if(num%4==0){
    if(num%100==0){
        if(num%400==0){
            console.log('the year'+ num +'is a leap year');
        }else{
            console.log('the year'+ num +'is not a leap year');
        }
        // console.log('the year'+ num+'is a leap year');
    }else{
        console.log('the year'+ num +'is leap year');
    }
    // console.log('the year'+ num +'is a leap year');
}else{
    console.log('the year'+ num +'is not a leap year');
}