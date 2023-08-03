function a(){
    setTimeout(() => {
        console.log('prt1')
    }, 1000)
}
function b() {
    setTimeout(() => {
        console.log('prt2')
    }, 800)
}

async function c(){
    setTimeout(() => {
        console.log('prt3')

    }, 700)
}
a()
b()
c()


