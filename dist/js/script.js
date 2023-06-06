// querySelector setting
function $$(element) {
  return document.querySelector(element);
}
function $$all(element) {
  return document.querySelectorAll(element);
}
// 移除第一次進入頁面的animated屬性
$$("#homePage").addEventListener("animationend", function () {
  $$("#homePage").classList.remove("animate__animated", "animate__fadeInDown");
});

// 顯示等待頁面
function showLoadingPage() {
  // homePage Out
  $$("#homePage").classList.add("d-none");
  // loadingPage In
  $$("#loadingPage").classList.remove("d-none");
  $$("#loadingPage").classList.add("animate__animated", "animate__zoomIn");
  $$("#loadingPage").addEventListener("animationend", function () {
    $$("#loadingPage").classList.remove(
      "animate__animated",
      "animate__zoomIn"
    );
  });
}
// 顯示結果頁面
function showResultPage() {
  // loadingPage Out
  $$("#loadingPage").classList.add("d-none");
  // resultPage In
  $$("#resultPage").classList.remove("d-none");
  $$("#resultPage").classList.add("animate__animated", "animate__zoomIn");
  $$("#resultPage").addEventListener("animationend", function () {
    $$("#resultPage").classList.remove("animate__animated", "animate__zoomIn");
  });
  loadRandomImage(); //顯示結果時立即刷新Loading頁面的gif
}
// 返回主畫面
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
});

// 實驗選擇
$$("#experimentSelect").addEventListener("change", function () {
  dataProcessor.statusExperiment = $$("#experimentSelect").value;
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

var imageLinks = [
  "https://cdn.discordapp.com/attachments/862518605433012268/1109140766024015934/Rick_Roll_Lossy.gif",
  "https://cdn.discordapp.com/attachments/862518605433012268/1113516851834650705/kita_speedup.gif",
  "https://cdn.discordapp.com/attachments/862518605433012268/1113317327799324692/think_Lossy.gif",
  "https://cdn.discordapp.com/attachments/862518605433012268/1113317328193585182/4d10aff27de4f7a4260dd6528b556c8d.gif",
  "https://cdn.discordapp.com/attachments/862518605433012268/1115052220476575855/VoarP6Z.gif",
  "https://cdn.discordapp.com/attachments/862518605433012268/1115052220887609344/2UOkaqJ.gif"
];

function loadRandomImage() {
  var randomIndex = Math.floor(Math.random() * imageLinks.length);
  var randomImageLink = imageLinks[randomIndex];
  var imgElement = document.getElementById('loadingImage');
  var image = new Image();
  image.onload = function() {
    imgElement.src = randomImageLink;
  };
  image.src = randomImageLink;
}
window.onload = loadRandomImage;