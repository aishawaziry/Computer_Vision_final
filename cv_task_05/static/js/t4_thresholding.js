let ts4DxWindow = document.querySelector('.ts4-dex'),
    ts4DxClsBtn = document.querySelector('.ts4-cls'),
    ts4TryBtn = document.querySelector(".t4_image_thresholding"),
    ts4OpWindow = document.querySelector('.ts4-op-window'),
    ts4OpWindowClsBtn = document.querySelector('.ts4-op-cls-btn'),
    ts4OpWindowOpnBtn = document.querySelector('.ts4-try-btn'),
    ts4UplImage = document.querySelector('.ts4-op-container .ts4-workspace img'),
    ts4InpImage = document.querySelector('.ts4-op-container .ts4-workspace .ts4-file'),
    ts4UpldImgBtn = document.querySelector('.ts4-op-container .ts4-workspace .ts4-upld-btn'),
    ts4DwnldImgBtn = document.querySelector('.ts4-op-container .ts4-workspace .ts4-dnld-btn'),
    ts4RmvImgBtn = document.querySelector('.ts4-img-rmv-btn'),
    ts4MainPanelElemnts = document.querySelectorAll('.ts4-panel .ts4-main-panel p'),
    ts4Panel = document.querySelector('.ts4-panel'),
    ts4Layout = document.querySelector('.ts4-layout'),
    ts4PanelMoreVar = document.querySelector('.ts4-more-opt-panel');
let ts4Data = {},
    ts4VarThrData = [
        {
            type: "local_thresholding", body: `
                    <h3><span class="material-symbols-outlined">inbox_customize</span><span>More Options</span></h3>
                    <div class="var-panel">
                        <div class="ts4-in">
                            <label for="ts4-blk-sz">Block Size</label>
                            <input type="number" id="ts4-blk-sz" value="11">
                        </div>
                        <div class="ts4-in">
                            <label for="ts4-thr-weight">Threshold Weight</label>
                            <input type="number" id="ts4-thr-weight" value="2">
                        </div>
                    </div>
                    <p class="ts4-thr-lcl-submit-btn"><span>Submit</span></p>
`},
        {
            type: "region_growing", body: `
                    <h3><span class="material-symbols-outlined">inbox_customize</span><span>More Options</span></h3>
                    <div class="var-panel">
                        <div class="ts4-in">
                            <label for="ts4-blk-sz">SeedX</label>
                            <input type="number" id="ts4-blk-sz" value="50">
                        </div>
                        <div class="ts4-in">
                            <label for="ts4-thr-weight">SeedY</label>
                            <input type="number" id="ts4-thr-weight" value="60">
                        </div>
                    </div>
                    <p class="ts4-thr-lcl-submit-btn"><span>Submit</span></p>
`},
        {
            type: "agglomerative_clustring", body: `
                    <h3><span class="material-symbols-outlined">inbox_customize</span><span>More Options</span></h3>
                    <div class="var-panel">
                        <div class="ts4-in">
                            <label for="ts4-blk-sz">N Clusters</label>
                            <input type="number" id="ts4-blk-sz" value="4">
                        </div>
                        <div class="ts4-in">
                            <label for="ts4-thr-weight">K Initial</label>
                            <input type="number" id="ts4-thr-weight" value="20">
                        </div>
                    </div>
                    <p class="ts4-thr-lcl-submit-btn"><span>Submit</span></p>
`},
        {
            type: "k_mean_segmentation", body: `
                    <h3><span class="material-symbols-outlined">inbox_customize</span><span>More Options</span></h3>
                    <div class="var-panel">
                        <div class="ts4-in">
                            <label for="ts4-blk-sz">K</label>
                            <input type="number" id="ts4-blk-sz" value="3">
                        </div>
                        <div class="ts4-in">
                            <label for="ts4-thr-weight">Max Iterations</label>
                            <input type="number" id="ts4-thr-weight" value="20">
                        </div>
                    </div>
                    <p class="ts4-thr-lcl-submit-btn"><span>Submit</span></p>
`},
        {
            type: "spectral_thresholding", body: `
            <h3><span class="material-symbols-outlined">inbox_customize</span><span>More Options</span></h3>
            <div class="thr-types-opt">
                <p value="hard_thresholding">
                    <span class="material-symbols-outlined">contrast_rtl_off</span>
                    <span>Hard Thresholding</span>
                </p>
                <p value="soft_thresholding">
                    <span class="material-symbols-outlined">low_density</span>
                    <span>Soft Thresholding</span>
                </p>
                <p value="garrote_thresholding">
                    <span class="material-symbols-outlined">line_weight</span>
                    <span>Garrote Thresholding</span>
                </p>
                </div>
                <div class="thr-sp-mode-var" style="display:flex; flex-direction:column;"></div>
`},
    ],
    sp4ModeData = [
        {
            type: "hard_thresholding",
            body: `
            <div class="var-panel">
            <div class="ts4-in" style="width:100%">
                <label for="ts4-sp-thr">Threshold</label>
                <input type="number" id="ts4-sp-thr" value="100">
            </div>
        </div>
        <p class="ts4-thr-lcl-submit-btn"><span>Submit</span></p>
    `
        },
        {
            type: "soft_thresholding",
            body: `
            <div class="var-panel">
                <div class="ts4-in">
                    <label for="ts4-sp-thr">Threshold</label>
                    <input type="number" id="ts4-sp-thr" value="100">
                </div>
                <div class="ts4-in">
                    <label for="ts4-sp-red">Reduction Ratio</label>
                    <input type="number" id="ts4-sp-red" value="0.1">
                </div>
            </div>
            <p class="ts4-thr-lcl-submit-btn"><span>Submit</span></p>
    `
        },
        {
            type: "garrote_thresholding",
            body: `
            <div class="var-panel">
                <div class="ts4-in">
                    <label for="ts4-sp-thr">Threshold</label>
                    <input type="number" id="ts4-sp-thr" value="100">
                </div>
                <div class="ts4-in">
                    <label for="ts4-sp-red">Reduction Ratio</label>
                    <input type="number" id="ts4-sp-red" value="0.1">
                </div>
            </div>
            <p class="ts4-thr-lcl-submit-btn"><span>Submit</span></p>
    `
        },
    ]
ts4DxClsBtn.addEventListener("click", _ => {
    ts4DxWindow.classList.remove("active");
    mainConatiner.classList.remove("inactive");
});

ts4TryBtn.addEventListener('click', _ => {
    ts4DxWindow.classList.add("active");
    mainConatiner.classList.add("inactive");
});

ts4UpldImgBtn.addEventListener('click', _ => ts4InpImage.click());
ts4InpImage.addEventListener("input", _ => {
    let file = ts4InpImage.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = _ => {
            let result = reader.result;
            console.log(result);
            ts4UplImage.classList.add('active');
            ts4UplImage.src = result;
            ts4Data.orImg = result;
            ts4RmvImgBtn.classList.add('active');
            ts4UpldImgBtn.classList.remove('active');
            ts4DwnldImgBtn.classList.add('active');
            console.log(ts4Data);
            ts4Data.thType = "";
            sendThresholdingData(ts4Data);
            ts4Panel.classList.add("active");
        }
        ts4RmvImgBtn.addEventListener('click', _ => {
            ts4UplImage.classList.remove('active');
            ts4OpWindow.classList.contains('sp') ? ts4OpWindow.classList.remove('sp') : "";
            ts4UplImage.src = '';
            ts4InpImage.value = '';
            ts4MainPanelElemnts.forEach(ele => ele.classList.contains('active') ? ele.classList.remove('active') : null);
            ts4RmvImgBtn.classList.remove('active');
            ts4UpldImgBtn.classList.add('active');
            ts4DwnldImgBtn.classList.remove('active');
            ts4Panel.classList.remove("active");
            ts4PanelMoreVar.innerHTML = ""
        });
        reader.readAsDataURL(file);
    };
});

ts4MainPanelElemnts.forEach(ele => {
    ele.addEventListener('click', _ => {
        ts4MainPanelElemnts.forEach(ele => ele.classList.contains('active') ? ele.classList.remove('active') : null);
        ele.classList.add('active');
        ts4Data.thType = ele.getAttribute('value');
        console.log(ts4Data);
        if (ele.getAttribute('value') == "local_thresholding" || ele.getAttribute('value') == "region_growing" || ele.getAttribute('value') == "agglomerative_clustring" || ele.getAttribute('value') == "k_mean_segmentation") {
            if (ele.getAttribute('value') == "local_thresholding") {
                ts4Data.lclBlockSize = 11;
                ts4Data.lclThresholdWeight = 2;
            }
            else if (ele.getAttribute('value') == "region_growing") {
                ts4Data.lclBlockSize = 50;
                ts4Data.lclThresholdWeight = 60;
            }
            else if (ele.getAttribute('value') == "agglomerative_clustring") {
                ts4Data.lclBlockSize = 4;
                ts4Data.lclThresholdWeight = 20;
            }
            else if (ele.getAttribute('value') == "k_mean_segmentation") {
                ts4Data.lclBlockSize = 3;
                ts4Data.lclThresholdWeight = 20;
            }
            ts4VarThrData.forEach(e => {
                switch (ele.getAttribute('value')) {
                    case "local_thresholding":
                        if (e.type == "local_thresholding")
                            ts4PanelMoreVar.innerHTML = e.body;
                        break;
                    case "region_growing":
                        if (e.type == "region_growing")
                            ts4PanelMoreVar.innerHTML = e.body;
                        break;
                    case "agglomerative_clustring":
                        if (e.type == "agglomerative_clustring")
                            ts4PanelMoreVar.innerHTML = e.body;
                        break;
                    case "k_mean_segmentation":
                        if (e.type == "k_mean_segmentation")
                            ts4PanelMoreVar.innerHTML = e.body;
                        break;
                    default:
                        break;
                }
            });
            document.querySelector('.ts4-thr-lcl-submit-btn').addEventListener('click', _ => {
                ts4Data.lclBlockSize = document.getElementById('ts4-blk-sz').value;
                ts4Data.lclThresholdWeight = document.getElementById('ts4-thr-weight').value;
                sendThresholdingData(ts4Data);
            });
            ts4OpWindow.classList.contains('sp') ? ts4OpWindow.classList.remove('sp') : "";
            sendThresholdingData(ts4Data);
        }
        else if (ele.getAttribute('value') == "optimal_thresholding" || ele.getAttribute('value') == "otsu_thresholding" || ele.getAttribute('value') == "mean_shift_segmentation" || ele.getAttribute('value') == "rgb_luv" || ele.getAttribute('value') == "spectral_thresholding_mod") {
            ts4PanelMoreVar.innerHTML = "";
            sendThresholdingData(ts4Data);
        }
        else if (ele.getAttribute('value') == "spectral_thresholding") {
            ts4OpWindow.classList.contains('sp') ? ts4OpWindow.classList.remove('sp') : "";
            ts4VarThrData.forEach(e => {
                if (e.type == "spectral_thresholding") {
                    ts4PanelMoreVar.innerHTML = e.body;
                    thrSpModes = ts4PanelMoreVar.querySelectorAll('p');
                    thrSpModesContVar = ts4PanelMoreVar.querySelector('.thr-sp-mode-var');
                    thrSpModes.forEach(el => {
                        el.addEventListener('click', _ => {
                            thrSpModesContVar.innerHTML = "";
                            ts4PanelMoreVar.querySelector('p.active')?.classList.remove('active');
                            el.classList.add('active');
                            sp4ModeData.forEach(v => {
                                if (el.getAttribute('value') == v.type) {
                                    thrSpModesContVar.innerHTML = v.body;
                                    ts4OpWindow.classList.contains('sp') ? "" : ts4OpWindow.classList.add('sp');
                                    document.querySelector('.ts4-thr-lcl-submit-btn').addEventListener('click', _ => {
                                        ts4Data.threshold = document.getElementById('ts4-sp-thr')?.value;
                                        ts4Data.reduction = document.getElementById('ts4-sp-red')?.value;
                                        ts4Data.mode = el.getAttribute('value');
                                        sendThresholdingData(ts4Data);
                                    });
                                }
                            });
                        })
                    })
                }
            });
        }
        else {
            ts4PanelMoreVar.innerHTML = ""
            ts4OpWindow.classList.contains('sp') ? ts4OpWindow.classList.remove('sp') : "";
        }
    });
});
ts4OpWindowOpnBtn.addEventListener("click", _ => {
    ts4DxWindow.classList.remove('active');
    ts4OpWindow.classList.add("active");
});

ts4OpWindowClsBtn.addEventListener('click', _ => {
    ts4DxWindow.classList.add('active');
    ts4OpWindow.classList.remove("active");
    ts4PanelMoreVar.innerHTML = ""
});
ts4DwnldImgBtn.addEventListener('click', _ => ts4DownloadElement(ts4UplImage.src, ts4UplImage.src.split("/")[ts4UplImage.src.split("/").length - 1]));
function sendThresholdingData(data) {
    console.log(data);
    loader.classList.add('active');
    ts4Layout.classList.add('active');
    fetch(`${window.origin}/ts4_recive_new`, {
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
            ts4Layout.classList.remove('active');
            return;
        }
        response.json().then(data => {
            console.log(data['Message']);
            console.log(data['img']);
            ts4UplImage.src = data['img'];
            loader.classList.remove('active');
            ts4Layout.classList.remove('active');
        });
    });
}


function ts4DownloadElement(fileUrl, fileName) {
    const downloadLink = document.createElement('a');
    downloadLink.href = fileUrl;
    downloadLink.download = fileName;
    downloadLink.click();
}

