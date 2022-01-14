const node = document.getElementById('metrics')
var card = 0
var chosen = 0
var r1=0 ;var r2=0 ;var r3=0 ;var r4=0 ;var r5=0 ;var r6=0

function rman(r) {
    var a;
    let id = "q"+r
    let chart = 'run'+r
    a = document.getElementById(id);
    // a.className = "las"
    // a.innerHTML = "&#xf7c5;";
    setTimeout(function () {
        a.innerHTML = "<span class='las la-fire-alt' id='"+chart+"'></span>";
        // a.innerHTML = "&#xf7c9";
    }, 1000);
    setTimeout(function () {
        a.innerHTML = "<span class='las la-burn' id='"+chart+"'></span>";
        // a.innerHTML = "&#xf7ce;";
    }, 2000);
    setTimeout(function () {
        a.innerHTML = "<span class='las la-fire' id='"+chart+"'></span>";
        // a.innerHTML = "&#xf7ce;";
    }, 3000);
}

function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds){
            break;
        }
    }
}

function chooseCard(v){
   card = document.getElementById(v);
}

function runCard(s,v){
    if (s === 'run'){
        if (v === 'c1' && !(r1)) {
            r1 = setInterval(function() { rman('1'); }, 3000);
        } else if (v === 'c2'  && !(r2)) {
            r2 = setInterval(function() { rman('2'); }, 3000);
        } else if (v === 'c3'  && !(r3)) {
            r3 = setInterval(function() { rman('3'); }, 3000);
        } else if (v === 'c4'  && !(r4)) {
            r4 = setInterval(function() { rman('4'); }, 3000);
        } else if (v === 'c5'  && !(r5)) {
            r5 = setInterval(function() { rman('5'); }, 3000);
        } else if (v === 'c6'  && !(r6)) {
            r6 = setInterval(function() { rman('6'); }, 3000);
        }
    } else {
        console.log('stop',v)
        if (v === 'c1') {
            clearInterval(r1)
            r1=0
        } else if (v === 'c2') {
            clearInterval(r2)
            r2=0
        } else if (v === 'c3') {
            clearInterval(r3)
            r3=0
        } else if (v === 'c4') {
            clearInterval(r4)
            r4=0
        } else if (v === 'c5') {
            clearInterval(r5)
            r5=0
        } else if (v === 'c6') {
            clearInterval(r6)
            r6=0
        }
    }
}

function run(c,s) {
    $.ajax({
        type:'POST',
        url: '/api/data/',
        // dataType: 'json'
        data:{'card':c,'status':s},
        success: function (e) {
            var num = e['card'][1]
            log = document.getElementById('t'+ num)
            log.value = e['log']
            p = document.getElementById('p'+num)
            nf = document.getElementById('nf'+num)
            if (p.textContent !== e['flow']) {
                p.textContent = e['flow']
                nf.textContent = e['nflow']
            }
            if (log.value.length !== e['log'].length) {
                log.scrollTo(0,log.scrollHeight)
            }
            if (e['status'] === 'running') {
                runCard('run',e['card'])
                run(e['card'],e['status'])
            } else if (e['status'] === 'pass') {
                runCard('stop',e['card'])
                c = document.getElementById(e['card'])
                c.style.color = 'seagreen'
                c = document.getElementById('n'+num)
                c.style.color = 'seagreen'
            } else if (e['status'] === 'fail') {
                runCard('stop',e['card'])
                c = document.getElementById(e['card'])
                c.style.color = '#d96c4e'
                c = document.getElementById('n'+num)
                c.style.color = '#d96c4e'
                console.log('fail')
                console.log(e)
            }
        },
        error: function (err) {
            console.log('error');
        }
    })
}

node.addEventListener("keyup", function(event) {
    let n = node.placeholder
    // let card = document.getElementById('c1')
    if (event.key === "Enter") {
        if (n==='ID' && !(eval('r'+node.value).valueOf())) {
            chosen = node.value
            chooseCard('c'+chosen)
            card.style.color = '#0120cc'
            card.textContent = '************'
            chooseCard('n'+chosen)
            card.style.color = '#0120cc'
            card.textContent = '************'
            node.placeholder = 'MAC'
            node.value = ''
        } else if (n==='MAC') {
            chooseCard('c'+chosen)
            card.textContent = node.value
            node.placeholder = 'SN'
            node.value = ''
        } else if (n==='SN') {
            chooseCard('n'+chosen)
            card.textContent = node.value
            node.placeholder = 'ID'
            node.value = ''
            chooseCard('c'+chosen)
            runCard('run',card.id)
            run(card.id.toString(),'start')
        } else {
            alert('input error')
            node.value = ''
        }
    }
});

$( document ).ready(function() {
    console.log( "ready!" );
    for (let i = 1; i <= 6; i++) {
        run('c'+i.toString(),'restore')
    }
});


// import Vue from 'vue'
// var vm = new Vue({
//   el: '#vm',
//   data: {
//     a: 1
//   },
//   beforeCreate: function(){
//     console.log('== beforeCreate ==')
//     console.log('this.a: ' + this.a)
//     console.log('this.$el: ' + this.$el)
//     console.log()
//   },
//   created: function(){
//     console.log('== created ==')
//     console.log('this.a: ' + this.a)
//     console.log('this.$el: ' + this.$el)
//     console.log()
//   },
//   mounted: function(){
//     console.log( "ready!" );
//     for (let i = 1; i <= 6; i++) {
//         run('c'+i.toString(),'restore')
//     }
//   }
// })

// vue.js axios
// function run(c,s) { 
//     axios({
//         method:'post',
//         url: '/api/data/',
//         data:{'card':c,'status':s},
//     })
//     .then(function (response) {
//         e = response.data
//         var num = e['card'][1]
//         log = document.getElementById('t'+ num)
//         log.value = e['log']
//         p = document.getElementById('p'+num)
//         nf = document.getElementById('nf'+num)
//         if (p.textContent !== e['flow']) {
//             p.textContent = e['flow']
//             nf.textContent = e['nflow']
//         }
//         if (log.value.length !== e['log'].length) {
//             log.scrollTo(0,log.scrollHeight)
//         }
//         if (e['status'] === 'running') {
//             runCard('run',e['card'])
//             run(e['card'],e['status'])
//         } else if (e['status'] === 'pass') {
//             runCard('stop',e['card'])
//             c = document.getElementById(e['card'])
//             c.style.color = 'seagreen'
//             c = document.getElementById('n'+num)
//             c.style.color = 'seagreen'
//         } else if (e['status'] === 'fail') {
//             runCard('stop',e['card'])
//             c = document.getElementById(e['card'])
//             c.style.color = '#d96c4e'
//             c = document.getElementById('n'+num)
//             c.style.color = '#d96c4e'
//             console.log('fail')
//             console.log(e)
//         }
//     })
//     .catch( (error) => console.log(error))
// }