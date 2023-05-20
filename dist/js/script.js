// querySelector setting
function $$(element) {
  return document.querySelector(element);
}
function $$all(element) {
  return document.querySelectorAll(element);
}
$$("#homePage").addEventListener("animationend", function () {
  $$("#homePage").classList.remove("animate__animated", "animate__fadeInDown");
});
// 顯示等待頁面
function showLoadingPage() {
  // homePage Out
  $$("#homePage").classList.add("d-none");
  // loadingPage In
  $$("#loadingPage").classList.remove("d-none");
  $$("#loadingPage").classList.add("animate__animated", "animate__flipInY");
  $$("#loadingPage").addEventListener("animationend", function () {
    $$("#loadingPage").classList.remove(
      "animate__animated",
      "animate__flipInY"
    );
  });
  console.log("等待中...");
}
// 顯示結果頁面
function showResultPage() {
  // loadingPage Out
  $$("#loadingPage").classList.add("d-none");
  // resultPage In
  $$("#resultPage").classList.remove("d-none");
  $$("#resultPage").classList.add("animate__animated", "animate__flipInY");
  $$("#resultPage").addEventListener("animationend", function () {
    $$("#resultPage").classList.remove("animate__animated", "animate__flipInY");
  });
  // $$("#loadingPage").classList.add("d-none");
  // // resultPage In
  // $$("#resultPage").classList.remove("d-none");
  // $$("#resultPage").classList.add("animate__animated", "animate__flipInY");
  // $$("#resultPage").addEventListener("animationend", function () {
  //   $$("#resultPage").classList.remove("animate__animated", "animate__flipInY");
  // });
  console.log("顯示結果頁面");
  // 顯示結果頁面的內容，使用回傳的圖片資料
}
// 回家
function returnToHome() {
  $$("#resultPage").classList.add("d-none");
  $$("#homePage").classList.remove("d-none");
  $$("#homePage").classList.add("animate__animated", "animate__zoomIn");
  $$("#homePage").addEventListener("animationend", function () {
    $$("#homePage").classList.remove("animate__animated", "animate__zoomIn");
  });
}

// 亮度校正滑動調整
$$("#sliderCount").innerHTML = $$("#brightAdjSlider").value + "%"; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
$$("#brightAdjSlider").oninput = function () {
  dataProcessor.statusBrightAdj = this.value;
  $$("#sliderCount").innerHTML = this.value + "%";
};

// Switch開關狀態切換
$$("#gaussianFilter").onclick = function () {
  if (this.value === "on") {
    this.value = "off";
    dataProcessor.statusGaussianFilter = false;
  } else {
    this.value = "on";
    dataProcessor.statusGaussianFilter = true;
  }
};
$$("#unsharpMasking").onclick = function () {
  if (this.value === "on") {
    this.value = "off";
    dataProcessor.statusUnsharpMasking = false;
  } else {
    this.value = "on";
    dataProcessor.statusUnsharpMasking = true;
  }
};
$$("#adaptiveThreshold").onclick = function () {
  if (this.value === "on") {
    this.value = "off";
    dataProcessor.statusAdaptiveThreshold = false;
  } else {
    this.value = "on";
    dataProcessor.statusAdaptiveThreshold = true;
  }
};

// 亮度校正方法選擇
$$("#BrightnessFixMethodSelect").addEventListener("change", function () {
  dataProcessor.statusBrightnessFixMethod = $$("#BrightnessFixMethodSelect").value;
  console.log(dataProcessor.statusBrightnessFixMethod);
});

// 實驗選擇
$$("#experimentSelect").addEventListener("change", function () {
  dataProcessor.statusExperiment = $$("#experimentSelect").value;
  console.log(dataProcessor.statusExperiment);
  // 選擇論文實驗2時，才會顯示亮度調整
  if ($$("#experimentSelect").value === "exp2") {
    $$("#brightAdj").style.visibility = "visible";
  } else {
    $$("#brightAdj").style.visibility = "hidden";
  }
});


function shakeAlert(element) {
  element.classList.add("animate__animated", "animate__headShake");
  element.addEventListener("animationend", function () {
    element.classList.remove("animate__animated", "animate__headShake");
  });
}
// 開始分析前，較驗輸入資料
function checkSettingInput() {
  if ($$("#previewImage").currentSrc === "") {
    shakeAlert($$("#imgFileInput"));
    return false;
  }
  if ($$("#BrightnessFixMethodSelect").value === "0") {
    shakeAlert($$("#BrightnessFixMethodSelect"));
    return false;
  }
  if ($$("#experimentSelect").value === "0") {
    shakeAlert($$("#experimentSelect"));
    return false;
  }
  return true;
}