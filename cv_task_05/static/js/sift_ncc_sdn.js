let ssdClsBtn = document.querySelector('.ssd-cls'),
    ssdDexWindow = document.querySelector('.ssd-ncc-dex'),
    matchingOpenBtn = document.querySelector('.landing-page .matching'),
    ssdTryNowBtn = document.querySelector('.ssd-try-btn'),
    opertingWindowClsBtn = document.querySelector('.ssd-op-cls-btn'),
    operatingWindow = document.querySelector('.ssd-ncc-op-window'),
    subWindowOpenBtn = document.querySelector('.pro-sub-opn-btn'),
    subWindow = document.querySelector('.ssd-submit'),
    subWindowClsBtn = document.querySelector('.pro-sub-cls-btn'),
    thInput = document.getElementById('ssd-threshold'),
    processBtn = document.querySelector('.st-prs'),
    ssdImg1 = document.querySelector('.ssd-imgs-container .img-s1 img'),
    ssdImg2 = document.querySelector('.ssd-imgs-container .img-s2 img'),
    ssdimgOneInput = document.getElementById('ssd-img-one'),
    ssdimgTwoInput = document.getElementById('ssd-img-two'),
    ssdAddImg1Btn = document.querySelector('.img-s1 .upld-img-ssd'),
    ssdAddImg2Btn = document.querySelector('.img-s2 .upld-img-ssd'),
    ssdRmvImg1Btn = document.querySelector('.img-s1 .rmv-sc-btn'),
    ssdRmvImg2Btn = document.querySelector('.img-s2 .rmv-sc-btn'),
    matchingMethods = document.querySelectorAll('.ssd-submit .type-matching span'),
    clsRsltWindowBtn = document.querySelector('.cls-rslt-window'),
    ssdRsltWindow = document.querySelector('.ssd_rslt-window'),
    ssdBackToOpWindowBtn = document.querySelector('.back-to-ssd-window'),
    ssdRsltImage = document.querySelector('.ris-img img'),
    ssdModeParInfo = document.querySelectorAll('.si-ty-in .type span'),
    siftModeParInfo = document.querySelectorAll('.si-ty-in .sift span');
let subIm1 = false,
    subIm2 = false,
    ssdData = {};

matchingOpenBtn.addEventListener('click', _ => {
    ssdDexWindow.classList.add('active');
    mainConatiner.classList.add('inactive');
});

ssdClsBtn.addEventListener('click', _ => {
    ssdDexWindow.classList.remove('active');
    mainConatiner.classList.remove('inactive');
});
ssdTryNowBtn.addEventListener('click', _ => {
    operatingWindow.classList.add('active');
    ssdDexWindow.classList.remove('active');
});

opertingWindowClsBtn.addEventListener('click', _ => {
    operatingWindow.classList.contains('active') ? operatingWindow.classList.remove('active') : '';
    mainConatiner.classList.contains('inactive') ? mainConatiner.classList.remove('inactive') : '';
    subWindow.classList.contains('active') ? subWindow.classList.remove('active') : '';
    ssdImg1.src = '';
    ssdImg2.src = '';
    ssdimgOneInput.value = '';
    ssdimgTwoInput.value = '';
    ssdImg1.classList.contains('active') ? ssdImg1.classList.remove('active') : '';
    ssdImg2.classList.contains('active') ? ssdImg2.classList.remove('active') : '';
    subIm1 = false;
    subIm2 = false;
    activateSubmitWindowAndSubBtn();
    ssdRmvImg1Btn.classList.contains('active') ? ssdRmvImg1Btn.classList.remove('active') : '';
    ssdRmvImg2Btn.classList.contains('active') ? ssdRmvImg2Btn.classList.remove('active') : '';
    thInput.value = '';
});

subWindowOpenBtn.addEventListener('click', _ => subWindow.classList.add('active'));
subWindowClsBtn.addEventListener('click', _ => subWindow.classList.remove('active'));

thInput.addEventListener('input', _ => {
    thInput.value === '' ? processBtn.classList.contains('active') ? processBtn.classList.remove('active') : '' : processBtn.classList.contains('active') ? '' : processBtn.classList.add('active');
});

ssdAddImg1Btn.addEventListener('click', _ => ssdimgOneInput.click());
ssdAddImg2Btn.addEventListener('click', _ => ssdimgTwoInput.click());

matchingMethods.forEach(ele => {
    ele.addEventListener('click', _ => {
        matchingMethods.forEach(ele => ele.classList.contains('active') && ele.classList.remove('active'));
        ele.classList.add('active');
    });
});

clsRsltWindowBtn.addEventListener('click', _ => {
    opertingWindowClsBtn.click();
    ssdRsltWindow.classList.remove('active');
});

ssdBackToOpWindowBtn.addEventListener('click', _ => {
    ssdRsltWindow.classList.remove('active');
    operatingWindow.classList.add('active');
});

// Review Uploaded Images
ssdimgOneInput.addEventListener('input', _ => {
    let file = ssdimgOneInput.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = _ => {
            let result = reader.result;
            console.log(result);
            ssdImg1.classList.add('active');
            ssdImg1.src = result;
            subIm1 = true;
            ssdData.img1 = result;
            activateSubmitWindowAndSubBtn();
            ssdRmvImg1Btn.classList.add('active');
        }
        ssdRmvImg1Btn.addEventListener('click', _ => {
            ssdImg1.classList.remove('active');
            ssdImg1.src = '';
            ssdimgOneInput.value = '';
            subIm1 = false;
            activateSubmitWindowAndSubBtn();
            ssdRmvImg1Btn.classList.remove('active');
        });
        reader.readAsDataURL(file);
    };
});
ssdimgTwoInput.addEventListener('input', _ => {
    let file = ssdimgTwoInput.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = _ => {
            let result = reader.result;
            console.log(result);
            ssdImg2.classList.add('active');
            ssdImg2.src = result;
            subIm2 = true;
            ssdData.img2 = result;
            activateSubmitWindowAndSubBtn();
            ssdRmvImg2Btn.classList.add('active');
        }
        ssdRmvImg2Btn.addEventListener('click', _ => {
            ssdImg2.classList.remove('active');
            ssdImg2.src = '';
            ssdimgTwoInput.value = '';
            subIm2 = false;
            activateSubmitWindowAndSubBtn();
            ssdRmvImg2Btn.classList.remove('active');
        });
        reader.readAsDataURL(file);
    };
});

// send data
processBtn.addEventListener('click', sendData);
function activateSubmitWindowAndSubBtn() {
    if (subIm1 && subIm2) {
        subWindowOpenBtn.classList.add('active');
        subWindow.classList.add('active');
    } else {
        subWindowOpenBtn.classList.remove('active');
        subWindow.classList.remove('active');
    }
}

function collectSsdData() {
    matchingMethods.forEach(ele => {
        ele.classList.contains('active') ? ssdData.method = ele.getAttribute('value') : null;
        ssdData.threshold = thInput.value;
    });
}

function sendData() {
    collectSsdData();
    console.log(ssdData);
    operatingWindow.classList.add("handle");
    loader.classList.add('active');
    processBtn.style = " pointer-events: none";
    subWindowOpenBtn.style = " pointer-events: none";
    fetch(`${window.origin}/ssd_ncc_recive`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(ssdData),
        cache: 'no-cache',
        headers: new Headers({
            'content-type': "application/json",
        }),
    }).then(response => {
        if (response.status !== 200) {
            console.log(`Response status was not 200: ${response.status}`);
            return;
        }
        response.json().then(data => {
            console.log(data['Message']);
            console.log(data['img']);
            console.log(data['mode']);
            ssdRsltImage.src = data['img'];
            ssdModeParInfo[0].innerText = data['mode'];
            ssdModeParInfo[1].innerHTML = `${data['mode_time']} <i>sec</i>`;
            siftModeParInfo[1].innerHTML = `${data['sift_time']} <i>sec</i>`;
            loader.classList.remove('active');
            operatingWindow.classList.remove("handle");
            processBtn.style = " pointer-events: auto";
            subWindowOpenBtn.style = " pointer-events: auto";
            ssdRsltWindow.classList.add('active');
            operatingWindow.classList.remove('active');
        });
    });
}