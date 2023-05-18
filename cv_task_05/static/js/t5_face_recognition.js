let ts5DexWindow = document.querySelector('.face-detection-dex'),
    ts5OpenDexWindowBtn = document.querySelector('p.face_detection'),
    ts5DexWindowClsBtn = document.querySelector('.face-detection-dex .ts5-bar span.ts5-cls'),
    ts5OperWindow = document.querySelector(".ts5-op-window"),
    ts5OpenOperWindowBtn = document.querySelector('.ts5-try-btn'),
    ts5ClsOperWindowBtn = document.querySelector('.ts5-op-cls-btn'),
    t5WrkSpaceImg = document.querySelector('.ts5-ws-01 img'),
    t5WrkSpaceImgInp = document.querySelector('.ts5-file'),
    ts5UpldBtn = document.querySelector('.ts5-upld-btn'),
    t5ImgRemoveBtn = document.querySelector('.ts5-img-rmv-btn'),
    prcSubmitWindow = document.querySelector('.prc-str'),
    t5ResWrkSpace = document.querySelector('.ts5-ws-02'),
    t5ShowSubWindowBtn = document.querySelector('.t5-show-sub-wind'),
    unknownFaceErrorWindow = document.querySelector('.unknown-window '),
    faceRecBtns = document.querySelector('.face-rec-btns'),
    faceDecWind = document.querySelector('.ts5-fd-window'),
    tdClsOpBtn = document.querySelector('.ts5-fd-cls-btn'),
    tdRmvImgBtn = document.querySelector('.ts5-fd-img-rmv-btn'),
    tdUldImgBtn = document.querySelector('.ts5-fd-upld-btn'),
    tdUpldImg = document.querySelector('.ts5-fd-01 img'),
    tdInpImgFile = document.querySelector('.ts5-fd-file'),
    tdResWrkSpace = document.querySelector('.ts5-fd-02'),
    tfPrecSubmitWindow = document.querySelector('.prc-str-fd'),
    tfShowSubWindow = document.querySelector('.t5-fd-show-sub-wind'),
    tfClsSubWindow = document.querySelector('.prc-fd-ts5-cls'),
    tdSubmitBtn = document.querySelector('.ts5-fd-str'),
    tdModelPerformanceWindow = document.querySelector('.roc-com_matrix-cont'),
    tdModelInfoClsBtn = document.querySelector('.ts5-roc-cls-btn'),
    tdMdlShowBrn = document.querySelector('span.mdl-prf');

let t5Data = {}, tfData = {};
ts5OpenDexWindowBtn.addEventListener('click', _ => {
    mainConatiner.classList.add('inactive');
    ts5DexWindow.classList.add('active');
});
tdUldImgBtn.addEventListener('click', _ => tdInpImgFile.click());
ts5DexWindowClsBtn.addEventListener('click', _ => {
    mainConatiner.classList.remove('inactive');
    ts5DexWindow.classList.remove('active');
});
tdModelInfoClsBtn.addEventListener('click', _ => {
    tdModelPerformanceWindow.classList.remove('active');
    ts5OperWindow.classList.add('active');
});
tdMdlShowBrn.addEventListener('click', _ => {
    tdModelPerformanceWindow.classList.add('active');
    ts5OperWindow.classList.remove('active');
});

ts5OpenOperWindowBtn.addEventListener('click', _ => {
    ts5DexWindow.classList.remove('active');
    faceRecBtns.classList.add('active');
    faceRecBtns.querySelectorAll('p').forEach(ele => {
        if (ele.classList.contains('active')) {
            if (ele.getAttribute('value') == 'tf-face-recognition')
                ts5OperWindow.classList.add('active');
            else
                faceDecWind.classList.add('active');
        }
    })
});
faceRecBtns.querySelectorAll('p').forEach(ele => {
    ele.addEventListener('click', _ => {
        faceRecBtns.querySelector("p.active").classList.remove('active');
        ele.classList.add('active');
        if (ele.classList.contains('active')) {
            if (ele.getAttribute('value') == 'tf-face-recognition') {
                ts5OperWindow.classList.add('active');
                faceDecWind.classList.contains('active') ? faceDecWind.classList.remove('active') : '';
            }
            else {
                faceDecWind.classList.add('active');
                ts5OperWindow.classList.contains('active') ? ts5OperWindow.classList.remove('active') : '';
            }
        }
    })
})
ts5ClsOperWindowBtn.addEventListener('click', _ => {
    mainConatiner.classList.remove('inactive');
    ts5OperWindow.classList.remove('active');
    faceRecBtns.classList.remove('active');
});
tfClsSubWindow.addEventListener('click', _ => {
    tfPrecSubmitWindow.classList.remove('active');
    tfShowSubWindow.classList.add('active');
})
ts5UpldBtn.addEventListener('click', _ => t5WrkSpaceImgInp.click());
t5WrkSpaceImgInp.addEventListener('input', _ => {
    ts5OperWindow.classList.contains('in-op') ? "" : ts5OperWindow.classList.add('in-op');
    t5ResWrkSpace.classList.contains('in-op') ? "" : t5ResWrkSpace.classList.add('in-op');
    let file = t5WrkSpaceImgInp.files[0];
    if (file) {
        let reader = new FileReader();
        console.log(file.name);
        reader.onload = _ => {
            let result = reader.result;
            t5WrkSpaceImg.classList.add('active');
            t5WrkSpaceImg.src = result;
            t5Data.img = result;
            t5Data.name = file.name;
            t5ImgRemoveBtn.classList.add('active');
            prcSubmitWindow.classList.add('active');
            t5ShowSubWindowBtn.classList.add('active');
        }
        t5ImgRemoveBtn.addEventListener('click', _ => {
            t5WrkSpaceImg.classList.remove('active');
            t5ImgRemoveBtn.classList.remove('active');
            t5Data.img = ""
            t5WrkSpaceImg.src = "";
            t5WrkSpaceImgInp.value = "";
            ts5OperWindow.classList.contains('in-op') ? "" : ts5OperWindow.classList.add('in-op');
            t5ResWrkSpace.classList.contains('in-op') ? "" : t5ResWrkSpace.classList.add('in-op');
            t5ShowSubWindowBtn.classList.remove('active');
        });
        reader.readAsDataURL(file);
    }
});
tdInpImgFile.addEventListener('input', _ => {
    faceDecWind.classList.contains('in-op') ? "" : faceDecWind.classList.add('in-op');
    tdResWrkSpace.classList.contains('in-op') ? "" : tdResWrkSpace.classList.add('in-op');
    let file = tdInpImgFile.files[0];
    if (file) {
        let reader = new FileReader();
        console.log(file.name);
        reader.onload = _ => {
            let result = reader.result;
            tdUpldImg.classList.add('active');
            tdUpldImg.src = result;
            tfData.img = result;
            tfData.name = file.name;
            tdRmvImgBtn.classList.add('active');
            tfPrecSubmitWindow.classList.add('active');
            tfShowSubWindow.classList.add('active');
        }
        tdRmvImgBtn.addEventListener('click', _ => {
            tdUpldImg.classList.remove('active');
            tdRmvImgBtn.classList.remove('active');
            tfData.img = ""
            tdUpldImg.src = "";
            tdInpImgFile.value = "";
            faceDecWind.classList.contains('in-op') ? "" : faceDecWind.classList.add('in-op');
            tdResWrkSpace.classList.contains('in-op') ? "" : tdResWrkSpace.classList.add('in-op');
            tfPrecSubmitWindow.classList.remove('active');
            tfShowSubWindow.classList.remove('active');
        });
        reader.readAsDataURL(file);
    }
});
tfShowSubWindow.addEventListener('click', _ => {
    tfPrecSubmitWindow.classList.add('active');
})
prcSubmitWindow.querySelector('.prc-ts5-cls').addEventListener('click', _ => {
    prcSubmitWindow.classList.remove('active');
    t5ShowSubWindowBtn.classList.add('active');
});
prcSubmitWindow.querySelector('.ts5-str').addEventListener('click', _ => {
    prcSubmitWindow.classList.remove('active');
    t5ShowSubWindowBtn.classList.remove('active');
    t5Data.thr = document.getElementById('t5-thr-input').value;
    sendDataToFaceNatching(t5Data);
});

t5ShowSubWindowBtn.addEventListener('click', _ => {
    t5ShowSubWindowBtn.classList.remove('active');
    prcSubmitWindow.classList.add('active');
})

function sendDataToFaceNatching(data) {
    console.log(data);
    loader.classList.add('active');
    fetch(`${window.origin}/face_recognition`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(data),
        cache: 'no-cache',
        headers: new Headers({
            'content-type': "application/json",
        }),
    }).then(response => {
        if (response.status !== 200) {
            console.log(`Response status was not 200: ${response.status}`);
            errorWindow.classList.add('active');
            loader.classList.remove('active');
            return;
        }
        response.json().then(data => {
            console.log(data['Message']);
            console.log(data['img']);
            console.log(data['stat']);
            console.log(data['prs_name']);
            if (data['stat'] == "Unknown face") {
                unknownFaceErrorWindow.classList.add('active');
            } else {
                t5ResWrkSpace.querySelector('img').src = data['img'];
                t5ResWrkSpace.querySelector('img').classList.add('active');
                ts5OperWindow.classList.remove('in-op');
                t5ResWrkSpace.classList.remove('in-op');
                document.querySelector('.t5-name').innerText = data['prs_name'];
                let t5Stat = document.querySelector('.t5-stat');
                if (data['stat'] == 'Matched') {
                    t5Stat.innerText = 'Matched';
                    t5Stat.style.color = 'rgb(9, 132, 9)';
                }
                else {
                    t5Stat.innerText = 'False matched';
                    t5Stat.style.color = 'rgb(137, 11, 11)';
                }
                // document.querySelector('.rm-img.roc-img img').src = data['roc'];
            }
            loader.classList.remove('active');
        });
    });
}

unknownFaceErrorWindow.querySelector('.unf-cls').addEventListener('click', _ => {
    unknownFaceErrorWindow.classList.remove('active');
    t5ShowSubWindowBtn.classList.add('active');
});


tdClsOpBtn.addEventListener('click', _ => {
    mainConatiner.classList.remove('inactive');
    faceDecWind.classList.remove('active');
    faceRecBtns.classList.remove('active');
});
tdSubmitBtn.addEventListener('click', _ => {
    console.log(tfData);
    sendFaceDetection(tfData);
});

function sendFaceDetection(data) {
    console.log(data);
    loader.classList.add('active');
    fetch(`${window.origin}/face_detection`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(data),
        cache: 'no-cache',
        headers: new Headers({
            'content-type': "application/json",
        }),
    }).then(response => {
        if (response.status !== 200) {
            console.log(`Response status was not 200: ${response.status}`);
            errorWindow.classList.add('active');
            loader.classList.remove('active');
            return;
        }
        response.json().then(data => {
            console.log(data['Message']);
            console.log(data['img']);
            faceDecWind.classList.contains('in-op') ? faceDecWind.classList.remove('in-op') : '';
            tdResWrkSpace.classList.contains('in-op') ? tdResWrkSpace.classList.remove('in-op') : '';
            tfPrecSubmitWindow.classList.remove('active');
            loader.classList.remove('active');
            tdResWrkSpace.querySelector('img').classList.add('active');
            tdResWrkSpace.querySelector('img').src = data['img'];
            tfShowSubWindow.classList.remove('active');
        });
    });
}
