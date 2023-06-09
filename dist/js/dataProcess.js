class DataProcessor {
  constructor() {
    this._imageData = null;
    this._statusGaussianFilter = true;
    this._statusBrightnessFixMethod = '0';
    this._statusUnsharpMasking = true;
    this._statusAdaptiveThreshold = true;
    this._statusExperiment = '0';
    this._statusBrightAdj = 0;
  }

  get imageData() {
    return this._imageData;
  }
  set imageData(newValue) {
    this._imageData = newValue;
  }

  get statusGaussianFilter() {
    return this._statusGaussianFilter;
  }
  set statusGaussianFilter(newValue) {
    this._statusGaussianFilter = newValue;
  }

  get statusBrightnessFixMethod() {
    return this._statusBrightnessFixMethod;
  }
  set statusBrightnessFixMethod(newValue) {
    this._statusBrightnessFixMethod = newValue;
  }

  get statusUnsharpMasking() {
    return this._statusUnsharpMasking;
  }
  set statusUnsharpMasking(newValue) {
    this._statusUnsharpMasking = newValue;
  }

  get statusAdaptiveThreshold() {
    return this._statusAdaptiveThreshold;
  }
  set statusAdaptiveThreshold(newValue) {
    this._statusAdaptiveThreshold = newValue;
  }

  get statusExperiment() {
    return this._statusExperiment;
  }
  set statusExperiment(newValue) {
    this._statusExperiment = newValue;
  }

  get statusBrightAdj() {
    return this._statusBrightAdj;
  }
  set statusBrightAdj(newValue) {
    this._statusBrightAdj = newValue;
  }
}
const dataProcessor = new DataProcessor();

// 將Base64轉為Blob圖像
function base64ToBlob(base64, contentType) {
  var byteCharacters = atob(base64);
  var byteArrays = [];

  var sliceSize = 1024;
  var offset = 0;

  while (offset < byteCharacters.length) {
    var slice = byteCharacters.slice(offset, offset + sliceSize);
    var byteNumbers = new Array(slice.length);

    for (var i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }

    var byteArray = new Uint8Array(byteNumbers);
    byteArrays.push(byteArray);

    offset += sliceSize;
  }

  return new Blob(byteArrays, { type: contentType });
}

function resultCarouselControl(){
  // 來修改 Carousel 頁數
  if (dataProcessor.statusExperiment === 'exp1') {
    // 2頁
    $('.carousel-item:nth-child(3)').remove();
  } else if (dataProcessor.statusExperiment === 'exp2') {
    // 3頁
  } else if (dataProcessor.statusExperiment === 'exp3') {
    // 1頁，隱藏左右換頁按鈕
    $('.carousel-control-prev, .carousel-control-next').hide();
  }

}

$(document).ready(function() {
  var originalContent = $('#resultCarousel').html(); // 儲存原始的 Carousel 內容

  // 按下 returnButton 按鈕時恢復原狀
  $('#returnButton').click(function() {
    $('#resultCarousel').html(originalContent); // 還原 Carousel 內容
    $('.carousel-control-prev, .carousel-control-next').show(); // 顯示左右換頁按鈕
  });
});

document
  .getElementById("sendButton")
  .addEventListener("click", async function () {
    try {
      if(checkSettingInput()!=true) return;

      const formData = new FormData();
      formData.append('img_content', dataProcessor.imageData); 
      formData.append('statusGaussianFilter', dataProcessor.statusGaussianFilter);
      formData.append('statusBrightnessFixMethod', dataProcessor.statusBrightnessFixMethod);
      formData.append('statusSharpen', dataProcessor.statusUnsharpMasking);
      formData.append('statusAdaptiveThreshold', dataProcessor.statusAdaptiveThreshold);
      formData.append('statusExperiment', dataProcessor.statusExperiment);
      formData.append('statusBrightAdj', dataProcessor.statusBrightAdj);

      // 顯示等待頁面
      showLoadingPage();

      const response = await axios.post("/api/orbProcessing", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if(dataProcessor.statusExperiment === 'exp1'){
        var contentType = 'image/jpg';
        var upperKeys = ["Left", "Right"];
        var lowerKeys = ["left", "right"];

        upperKeys.forEach(function(key, index) {
          var resultImage = response.data["processedImage" + key];
          var blobResultImg = base64ToBlob(resultImage, contentType);
          var resultImgUrl = URL.createObjectURL(blobResultImg);
          $("#resultImage" + key).attr("src", resultImgUrl);

          var kpNum = response.data["keypointNum" + key];
          var dTime = response.data["detectTime" + key];

          $$("#keypoint" + upperKeys[index] + "Num").innerHTML = kpNum;
          $$("#time" + upperKeys[index] + "Num").innerHTML = dTime + " s";
        });
        $$("#category-title-1").innerHTML = "原始ORB算法 檢測結果"
        $$("#category-title-2").innerHTML = "調整後算法 檢測結果"
        // 控制Carousel頁數
        resultCarouselControl()
        // 顯示結果頁面
        showResultPage();

      }
      else if(dataProcessor.statusExperiment === 'exp2'){
        var contentType = 'image/jpg';

        var upperKeys = ["Left", "Right", "Match"];
        var lowerKeys = ["left", "right", "match"];

        upperKeys.forEach(function(key, index) {
          var resultImage = response.data["processedImage" + key];
          var blobResultImg = base64ToBlob(resultImage, contentType);
          var resultImgUrl = URL.createObjectURL(blobResultImg);
          $("#resultImage" + key).attr("src", resultImgUrl);

          var kpNum = response.data["keypointNum" + key];
          var dTime = response.data["detectTime" + key];

          $$("#keypoint" + upperKeys[index] + "Num").innerHTML = kpNum;
          $$("#time" + upperKeys[index] + "Num").innerHTML = dTime + " s";
        });

        var matchAcc = response.data["matchingAccuracy"];
        $$("#matchAccNum").innerHTML = matchAcc + " %";

        $$("#category-title-1").innerHTML = "原亮度檢測結果"
        if(dataProcessor.statusBrightAdj >= 0) var catText2 = "亮度 +" + dataProcessor.statusBrightAdj + "% 檢測結果" ;
        else var catText2 = "亮度 " + dataProcessor.statusBrightAdj + "% 檢測結果";
        $$("#category-title-2").innerHTML = catText2
        $$("#category-title-3").innerHTML = "Match結果"
        
        // 控制Carousel頁數
        resultCarouselControl()
        // 顯示結果頁面
        showResultPage();
        
      }

      else if(dataProcessor.statusExperiment === 'exp3'){
        var contentType = 'image/jpg';
        var resultImage = response.data.processedImage;
        var blobResultImg = base64ToBlob(resultImage, contentType);
        var resultImgUrl = URL.createObjectURL(blobResultImg);
        $("#resultImageLeft").attr("src", resultImgUrl);

        var keypointNum = response.data.keypointNum;
        var detectTime = response.data.detectTime;
        $$("#keypointLeftNum").innerHTML = keypointNum;
        $$("#timeLeftNum").innerHTML = detectTime + " s";

        $$("#category-title-1").innerHTML = "檢測結果"
        // 控制Carousel頁數
        resultCarouselControl()
        // 顯示結果頁面
        showResultPage();
      }
    } catch (error) {
      console.error(error);
    }
  });

// 將file圖像轉為buffer
function readFileAsBuffer(file) {
  const reader = new FileReader();
  reader.readAsArrayBuffer(file);
  return new Promise((resolve) => {
    reader.onload = () => resolve(reader.result);
  });
}

// 將選擇的檔案以Blob型式顯示在$("#previewImage")中
async function handlePreviewImageFile(event) {
  const { files } = event.target;
  const file = files[0];
  const imgBuffer = await readFileAsBuffer(file);
  const previewURL = URL.createObjectURL(
    new Blob([imgBuffer], { type: "image/jpeg" })
  );
  $("#previewImage").attr("src", previewURL);
  dataProcessor.imageData = file;
}
